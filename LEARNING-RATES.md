# Learning rates

The best tested, independently confirmed recipe for the native Qwen3 BF16
128-update response cohort is **G 0.002 / D 0.054 / particle bank 0.03**:

```json
{"lr": 0.002, "d_lr_mult": 27.0, "prior_lr_mult": 15.0}
```

At 128 completed updates with a declared horizon of 128, held-out development
relative SSE was **0.7003497239527556** across four examples. Four new sealed
confirmation examples, opened after freezing that endpoint, scored
**0.7981414033678553**. Lower is better; OFF is 1. These measurements qualify
this source/model/data/numerical recipe, rather than a universal optimum or a
new package default. Exact identities, numerical policy and artifact hashes are
in the [confirmation receipt](docs/native-lr-confirmation-pg095-20261105.json).

## Native recipe and API

Use the separate [native candidate environment](NATIVE-CANDIDATE.md): exact core
`3dd672a7f9b8c169daef90fd63e4bb42b9ddc423` (**0.13.0**), published ParticleGAN
**0.9.5** at `1b8355b184b21bb7d81104ee590813c262f6df0a`, the explicit
`release-0.9.5` / `continuous` pair, Torch **2.9.1+cu128** and Transformers
**5.3.0**. This was a fresh PG0.9.5 cohort, including fresh teachers and complete
initialization; no historical PG801 checkpoint was resumed.

The measurement used local `Qwen/Qwen3-0.6B-Base` assets at revision
`da87bfb608c14b7cf20ba1ce41287e8de496c0cd`, BF16 base weights with eager
attention, FP32 HNDL attention q/k/v/o branches at rank 8/alpha 8, and one real
128 × 4 routed bank. The response is the full 1024-wide last hidden vector with at most 128 input
tokens; training and RAW evaluation use strength +1. Batch size was 2, seed 7, EMA was
disabled, and the preset was `bispf_optimized` throughout.

The seven installed runtime package files, including the source lock, were
byte-identical to public product commit
`91ed7147fe17be97f129a4f695ba7ae125911e69`. No runtime implementation changes or
new defaults are part of this recommendation.

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
    product.NAME, "tinyqwen-native-pg095-fresh128-primary-v1-BF16",
    fixture=False, steps=128, batch=2, seed=7, ema_decay=None,
    lr=0.002, d_lr_mult=27.0, prior_lr_mult=15.0,
    pg_source_profile="release-0.9.5",
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
four development pairs and four new separate confirmation pairs, distinct from
the already-opened historical PG801 confirmation set. The data file
accepts distinct `train` and `evaluation` lists of neutral/positive text pairs
with optional shared history. The earlier diagnostic
`docs/native-qualification-pairs.json` is a different corpus.

Keep the original complete `SessionConfig` to resume a measured packet,
including this custom cohort, data identities, rates and 128-step horizon.
`product.config(fixture=False, ...)` uses the generic v7 native cohort instead;
it must not relabel measured packets. A changed rate/configuration starts a new
experiment. Old v2–v6 packets still require their original source/environment.

## Selection and confirmation

All four generator rates began with matched actual initialization and
source-bound teachers under the same 128-step schedule. Actual D **0.054** and
bank **0.03** were bit-identical across candidates. All four finite recipes
completed their declared 32-update screen:

| Actual G / D / bank | RAW development SSE at 32 | RAW development SSE at 64 |
| --- | ---: | ---: |
| 0.0005 / 0.054 / 0.03 | 0.3964182348877579 | Not selected |
| 0.001 / 0.054 / 0.03 | 0.34630424391493014 | 0.6781853306671439 |
| **0.002 / 0.054 / 0.03** | **0.3403981678427398** | **0.37447132147774026** |
| 0.004 / 0.054 / 0.03 | 0.93613693225549 | Not selected |

The best two at 32 continued from their exact full-state checkpoints to 64.
The better 64-update recipe continued to 128, then received independent held-out
confirmation without further tuning. Only this selected winner was measured at
128. There were **256 logical candidate updates** and **258 completed physical
update calls**, including two duplicated mechanical-proof calls. All twelve
native phases exited successfully and their owned processes were reaped. The
fresh-two versus fresh-process one-plus-one proof matched full state and metrics
exactly; public RAW native inference reproduced the saved response. Confirmation
used the public native-only reader without training constructors. An independent
CPU audit of the saved final tensors reproduced every per-example SSE, teacher
energy and OFF/teacher/reverse control exactly, including the above-OFF example;
all four examples remained in the mean.

The sole ranking and confirmation metric follows the
[common evaluation protocol](https://github.com/HyperGAN/particle-sliders/blob/main/packages/particle-sliders-core/EVALUATION-AND-LR-SEARCH.md):
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
correctness checks. The historical
[PG801 confirmation receipt](docs/native-lr-confirmation-20261105.json) records
G **0.001** / D **0.054** / bank **0.03**, development **0.5614657431858548** and
confirmation **0.40601743965471515** on its original core/PG801 source and data.
Those are not PG0.9.5 results and their original packets remain unchanged. The
[64-horizon development report](docs/NATIVE-LR-DEVELOPMENT-20261104.md) is also
historical. Its preservation/semantic-based “no nominee” conclusion is
superseded for the sole RAW-response goal by the source-qualified confirmations;
no semantic-quality claim follows.

## Controls, defaults and historical packages

The optional `lr`, `d_lr_mult` and `prior_lr_mult` keys accept only finite
positive numbers, rejecting booleans before allocation. Shared ParticleGAN
creates the optimizers: D = `lr * d_lr_mult`, bank = `lr * prior_lr_mult`.
No product GAN or optimizer mathematics is duplicated.

Omitting the keys retains the inherited `bispf_optimized` defaults: G **0.012**,
D multiplier **1.5**, bank multiplier **2.5**. These defaults are unchanged.
The current package is 0.7.0 with separate v7 fixture/native identities, recorded
in `sources.lock.json` and `PG095-MIGRATION.json`. Historical
`NATIVE-MIGRATION.json`,
`CORE-MIGRATION.json`, `LR-MIGRATION.json` and the v4/v5 compatibility receipts
remain intact; use their original product/core environment for their packets.
