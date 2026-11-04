# Explicit native TinyQwen candidate

The default dependency and CPU fixture keep official ParticleGAN0.9.4 with its
release/auto guard. Native width1024 requires the separately selected exact
PG801ae1e continuous source profile, core5d68473, Torch2.9.1+cu128,
Transformers5.3.0, BF16 Qwen3-0.6B-Base at da87bfb, and eager attention.
This creates new v6 fixture/native cohorts. Old v2/v3/v4/v5 packets retain their
original immutable source/environment; none is converted or relabelled.

Install `requirements-native-candidate.txt` into a separate CUDA environment,
then install this product artifact without replacing its pinned engine.
The eight exact local model assets are fully hashed before loading, including
the1,192,135,096-byte weights. No Hub download or remote model code is allowed.
`model_dir`, explicit `device='cuda:0'`, paired-text `data_file`,
`base_precision='bfloat16'`,
`pg_source_profile='source-801ae1e-continuous-v1'`, and
`penalty_input_domain='continuous'` are required for `config(fixture=False,...)`.
Training and heldout rows are distinct paired text, tokenized by the exact
native tokenizer, with no projection/truncation of the1024-wide response.

`docs/native-qualification-pairs.json` is a small fixed warmth/style diagnostic
bank. It provides eight training and eight unused evaluation pairs. It is not a
semantic benchmark or proof of generated-token quality. LR defaults remain
G0.012/D0.018/P0.03 until an actual native rate comparison qualifies new values.
The existing three optional LR keys keep all core optimizer/update logic.

Portable raw/EMA inference artifacts contain the construction/model/source
identity and adapter tensors, without training data. Open using the matching
native runtime and `open_inference(..., options=dict(model_dir=...,device='cuda:0'))`;
response token IDs must belong to the exact tokenizer vocabulary. The model
assets are rehashed and construction identity checked before hooks attach.
CPU fixture inference continues to require no external runtime inputs.

Native numerical/update/resume evidence is recorded separately from source
admission. This candidate does not claim semantic-quality qualification.
