# Archived preview v2

The v2 extraction remains recoverable at public product commit
`a2798264059c2b7c260ec98f3db8a21e41c8819c` (distribution 0.2.0,
`tinyqwen-pg094-hypergan-hndl-v2-cpu-fixture`). Its exact source lock is preserved
byte-for-byte as `preview-v2-source.lock.json` here. The original umbrella source
also remains at `6ce328561dbcba1bb981217487ce594a01bd13d2`.

Use that original product commit and core 4abc0eb environment for v2 packets.
Do not load, edit or relabel their metadata into the current v3 cohort.
V3 uses exact core a794e3b4a8813b012f2c4faa3da82b78d4a90214 and has new
implementation/lifecycle identities. V2 training and inference packets are
intentionally refused; no conversion or continuation compatibility is promised.
The model, objective, rank 8/alpha 8, one 128 x 4 bank and native 1024 refusal are unchanged.

The archived historical Rp/VIC environment is separate from both previews and
remains in the umbrella as tracked in `MIGRATION.md`.
