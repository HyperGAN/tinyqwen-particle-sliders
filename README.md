# TinyQwen shared ParticleGAN 0.9.5 cohort

The current `tinyqwen-shared-preview==0.7.0` pins core0.13.0 at
`3dd672a7f9b8c169daef90fd63e4bb42b9ddc423`. It explicitly imports
`particle_sliders.pg095.ConditionalPG095` and verifies both installed core
namespaces plus its own complete source/data closure and immutable Git origin.

The v7 CPU fixture and native BF16 profiles are separate. The CPU fixture uses
random width16/32 model hosts with real PG/HG/HNDL updates, exact continuation,
and public RAW/EMA inference. Native width1024 requires the published
`release-0.9.5` profile and explicit `penalty_input_domain="continuous"`, plus the
unchanged Qwen3 model revision, Torch2.9.1+cu128, Transformers5.3.0 and BF16 base.
A declaration permits the native continuous-vector domain; it does not qualify a
pretrained training run. The new PG0.9.5 learning rates remain **uncalibrated**.

Use a new environment and new cohort/output paths. See [integration](docs/INTEGRATION.md)
and [native admission](NATIVE-CANDIDATE.md). The fixture cohort is
`tinyqwen-pg095-hypergan-hndl-v7-cpu-fixture`; the native cohort is
`tinyqwen-pg095-hypergan-hndl-v7-native-bf16`. Attention targets, bank geometry,
learning-rate defaults and numerical policies are unchanged.

The [measured native recommendation](LEARNING-RATES.md) is explicitly historical:
its old core5d68473 / PG801ae1e source and confirmed RAW score are not PG0.9.5
calibration. Keep those packages/checkpoints in their original environment.
`NATIVE-MIGRATION.json` remains unchanged; `PG095-MIGRATION.json` records this
separate migration. The [v6 source lock and guides](compatibility/preview-v6/README.md)
retain their original identity. V2 through v6 packets are never relabeled.
