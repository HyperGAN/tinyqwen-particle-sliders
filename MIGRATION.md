# Phase1 extraction scope and later migration

Source: public `HyperGAN/particle-sliders` commit
`6ce328561dbcba1bb981217487ce594a01bd13d2`.

Phase1 exports the modern product, its directly required model host, tests,
minimal test-only architecture excerpts, guide and inherited MIT license. The
shared `particle_sliders` implementation is an exact external dependency, not
copied into this repository. The runtime import namespace and source lock stay
unchanged; local build paths are the only packaging relocation.

The original embedded paths are preserved. Later migration tracks:

| Original path | Phase1 / later status |
|---|---|
| `packages/tinyqwen-shared-preview/` | Modern source exported here; original intact pending replacement verification/review. |
| `conceptmod/textsliders/tiny_llm_backend.py` | Required installed host exported byte-for-byte to `src/tinyqwen_shared_preview/backend.py`; original intact. |
| `conceptmod/textsliders/tiny_llm_particle.py` | Full historical slider/export loader remains in umbrella. Only its exact projection class is a non-runtime parity fixture here. |
| `conceptmod/textsliders/train_lora_tiny_llm.py` | Historical Rp/VIC trainer remains in umbrella; later migration must preserve checkpoint/runtime semantics. |
| `conceptmod/textsliders/particle_bridge_gan.py`, `lm_adv.py`, `analysis/slider2d/adv.py` | Legacy game dependencies remain in their original environment. They are not copied as live implementations into this repository; central shared-library ownership must be respected. Only the two exact network reference definitions used by parity tests are excerpted. |
| `conceptmod/textsliders/data/prompts-tiny-llm.yaml` | Historical prompt configuration remains in umbrella; modern API accepts explicit token rows. |
| `docs/tiny-llm-slider.md`, `tests/test_tiny_llm_slider.py` | Historical guide and17-case regressions remain in umbrella; not required for installed modern behavior. |

No old checkpoint conversion or relabeling is performed. Modern source-profile,
wide-vector, original-model and native inference identity gates remain intact.
The new repository's extraction PR must pass tests, Claude actual-diff review,
fixes and RETURN review before landing. No merge or automatic release is implied.
