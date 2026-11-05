# Learning rates

The best tested, independently confirmed recipe for the native Qwen3 BF16
128-update response cohort is **G 0.001 / D 0.054 / particle bank 0.03**:

```json
{"lr": 0.001, "d_lr_mult": 54.0, "prior_lr_mult": 30.0}
```

At 128 completed updates with a declared horizon of 128, held-out development
relative SSE was **0.5614657431858548** across four examples. The original four
sealed confirmation examples, opened after freezing that endpoint, scored
**0.40601743965471515**. Lower is better; OFF is 1. These measurements qualify
this source/model/data/numerical recipe, rather than a universal optimum or a
new package default. Exact identities, numerical policy and artifact hashes are
in the [confirmation receipt](docs/native-lr-confirmation-20261105.json).

## Native recipe and API

Use the separate [native candidate environment](NATIVE-CANDIDATE.md): exact core
`5d68473a098801ee1ab3ebbb12463daef51c6346`, PG source
`801ae1ead8f88b88eca8f5398137e3e1bc01ad36`, the explicit
`source-801ae1e-continuous-v1` / `continuous` pair, Torch **2.9.1+cu128** and
Transformers **5.3.0**. PG801 reports version 0.9.4 but has distinct source bytes;
the default official 0.9.4 release/auto profile still refuses native width 1024.

The measurement used local `Qwen/Qwen3-0.6B-Base` assets at revision
`da87bfb608c14b7cf20ba1ce41287e8de496c0cd`, BF16 base weights with eager
attention, FP32 HNDL attention q/k/v/o branches at rank 8/alpha 8, and one real
128 × 4 routed bank. The response is the full 1024-wide last hidden vector with at most 128 input
tokens; training and RAW evaluation use strength +1. Batch size was 2, seed 7, EMA was
disabled, and the preset was `bispf_optimized` throughout.

The measured runtime package tree at product commit
`5d91b962b2494e5d897d71d73e6bc3339756e5bf` is identical to the public runtime at
`fa19c943da52a009fe03d380cbf5871ec4971a7b`, including its source lock, package
configuration and native requirements. No runtime implementation changes are
needed to use these options.

Native training uses the public response-session API. The registered
`tinyqwen-cpu-fixture` common CLI profile requires `dummy: true` and only admits
CPU fixtures; it is not a native training command.

Before importing Torch, expose only the admitted device with
`CUDA_VISIBLE_DEVICES`; `cuda:0` is its process-local index. Set
`CUBLAS_WORKSPACE_CONFIG=:4096:8` and leave
`NVIDIA_TF32_OVERRIDE` and `TORCH_ALLOW_TF32_CUBLAS_OVERRIDE` unset. Apply the
measured caller policy before native construction:

```python
import torch

torch.set_num_threads(4)
torch.use_deterministic_algorithms(True, warn_only=False)
torch.set_float32_matmul_precision("highest")
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction = False
torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = False
torch.backends.cuda.enable_flash_sdp(False)
torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_cudnn_sdp(False)
torch.backends.cuda.enable_math_sdp(True)
torch.backends.cuda.allow_fp16_bf16_reduction_math_sdp(False)

from particle_sliders.lifecycle import SessionConfig
from particle_sliders.response import open_response
from tinyqwen_shared_preview import binding as product

config = SessionConfig(
    product.NAME, "tinyqwen-fresh128-primary-v1-nativeBF16",
    fixture=False, steps=128, batch=2, seed=7, ema_decay=None,
    lr=0.001, d_lr_mult=54.0, prior_lr_mult=30.0,
    pg_source_profile="source-801ae1e-continuous-v1",
    penalty_input_domain="continuous", base_precision="bfloat16",
    device="cuda:0", model_dir=EXACT_LOCAL_MODEL_DIR,
    data_file=EXACT_PAIRED_TEXT_FILE,
)
# After caller-owned device/resource admission:
# with open_response(config, resume=UNCHANGED_MATCHING_PACKET_OR_NONE) as session:
#     ...
```

