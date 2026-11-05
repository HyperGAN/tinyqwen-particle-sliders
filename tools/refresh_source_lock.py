"""Regenerate the coherent v7 / official PG0.9.5 source/data indexes from the approved Git objects.

Maintenance only: python tools/refresh_source_lock.py --core-source /path/to/core
Requires an installed exact-Git core and an unchanged approved source checkout.
"""
import argparse
import hashlib
from importlib.metadata import distribution
import json
from pathlib import Path
import subprocess

CORE = '3dd672a7f9b8c169daef90fd63e4bb42b9ddc423'
PREVIOUS = 'c0a2da58c71162f8110c78443b4fea91faf7aaf0'
ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'packages/particle-sliders-core/src/'


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
    paths = git('ls-tree', '-r', '--name-only', CORE, '--',
                PREFIX + 'particle_sliders', PREFIX + 'concept_slider_core').decode().splitlines()
    expected = {path.removeprefix(PREFIX): digest(git('show', CORE + ':' + path)) for path in paths}
    import particle_sliders
    dist = distribution('particle-sliders-core')
    roots = {'particle_sliders': Path(particle_sliders.__file__).parent,
             'concept_slider_core': Path(dist.locate_file('concept_slider_core'))}
    actual = {package + '/' + path: value for package, root in roots.items()
              for path, value in sources(root).items()}
    if actual != expected:
        raise SystemExit('Actually imported core source/data differs from approved Git objects')
    origin = json.loads(dist.read_text('direct_url.json') or '{}')
    if (dist.version != '0.13.0' or origin.get('vcs_info', {}).get('commit_id') != CORE
            or origin.get('url') != 'https://github.com/HyperGAN/particle-sliders.git'
            or origin.get('subdirectory') != 'packages/particle-sliders-core'):
        raise SystemExit('Require exact installed immutable Git origin')
    package = ROOT / 'src/tinyqwen_shared_preview'
    product = sources(package, exclude=('sources.lock.json',))
    archived = json.loads((ROOT / 'compatibility/preview-v2-source.lock.json').read_text())
    lock = dict(schema='tinyqwen-shared-preview-lock-v7', core_commit=CORE, core_version='0.13.0',
        core_repository='https://github.com/HyperGAN/particle-sliders.git',
        core_subdirectory='packages/particle-sliders-core', core_sources=expected,
        core_sources_index_sha256=index_digest(expected), product_sources=product,
        product_sources_index_sha256=index_digest(product),
        inventory_exclusions=['generated __pycache__ directories', 'generated .pyc files',
                              'product sources.lock.json self-reference only'],
        pg='0.9.5', hndl='0.10.0', hypergan='5f368a3770cf5bdae0448995c9f76e29af8049f7',
        host_source=archived['host_source'], native_hidden_width=1024, native_qualified=False, native_candidate_profile='release-0.9.5',
        native_candidate_pg_commit='1b8355b184b21bb7d81104ee590813c262f6df0a')
    (package / 'sources.lock.json').write_text(json.dumps(lock, indent=2, sort_keys=True) + '\n')
    # Preserve the original extraction receipt; index only changes/new files since it.
    def product_git(*args):
        return subprocess.check_output(['git', '-C', str(ROOT), *args])
    names = set(product_git('ls-files', '--cached', '--others', '--exclude-standard').decode().splitlines())
    updates = []
    for name in sorted(names - {'CORE-MIGRATION.json', 'LR-MIGRATION.json', 'NATIVE-MIGRATION.json', 'PG095-MIGRATION.json'}):
        path = ROOT / name
        if not path.is_file():
            raise SystemExit('No deletion is allowed in this final migration: ' + name)
        old = subprocess.run(['git', '-C', str(ROOT), 'show', PREVIOUS + ':' + name], capture_output=True)
        current = path.read_bytes()
        if old.returncode or current != old.stdout:
            updates.append(dict(path=name, before_sha256=None if old.returncode else digest(old.stdout),
                                after_sha256=digest(current)))
    migration = dict(schema='tinyqwen-pg095-migration-v1', predecessor_commit=PREVIOUS,
        core_commit=CORE, product_version='0.7.0', cohort='tinyqwen-pg095-hypergan-hndl-v7-cpu-fixture',
        artifact_policy='v2/v3/v4/v5/v6 packets require their original source/environment; no relabel/conversion',
        previous_native_migration_sha256=digest((ROOT / 'NATIVE-MIGRATION.json').read_bytes()),
        predecessor_post_native_source_deltas_sha256=digest((ROOT / 'compatibility/preview-v6/post-native-source-deltas.json').read_bytes()),
        new_training_cohort_required=True, native_pg095_calibration=False, files=updates)
    (ROOT / 'PG095-MIGRATION.json').write_text(json.dumps(migration, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(core_files=len(expected), product_files=len(product),
                         core_sources_index_sha256=lock['core_sources_index_sha256'], updates=len(updates)), indent=2))


if __name__ == '__main__':
    main()
