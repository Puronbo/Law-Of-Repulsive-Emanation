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
    names = []
    for f in sorted(os.listdir(EXPERIMENTS)):
        if f.endswith('.py') and not f.startswith('__'):
            names.append(f[:-3])
    return names


def main(argv=None):
    p = argparse.ArgumentParser(
        prog='puno',
        description='Puno Calculus experiment runner')
    sub = p.add_subparsers(dest='cmd', metavar='{list,run,test}')
    sub.add_parser('list', help='list available experiments')
    run = sub.add_parser('run', help='run an experiment by name')
    run.add_argument('name', help='experiment module name (see: puno list)')
    sub.add_parser('test', help='run the regression suite (pytest)')
    args = p.parse_args(argv)

    if args.cmd == 'list':
        for name in _available():
            print(name)
        return 0
    if args.cmd == 'test':
        return subprocess.call(
            [sys.executable, '-m', 'pytest', TESTS, '-q'])
    if args.cmd == 'run':
        if args.name not in _available():
            print(f"unknown experiment {args.name!r}; try: puno list")
            return 2
        return subprocess.call(
            [sys.executable, os.path.join(EXPERIMENTS, args.name + '.py')])
    p.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
