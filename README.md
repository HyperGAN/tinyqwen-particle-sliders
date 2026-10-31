# TinyQwen particle sliders — phase1 review

This repository separates the modern TinyQwen model-specific product from the
shared `HyperGAN/particle-sliders` library. Source is exported from public commit
`6ce328561dbcba1bb981217487ce594a01bd13d2`; no history was mirrored. The runtime
Python files and source lock are byte-identical to that source cohort.

**Review only.** Native Qwen3-0.6B hidden width1024 remains blocked by the exact
reviewed core's continuous-vector admission. Only random CPU fixture16/32 is
qualified as software plumbing. No pretrained/GPU, quality or convergence claim.

The distribution is still `tinyqwen-shared-preview==0.2.0`, import namespace
`tinyqwen_shared_preview`, cohort `tinyqwen-pg094-hypergan-hndl-v2-cpu-fixture`.
The dependency stays `particle-sliders-core[hypergan-hndl]==0.12.0`, with the exact
core4abc0eb source/wheel closure, official PG0.9.4, HyperGAN5f368a3770cf5bdae0448995c9f76e29af8049f7
and HNDL0.10.0 gates preserved. No game mathematics or core API is implemented here.

Read [the integration guide](docs/INTEGRATION.md), [migration scope](MIGRATION.md)
and [source/blob provenance](EXTRACTION-PROVENANCE.json) before use. Build a wheel
from this repository root in the exact isolated environment described in the guide:

```bash
python -m pip wheel --no-deps . -w /tmp/tinyqwen-wheels
python -m pip install /tmp/tinyqwen-wheels/tinyqwen_shared_preview-0.2.0-py3-none-any.whl
```

No umbrella checkout is needed for installation, entrypoints or tests. Architecture
parity fixtures contain only exact selected reference definitions, not historical
GAN losses, penalties, optimizers or trainers. The complete historical paths remain
intact in the umbrella until a separately reviewed migration is verified.

No workflow, model weights, recordings, run outputs, deployment, package-index
release or access/CI permission change is included. Root coordinates tests, Claude
actual-diff and RETURN review, final core review, Ada routing and merges. The main
branch stays a minimal scaffold until that review completes.
