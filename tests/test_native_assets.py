"""Native refusal/data admission checks never allocate or open actual model weights."""
import json
from pathlib import Path

import pytest
from tinyqwen_shared_preview import native_assets as assets


def pair(a,b):
    return dict(neutral=a,positive=b)


def test_native_assets_match_complete_pinned_weight_contract():
    assert assets.REVISION=='da87bfb608c14b7cf20ba1ce41287e8de496c0cd'
    assert len(assets.EXPECTED_FILES)==8
    weight=assets.EXPECTED_FILES['model.safetensors']
    assert weight['bytes']==1192135096
    assert weight['sha256']=='cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba'


def test_asset_path_size_and_unknown_loader_files_fail_before_hash(tmp_path,monkeypatch):
    monkeypatch.setattr(assets,'file_sha',lambda p:pytest.fail('read before cheap admission'))
    with pytest.raises(ValueError,match='existing'):
        assets.verify_model(tmp_path/'absent')
    with pytest.raises(ValueError,match='size/path'):
        assets.verify_model(tmp_path)
    (tmp_path/'pytorch_model.bin').write_bytes(b'other')
    with pytest.raises(ValueError,match='unadmitted'):
        assets.verify_model(tmp_path)


def test_asset_same_size_modified_bytes_fail_closed(tmp_path,monkeypatch):
    (tmp_path/'model.safetensors').write_bytes(b'changed')
    monkeypatch.setattr(assets,'EXPECTED_FILES',{'model.safetensors':dict(bytes=7,sha256='0'*64)})
    with pytest.raises(ValueError,match='SHA'):
        assets.verify_model(tmp_path)


def test_text_splits_content_hash_and_overlap_refusal(tmp_path):
    file=tmp_path/'pairs.json'
    data=dict(train=[pair('plain one','warm one'),pair('plain two','warm two')],
              evaluation=[pair('plain three','warm three'),pair('plain four','warm four')])
    file.write_text(json.dumps(data))
    actual,sha=assets.read_text_rows(file)
    assert actual==data and sha==assets.file_sha(file)
    data['evaluation'][0]=data['train'][0]
    file.write_text(json.dumps(data))
    with pytest.raises(ValueError,match='overlap'):
        assets.read_text_rows(file)


@pytest.mark.parametrize('value',[None,{},[],dict(train=[],evaluation=[]),
    dict(train=[pair('x','y')]*2,evaluation=[dict(neutral='a',positive='b',tokens=[1])]*2)])
def test_malformed_text_data_is_rejected(tmp_path,value):
    file=tmp_path/'rows.json';file.write_text(json.dumps(value))
    with pytest.raises(ValueError):
        assets.read_text_rows(file)


def test_native_profile_required_before_loader(monkeypatch):
    from tinyqwen_shared_preview import binding
    monkeypatch.setattr(binding,'TinyLLMBackend',lambda **kw:pytest.fail('native loader reached'))
    with pytest.raises(ValueError,match='continuous'):
        binding._native_runtime_options({})
    with pytest.raises(ValueError,match='bfloat16'):
        binding._native_runtime_options(dict(pg_source_profile=binding.NATIVE_PROFILE,penalty_input_domain='continuous'))
