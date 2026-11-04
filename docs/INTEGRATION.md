# TinyQwen v6 integration

The active `tinyqwen-shared-preview==0.6.0` package uses exact core
`5d68473a098801ee1ab3ebbb12463daef51c6346`. The default official ParticleGAN
0.9.4 release/auto profile supports random CPU fixtures of width 16/32 and still
refuses native width 1024 before model allocation.

A distinct explicit [native BF16 candidate](../NATIVE-CANDIDATE.md) admits the
full 1024-wide Qwen3 last-hidden response only with exact PG801 continuous-source
selection, local model assets and the declared CUDA numerical cohort. Its actual
update/resume/portable inference proof does not establish semantic quality or a
new default rate. The `tinyqwen-cpu-fixture` dispatcher profile remains a fixture.

## Exact origin and recursive source/data admission

The package owns only `tinyqwen_shared_preview`; it does not install `conceptmod`
or any umbrella initializer. Its host remains the extracted model-specific
`backend.py`. The shared dependency is an immutable Git URL:

```text
particle-sliders-core[hypergan-hndl] @ git+https://github.com/HyperGAN/particle-sliders.git@5d68473a098801ee1ab3ebbb12463daef51c6346#subdirectory=packages/particle-sliders-core
```

Admission requires the exact PEP610 Git repository, commit, package subdirectory,
noneditable installation and expected core version 0.12.0. A version-only install,
an old core wheel or a different Git origin is refused. The recursive lock covers
all 575 installed core source/data files across `particle_sliders` and
`concept_slider_core`, including LICENSE and nested data, and all
product source/data files except the lock's own self-reference. Only generated
`__pycache__` directories and `.pyc` files are excluded. Missing, changed or extra
data fails closed. File indexes have canonical SHA256 identities.

The default shared gates verify official ParticleGAN 0.9.4; only the separately
selected native source/domain pair admits exact PG801. Both profiles verify clean
HyperGAN develop `5f368a3770cf5bdae0448995c9f76e29af8049f7`, HNDL 0.10.0 and their
reviewed source closures. This product does not independently hash Torch or the
standard library; the common game records runtime versions in its packet signature.
Git metadata is not a cryptographic attestation by itself, so imported file bytes
are independently compared with the approved lock.

## Reproducible CPU installation and artifacts

Use a separate Python 3.11+ environment with a supported CPU Torch build. The
latest installed fixture checks used CPython 3.12 and Torch 2.9.1+cu128 with CUDA
hidden; no GPU was initialized by those CPU checks.
Do not combine this environment with archived preview or HNDL 0.8.2 environments.

```bash
export CUDA_VISIBLE_DEVICES=''
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'setuptools==84.2.1' 'build==1.6.1' 'hatchling==1.33.0' 'pytest>=8,<10'
python -m pip install 'torch==2.9.1' --index-url https://download.pytorch.org/whl/cpu
python -m pip install --no-build-isolation 'particle-sliders-core[hypergan-hndl] @ git+https://github.com/HyperGAN/particle-sliders.git@5d68473a098801ee1ab3ebbb12463daef51c6346#subdirectory=packages/particle-sliders-core'
python -m build --no-isolation --sdist --wheel
python -m pip install --no-deps --force-reinstall dist/tinyqwen_shared_preview-0.6.0-py3-none-any.whl
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
in `NATIVE-MIGRATION.json`. Historical `CORE-MIGRATION.json` and
`LR-MIGRATION.json` remain unchanged. `EXTRACTION-PROVENANCE.json` remains the original phase 1
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
    session.checkpoint('/tmp/tinyqwen-v6-resume.pt')
    session.export_inference('/tmp/tinyqwen-v6-native.pt', selection='ema')
    hidden = session.evaluate(strength=0)
with open_inference('/tmp/tinyqwen-v6-native.pt', operation='response') as native:
    hidden = native.response(ids=[1, 2], strength=-1.)
```

Training uses scale +1. Runtime probes support finite signed and extrapolated
scalars because each attachment computes `base(x) + strength * branch(x)`.
Scale 0 bypasses exactly. The nonlinear whole-model response need not interpolate
linearly, and no quality calibration is claimed outside the training scale.
Nonfinite strengths and responses are rejected. Inference and evaluation disable
autograd; the shared training path retains adapter gradients.

