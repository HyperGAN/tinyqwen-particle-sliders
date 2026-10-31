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


def test_allowlisted_sources_and_provenance_are_complete_and_unchanged():
    record = json.loads((ROOT / 'EXTRACTION-PROVENANCE.json').read_text())
    assert record['source_commit'] == SOURCE
    assert record['destination_repository'] == 'https://github.com/HyperGAN/tinyqwen-particle-sliders'
    indexed = set()
    for item in record['files']:
        rel = item['destination_path']
        assert rel not in indexed
        indexed.add(rel)
        assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
        data = (ROOT / rel).read_bytes()
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
    assert not (ROOT / 'conceptmod').exists()
    assert not (ROOT / '.github').exists()


def test_packaging_is_self_contained_and_preserves_dependency_and_entrypoints():
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    assert project['project']['name'] == 'tinyqwen-shared-preview'
    assert project['project']['version'] == '0.2.0'
    assert project['project']['dependencies'] == ['particle-sliders-core[hypergan-hndl]==0.12.0']
    assert project['project']['license'] == {'file': 'LICENSE'}
    assert project['tool']['hatch']['build']['targets']['wheel'] == {'packages': ['src/tinyqwen_shared_preview']}
    actual = {(ep.group, ep.name): ep.value for ep in distribution('tinyqwen-shared-preview').entry_points}
    assert actual[('particle_sliders.response_backends', 'tinyqwen-shared-preview')] == 'tinyqwen_shared_preview.binding:BACKEND'
    assert actual[('particle_sliders.inference_backends', 'tinyqwen-shared-preview')] == 'tinyqwen_shared_preview.binding:INFERENCE'


def test_installed_runtime_payload_and_relocated_source_lock_match_export():
    lock = json.loads((ROOT / 'src/tinyqwen_shared_preview/sources.lock.json').read_text())
    assert json.loads((binding.ROOT / 'sources.lock.json').read_text()) == lock
    for name, digest in lock['product_sources'].items():
        assert sha256((binding.ROOT / name).read_bytes()).hexdigest() == digest
        assert (binding.ROOT / name).read_bytes() == (ROOT / 'src/tinyqwen_shared_preview' / name).read_bytes()
    assert lock['core_commit'] == '4abc0eb03a4e3a84fc3e6d02734c13dc7e8ea231'
    assert lock['native_hidden_width'] == 1024 and lock['native_qualified'] is False
    assert binding.COHORT == 'tinyqwen-pg094-hypergan-hndl-v2-cpu-fixture'
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
                    'tinyqwen_shared_preview/binding.py', 'tinyqwen_shared_preview/sources.lock.json'}
        assert {n for n in names if n.startswith('tinyqwen_shared_preview/')} == expected
        assert all(n.startswith(('tinyqwen_shared_preview/', 'tinyqwen_shared_preview-0.2.0.dist-info/')) for n in names)
        assert any(n.endswith('/LICENSE') for n in names)
