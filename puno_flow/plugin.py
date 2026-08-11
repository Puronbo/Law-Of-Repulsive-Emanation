"""Plug-and-play function registry: drop a function in, get a UI for it.

The point of this module is "any function, zero boilerplate."  A plugin is a
plain Python function decorated with ``@plugin(...)``; its parameters are
declared either explicitly (``params=[param(...), ...]``) or derived from the
signature's type hints and defaults.  The same registry feeds the web UI, the
CLI, and the test suite, so one declaration covers every front end:

    from puno_flow.plugin import plugin, param

    @plugin(title="Add two numbers", description="...",
            params=[param("a", float, 0.0, "first operand"),
                    param("b", float, 0.0, "second operand")])
    def add(params):
        return {"sum": params["a"] + params["b"]}

Or with no explicit params, the signature is introspected:

    @plugin(title="Fahrenheit -> Celsius")
    def to_celsius(f: float = 32.0) -> float:
        return (f - 32.0) * 5.0 / 9.0

Plug-ins live in a ``plugins/`` directory (any module that calls ``@plugin``)
and are also auto-discovered from ``experiments/`` by
``experiments_catalog()`` - every verdict experiment in the repo ships its
docstring + ``--verdict`` flag, so it appears in the catalog without any
declaration.  The registry keeps separate "function" (callable) and
"experiment" (subprocess verdict) entries but presents one unified catalog.

Run a plugin programmatically:

    from puno_flow.plugin import registry, run
    result = run("add", {"a": 2, "b": 3})

Useful bits:
  - ``jsonable()`` normalizes numpy scalars/arrays, sets, tuples, enums, and
    arbitrary objects to JSON-safe values, so a plugin may return anything.
  - ``Registry.catalog()`` returns the full spec (name, title, description,
    params, source, kind) that the web UI turns into a form with zero code.
"""

from __future__ import annotations

import dataclasses
import enum
import importlib
import inspect
import json
import os
import pathlib
import sys
import types
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

__all__ = [
    "Param", "Plugin", "param", "plugin", "jsonable", "run", "run_async",
    "Registry", "registry", "discover_plugins", "experiments_catalog",
]


# ---------------------------------------------------------------------- #
# Parameter + plugin spec
# ---------------------------------------------------------------------- #
class Param:
    """One form field.  ``type`` is one of str/int/float/bool/choice/bytes
    or a callable coercer.  ``choices`` turns the field into a dropdown."""

    __slots__ = ("name", "type", "default", "description", "choices",
                 "required")

    def __init__(self, name, type="str", default=None, description="",
                 choices=None, required=False):
        self.name = name
        self.type = type
        self.default = default
        self.description = description
        self.choices = choices
        self.required = required

    @property
    def type_name(self):
        if isinstance(self.type, type):
            return _TYPE_NAMES.get(self.type, self.type.__name__)
        if isinstance(self.type, str):
            return self.type
        return getattr(self.type, "__name__", str(self.type))

    def coerce(self, value):
        """Coerce a form/JSON value to the declared type (with defaults)."""
        if value is None:
            return self.default
        t = self.type
        if t is bool:
            if isinstance(value, str):
                return value.strip().lower() in ("1", "true", "yes", "on")
            return bool(value)
        if t is int:
            return int(float(value))
        if t is float:
            return float(value)
        if t in (str, bytes):
            return value if isinstance(value, t) else str(value)
        if isinstance(t, type) and t in (list, tuple, dict, set):
            return t(value)
        if callable(t):          # custom coercer
            return t(value)
        return value

    def spec(self):
        out = {"name": self.name, "type": self.type_name,
               "description": self.description, "choices": self.choices,
               "required": self.required}
        try:
            json.dumps(self.default)          # JSON-safe default?
            out["default"] = self.default
        except (TypeError, ValueError):
            out["default"] = jsonable(self.default)
        return out


_TYPE_NAMES = {str: "str", int: "int", float: "float", bool: "bool",
               bytes: "bytes", list: "list", tuple: "tuple", dict: "dict"}


def param(name, type="str", default=None, description="", choices=None,
          required=False):
    """Declare one form parameter for a plugin."""
    return Param(name, type=type, default=default, description=description,
                 choices=choices, required=required)


