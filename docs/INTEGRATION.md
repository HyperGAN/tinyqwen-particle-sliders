# TinyQwen final modern-core preview

The active `tinyqwen-shared-preview==0.3.0` distribution uses the v3 CPU fixture
cohort and exact shared core commit `a794e3b4a8813b012f2c4faa3da82b78d4a90214`.
This changes source and lifecycle identities, not the model, training objective,
attention targets, rank 8/alpha 8, or one 128 x 4 bank architecture.

Native `Qwen/Qwen3-0.6B-Base` hidden width 1024 remains **blocked** by the reviewed
release 0.9.4/auto continuous-vector gate. No weights are loaded, reshaped or
converted to evade it. Root's synthetic CUDA qualification concerns the shared
software fixture only; it grants no native TinyQwen, model-width or quality admission.
Product qualification here uses random CPU fixtures with widths 16 and 32.

## Exact origin and recursive source/data admission

The package owns only `tinyqwen_shared_preview`; it does not install `conceptmod`
or any umbrella initializer. Its host remains the extracted model-specific
`backend.py`. The shared dependency is an immutable Git URL:

```text
particle-sliders-core[hypergan-hndl] @ git+https://github.com/HyperGAN/particle-sliders.git@a794e3b4a8813b012f2c4faa3da82b78d4a90214#subdirectory=packages/particle-sliders-core
```

Admission requires the exact PEP610 Git repository, commit, package subdirectory,
noneditable installation and expected core version 0.12.0. A version-only install,
an old core wheel or a different Git origin is refused. The recursive lock covers
all installed core source/data files, including LICENSE and nested data, and all
product source/data files except the lock's own self-reference. Only generated
`__pycache__` directories and `.pyc` files are excluded. Missing, changed or extra
data fails closed. File indexes have canonical SHA256 identities.

The unchanged shared gates additionally verify official ParticleGAN 0.9.4, clean
HyperGAN develop `5f368a3770cf5bdae0448995c9f76e29af8049f7`, HNDL 0.10.0 and their
reviewed source closures. This product does not independently hash Torch or the
standard library; the common game records runtime versions in its packet signature.
Git metadata is not a cryptographic attestation by itself, so imported file bytes
are independently compared with the approved lock.

## Reproducible CPU installation and artifacts

Use a separate Python 3.12 environment with a supported CPU Torch build. The
product checks use Torch 2.14.1+cpu; shared-core qualification also covers Torch 2.6.
Do not combine this environment with archived preview or HNDL 0.8.2 environments.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'setuptools==84.2.1' 'build==1.6.1' 'hatchling==1.28.0' 'pytest==9.1.1'
python -m pip install 'torch==2.14.1+cpu' --index-url https://download.pytorch.org/whl/cpu
python -m pip install --no-build-isolation 'particle-sliders-core[hypergan-hndl] @ git+https://github.com/HyperGAN/particle-sliders.git@a794e3b4a8813b012f2c4faa3da82b78d4a90214#subdirectory=packages/particle-sliders-core'
python -m build --no-isolation --sdist --wheel
python -m pip install --no-deps --force-reinstall dist/tinyqwen_shared_preview-0.3.0-py3-none-any.whl
python -m pip check
```

Both the wheel and sdist carry the package, source lock and inherited MIT license.
The sdist includes the standalone build, test and reference-fixture inputs. It can
be unpacked and rebuilt outside this checkout. No umbrella source is needed.
Maintenance lock regeneration is explicit and does not widen admission:

```bash
# The source checkout must be clean at the exact approved core commit.
python tools/refresh_source_lock.py --core-source /path/to/approved/core-checkout
```

The script compares actually imported core bytes with immutable Git objects,
regenerates the complete indexes coherently, and records the controlled changes
in `CORE-MIGRATION.json`. `EXTRACTION-PROVENANCE.json` remains the original phase 1
receipt; it is not rewritten to imply that updated files are still byte-identical.

## Lifecycle, strengths and old packets

```python
from tinyqwen_shared_preview.binding import config
from particle_sliders.response import open_response
from particle_sliders.inference import open_inference

rows = [dict(neutral_ids=[1, 2], positive_ids=[1, 3]),
        dict(neutral_ids=[4, 5], positive_ids=[4, 6])]
