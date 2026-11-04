# Learning rates

The current training configuration accepts optional `lr` (base/generator), `d_lr_mult` (critic), and `prior_lr_mult` (actual routed particle bank). Values must be finite positive numbers; booleans are rejected before model allocation. The existing shared ParticleGAN recipe creates all optimizers: D = `lr * d_lr_mult`, bank = `lr * prior_lr_mult`. No product GAN or optimizer math is duplicated.

Omitted controls retain the default `bispf_optimized` recipe: G **0.012**, D multiplier **1.5**, bank multiplier **2.5**. These are inherited defaults, not native calibration results. This factory uses its fixed optimized preset. Use the keys in the shared session configuration; the registered common training dispatcher executes the same recipe. Historical/source-only CLI cohorts retain their original interfaces.

Use `"lr": 0.00002, "d_lr_mult": 1.5, "prior_lr_mult": 2.5` in common session `options`. The numbers are an input example, not a tuned recommendation. The actual resolved shared recipe and configuration bind full-state resume; a changed rate requires a fresh experiment output/cohort. Older packets and closed HNDL source cohorts keep their original source/defaults. Current CPU optimizer/resume tests do not qualify pretrained/native learning rates, audio or semantic quality.

The official release/auto profile still refuses native width 1024. The separate
v6 native candidate requires the exact core/PG/model/numerical configuration in
[NATIVE-CANDIDATE.md](NATIVE-CANDIDATE.md). Its numerical update/resume proof is
not a calibrated rate or semantic quality result. Native rate comparisons must
freeze source/model/data, actual initial tensors, seeds, horizons and evaluation
controls, with development and final confirmation kept separate.

The current package is 0.6.0 with separate v6 fixture/native identities. Its full
product/core closure is recorded in `sources.lock.json`; controlled current
changes are in `NATIVE-MIGRATION.json`. Historical `CORE-MIGRATION.json` and
`LR-MIGRATION.json` remain intact. The exact v4 and v5 locks, receipts and product
requirements are preserved in `compatibility/preview-v4` and `compatibility/preview-v5`.
Use each old product commit and its original core environment for its packets.
