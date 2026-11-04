# Explicit native TinyQwen candidate

The default dependency and CPU fixture keep official ParticleGAN 0.9.4 with its
release/auto guard. Native width 1024 requires the separately selected exact
PG 801ae1e continuous source profile, core 5d68473, Torch 2.9.1+cu128,
Transformers 5.3.0, BF16 Qwen3-0.6B-Base at da87bfb, and eager attention.
This creates new v6 fixture/native cohorts. Old v2/v3/v4/v5 packets retain their
original immutable source/environment; none is converted or relabelled.

Use a separate CUDA environment. Install a CUDA 12.8 Torch build whose runtime
reports exactly `2.9.1+cu128`, then select the explicit source pair:

```bash
python -m pip install -r requirements-native-candidate.txt
python -m pip install --no-deps dist/tinyqwen_shared_preview-0.6.0-py3-none-any.whl
```

The requirements file pins core `5d68473a098801ee1ab3ebbb12463daef51c6346`, exact
PG `801ae1ead8f88b88eca8f5398137e3e1bc01ad36` and Transformers 5.3.0. This
installer differs from the official-release CPU environment. Runtime versions,
source closures and exact local assets are checked again before construction.
The eight exact local model assets are fully hashed before loading, including
the 1,192,135,096-byte weights. No Hub download or remote model code is allowed.
`model_dir`, explicit `device='cuda:0'`, paired-text `data_file`,
`base_precision='bfloat16'`,
`pg_source_profile='source-801ae1e-continuous-v1'`, and
`penalty_input_domain='continuous'` are required for `config(fixture=False,...)`.
Training and heldout rows are distinct paired text, tokenized by the exact
native tokenizer, with no projection/truncation of the 1024-wide response.

`docs/native-qualification-pairs.json` is a small fixed warmth/style diagnostic
bank. It provides eight training and eight evaluation pairs separate from training. These examples
were used for the numerical checks and are not a sealed confirmation bank. It is not a
semantic benchmark or proof of generated-token quality. LR defaults remain
G 0.012 / D 0.018 / P 0.03 until an actual native rate comparison qualifies new values.
The existing three optional LR keys keep all core optimizer/update logic.

Portable raw/EMA inference artifacts contain the construction/model/source
identity and adapter tensors, without training data. Open using the matching
native runtime and `open_inference(..., options=dict(model_dir=...,device='cuda:0'))`;
response token IDs must belong to the exact tokenizer vocabulary. The model
assets are rehashed and construction identity checked before hooks attach.
CPU fixture inference continues to require no external runtime inputs.

Native numerical/update/resume evidence is recorded separately from source
admission. This candidate does not claim semantic-quality qualification.

The [native LR development comparison](docs/NATIVE-LR-DEVELOPMENT-20261104.md)
completed a bounded coordinate bracket and one default-rate control at a common
64-step budget. It found no rate nominee or consistent intended native language
edit. Defaults remain unchanged and the final evaluation set remains sealed.

The exact native numerical check is recorded in [the validation receipt](docs/native-numerical-validation.json): two real updates, frozen/OFF identity, exact full-state fresh-process resume, and raw portable inference. It establishes no tuned rate or semantic quality.
