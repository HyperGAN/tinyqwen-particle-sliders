"""Regenerate the coherent v3 source/data indexes from the approved Git objects.

Maintenance only: python tools/refresh_source_lock.py --core-source /path/to/core
Requires an installed exact-Git core and an unchanged approved source checkout.
"""
import argparse
import hashlib
from importlib.metadata import distribution
import json
from pathlib import Path
import subprocess

CORE = 'a794e3b4a8813b012f2c4faa3da82b78d4a90214'
PREVIOUS = 'a2798264059c2b7c260ec98f3db8a21e41c8819c'
ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'packages/particle-sliders-core/src/particle_sliders/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def index_digest(index):
    return digest(json.dumps(index, sort_keys=True, separators=(',', ':')).encode())


def sources(root, exclude=()):
    return {str(p.relative_to(root)): digest(p.read_bytes()) for p in root.rglob('*')
            if p.is_file() and '__pycache__' not in p.relative_to(root).parts
            and p.suffix != '.pyc' and str(p.relative_to(root)) not in exclude}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--core-source', type=Path, required=True)
    args = parser.parse_args()
    core = args.core_source.resolve()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(core), *args])
    if git('rev-parse', 'HEAD').decode().strip() != CORE or git('status', '--porcelain').strip():
        raise SystemExit('Require a clean checkout of the exact approved core commit')
    paths = git('ls-tree', '-r', '--name-only', CORE, '--', PREFIX).decode().splitlines()
    expected = {path.removeprefix(PREFIX): digest(git('show', CORE + ':' + path)) for path in paths}
    import particle_sliders
    actual = sources(Path(particle_sliders.__file__).parent)
    if actual != expected:
        raise SystemExit('Actually imported core source/data differs from approved Git objects')
    dist = distribution('particle-sliders-core')
    origin = json.loads(dist.read_text('direct_url.json') or '{}')
    if (dist.version != '0.12.0' or origin.get('vcs_info', {}).get('commit_id') != CORE
            or origin.get('url') != 'https://github.com/HyperGAN/particle-sliders.git'
            or origin.get('subdirectory') != 'packages/particle-sliders-core'):
        raise SystemExit('Require exact installed immutable Git origin')
    package = ROOT / 'src/tinyqwen_shared_preview'
    product = sources(package, exclude=('sources.lock.json',))
    archived = json.loads((ROOT / 'compatibility/preview-v2-source.lock.json').read_text())
    lock = dict(schema='tinyqwen-shared-preview-lock-v3', core_commit=CORE, core_version='0.12.0',
        core_repository='https://github.com/HyperGAN/particle-sliders.git',
        core_subdirectory='packages/particle-sliders-core', core_sources=expected,
        core_sources_index_sha256=index_digest(expected), product_sources=product,
        product_sources_index_sha256=index_digest(product),
        inventory_exclusions=['generated __pycache__ directories', 'generated .pyc files',
                              'product sources.lock.json self-reference only'],
        pg='0.9.4', hndl='0.10.0', hypergan='5f368a3770cf5bdae0448995c9f76e29af8049f7',
        host_source=archived['host_source'], native_hidden_width=1024, native_qualified=False)
    (package / 'sources.lock.json').write_text(json.dumps(lock, indent=2, sort_keys=True) + '\n')
    # Preserve the original extraction receipt; index only changes/new files since it.
    def product_git(*args):
        return subprocess.check_output(['git', '-C', str(ROOT), *args])
    names = set(product_git('ls-files', '--cached', '--others', '--exclude-standard').decode().splitlines())
    updates = []
    for name in sorted(names - {'CORE-MIGRATION.json'}):
        path = ROOT / name
        if not path.is_file():
            raise SystemExit('No deletion is allowed in this final migration: ' + name)
        old = subprocess.run(['git', '-C', str(ROOT), 'show', PREVIOUS + ':' + name], capture_output=True)
        current = path.read_bytes()
        if old.returncode or current != old.stdout:
            updates.append(dict(path=name, before_sha256=None if old.returncode else digest(old.stdout),
                                after_sha256=digest(current)))
    migration = dict(schema='tinyqwen-final-core-migration-v1', predecessor_commit=PREVIOUS,
        core_commit=CORE, product_version='0.3.0', cohort='tinyqwen-pg094-hypergan-hndl-v3-cpu-fixture',
        artifact_policy='v2 packets require their original source/environment; no relabel/conversion',
        files=updates)
    (ROOT / 'CORE-MIGRATION.json').write_text(json.dumps(migration, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(core_files=len(expected), product_files=len(product),
                         core_sources_index_sha256=lock['core_sources_index_sha256'], updates=len(updates)), indent=2))


if __name__ == '__main__':
    main()