with open_response(config(fixture=True, fixture_width=16, steps=4, ema_decay=.9), rows=rows) as session:
    session.train()  # Bounded software fixture updates, not pretrained training.
    session.checkpoint('/tmp/tinyqwen-v3-resume.pt')
    session.export_inference('/tmp/tinyqwen-v3-native.pt', selection='ema')
    hidden = session.evaluate(strength=0)
with open_inference('/tmp/tinyqwen-v3-native.pt', operation='response') as native:
    hidden = native.response(ids=[1, 2], strength=-1.)
```

Training uses scale +1. Runtime probes support finite signed and extrapolated
scalars because each attachment computes `base(x) + strength * branch(x)`.
Scale 0 bypasses exactly. The nonlinear whole-model response need not interpolate
linearly, and no quality calibration is claimed outside the training scale.
Nonfinite strengths and responses are rejected. Inference and evaluation disable
autograd; the shared training path retains adapter gradients.

The new cohort is `tinyqwen-pg094-hypergan-hndl-v3-cpu-fixture`. Old v2 training and
inference packets require their original product/core environment and are refused
by v3. Their exact lock and recovery instructions are preserved in `compatibility`.
No old metadata is edited or relabeled. Historical Rp/VIC trainers and checkpoints
remain in the umbrella, as tracked in `MIGRATION.md`.

## Cleanup guarantees and remaining shared gaps

Product cleanup attempts every owned forward and saved mode/gradient restoration.
Foreign forwards are retained rather than overwritten; unresolved actions and failed
checkpoint handles remain in retry ledgers. Product factory failures retain their
initiating exception and an explicit `cleanup_owner` when cleanup also fails.
These are best-effort guarantees, not guaranteed removal of foreign hooks.

The approved core now preserves the original error and adds cleanup failure notes
on outer lifecycle failure paths. A failed close leaves an existing session open
for a genuine retry; it is marked closed only after successful cleanup. Tests cover
that behavior with an actual TinyQwen binding and injected bounded failures.

Two distinctions remain important:

- **Deep training packet admission still follows product preparation and attachment.**
  Packet checksum/config checks precede preparation, and full signature/tensor
  preflight precedes live module state loading. That is not rejection before any
  native product hook. A test confirms attachment occurs before deep signature
  rejection, followed by cleanup. A packet-aware pre-prepare core seam remains needed.
- **Cleanup notes do not always expose a public retry owner.** If shared session
  construction fails after preparation and cleanup also fails, the core preserves
  the original error and note text but does not attach `cleanup_owner`. A test
  confirms this remaining owner-preservation gap. Existing callers holding a
  session or binding can retry; failed factory callers may lack that public handle.

Native-only inference still compares its complete model/source/shape identity on
unattached real graphs before hooking or loading adapter values. The product-bound
verified Linear16/SiLU/Linear1 graph remains unchanged. A canonical identity-bound
shared vector critic is still a central API request, not a new import invented here.

No core API, GAN mathematics, HNDL optimization, native response-domain admission,
model license, workflow or access permission changes are made by this pin.

## Installed conformance

Run the tests outside the checkout, copying the adjacent architecture fixtures:

```bash
mkdir -p /tmp/tinyqwen-installed-tests
cp tests/test_*.py /tmp/tinyqwen-installed-tests/
cp -R tests/fixtures /tmp/tinyqwen-installed-tests/
TINYQWEN_EXPECT_INSTALLED=1 TINYQWEN_EXTRACTED_ROOT="$PWD" \
TINYQWEN_WHEEL="$PWD/dist/tinyqwen_shared_preview-0.3.0-py3-none-any.whl" \
TINYQWEN_SDIST="$PWD/dist/tinyqwen_shared_preview-0.3.0.tar.gz" \
  python -m pytest -q /tmp/tinyqwen-installed-tests
```

The suite covers real HyperGAN/HNDL execution, matched projection VJPs, actual
shared BISPF penalty derivatives, updates, exact resume, raw/EMA/OFF inference,
source/data/origin tamper refusal, native width refusal and lifecycle cleanup/retry.
It also records the two remaining shared gaps above without claiming they are fixed.

The executor has no `/dev/nvidia*`; GPU occupancy is unknown and GPU 0 is reserved.
No product GPU job, pretrained model training, memory-fit, quality, deployment,
package-index release, weight publication or checkpoint conversion is included.
