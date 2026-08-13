"""
Puno Calculus CLI: dispatch any experiment in experiments/ by name, list
the catalog, or run the regression suite.

Run directly:
    python puno_cli.py list
    python puno_cli.py run spring_fold
    python puno_cli.py test

Or install once and use the console script:
    pip install -e .
    puno list | puno run <name> | puno test
"""

import os, sys, argparse, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
EXPERIMENTS = os.path.join(ROOT, 'experiments')
TESTS = os.path.join(ROOT, 'tests')


def _available():
    if not os.path.isdir(EXPERIMENTS):
        return []
    names = []
    for f in sorted(os.listdir(EXPERIMENTS)):
        if f.endswith('.py') and not f.startswith('__'):
            names.append(f[:-3])
    return names


def _need_checkout():
    """Explain that experiments only run from a source checkout."""
    print("puno: no experiments/ directory here; the experiment catalog "
          "ships with a source checkout of the repo, not in the wheel.")
    print("      clone Law-Of-Repulsive-Emanation and run `pip install -e .`, "
          "or run experiments/ directly.")


def main(argv=None):
    p = argparse.ArgumentParser(
        prog='puno',
        description='Puno Calculus experiment runner')
    sub = p.add_subparsers(dest='cmd', metavar='{list,run,test,mandates}')
    sub.add_parser('list', help='list available experiments')
    run = sub.add_parser('run', help='run an experiment by name')
    run.add_argument('name', help='experiment module name (see: puno list)')
    sub.add_parser('test', help='run the regression suite (pytest)')
    sub.add_parser('mandates', help='report which professions are text-mandatable')
    args = p.parse_args(argv)

    if args.cmd == 'list':
        names = _available()
        if not names:
            _need_checkout()
            return 0
        for name in names:
            print(name)
        return 0
    if args.cmd == 'test':
        if not os.path.isdir(TESTS):
            _need_checkout()
            return 0
        return subprocess.call(
            [sys.executable, '-m', 'pytest', TESTS, '-q'])
    if args.cmd == 'mandates':
        from puno_app.mandates_server import _print_report
        from professions.report import build_report
        _print_report(build_report())
        return 0
    if args.cmd == 'run':
        if not _available():
            _need_checkout()
            return 2
        if args.name not in _available():
            print(f"unknown experiment {args.name!r}; try: puno list")
            return 2
        return subprocess.call(
            [sys.executable, os.path.join(EXPERIMENTS, args.name + '.py')])
    p.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
