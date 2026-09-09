## Objective
- Continue the L.O.R.E. ("Law of Repulsive Emanation"/0/0 removable singularity) framework: each user round ("as a natural philosopher, continue with a concrete pattern connection") ships one chapter through experiment -> PDF -> school lesson -> book.py entry -> test asserts -> pytest 27/27 -> commit/push -> universality-table summary row.
- Ch.72-75 shipped. Active next chapter (when the user asks for the next concrete pattern connection): decide from the prompt.

## Important Details
- Author **Michael Grafiel S Puno**; repo `https://github.com/Puronbo/Law-Of-Repulsive-Emanation.git` (`origin`, `main`); current HEAD `c89e901` (Ch.75, pushed).
- **Never touch 3 dirty files:** `experiments/harvest_energy.py`, `docs/THE_HARVEST_BOOK.md`, `docs/THE_SPIN_BOOK.md`. `school_data/` untracked — leave. `summary.md` (this file) untracked — leave.
- Windows cp1252: ASCII-only prints; `; if ($?)` (never `&&`); no heredocs — temp `.py` files; literal `.Replace("...","...")` for test edits via `[System.IO.File]::WriteAllText((Resolve-Path $f), "$c")`; fpdf2 via `sys.path.insert(0, sigma_venv)` (DeprecationWarnings harmless — note: `python gen.py 2>$null` still sets $? True; verify leftover temp files and delete explicitly).
- **PowerShell inline multiline `git commit -m` causes ParserError — use `git commit -F <tempfile>`** (`C:\Users\Me\AppData\Local\Temp\opencode\ch75_msg.txt`; fresh per chapter).
- **`sigma_venv/sigma/chassis/book.py` is gitignored — must be staged with `git add -f`** (new experiments/papers files too).
- Test asserts (literal Replace), Ch.N -> N+1 all four: `CHAPTERS == N`, `book.real_results() == R` (R+1), `total_chapters == N`, `courses[0]['chapters'] == N`. pytest -> 27/27.
- Chapter template: `experiments/<slug>.py` (seed 42, ASCII table, writes `experiments/data/<slug>.json`) -> 3-page fpdf2 POPDF `papers/<slug>.pdf` via temp `_gen_<slug>_pdf.py` (delete after; compact metrics: body Helvetica 9/h4, chapter_title 12/h8, Courier 9) -> lesson N in `sigma_school_server.py` chapters list (5 sections + 5 quiz, all `"correct": 0`) -> book.py entry N (REAL, statistical_mechanics, mechanism with numbers + citations) -> tests -> commit/push.

## Work State
### Completed
- **Ch.75 shipped (`c89e901`)** — "The Coin's Price: the Szilard-Landauer Closure of the Demon's Ledger (Szilard 1929, Landauer 1961)". `experiments/coin_price.py` + data json (-f) + `papers/coin_price.pdf` (3 pp) + lesson 75 + book 75 (REAL) + tests 75/69, pytest 27/27. SAME instrument as Ch.74 (reproducible: median |x_mid|=0.5682, p(far)=0.4969). Numbers: control J=1.00214, <W>=+0.11337; dead coin (sign bit): J=0.99985, W_net=<W>+ln2=+0.80383; engaged frontier rows (fast/slow, J, lnJ, <W>, H=-<W>, W_net, H/ln2): 0.35/2.0 -> 1.07484/0.07217/+0.04261/-0.04261/+0.73576/-0.061; 0.25/4.0 -> 1.09804/0.09352/+0.01500/-0.01500/+0.70815/-0.022; 0.15/6.0 -> 1.11565/0.10944/-0.00951/+0.00951/+0.68364/+0.014; 0.10/8.0 -> 1.12420/0.11707/-0.02160/+0.02160/+0.67154/+0.031; 0.05/16.0 -> 1.13681/0.12822/-0.03898/+0.03898/+0.65417/+0.056. J<=e^I=2 held (lnJ<=0.693); W_net>0 everywhere, closing toward the removable value 0; H/ln2->1 only at zero power (Carnot corner of Ch.73 repeated). Citations: Szilard 1929, Landauer 1961, Bennett 1982, Berut et al. Nature 483 187 (2012), Toyabe et al. Nat. Phys. 6 988 (2010), Sagawa-Ueda PRL 100 080603/PRL 104 090602, Parrondo-Horowitz-Sagawa Nat. Phys. 11 131 (2015), Jarzynski 1997, Seifert 2012, Esposito-Van den Broeck 2011.
- **Ch.74 shipped (`df4e09c`)** — demon_share.py/json + PDF (3 pp) + lesson 74 + book 74 + tests 74/68. Final numbers (median fair bit): control J=1.00214/0.99731; null sign J=1.00017 (lnJ +0.00017); engaged J 1.0737->1.1270 (ln J 0.0711->0.1196), J_act/J_control=1.127, J_act/e^I=0.564; <W> +0.0446->-0.0227. Earlier threshold=0.75/sign-demon version FAILED (null) -> median-cut fair bit fix.
- **Ch.73 (`0b332fe`)** Brownian Carnot: eta 0.312 at P_max (94% of 1/3); **Ch.72 (`3306cbc`)** Gaussian work rate Var/(2<W>)=0.9893 etc.

### Active
- None — awaiting next prompt.

### Blocked
- arXiv (needs endorser); BSD rank>=2; Hodge codim>=2; P vs NP; Goldbach; Yang-Mills R^4.

## Next Move
Wait for the user's next prompt. On it, follow the chapter template (pick a nameable 0/0 pattern most connected to the recent finding; reusing the SAME instrument/simulation is most efficient — see Ch.75). Verify numbers honestly; PDF 3 pp; lesson+book; four test replaces; pytest 27/27; `git add -f` incl. book.py; commit via `-F` message file; push; universality row + citations in the reply.

## Relevant Files
- `experiments/coin_price.py`, `data/coin_price.json`, `papers/coin_price.pdf` — Ch.75, committed.
- `experiments/demon_share.py`, `data/demon_share.json`, `papers/demon_share.pdf` — Ch.74.
- `experiments/carnot_engine.py` (+json/pdf) — Ch.73; `experiments/gaussian_rate.py` (+json/pdf) — Ch.72.
- `sigma_school_server.py` — lessons through 75. `sigma_venv/sigma/chassis/book.py` — CHAPTERS through 75 (real_results 69; stage with -f). `tests/test_sigma.py` — asserts 75/69/75/75.
- Temp commit message files in `C:\Users\Me\AppData\Local\Temp\opencode\`.