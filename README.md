# TinyQwen particle sliders

The current `tinyqwen-shared-preview==0.6.0` package pins shared core
`5d68473a098801ee1ab3ebbb12463daef51c6346` and verifies its complete recursive
source/data closure and immutable Git origin. Shared core and ParticleGAN own
all game, optimizer and lifecycle mathematics.

Two v6 profiles are deliberately separate:

- The default official ParticleGAN 0.9.4 release/auto profile supports random
  CPU fixtures at widths 16 and 32 and still refuses native width 1024.
- The explicit [native BF16 candidate](NATIVE-CANDIDATE.md) selects exact PG
  `801ae1ead8f88b88eca8f5398137e3e1bc01ad36` with the continuous domain API,
  exact local Qwen3-0.6B-Base assets, Torch 2.9.1+cu128 and Transformers 5.3.0.
  Actual native updates, exact resume and raw portable inference pass the
  [numerical checks](docs/native-numerical-validation.json). This establishes
  no semantic quality, generally tuned learning rate or published weights.

The namespace remains `tinyqwen_shared_preview`. New identities are
`tinyqwen-pg094-hypergan-hndl-v6-cpu-fixture` and
`tinyqwen-pg094-hypergan-hndl-v6-native-bf16`. Both retain attention q/k/v/o
branches, rank 8/alpha 8 and one 128 x 4 routed bank. Old v2-v5 packets require
their original source/environment; no packet is converted or relabelled.

The installed `tinyqwen-cpu-fixture` profile supports the shared
`particle-slider plan` and `particle-slider train` dispatcher, periodic full
checkpoints, exact continuation and raw/EMA export. It requires `dummy: true`;
token rows can be carried in the session JSON. The native candidate uses the
explicit response-session API and its separate installer, not this fixture profile.

[Installation and contracts](docs/INTEGRATION.md) cover the current CPU package.
[Learning-rate controls](LEARNING-RATES.md) preserve inherited defaults and bind
resolved optimizer groups to full-state resume. [NATIVE-MIGRATION.json](NATIVE-MIGRATION.json)
records the current source migration. The original extraction and historical
core/LR migration receipts remain unchanged, with recovery instructions in
[compatibility](compatibility/README.md). No umbrella checkout is required.
