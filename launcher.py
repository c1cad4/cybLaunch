#!/usr/bin/env python3
"""Explicit development commands for the cybOS repositories; no shell interpolation."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def load_registry(root):
    data = json.loads((root / 'cybOS' / 'ecosystem.json').read_text())
    repos = data['repositories']
    names = [repo['name'] for repo in repos]
    if len(names) != len(set(names)):
        raise ValueError('duplicate repository names')
    for repo in repos:
        name = repo['name']
        if not name or Path(name).name != name or name in ('.', '..'):
            raise ValueError('invalid repository path')
        command = repo.get('test_command')
        if command is not None and (not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command)):
            raise ValueError('test_command must be an argv list')
    return repos


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('list')
    test = sub.add_parser('test'); test.add_argument('repository', nargs='?', default='all')
    serve = sub.add_parser('serve'); serve.add_argument('repository'); serve.add_argument('--port', type=int, default=8000)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    repos = load_registry(root)
    if args.action == 'list':
        for repo in repos:
            print(f"{repo['name']:25} {repo['status']:18} {repo['role']}")
        return 0
    chosen = repos if getattr(args, 'repository') == 'all' else [r for r in repos if r['name'] == args.repository]
    if not chosen:
        parser.error('unknown repository')
    if args.action == 'serve':
        repo = chosen[0]
        if not repo.get('web_entry'):
            parser.error('repository has no static web application')
        if not 1024 <= args.port <= 65535:
            parser.error('port must be between 1024 and 65535')
        subprocess.run([sys.executable, '-m', 'http.server', str(args.port), '--bind', '127.0.0.1', '--directory', str(root / repo['name'])], check=True)
        return 0
    failures = 0
    for repo in chosen:
        command = repo.get('test_command')
        if command is None:
            print(f"UNRUN {repo['name']}: {repo.get('limitation', 'manual or platform-specific workflow')}", flush=True)
            continue
        if not (root / repo['name']).is_dir():
            print(f"MISSING {repo['name']}", flush=True); failures += 1; continue
        print(f"CHECK {repo['name']}", flush=True)
        result = subprocess.run(command, cwd=root / repo['name'])
        print(f"{'PASS' if result.returncode == 0 else 'FAIL'} {repo['name']}", flush=True)
        failures += result.returncode != 0
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
