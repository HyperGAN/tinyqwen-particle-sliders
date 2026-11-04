# TinyQwen particle sliders — modern core candidate

This separate model-specific repository uses shared `HyperGAN/particle-sliders`.
The active **0.4.0/v4 CPU preview** pins exact core
`ddb41423bcefc1fe76cd94d0f9b367353b3ea137` through a Git dependency and checks its
complete recursive installed source/data closure and immutable Git origin.

Native Qwen3-0.6B hidden width 1024 remains **blocked**. Only random CPU fixtures 16 and 32
are product software-qualified; there is no pretrained/GPU, quality or convergence
claim. The model, target layout, objective, rank 8/alpha 8 and one 128 x 4 bank have not
changed. Shared core owns all game/optimizer/lifecycle mathematics.

The import namespace remains `tinyqwen_shared_preview`; new artifacts use
`tinyqwen-pg094-hypergan-hndl-v4-cpu-fixture`. Old v2/v3 packets require their original
product/core environment and are intentionally refused here. Their exact lock is
preserved in [compatibility](compatibility/README.md); no metadata is relabeled.

The installed `tinyqwen-cpu-fixture` training profile supports the shared
`particle-slider plan` and `particle-slider train` dispatcher, periodic checkpoints,
exact continuation, and raw/EMA v1/v2 export. The profile requires `dummy: true`;
token rows can be carried by the JSON session configuration. See the
[bounded CPU example](docs/INTEGRATION.md#shared-training-command).

[Installation and contracts](docs/INTEGRATION.md) include exact Git install and
wheel/sdist commands. [CORE-MIGRATION.json](CORE-MIGRATION.json) indexes the final
pin migration. The original [extraction receipt](EXTRACTION-PROVENANCE.json) is
preserved as historical evidence, with [later historical migration](MIGRATION.md)
still tracked. No umbrella checkout is required for this product.

This remains a DRAFT candidate. Root coordinates tests, Claude actual-diff and
RETURN review, final core review, Ada routing and merges. Main is still the
minimal scaffold; no workflow, deployment, package-index release, model weights,
GPU job or access/CI permission change is included.
