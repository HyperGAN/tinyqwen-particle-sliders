"""Exact local native Qwen3 assets and text data; no model imports or downloads."""
import hashlib
import json
from pathlib import Path

MODEL_ID = 'Qwen/Qwen3-0.6B-Base'
REVISION = 'da87bfb608c14b7cf20ba1ce41287e8de496c0cd'
EXPECTED_FILES = {'config.json': {'bytes': 727, 'sha256': '504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59'}, 'generation_config.json': {'bytes': 138, 'sha256': '8c970692323e3ea0e9b8b0a4dca79388d31226e41f83c9fd6014804280ebf6e8'}, 'tokenizer.json': {'bytes': 7031645, 'sha256': 'c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539'}, 'tokenizer_config.json': {'bytes': 9678, 'sha256': '3c04ed3ca964ea2f6b2b5faf0dc4d31aec1cb1e8b4bcf63f402d295046b422b5'}, 'merges.txt': {'bytes': 1671853, 'sha256': '8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5'}, 'vocab.json': {'bytes': 2776833, 'sha256': 'ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910'}, 'LICENSE': {'bytes': 11343, 'sha256': '832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e'}, 'model.safetensors': {'bytes': 1192135096, 'sha256': 'cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba'}}


def file_sha(path):
    result=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):
            result.update(block)
    return result.hexdigest()


def verify_model(model_dir):
    """Hash all eight approved assets, including the complete weight file."""
    root=Path(model_dir)
    if not root.is_dir():
        raise ValueError('native Qwen requires an existing exact local model directory')
    unexpected={p.name for p in root.iterdir() if p.is_file()} - set(EXPECTED_FILES) - {'qualification-manifest.json','download-plan.json'}
    if unexpected:
        raise ValueError('unadmitted native loader files: '+str(sorted(unexpected)))
    actual={}
    for name, expected in EXPECTED_FILES.items():
        path=root/name
        if not path.is_file() or path.stat().st_size != expected['bytes']:
            raise ValueError('native Qwen asset size/path differs: '+name)
        value=dict(bytes=path.stat().st_size,sha256=file_sha(path))
        if value != expected:
            raise ValueError('native Qwen asset SHA differs: '+name)
        actual[name]=value
    config=json.loads((root/'config.json').read_text())
    contract={'model_type':'qwen3','hidden_size':1024,'num_hidden_layers':28,
              'num_attention_heads':16,'num_key_value_heads':8,'vocab_size':151936,
              'head_dim':128,'intermediate_size':3072,'tie_word_embeddings':True}
    if any(config.get(key)!=value for key,value in contract.items()):
        raise ValueError('native Qwen architecture differs from exact pinned model')
    return dict(schema='tinyqwen-native-model-v1',model_id=MODEL_ID,revision=REVISION,
                files=actual,architecture=contract,local_files_only=True)


def read_text_rows(path):
    if not isinstance(path,(str,Path)):
        raise ValueError('bounded local native paired-text data file required')
    path=Path(path)
    if not path.is_file() or path.stat().st_size>65536:
        raise ValueError('bounded local native paired-text data file required')
    data=json.loads(path.read_text())
    if not isinstance(data,dict) or set(data)!={'train','evaluation'}:
        raise ValueError('native data requires distinct train and evaluation row lists')
    for split,rows in data.items():
        if not isinstance(rows,list) or not 2<=len(rows)<=32:
            raise ValueError('native splits require 2..32 text pairs')
        for row in rows:
            if (not isinstance(row,dict) or set(row)-{'neutral','positive','history'}
                    or any(not isinstance(row.get(key),str) or not row[key].strip()
                           for key in ('neutral','positive'))
                    or not isinstance(row.get('history',''),str)):
                raise ValueError('native row requires paired text and optional shared history')
    train={(r['neutral'],r['positive'],r.get('history','')) for r in data['train']}
    if any((r['neutral'],r['positive'],r.get('history','')) in train for r in data['evaluation']):
        raise ValueError('native evaluation rows overlap training data')
    return data,file_sha(path)
