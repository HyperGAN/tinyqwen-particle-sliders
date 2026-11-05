# TinyQwen shared ParticleGAN 0.9.5 cohort

The current `tinyqwen-shared-preview==0.7.0` pins core0.13.0 at
`3dd672a7f9b8c169daef90fd63e4bb42b9ddc423`. It explicitly imports
`particle_sliders.pg095.ConditionalPG095` and verifies both installed core
namespaces plus its own complete source/data closure and immutable Git origin.

The v7 CPU fixture and native BF16 profiles are separate. The CPU fixture uses
random width16/32 model hosts with real PG/HG/HNDL updates, exact continuation,
and public RAW inference. Native width1024 requires the published
`release-0.9.5` profile and explicit `penalty_input_domain="continuous"`, plus the
unchanged Qwen3 model revision, Torch2.9.1+cu128, Transformers5.3.0 and BF16 base.
The fresh native PG0.9.5 response campaign now has a source-qualified measured
recipe: **G 0.002 / D 0.054 / particle bank 0.03**, with a common 128-update
horizon, development RAW relative SSE **0.7003497239527556** and four-example
held-out confirmation **0.7981414033678553**. See the [learning-rate guide](LEARNING-RATES.md)
and [numerical/source receipt](docs/native-lr-confirmation-pg095-20261105.json).
The inherited package defaults remain unchanged. New sessions explicitly use
`ema_decay=None`; training, evaluation, export and inference use RAW weights.
Do not enable EMA averaging, comparison or selection. Historical EMA receipts
retain their original source and do not define current guidance.

Use a new environment and new cohort/output paths. See [integration](docs/INTEGRATION.md)
and [native admission](NATIVE-CANDIDATE.md). The fixture cohort is
`tinyqwen-pg095-hypergan-hndl-v7-cpu-fixture`; the native cohort is
`tinyqwen-pg095-hypergan-hndl-v7-native-bf16`. Attention targets, bank geometry,
learning-rate defaults and numerical policies are unchanged.

Native training uses public `open_response(SessionConfig)`; the registered
`tinyqwen-cpu-fixture` CLI is a CPU fixture route. The measured custom cohort and
full recipe are documented in the [native API example](LEARNING-RATES.md#native-recipe-and-api).
The earlier [PG801 confirmation](docs/native-lr-confirmation-20261105.json) remains
historical and cannot be relabeled as PG0.9.5. Keep those packages/checkpoints in
their original environment. `NATIVE-MIGRATION.json` remains unchanged;
`PG095-MIGRATION.json` records this separate migration. The
[v6 source lock and guides](compatibility/preview-v6/README.md) retain their
original identity. V2 through v6 packets are never relabeled.