The path variables stand for the exact local model and paired corpus; this
documentation does not distribute them. The corpus was eight training pairs,
four development pairs and four separate confirmation pairs. The data file
accepts distinct `train` and `evaluation` lists of neutral/positive text pairs
with optional shared history. The earlier diagnostic
`docs/native-qualification-pairs.json` is a different corpus.

Keep the original complete `SessionConfig` to resume a measured packet,
including this custom cohort, data identities, rates and 128-step horizon.
`product.config(fixture=False, ...)` uses the generic v6 native cohort instead;
it must not relabel measured packets. A changed rate/configuration starts a new
experiment. Old v2–v5 packets still require their original source/environment.

## Selection and confirmation

All recipes began with matched actual initialization and source-bound teachers
under the same 128-step schedule. This was a named/coupled recipe comparison,
not a generator-only sweep. All four finite recipes completed their declared
32-update screen, including the result above OFF:

| Actual G / D / bank | RAW development SSE at 32 | RAW development SSE at 64 |
| --- | ---: | ---: |
| 0.001 / 0.054 / 0.09 | 0.3147800560543701 | 0.931899634380866 |
| **0.001 / 0.054 / 0.03** | **0.34630424391493014** | **0.6781853306671439** |
| 0.012 / 0.018000000000000002 / 0.03 | 0.6666896911448938 | Not selected |
| 0.003 / 0.054 / 0.03 | 1.1625149932175598 | Not selected |

The best two at 32 continued from their exact full-state checkpoints to 64.
The better 64-update recipe continued to 128, then received independent held-out
confirmation without further tuning. There were 256 logical candidate updates
and 262 known completed physical update calls, including six historical
duplicates. Host-preempted and resource-failed execution history remains
archived with its real exits; possible uncommitted calls are not counted as
known completed work. Atomic journals preserved completed prefixes for exact
continuation. The separate native fresh-two versus one-plus-one and public RAW
inference correctness proofs remain intact.

The sole ranking and confirmation metric follows the
[common evaluation protocol](https://github.com/HyperGAN/particle-sliders/blob/main/packages/particle-sliders-core/EVALUATION-PROTOCOL.md):
cast student, teacher and neutral operands to FP64 **before subtraction**;
pool declared positions and coordinates within each example; divide by that
example's teacher-edit energy; then average examples equally. Freeze the
teacher-only valid/excluded set across candidates. Zero energy is undefined,
never epsilon-ranked, and a student failure never removes an example. Every
finite candidate finishes its declared stage budget with the common schedule
horizon held fixed.

Preservation/no-edit, late/weak, generated-language and media observations are
optional diagnostics and cannot veto this recommendation. Endpoint net
G/D/bank displacement is diagnostic after native mechanical qualification;
source, actual rates, finite updates, native responses and exact replay remain
correctness checks. The earlier
[64-horizon development report](docs/NATIVE-LR-DEVELOPMENT-20261104.md) remains
historical. Its preservation/semantic-based “no nominee” conclusion is
superseded for this sole RAW-response goal by the new 128-horizon confirmation;
its old packets and evidence are unchanged. No semantic-quality claim follows.

## Controls, defaults and historical packages

The optional `lr`, `d_lr_mult` and `prior_lr_mult` keys accept only finite
positive numbers, rejecting booleans before allocation. Shared ParticleGAN
creates the optimizers: D = `lr * d_lr_mult`, bank = `lr * prior_lr_mult`.
No product GAN or optimizer mathematics is duplicated.

Omitting the keys retains the inherited `bispf_optimized` defaults: G **0.012**,
D multiplier **1.5**, bank multiplier **2.5**. These defaults are unchanged.
The current package is 0.6.0 with separate v6 fixture/native identities, recorded
in `sources.lock.json` and `NATIVE-MIGRATION.json`. Historical
`CORE-MIGRATION.json`, `LR-MIGRATION.json` and the v4/v5 compatibility receipts
remain intact; use their original product/core environment for their packets.