class Plugin:
    """A registered callable (function kind) or subprocess verdict
    (experiment kind).  ``fn`` is the callable for functions; for
    experiments ``module`` names the experiments/ module and ``script`` the
    argv to run its verdict."""

    def __init__(self, name, fn=None, title=None, description="",
                 params=(), kind="function", source="", module=None,
                 script=None, data_json=None):
        self.name = name
        self.fn = fn
        self.title = title or name
        self.description = description
        self.params = list(params)
        self.kind = kind                     # "function" | "experiment"
        self.source = source                 # human-readable origin
        self.module = module                 # experiments/<module>.py
        self.script = script                 # argv list for the verdict
        self.data_json = data_json           # data/<module>_data.json

    def spec(self, with_source=False):
        out = {"name": self.name, "title": self.title,
               "description": self.description, "kind": self.kind,
               "params": [p.spec() for p in self.params]}
        if with_source:
            out["source"] = self.source
        if self.data_json:
            out["data_json"] = os.path.basename(self.data_json)
        return out

    def run(self, values=None):
        if self.fn is None:
            raise ValueError(f"{self.name} is an experiment, not a callable "
                             "(use the subprocess runner)")
        values = values or {}
        kwargs = {p.name: p.coerce(values.get(p.name))
                  for p in self.params}
        extra = {k: v for k, v in values.items()
                 if k not in {p.name for p in self.params}}
        kwargs.update(extra)
        out = self.fn(**kwargs)
        return jsonable(out)


# ---------------------------------------------------------------------- #
# Decorators
# ---------------------------------------------------------------------- #
def plugin(title=None, description="", params=(), kind="function", name=None):
    """Decorator: register a function as a UI-visible plugin.

    ``params`` may be a list of Param, or omitted to introspect the
    signature (type hints + defaults become the form fields)."""
    def deco(fn):
        pname = name or fn.__name__
        p = Plugin(pname, fn=fn, title=title or fn.__name__,
                   description=description or _doc_first_line(fn),
                   params=params or _introspect(fn), kind=kind,
                   source="plugins/ (decorated function)")
        registry.register(p)
        return fn
    return deco


def _doc_first_line(fn):
    doc = inspect.getdoc(fn) or ""
    return doc.strip().splitlines()[0] if doc.strip() else ""


def _introspect(fn):
    """Build Param list from the callable's signature (type hints, defaults,
    and the first line of each parameter's own docstring if present)."""
    sig = inspect.signature(fn)
    out = []
    hints = getattr(fn, "__annotations__", {})
    for name, pinfo in sig.parameters.items():
        if name in ("self", "cls") or pinfo.kind in (
                inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
            continue
        dflt = (pinfo.default if pinfo.default is not inspect.Parameter.empty
                else None)
        t = hints.get(name)
        if t is None or t is inspect.Parameter.empty:
            if isinstance(dflt, bool):
                t = bool
            elif isinstance(dflt, int):
                t = int
            elif isinstance(dflt, float):
                t = float
            elif isinstance(dflt, str):
                t = str
            else:
                t = str
        out.append(Param(name, type=t, default=dflt))
    return out


# ---------------------------------------------------------------------- #
# JSON normalizer
# ---------------------------------------------------------------------- #
def jsonable(obj):
    """Recursively normalize arbitrary plugin output to JSON-safe values:
    numpy scalars/arrays, sets, tuples, enums, dataclasses, dicts, lists."""
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, bytes):
        return obj.hex()
    if isinstance(obj, enum.Enum):
        return obj.value
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (np_array,)):
        return obj.tolist()
    if isinstance(obj, np_generic):
        return obj.item()
    if dataclasses.is_dataclass(obj):
        return {f.name: jsonable(getattr(obj, f.name))
                for f in dataclasses.fields(obj)}
    if hasattr(obj, "tolist"):                    # numpy-ish
        try:
            return obj.tolist()
        except Exception:
            pass
    if hasattr(obj, "items"):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if hasattr(obj, "__dict__"):
        return {k: jsonable(v) for k, v in vars(obj).items()}
    return str(obj)


try:                                  # numpy is optional for the registry
    import numpy as np
    np_array = np.ndarray
    np_generic = np.generic
except Exception:                     # pragma: no cover
    np_array = ()
    np_generic = ()


