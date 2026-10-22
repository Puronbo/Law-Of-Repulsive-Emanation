#!/usr/bin/env python3
"""Build the multi-dimensional map of the register from the repo's own ledgers.

The point of this generator is that the map is **not hand-drawn**. Every point
in the output is an item that actually exists in the repository, and every
attribute of that point is read out of a ledger file:

* ``MODULE_LEDGER.md``      -> the module rows (name, category, card refs)
* ``MATHEMATICAL_LINK_GRAPH.md`` -> the real ``import`` edges
* ``THE_GAP_LEDGER.md``     -> the open walls (tier, subject, proof-attempt kind)
* ``CLAIM_TRACEABILITY.md`` -> the claim cards (type, Lean artifact, link)
* the Lean sources          -> the declaration names that carry each module

Dimensions exposed (any three can be mapped onto the x/y/z axes at runtime):

1. ``category`` -- the ledger category (9 values)
2. ``status``   -- how the item stands: machine-checked / partial / no-go /
   citation-only / open / empirical
3. ``depth``    -- the module's position in the real ``import`` DAG
4. ``kind``     -- module / gap / card
5. ``tier``     -- register debt tier (gaps only)

Usage::

    python build_multidimensional_map.py [--out HTML] [--json JSON]

Run from the repository root.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

DOCS = Path("05_Documentation_and_Research_Specifications/05_Complete_Framework_Documentation")
LEAN = Path("01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus")
# Generated JSON lands in a `data/` root, per the repo's persistence standard:
# generated artifacts are regenerable output, not committed load-bearing files.
DATA_OUT = Path(
    "02_Experimental_Implementations_and_Verification/data/multidimensional_map_data.json"
)

# The status ladder, ordered from strongest to weakest claim.
STATUS_ORDER = [
    "machine-checked",
    "partial",
    "no-go",
    "citation-only",
    "empirical",
    "open",
]

CATEGORY_ORDER = [
    "card",
    "millennium-cert",
    "rh-research",
    "number-theory-cert",
    "fluid-diagnostic",
    "numerical-cert",
    "cosmology",
    "core-scaffold",
    "information-bridge",
]

PROOF_KIND_TO_STATUS = {
    "certificate": "machine-checked",
    "partial": "partial",
    "no-go": "no-go",
    "citation-only": "citation-only",
    "none": "open",
    "resolved": "machine-checked",
}

CARD_TYPE_TO_STATUS = {
    "Theorem": "machine-checked",
    "Formal": "machine-checked",
    "Empirical": "empirical",
    "Conjecture/Open": "open",
    "Conjecture": "open",
    "Open": "open",
}

DECL_RE = re.compile(r"^\s*(?:theorem|lemma|def|instance|abbrev)\s+([A-Za-z_][A-Za-z0-9_'.]*)", re.M)


def read_text(path: Path) -> str:
    """Read a file as text, tolerating the legacy cp1252 bytes in old docs."""
    data = path.read_bytes()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def parse_module_ledger(text: str) -> list[dict]:
    """Rows look like: | `Name` | category | card | description |"""
    rows = []
    row_re = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([a-z\-]+)\s*\|([^|]*)\|", re.M)
    for m in row_re.finditer(text):
        name, cat, card = m.group(1), m.group(2), m.group(3).strip()
        if cat not in CATEGORY_ORDER:
            continue
        rows.append({"name": name, "category": cat, "cards": card})
    return rows


def parse_edges(text: str) -> list[tuple[str, str]]:
    """Read the EDGES block: 'A -> B' lines."""
    m = re.search(r"<!--\s*EDGES:BEGIN\s*-->(.*?)<!--\s*EDGES:END\s*-->", text, re.S)
    if not m:
        return []
    edges = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        mm = re.match(r"^([A-Za-z0-9_.'-]+)\s*->\s*([A-Za-z0-9_.'-]+)$", line)
        if mm:
            edges.append((mm.group(1), mm.group(2)))
    return edges


def compute_depths(edges: list[tuple[str, str]]) -> dict[str, int]:
    """depth(M) = 1 + max(depth of the modules M imports). 0 for foundations."""
    imports: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        imports[a].append(b)
    depth: dict[str, int] = {}
    visiting: set[str] = set()

    def d(node: str) -> int:
        if node in depth:
            return depth[node]
        if node in visiting:  # defensive: the graph is acyclic, but be safe
            return 0
        visiting.add(node)
        kids = imports.get(node, [])
        best = 0
        for k in kids:
            best = max(best, d(k))
        visiting.discard(node)
        depth[node] = best + 1 if kids else 0
        return depth[node]

    for a, _ in edges:
        d(a)
    for a, b in edges:
        d(b)
    return depth


def parse_gap_ledger(text: str) -> list[dict]:
    """Sections '## Gn -- title' with '- **Field:** value' lines."""
    gaps = []
    cur = None
    for line in text.splitlines():
        m = re.match(r"^##\s+(G\d+)\s*[—\-–]+\s*(.*)$", line.strip())
        if m:
            if cur:
                gaps.append(cur)
            cur = {"id": m.group(1), "title": m.group(2).strip(), "fields": {}}
            continue
        if cur is None:
            continue
        fm = re.match(r"^-\s*\*\*([^*]+):\*\*\s*(.*)$", line.strip())
        if fm:
            cur["fields"][fm.group(1).strip()] = fm.group(2).strip()
    if cur:
        gaps.append(cur)
    out = []
    for g in gaps:
        f = g["fields"]
        attempt = f.get("Proof attempt", "")
        kind = attempt.split(" - ")[0].strip() if attempt else "none"
        if kind not in PROOF_KIND_TO_STATUS:
            kind = "none"
        artifact = attempt.split(" - ", 1)[1].strip() if " - " in attempt else ""
        out.append(
            {
                "id": g["id"],
                "title": g["title"],
                "tier": (f.get("Tier", "") or "").split("(")[0].strip(),
                "subject": f.get("Subject", ""),
                "status_field": f.get("Status", ""),
                "kind": "gap",
                "status": PROOF_KIND_TO_STATUS[kind],
                "proof_kind": kind,
                "artifact": artifact,
                "related_cards": f.get("Related cards", ""),
                "pins": re.findall(r"`([A-Za-z0-9_]+)`", f.get("Pin", "") + " " + f.get("Pins", "")),
                "barrier": f.get("Barrier", "")[:400],
                "missing": f.get("Missing (the object that does not exist as a proof):", "")[:400],
            }
        )
    return out


def parse_claim_traceability(text: str) -> list[dict]:
    """Rows: | **C1** | Theorem | `Mod` (`decl`, ...) | exp | cite | link |"""
    cards = []
    row_re = re.compile(r"^\|\s*\*\*(C[\w\-]+)\*\*\s*\|\s*([^|]*?)\s*\|([^|]*)\|", re.M)
    for m in row_re.finditer(text):
        cid, ctype, art = m.group(1), m.group(2).strip(), m.group(3).strip()
        mods = re.findall(r"`([A-Za-z0-9_.'-]+)`", art)
        decls = re.findall(r"`([A-Za-z0-9_.'#]+)`", art)
        status = CARD_TYPE_TO_STATUS.get(ctype, "open")
        cards.append(
            {
                "id": cid,
                "title": ctype,
                "kind": "card",
                "status": status,
                "type": ctype,
                "modules": mods,
                "decls": decls,
                "artifact": art,
            }
        )
    return cards


def module_decls(name: str) -> list[str]:
    path = LEAN / f"{name}.lean"
    if not path.exists():
        return []
    return DECL_RE.findall(read_text(path))


def build() -> dict:
    module_ledger = read_text(DOCS / "MODULE_LEDGER.md")
    link_graph = read_text(DOCS / "MATHEMATICAL_LINK_GRAPH.md")
    gap_ledger = read_text(DOCS / "THE_GAP_LEDGER.md")
    trace = read_text(DOCS / "CLAIM_TRACEABILITY.md")

    modules = parse_module_ledger(module_ledger)
    edges = parse_edges(link_graph)
    depth = compute_depths(edges)
    gaps = parse_gap_ledger(gap_ledger)
    cards = parse_claim_traceability(trace)

    # Which modules does each gap touch?  Via the proof-attempt artifact path.
    gap_by_module: dict[str, list[str]] = defaultdict(list)
    for g in gaps:
        art = g.get("artifact", "")
        if art:
            m = re.search(r"PunoCalculus/([A-Za-z0-9_.']+)\.lean", art)
            if not m:
                m = re.search(r"/([A-Za-z0-9_.']+)\.lean", art)
            if m:
                gap_by_module[m.group(1)].append(g["id"])

    card_by_module: dict[str, list[str]] = defaultdict(list)
    for c in cards:
        for mod in c["modules"]:
            card_by_module[mod].append(c["id"])

    items = []
    for row in modules:
        name = row["name"]
        decls = module_decls(name)
        items.append(
            {
                "id": name,
                "label": name,
                "kind": "module",
                "category": row["category"],
                "status": "machine-checked" if decls else "citation-only",
                "depth": depth.get(name, 0),
                "tier": "",
                "ndecls": len(decls),
                "decls": decls[:24],
                "gaps": gap_by_module.get(name, []),
                "cards": row["cards"] or card_by_module.get(name, []),
                "artifact": f"01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/{name}.lean",
                "detail": row["cards"],
            }
        )

    for g in gaps:
        mods = []
        art = g.get("artifact", "")
        m = re.search(r"/([A-Za-z0-9_.']+)\.lean", art)
        if m:
            mods.append(m.group(1))
        cat = "core-scaffold"
        for mod in mods:
            for row in modules:
                if row["name"] == mod:
                    cat = row["category"]
                    break
        items.append(
            {
                "id": g["id"],
                "label": g["id"],
                "kind": "gap",
                "category": cat,
                "status": g["status"],
                "depth": depth.get(mods[0], 0) if mods else 0,
                "tier": g["tier"],
                "ndecls": 0,
                "decls": [],
                "gaps": [g["id"]],
                "cards": [c.strip() for c in re.split(r"[,\s]+", g["related_cards"]) if c.strip()],
                "artifact": g["artifact"],
                "title": g["title"],
                "subject": g["subject"],
                "proof_kind": g["proof_kind"],
                "pins": g["pins"],
                "barrier": g["barrier"],
                "missing": g["missing"],
            }
        )

    for c in cards:
        mods = [m for m in c["modules"] if m in {r["name"] for r in modules}]
        cat = "card"
        if mods:
            for row in modules:
                if row["name"] == mods[0]:
                    cat = row["category"]
                    break
        items.append(
            {
                "id": c["id"],
                "label": c["id"],
                "kind": "card",
                "category": cat,
                "status": c["status"],
                "depth": max([depth.get(m, 0) for m in mods], default=0),
                "tier": "",
                "ndecls": len(c["decls"]),
                "decls": c["decls"][:24],
                "gaps": [],
                "cards": [c["id"]],
                "artifact": c["artifact"],
                "title": c["type"],
            }
        )

    return {
        "items": items,
        "edges": edges,
        "dims": {
            "category": CATEGORY_ORDER,
            "status": STATUS_ORDER,
            "kind": ["module", "gap", "card"],
            "tier": ["A", "B", "C"],
        },
        "counts": {
            "modules": len(modules),
            "gaps": len(gaps),
            "cards": len(cards),
            "edges": len(edges),
            "items": len(items),
        },
    }


def render_html(data: dict) -> str:
    """Render the self-contained multi-dimensional map.

    The page is a rotating 3-D point cloud in which **every point is a real
    repository item** and **every axis is a real attribute** read out of the
    ledgers.  The three axes are user-selectable, so the same object can be read
    along any three of the five dimensions.  Clicking a point opens a panel that
    quotes the item's Lean declarations, its artifact path, its pins, and --
    for a gap -- the barrier and the missing object.
    """
    payload = json.dumps(data, ensure_ascii=False)
    return _HTML_TEMPLATE.replace("/*__DATA__*/", payload)


_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Multi-dimensional map of the register</title>
<style>
  :root{
    --ink:#e8e8e8; --dim:#8a8a8a; --faint:#4a4a52;
    --ok:#56d364; --warn:#e3b341; --bad:#f85149; --info:#79c0ff; --mag:#d2a8ff;
  }
  *{box-sizing:border-box}
  body{margin:0;background:#0b0b0d;color:var(--ink);
       font-family:"Consolas","DejaVu Sans Mono",monospace;font-size:13px}
  header{padding:14px 20px 8px;border-bottom:1px solid #1e1e24}
  h1{margin:0 0 4px;font-size:15px;letter-spacing:2px}
  .sub{color:var(--dim);font-size:11px;line-height:1.6;max-width:1100px}
  .sub b{color:var(--ink)}
  .wrap{display:flex;gap:0;height:calc(100vh - 92px)}
  .left{width:268px;flex:0 0 268px;padding:14px;overflow-y:auto;
        border-right:1px solid #1e1e24;background:#0e0e11}
  .mid{flex:1;position:relative;min-width:420px}
  .right{width:360px;flex:0 0 360px;padding:14px;overflow-y:auto;
         border-left:1px solid #1e1e24;background:#0e0e11}
  .grp{margin-bottom:16px}
  .lbl{font-size:10px;letter-spacing:2px;color:var(--faint);margin-bottom:6px}
  select{width:100%;background:#16161b;color:var(--ink);border:1px solid #2e2e36;
         border-radius:6px;padding:6px;font-family:inherit;font-size:12px;margin-bottom:6px}
  .chk{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--dim);
       margin:3px 0;cursor:pointer;user-select:none}
  .chk:hover{color:var(--ink)}
  .sw{width:11px;height:11px;border-radius:3px;flex:0 0 11px}
  .axis3{position:absolute;left:20px;top:16px;font-size:10px;letter-spacing:1px;
         color:var(--faint);line-height:1.7;pointer-events:none}
  canvas{display:block;cursor:grab}
  canvas:active{cursor:grabbing}
  .hud{position:absolute;right:14px;top:14px;text-align:right;font-size:11px;
       color:var(--dim);line-height:1.7;pointer-events:none}
  .card{border:1px solid #26262e;border-radius:9px;padding:11px 13px;margin-bottom:11px;
        background:#111114}
  .card h3{margin:0 0 5px;font-size:12px;letter-spacing:1px}
  .card p{margin:0 0 7px;font-size:11px;color:var(--dim);line-height:1.6}
  code{color:var(--info)}
  .pill{display:inline-block;font-size:10px;padding:1px 7px;border-radius:999px;
        border:1px solid var(--faint);margin:0 4px 4px 0;color:var(--dim)}
  .pill.ok{color:var(--ok);border-color:var(--ok)}
  .pill.warn{color:var(--warn);border-color:var(--warn)}
  .pill.bad{color:var(--bad);border-color:var(--bad)}
  .pill.info{color:var(--info);border-color:var(--info)}
  .pill.mag{color:var(--mag);border-color:var(--mag)}
  .decls{max-height:210px;overflow:auto;font-size:10.5px;color:var(--info);
         background:#0a0a0d;border:1px solid #1c1c22;border-radius:6px;padding:8px;
         line-height:1.55;word-break:break-all}
  .empty{color:var(--faint);font-size:11px;font-style:italic}
  .legend{font-size:10.5px;color:var(--dim);line-height:1.7}
  .foot{padding:8px 20px 20px;color:var(--faint);font-size:10.5px;line-height:1.6}
  a{color:var(--info)}
</style>
</head>
<body>
<header>
  <h1>MULTI-DIMENSIONAL MAP OF THE REGISTER</h1>
  <div class="sub">
    Every point is a <b>real repository item</b>; every axis is a <b>real attribute</b> read
    out of the ledgers &mdash; never drawn by hand. Axes:
    <b>category</b> (the 9 ledger categories), <b>status</b> (machine-checked &rarr; open),
    <b>depth</b> (position in the true <code>import</code> DAG), <b>kind</b> (module / gap / card),
    <b>tier</b> (register-debt tier). Pick any three for x/y/z. Drag to rotate, scroll to zoom,
    click a point to inspect it.
  </div>
</header>

<div class="wrap">
  <div class="left">
    <div class="grp">
      <div class="lbl">AXES</div>
      <select id="axX"></select>
      <select id="axY"></select>
      <select id="axZ"></select>
    </div>
    <div class="grp">
      <div class="lbl">KIND</div>
      <div id="kindBox"></div>
    </div>
    <div class="grp">
      <div class="lbl">STATUS</div>
      <div id="statusBox"></div>
    </div>
    <div class="grp">
      <div class="lbl">CATEGORY</div>
      <div id="catBox"></div>
    </div>
    <div class="grp legend" id="legend"></div>
    <div class="grp">
      <div class="lbl">RESET</div>
      <button id="reset" style="width:100%;background:#16161b;color:var(--ink);
        border:1px solid #2e2e36;border-radius:6px;padding:6px;cursor:pointer;
        font-family:inherit;font-size:12px">show all</button>
    </div>
  </div>

  <div class="mid">
    <div class="axis3" id="axisLbl"></div>
    <canvas id="cv"></canvas>
    <div class="hud" id="hud"></div>
  </div>

  <div class="right" id="detail">
    <div class="card"><h3>INSPECT</h3>
      <p class="empty">Click any point in the cloud.</p></div>
  </div>
</div>

<div class="foot" id="foot"></div>

<script>
const DATA = /*__DATA__*/;
const DIMS = DATA.dims;
const ITEMS = DATA.items;
const EDGES = DATA.edges;

const STATUS_COLOR = {
  "machine-checked":"#56d364", "partial":"#e3b341", "no-go":"#d2a8ff",
  "citation-only":"#79c0ff", "empirical":"#8a8a8a", "open":"#f85149"
};
const KIND_COLOR = { "module":"#79c0ff", "gap":"#f85149", "card":"#56d364" };

const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
let W=0,H=0;

let axX='category', axY='status', axZ='depth';
const off = {module:{x:0,y:0}, gap:{x:0,y:0}, card:{x:0,y:0}};
const visible = {kind:new Set(Object.keys(KIND_COLOR)),
                 status:new Set(DIMS.status),
                 category:new Set(DIMS.category)};

let rotY = 0.62, rotX = -0.42, zoom = 1;
let dragging=false, lx=0, ly=0, moved=false;
let pts=[]; let sel=null;

function dimValues(d){
  if(d==='depth'){
    const m = Math.max(1, ...ITEMS.map(i=>i.depth||0));
    return {keys:Array.from({length:m+1},(_,i)=>String(i)), isNum:true};
  }
  if(d==='kind') return {keys:DIMS.kind, isNum:false};
  if(d==='status') return {keys:DIMS.status, isNum:false};
  if(d==='tier') return {keys:DIMS.tier, isNum:false};
  return {keys:DIMS.category, isNum:false};
}
function coord(item, dim){
  const dv = dimValues(dim);
  const v = dim==='depth' ? (item.depth||0)
          : dim==='kind' ? item.kind
          : dim==='status' ? item.status
          : dim==='tier' ? (item.tier||'B')
          : item.category;
  let idx = dv.keys.indexOf(String(v));
  if(idx<0) idx = 0;
  const n = Math.max(1, dv.keys.length-1);
  return dv.isNum ? (n? idx/n : 0) : (n? idx/n : 0);
}

function buildOptions(){
  const sel=document.getElementById('axX');
  const dims=[['category','category'],['status','status'],['depth','depth'],
              ['kind','kind'],['tier','tier']];
  for(const id of ['axX','axY','axZ']){
    const s=document.getElementById(id); s.innerHTML='';
    for(const [v,l] of dims){
      const o=document.createElement('option');
      o.value=v; o.textContent=l; s.appendChild(o);
    }
  }
  sel.value=axX;
  document.getElementById('axY').value=axY;
  document.getElementById('axZ').value=axZ;
}

function buildFilters(){
  const mk=(boxId, dim, keys)=>{
    const box=document.getElementById(boxId); box.innerHTML='';
    keys.forEach(k=>{
      const lab=document.createElement('label');
      lab.className='chk';
      const cb=document.createElement('input');
      cb.type='checkbox'; cb.checked=true;
      cb.onchange=()=>{
        if(cb.checked) visible[dim].add(k); else visible[dim].delete(k);
        draw();
      };
      const sw=document.createElement('span'); sw.className='sw';
      sw.style.background = dim==='status'? (STATUS_COLOR[k]||'#666')
                          : dim==='kind'? (KIND_COLOR[k]||'#666') : '#4a4a52';
      const tx=document.createElement('span'); tx.textContent=k;
      lab.appendChild(cb); lab.appendChild(sw); lab.appendChild(tx);
      box.appendChild(lab);
    });
  };
  mk('kindBox','kind',DIMS.kind);
  mk('statusBox','status',DIMS.status);
  mk('catBox','category',DIMS.category);
}

function shown(item){
  return visible.kind.has(item.kind) && visible.status.has(item.status)
      && visible.category.has(item.category);
}

function layout(){
  const jitter = {};
  const byKey = {};
  for(const it of ITEMS){
    const k = it.kind+'|'+(it.category)+'|'+(it.status);
    (byKey[k] = byKey[k]||[]).push(it);
  }
  for(const k in byKey){
    const arr = byKey[k];
    arr.forEach((it,idx)=>{
      // deterministic spread within the cell so points don't overlap exactly
      const a = (idx*2.39996322972865332) % (2*Math.PI);
      const r = 0.06 + 0.028*Math.sqrt(idx);
      const x0 = coord(it,axX)*2-1, y0 = coord(it,axY)*2-1, z0 = coord(it,axZ)*2-1;
      it._x = x0 + Math.cos(a)*r*0.9;
      it._y = y0 + Math.sin(a)*r*0.9;
      it._z = z0 + ((idx%3)-1)*0.03;
    });
  }
}

function project(p){
  const cy=Math.cos(rotY), sy=Math.sin(rotY);
  const cx=Math.cos(rotX), sx=Math.sin(rotX);
  let x=p._x*cy - p._z*sy;
  let z=p._x*sy + p._z*cy;
  let y=p._y*cx - z*sx;
  z=p._y*sx + z*cx;
  const s=1.6*zoom/(2.4+z*0.5);
  return { x:W/2 + x*s*Math.min(W,H)*0.42, y:H/2 - y*s*Math.min(W,H)*0.42, s:s, z:z };
}

function draw(){
  layout();
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#0a0a0c'; ctx.fillRect(0,0,W,H);
  // grid floor
  ctx.strokeStyle='#15151a'; ctx.lineWidth=1;
  for(let i=-1;i<=1;i+=0.25){
    const a=project({_x:i,_y:-1,_z:-1}), b=project({_x:i,_y:1,_z:-1});
    ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
    const c=project({_x:-1,_y:i,_z:-1}), d=project({_x:1,_y:i,_z:-1});
    ctx.beginPath(); ctx.moveTo(c.x,c.y); ctx.lineTo(d.x,d.y); ctx.stroke();
  }
  // import edges (module -> module) among visible items
  const idset = new Set(ITEMS.filter(shown).map(i=>i.id));
  ctx.strokeStyle='rgba(121,192,255,0.13)'; ctx.lineWidth=1;
  for(const [a,b] of EDGES){
    if(!idset.has(a)||!idset.has(b)) continue;
    const ia=ITEMS.find(i=>i.id===a), ib=ITEMS.find(i=>i.id===b);
    if(!ia||!ib||ia.kind!=='module'||ib.kind!=='module') continue;
    const pa=project(ia), pb=project(ib);
    ctx.beginPath(); ctx.moveTo(pa.x,pa.y); ctx.lineTo(pb.x,pb.y); ctx.stroke();
  }
  // points
  pts=[];
  for(const it of ITEMS){
    if(!shown(it)) continue;
    const p=project(it);
    p.item=it; pts.push(p);
  }
  pts.sort((a,b)=>a.z-b.z);
  for(const p of pts){
    const it=p.item;
    const r = it.kind==='module' ? 4.5 : it.kind==='card' ? 3.4 : 4.0;
    const rad = r*Math.max(0.45,p.s*1.1);
    ctx.fillStyle = KIND_COLOR[it.kind] || '#888';
    ctx.globalAlpha = it.status==='open' ? 0.95 : 0.85;
    ctx.beginPath(); ctx.arc(p.x,p.y,rad,0,7); ctx.fill();
    ctx.globalAlpha=1;
    if(it.status==='open'){
      ctx.strokeStyle=STATUS_COLOR[it.status]; ctx.lineWidth=1.2;
      ctx.beginPath(); ctx.arc(p.x,p.y,rad+3.5,0,7); ctx.stroke();
    }
    if(sel && sel.id===it.id){
      ctx.strokeStyle='#fff'; ctx.lineWidth=1.6;
      ctx.beginPath(); ctx.arc(p.x,p.y,rad+6,0,7); ctx.stroke();
    }
  }
  // labels for a few
  ctx.font='10px monospace'; ctx.fillStyle='#5a5a62';
  for(const p of pts){
    const it=p.item;
    if(it.kind!=='module') continue;
    if(rotY<0.9 || rotY>5.4) continue;
    ctx.fillText(it.id, p.x+8, p.y+3);
  }
  document.getElementById('hud').innerHTML =
    '<div>items: '+pts.length+' / '+ITEMS.length+'</div>'+
    '<div>edges: '+EDGES.length+'</div>'+
    '<div>x='+axX+'  y='+axY+'  z='+axZ+'</div>';
  document.getElementById('axisLbl').innerHTML =
    'x &larr; '+axX+'<br>y &larr; '+axY+'<br>z &larr; '+axZ;
}

function resize(){
  const mid=document.querySelector('.mid');
  W=mid.clientWidth; H=mid.clientHeight;
  cv.width=W; cv.height=H; draw();
}

function pick(mx,my){
  let best=null, bd=1e9;
  for(const p of pts){
    const d=(p.x-mx)*(p.x-mx)+(p.y-my)*(p.y-my);
    if(d<bd){bd=d; best=p;}
  }
  if(best && bd<400) return best.item;
  return null;
}

function esc(s){
  return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;');
}

function statusPill(s){
  const cls = s==='machine-checked'?'ok': s==='open'?'bad':
              (s==='partial'||s==='no-go')?'warn': s==='citation-only'?'info':'';
  return '<span class="pill '+cls+'">'+esc(s)+'</span>';
}

function showDetail(it){
  const box=document.getElementById('detail');
  if(!it){ box.innerHTML='<div class="card"><h3>INSPECT</h3><p class="empty">Click any point in the cloud.</p></div>'; return; }
  let h='<div class="card"><h3>'+esc(it.id)+' &mdash; '+esc(it.kind)+'</h3>';
  if(it.title) h+='<p>'+esc(it.title)+'</p>';
  h+='<div>'+statusPill(it.status);
  h+='<span class="pill">'+esc(it.category)+'</span>';
  h+='<span class="pill mag">depth '+esc(it.depth)+'</span>';
  if(it.tier) h+='<span class="pill">tier '+esc(it.tier)+'</span>';
  if(it.proof_kind) h+='<span class="pill">attempt: '+esc(it.proof_kind)+'</span>';
  h+='</div>';
  if(it.subject) h+='<p><b>subject:</b> '+esc(it.subject)+'</p>';
  if(it.artifact) h+='<p><b>artifact:</b><br><code>'+esc(it.artifact)+'</code></p>';
  if(it.pins && it.pins.length) h+='<p><b>pins:</b> '+it.pins.map(p=>'<code>'+esc(p)+'</code>').join(' ')+'</p>';
  if(it.barrier) h+='<p><b>barrier:</b> '+esc(it.barrier)+'</p>';
  if(it.missing) h+='<p><b>missing object:</b> '+esc(it.missing)+'</p>';
  if(it.cards && it.cards.length) h+='<p><b>cards:</b> '+it.cards.map(c=>'<code>'+esc(c)+'</code>').join(' ')+'</p>';
  if(it.gaps && it.gaps.length) h+='<p><b>gaps:</b> '+it.gaps.map(c=>'<code>'+esc(c)+'</code>').join(' ')+'</p>';
  if(it.decls && it.decls.length){
    h+='<p><b>lean declarations</b> ('+it.ndecls+' total):</p><div class="decls">';
    h+=it.decls.map(d=>esc(d)).join('<br>');
    h+='</div>';
  }
  h+='</div>';
  box.innerHTML=h;
}

cv.addEventListener('mousedown',e=>{dragging=true;moved=false;lx=e.clientX;ly=e.clientY;});
window.addEventListener('mouseup',e=>{
  if(dragging && !moved){
    const r=cv.getBoundingClientRect();
    const it=pick(e.clientX-r.left, e.clientY-r.top);
    sel=it; showDetail(it); draw();
  }
  dragging=false;
});
window.addEventListener('mousemove',e=>{
  if(!dragging) return;
  const dx=e.clientX-lx, dy=e.clientY-ly;
  if(Math.abs(dx)+Math.abs(dy)>3) moved=true;
  rotY+=dx*0.008; rotX+=dy*0.008;
  rotX=Math.max(-1.4,Math.min(1.4,rotX));
  lx=e.clientX; ly=e.clientY; draw();
});
cv.addEventListener('wheel',e=>{e.preventDefault();zoom*= (e.deltaY<0?1.08:0.93);
  zoom=Math.max(0.4,Math.min(3.2,zoom)); draw();},{passive:false});

for(const id of ['axX','axY','axZ']){
  document.getElementById(id).addEventListener('change',e=>{
    if(id==='axX')axX=e.target.value; else if(id==='axY')axY=e.target.value;
    else axZ=e.target.value; draw();
  });
}
document.getElementById('reset').onclick=()=>{
  visible.kind=new Set(Object.keys(KIND_COLOR));
  visible.status=new Set(DIMS.status);
  visible.category=new Set(DIMS.category);
  buildFilters(); draw();
};

buildOptions(); buildFilters();
document.getElementById('foot').innerHTML =
  'Generated by <code>04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/build_multidimensional_map.py</code> '+
  'from <code>MODULE_LEDGER.md</code>, <code>MATHEMATICAL_LINK_GRAPH.md</code>, '+
  '<code>THE_GAP_LEDGER.md</code>, <code>CLAIM_TRACEABILITY.md</code> and the Lean sources. '+
  'Counts: '+DATA.counts.modules+' modules, '+DATA.counts.gaps+' gap rows, '+
  DATA.counts.cards+' cards, '+DATA.counts.edges+' real import edges. '+
  'The blue lines are the <b>actual</b> <code>import</code> edges, not a drawing.';
window.addEventListener('resize',resize);
resize();
</script>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DOCS / "MULTIDIMENSIONAL_MAP.html"))
    ap.add_argument("--json", default=str(DATA_OUT))
    args = ap.parse_args()

    data = build()

    # The JSON is a *generated* artifact: it goes to a `data/` root so the
    # persistence standard (regen_data.py) sees it as regenerable, not as a
    # load-bearing file that would vanish in a fresh clone.
    jpath = Path(args.json)
    jpath.parent.mkdir(parents=True, exist_ok=True)
    jpath.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")

    html = render_html(data)
    Path(args.out).write_text(html, encoding="utf-8")

    print(json.dumps(data["counts"], indent=1))
    print("wrote", jpath)
    print("wrote", args.out)


if __name__ == "__main__":
    main()

