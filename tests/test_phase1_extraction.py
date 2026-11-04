"""Source-only extraction checks; no umbrella checkout or native weights required."""
import ast
from hashlib import sha256
from importlib.metadata import distribution
import json
import os
from pathlib import Path
import tomllib
import zipfile

from tinyqwen_shared_preview import binding

ROOT = Path(os.environ.get('TINYQWEN_EXTRACTED_ROOT', Path(__file__).resolve().parents[1]))
SOURCE = '6ce328561dbcba1bb981217487ce594a01bd13d2'


def test_original_extraction_receipt_and_explicit_current_migration_are_complete():
    record = json.loads((ROOT / 'EXTRACTION-PROVENANCE.json').read_text())
    assert record['source_commit'] == SOURCE
    assert record['destination_repository'] == 'https://github.com/HyperGAN/tinyqwen-particle-sliders'
    migration = json.loads((ROOT / 'CORE-MIGRATION.json').read_text())
    assert migration['predecessor_commit'] == 'a2798264059c2b7c260ec98f3db8a21e41c8819c'
    assert migration['core_commit'] == binding.CORE_COMMIT
    updates = {item['path']: item for item in migration['files']}
    indexed = set()
    for item in record['files']:
        rel = item['destination_path']
        assert rel not in indexed
        indexed.add(rel)
        assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
        data = (ROOT / rel).read_bytes()
        if rel in updates:
            assert updates[rel]['before_sha256'] == item['destination_sha256']
            assert sha256(data).hexdigest() == updates[rel]['after_sha256']
        else:
            assert sha256(data).hexdigest() == item['destination_sha256']
        if item.get('source_commit'):
            assert item['source_commit'] == SOURCE
            assert item['source_repository'] == 'https://github.com/HyperGAN/particle-sliders'
            assert len(item['source_blob']) == 40
            if item['transformation'] == 'byte-identical export':
                assert item['destination_sha256'] == item['source_sha256']
                assert item['destination_blob'] == item['source_blob']
    expected = {
        '.gitignore', 'README.md', 'LICENSE', 'MIGRATION.md', 'pyproject.toml',
        'docs/INTEGRATION.md', 'src/tinyqwen_shared_preview/__init__.py',
        'src/tinyqwen_shared_preview/backend.py', 'src/tinyqwen_shared_preview/binding.py',
        'src/tinyqwen_shared_preview/sources.lock.json', 'tests/test_tiny_llm_shared.py',
        'tests/test_phase1_extraction.py', 'tests/fixtures/particle_bridge_network.py',
        'tests/fixtures/tiny_llm_projection.py',
    }
    assert indexed == expected
    for rel, item in updates.items():
        assert sha256((ROOT / rel).read_bytes()).hexdigest() == item['after_sha256']
        if rel not in indexed:
            assert item['before_sha256'] is None
    assert set(updates) - indexed == {'compatibility/README.md', 'compatibility/preview-v2-source.lock.json',
        'compatibility/preview-v3-source.lock.json', 'compatibility/preview-v3-core-migration.json',
        'src/tinyqwen_shared_preview/training_profile.py', 'tools/refresh_source_lock.py'}
    archived = (ROOT / 'compatibility/preview-v2-source.lock.json').read_bytes()
    original_lock = next(i for i in record['files'] if i['destination_path'].endswith('/sources.lock.json'))
    assert sha256(archived).hexdigest() == original_lock['destination_sha256']
    assert sha256((ROOT / 'compatibility/preview-v3-source.lock.json').read_bytes()).hexdigest() == '30be37fb2aed143e418de6cfbeecab95061100bd1dab9c8c40715edd1e309afc'
    assert sha256((ROOT / 'compatibility/preview-v3-core-migration.json').read_bytes()).hexdigest() == '2b4b22bbe748ff6a84217fe135594c7913b38686a913d9b841fb2a9e2a4cf346'
    assert not (ROOT / 'conceptmod').exists()
    assert not (ROOT / '.github').exists()