# ---------------------------------------------------------------------- #
# Registry
# ---------------------------------------------------------------------- #
class Registry:
    """Name -> Plugin map with lookup + a unified catalog for the UI."""

    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}

    def register(self, p: Plugin):
        if p.name in self._plugins:
            existing = self._plugins[p.name]
            if existing.kind == p.kind and existing.source == p.source:
                return                     # idempotent re-import
            raise ValueError(
                f"duplicate plugin name {p.name!r} ({existing.source} vs "
                f"{p.source})")
        self._plugins[p.name] = p
        return p

    def get(self, name):
        return self._plugins.get(name)

    def __contains__(self, name):
        return name in self._plugins

    def names(self, kind=None):
        if kind is None:
            return sorted(self._plugins)
        return sorted(n for n, p in self._plugins.items()
                      if p.kind == kind)

    def catalog(self, with_source=False):
        return [self._plugins[n].spec(with_source=with_source)
                for n in sorted(self._plugins)]

    def merge(self, other: "Registry"):
        for p in other._plugins.values():
            self.register(p)


registry = Registry()


def run(name, values=None):
    """Run a function-kind plugin by name; raises KeyError if absent and
    TypeError if the name refers to an experiment."""
    p = registry.get(name)
    if p is None:
        raise KeyError(f"no plugin named {name!r}")
    return p.run(values)


def run_async(name, values=None):
    """Run a plugin in a worker thread; returns a future whose result is
    already JSON-normalized (the UI uses this so heavy functions do not
    block other requests)."""
    import concurrent.futures
    return concurrent.futures.ThreadPoolExecutor(1).submit(
        lambda: run(name, values))


# ---------------------------------------------------------------------- #
# Discovery: plugins/ directory
# ---------------------------------------------------------------------- #
def repo_root():
    here = pathlib.Path(__file__).resolve()
    return here.parents[1]


def plugins_dir():
    return repo_root() / "plugins"


def discover_plugins():
    """Import every module in plugins/ that calls @plugin; returns the count
    registered.  Missing/non-Python files are skipped silently."""
    pdir = plugins_dir()
    if not pdir.is_dir():
        return 0
    before = set(registry._plugins)
    for f in sorted(pdir.iterdir()):
        if f.suffix != ".py" or f.name.startswith("_"):
            continue
        mod = f.stem
        if mod in sys.modules:
            continue
        try:
            importlib.import_module(f"plugins.{mod}")
        except Exception as exc:                      # pragma: no cover
            print(f"[plugins] {mod}: skipped ({exc})", file=sys.stderr)
    return len(set(registry._plugins) - before)


# ---------------------------------------------------------------------- #
# Discovery: experiments/ catalog
# ---------------------------------------------------------------------- #
def experiments_dir():
    return repo_root() / "experiments"


def _read_experiment_doc(module_file):
    """Docstring first line + verdict flag from an experiment module's
    source, without importing it (imports can be heavy: numpy/sklearn...)."""
    text = module_file.read_text(encoding="utf-8", errors="replace")
    head = text[:2000]
    first = ""
    if head.startswith('"""') or head.startswith("'''"):
        q = head[:3]
        rest = head[3:]
        first = rest.split(q, 1)[0].strip().splitlines()
        first = first[0].strip() if first else ""
    verdict = '"--verdict"' in text
    return first, verdict


def _default_data_json(mod):
    """The repo convention: data/<module>_data.json when it exists."""
    cand = repo_root() / "data" / (mod + "_data.json")
    return str(cand) if cand.is_file() else None


def experiments_catalog():
    """Auto-discover experiments/: every module in experiments/ becomes a
    catalog entry with its docstring's first line as the description.  A
    module that also carries a module-level ``PLUGIN_PARAMS`` list (Param
    objects) exposes form fields; otherwise the entry is a plain "run the
    verdict" card.  Verdict JSONs are linked by the standard
    ``data/<module>_data.json`` convention."""
    edir = experiments_dir()
    if not edir.is_dir():
        return
    for f in sorted(edir.glob("*.py")):
        if f.name.startswith("__"):
            continue
        mod = f.stem
        if registry.get(mod) is not None:
            continue                     # explicit plugin already registered
        first, verdict = _read_experiment_doc(f)
        title = first or mod
        script = ([sys.executable, str(f)]
                  + (["--verdict"] if verdict else []))
        p = Plugin(mod, title=title, description=first,
                   params=[], kind="experiment",
                   source="experiments/ (auto-discovered)",
                   module=mod, script=script,
                   data_json=_default_data_json(mod))
        registry.register(p)
    return True