The default fixture cohort is `tinyqwen-pg094-hypergan-hndl-v6-cpu-fixture`.
The explicit native cohort is `tinyqwen-pg094-hypergan-hndl-v6-native-bf16`.
Old v2-v5 training and inference packets require their original product/core
environment and are refused by v6. Their exact locks and recovery instructions are preserved in `compatibility`.
No old metadata is edited or relabeled. Historical Rp/VIC trainers and checkpoints
remain in the umbrella, as tracked in `MIGRATION.md`.

## Shared training command

The installed `tinyqwen-cpu-fixture` profile declares `interface: response` and
`status: fixture`. Its options require an actual JSON boolean `dummy: true`.
`fixture` controls the bounded host; `dummy` records the shared dispatcher admission
and must match `fixture` when supplied. `config(fixture=True, ...)` writes both.
The historical API can still pass rows to `open_response(..., rows=rows)`; the
isolated command carries them in the configuration instead. Supplying both is refused.

```bash
python - <<'PY'
import json
from pathlib import Path
from tinyqwen_shared_preview.binding import config
rows = [dict(neutral_ids=[1, 2], positive_ids=[1, 3]),
        dict(neutral_ids=[4, 5], positive_ids=[4, 6])]
Path('tinyqwen-fixture.json').write_text(json.dumps(
    config(fixture=True, fixture_width=16, rows=rows, steps=4, ema_decay=.9).as_dict()))
PY
particle-slider plan --config tinyqwen-fixture.json --profile tinyqwen-cpu-fixture --no-reporting
particle-slider train --config tinyqwen-fixture.json --profile tinyqwen-cpu-fixture --no-reporting --check
particle-slider train --config tinyqwen-fixture.json --profile tinyqwen-cpu-fixture --no-reporting \
  --out tinyqwen-partial --checkpoint-every 1 --stop-after 2 --selection ema --export-format both
particle-slider train --config tinyqwen-fixture.json --profile tinyqwen-cpu-fixture --no-reporting \
  --out tinyqwen-complete --resume tinyqwen-partial/artifacts/checkpoints/step-000002 \
  --checkpoint-every 2 --selection ema --export-format both
```

The four-update target stays fixed across the partial run and continuation.
Training remains owned by the installed shared response session. Checkpoints and
EMA inference exports contain fixture qualification and source identity; this
profile does not admit native TinyQwen, download models or generate tokens.

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

The native source/domain extension is explicit and does not widen the default
official-release guard. No product GAN mathematics, HNDL optimization, model
license, workflow or access permission changes accompany these profiles.

## Installed conformance

Run the tests outside the checkout, copying the adjacent architecture fixtures:

```bash
mkdir -p /tmp/tinyqwen-installed-tests
cp tests/test_*.py /tmp/tinyqwen-installed-tests/
cp -R tests/fixtures /tmp/tinyqwen-installed-tests/
TINYQWEN_EXPECT_INSTALLED=1 TINYQWEN_EXTRACTED_ROOT="$PWD" \
TINYQWEN_WHEEL="$PWD/dist/tinyqwen_shared_preview-0.6.0-py3-none-any.whl" \
TINYQWEN_SDIST="$PWD/dist/tinyqwen_shared_preview-0.6.0.tar.gz" \
  python -m pytest -q /tmp/tinyqwen-installed-tests
```

The suite covers real HyperGAN/HNDL execution, matched projection VJPs, actual
shared BISPF penalty derivatives, updates, exact resume, raw/EMA/OFF inference,
source/data/origin tamper refusal, default-release native width refusal, exact
asset/data admission and lifecycle cleanup/retry.
It also records the two remaining shared gaps above without claiming they are fixed.

The v6 runtime passes 93 installed CPU checks, plus the separate actual native
[numerical qualification](native-numerical-validation.json). Native CUDA work
requires fresh physical-device admission, its own role lock and a measured
memory cap; the package does not reserve hardware. These results establish no
semantic quality, package-index release, weight publication or old-packet conversion.
