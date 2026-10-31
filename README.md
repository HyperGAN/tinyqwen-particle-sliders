# TinyQwen particle sliders — modern core candidate

This separate model-specific repository uses shared `HyperGAN/particle-sliders`.
The active **0.3.0/v3 CPU preview** pins exact core
`a794e3b4a8813b012f2c4faa3da82b78d4a90214` through a Git dependency and checks its
complete recursive installed source/data closure and immutable Git origin.

Native Qwen3-0.6B hidden width 1024 remains **blocked**. Only random CPU fixtures 16 and 32
is product software-qualified; there is no pretrained/GPU, quality or convergence
claim. The model, target layout, objective, rank 8/alpha 8 and one 128 x 4 bank have not
changed. Shared core owns all game/optimizer/lifecycle mathematics.

The import namespace remains `tinyqwen_shared_preview`; new artifacts use
`tinyqwen-pg094-hypergan-hndl-v3-cpu-fixture`. Old v2 packets require their original
product/core environment and are intentionally refused here. Their exact lock is
preserved in [compatibility](compatibility/README.md); no metadata is relabeled.

[Installation and contracts](docs/INTEGRATION.md) include exact Git install and
wheel/sdist commands. [CORE-MIGRATION.json](CORE-MIGRATION.json) indexes the final
pin migration. The original [extraction receipt](EXTRACTION-PROVENANCE.json) is
preserved as historical evidence, with [later historical migration](MIGRATION.md)
still tracked. No umbrella checkout is required for this product.

This remains a DRAFT candidate. Root coordinates tests, Claude actual-diff and
RETURN review, final core review, Ada routing and merges. Main is still the
minimal scaffold; no workflow, deployment, package-index release, model weights,
GPU job or access/CI permission change is included.
