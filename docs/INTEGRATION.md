# TinyQwen v7 / PG0.9.5 integration

Install the current package in a new Python3.11–3.14 environment:

```bash
python -m pip install .
particle-slider train --profile tinyqwen-cpu-fixture --check --no-reporting
```

The installer pins `particle-sliders-core[hypergan-hndl]` to public commit
`3dd672a7f9b8c169daef90fd63e4bb42b9ddc423` (core0.13.0), published
`particlegan==0.9.5`, HyperGAN5f368a3 and HNDL0.10.0. The installed core must have
that genuine noneditable immutable VCS origin. Complete recursive installed
source/data inventories cover `particle_sliders`, `concept_slider_core` and the
product package; source checks precede model mutation. The official PG wheel
source manifest independently validates all ParticleGAN Python bytes.

The common CLI/profile and Python API share `ConditionalPG095`. A minimal
fixture configuration is
`binding.config(fixture=True, steps=4, batch=2, ema_decay=None)`.
Use `open_response` checkpoint/resume and `open_inference` with RAW weights;
all new sessions disable EMA, and exports explicitly select `raw`. The APIs
create separate v7 source/cohort identities. Historical EMA compatibility does
not recommend averaging, comparison or EMA selection for new runs.
Use explicit held-out evaluation rows when measuring an LR. Do not treat random
CPU fixture scores as native calibration.

For [native BF16 staging](../NATIVE-CANDIDATE.md), use
`pg_source_profile="release-0.9.5", penalty_input_domain="continuous"`.
The native model, precision, rank, bank and loader requirements remain unchanged;
the fresh [native measurement](../LEARNING-RATES.md) now records actual
PG0.9.5 training, exact native continuation and RAW-only confirmation.

`tools/refresh_source_lock.py --core-source /clean/exact/core3dd-checkout`
regenerates v7 indexes from Git objects and the actual installed core. It writes
only the new `PG095-MIGRATION.json`; the original extraction, core, LR and native
migration receipts remain unchanged. The old native recipe and final score in
[learning-rate evidence](../LEARNING-RATES.md) require their old source pins.

Use held-out RAW teacher/student relative squared error as the sole LR ranking
and confirmation metric. Cast operands to FP64 before subtraction, pool all
declared positions inside each example, then average examples equally. Freeze
teacher-only zero-energy exclusions, use equal update budgets and a common
horizon, and complete every finite candidate budget. Preservation, late/weak
scores and media are optional diagnostics.