def test_packaging_is_self_contained_and_preserves_dependency_and_entrypoints():
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    assert project['project']['name'] == 'tinyqwen-shared-preview'
    assert project['project']['version'] == '0.4.0'
    assert project['project']['dependencies'] == ['particle-sliders-core[hypergan-hndl] @ git+https://github.com/HyperGAN/particle-sliders.git@ddb41423bcefc1fe76cd94d0f9b367353b3ea137#subdirectory=packages/particle-sliders-core']
    assert project['project']['license'] == {'file': 'LICENSE'}
    assert project['tool']['hatch']['metadata']['allow-direct-references'] is True
    assert project['tool']['hatch']['build']['targets']['wheel'] == {'packages': ['src/tinyqwen_shared_preview']}
    actual = {(ep.group, ep.name): ep.value for ep in distribution('tinyqwen-shared-preview').entry_points}
    assert actual[('particle_sliders.response_backends', 'tinyqwen-shared-preview')] == 'tinyqwen_shared_preview.binding:BACKEND'
    assert actual[('particle_sliders.inference_backends', 'tinyqwen-shared-preview')] == 'tinyqwen_shared_preview.binding:INFERENCE'
    assert actual[('particle_sliders.training_profiles', 'tinyqwen-cpu-fixture')] == 'tinyqwen_shared_preview.training_profile:TRAINING_PROFILE'


def test_installed_runtime_payload_and_relocated_source_lock_match_export():
    lock = json.loads((ROOT / 'src/tinyqwen_shared_preview/sources.lock.json').read_text())
    assert json.loads((binding.ROOT / 'sources.lock.json').read_text()) == lock
    for name, digest in lock['product_sources'].items():
        assert sha256((binding.ROOT / name).read_bytes()).hexdigest() == digest
        assert (binding.ROOT / name).read_bytes() == (ROOT / 'src/tinyqwen_shared_preview' / name).read_bytes()
    assert lock['core_commit'] == 'ddb41423bcefc1fe76cd94d0f9b367353b3ea137'
    assert lock['native_hidden_width'] == 1024 and lock['native_qualified'] is False
    assert len(lock['core_sources']) == 574
    assert 'concept_slider_core/__init__.py' in lock['core_sources']
    assert binding.COHORT == 'tinyqwen-pg094-hypergan-hndl-v4-cpu-fixture'
    binding.verify_runtime()


def test_reference_fixtures_contain_only_exact_selected_network_definitions():
    allowed = {'particle_bridge_network.py': ['mlp', 'RoutedMLP'],
               'tiny_llm_projection.py': ['TinyParticleProjection']}
    for name, definitions in allowed.items():
        tree = ast.parse((ROOT / 'tests/fixtures' / name).read_text())
        assert [node.name for node in tree.body] == definitions
        assert all(isinstance(node, (ast.ClassDef, ast.FunctionDef)) for node in tree.body)
        assert not any('loss' in node.name.lower() or 'update' in node.name.lower() for node in tree.body)


def test_wheel_contains_no_umbrella_or_unrelated_runtime_payload():
    with zipfile.ZipFile(os.environ['TINYQWEN_WHEEL']) as archive:
        names = archive.namelist()
        expected = {'tinyqwen_shared_preview/__init__.py', 'tinyqwen_shared_preview/backend.py',
                    'tinyqwen_shared_preview/binding.py', 'tinyqwen_shared_preview/sources.lock.json',
                    'tinyqwen_shared_preview/training_profile.py'}
        assert {n for n in names if n.startswith('tinyqwen_shared_preview/')} == expected
        assert all(n.startswith(('tinyqwen_shared_preview/', 'tinyqwen_shared_preview-0.4.0.dist-info/')) for n in names)
        assert any(n.endswith('/LICENSE') for n in names)


def test_sdist_carries_all_standalone_build_and_test_inputs():
    import tarfile
    with tarfile.open(os.environ['TINYQWEN_SDIST']) as archive:
        names={str(Path(name).relative_to('tinyqwen_shared_preview-0.4.0')) for name in archive.getnames()
               if name != 'tinyqwen_shared_preview-0.4.0'}
    required={'pyproject.toml','README.md','LICENSE','EXTRACTION-PROVENANCE.json','CORE-MIGRATION.json',
        'src/tinyqwen_shared_preview/binding.py','src/tinyqwen_shared_preview/sources.lock.json',
        'src/tinyqwen_shared_preview/backend.py','tests/fixtures/particle_bridge_network.py',
        'tests/fixtures/tiny_llm_projection.py','tools/refresh_source_lock.py',
        'compatibility/preview-v2-source.lock.json','tests/test_tiny_llm_shared.py'}
    assert required <= names
    assert not any(name.startswith(('.git/','evidence/','.venv')) for name in names)
