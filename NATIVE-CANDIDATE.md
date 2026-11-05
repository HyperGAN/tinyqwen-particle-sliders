# PG0.9.5 native TinyQwen candidate: new v7 cohort

Install `requirements-native-candidate.txt` in a fresh environment, then the
0.7.0 product wheel with `--no-deps`. The requirements pin official
`particlegan==0.9.5`, exact core3dd672a/core0.13.0 and Transformers5.3.0.
Install Torch2.9.1+cu128 from its official CUDA wheel index separately.

The native options require `fixture=False`, `base_precision="bfloat16"`, explicit
`cuda:N`, local model/data paths, `pg_source_profile="release-0.9.5"` and
`penalty_input_domain="continuous"`. No implicit hub load is allowed. Model
revision `da87bfb608c14b7cf20ba1ce41287e8de496c0cd`, all eight model asset hashes,
native last-hidden width1024, attention LoRA targets, routing/bank geometry and
numerical guards remain unchanged. The released upstream continuous declaration
admits the actual vector shape without reshaping it into categorical data.

This is source/API readiness, not a PG0.9.5 native training or LR qualification.
Old v6 native receipts and confirmed rate evidence belong to core5d68473 and
PG801ae1e; retain their original environments and never restore them into v7.
See [historical v6 native guide](compatibility/preview-v6/NATIVE-CANDIDATE.md).
The original `NATIVE-MIGRATION.json` and its archived copy remain byte-identical.
