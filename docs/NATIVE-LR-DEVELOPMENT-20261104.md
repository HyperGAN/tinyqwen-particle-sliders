# Native TinyQwen learning-rate development, 2026-11-04

No learning-rate change is nominated. The two coordinate finalists regressed
between steps 32 and64. A separately authorized full-budget control using the
inherited defaults had better average hidden fit, but none demonstrated the
intended positive language edit. The independent final examples remain sealed,
the default G/D/P base rates remain 0.012/0.018/0.03, and no more TinyQwen GPU
work is queued by this result.

This result applies only to runtime 5d91b962, core 5d68473, explicit PG 801ae1e
continuous source, Qwen3-0.6B-Base at da87bfb, Torch 2.9.1+cu128,
Transformers 5.3.0, BF16/eager native hidden 1024, and the frozen small paired-text
cohort in the [machine-readable receipt](native-lr-development-results-20261104.json).
It does not select a rate for another model, source, numerical profile or task.
The earlier [two-update numerical proof](native-numerical-validation.json)
remains separate from rate or language-quality qualification.

All trials used the same actual initialization, seed 7, batch 2, eight training
pairs, fixed 64-step schedule, and four development examples. The remaining four
evaluation examples were not evaluated. Prefix screens stopped at 16 while
retaining the 64-step schedule. Reused centers required exact identity proof.
The three full-budget runs restored their original step 16 packets only after
proving source/config/recipe/data, complete state/RNG/streams, actual common
initialization, and native step 16 responses equal. Each then ran 48 new updates.
An explicitly configured diagnostic EMA 0.9 was retained; all selection metrics,
responses and exports in this comparison use **raw** parameters.

The primary score R is the mean across development examples of squared hidden
student-to-teacher error divided by squared neutral-to-teacher edit energy.
Neutral, exact teacher and reversed-edit controls are 1, 0, 4. Smaller is better.
These hidden-fit scores do not measure language quality. G/D/P are absolute
base rates before the common schedule; actual optimizer groups and full raw
per-example totals are retained in the receipt and original trial reports.

| Phase | G | D | P | Full-strength R at 16 | R at 32 | R at 64 |
|---|---:|---:|---:|---:|---:|---:|
| G screen | 0.00001 | 0.018 | 0.03 | 1.013273 | — | — |
| G screen | 0.0001 | 0.018 | 0.03 | 0.991695 | — | — |
| G screen / reused D center | 0.001 | 0.018 | 0.03 | 0.538841 | — | — |
| Default-rate control | 0.012 | 0.018 | 0.03 | 0.786527 | 0.630041 | 0.801468 |
| D screen | 0.001 | 0.006 | 0.03 | 0.548540 | — | — |
| D screen / reused P center / finalist | 0.001 | 0.054 | 0.03 | 0.475952 | 0.323283 | 0.966394 |
| P screen | 0.001 | 0.054 | 0.003 | 0.489678 | — | — |
| P screen / finalist | 0.001 | 0.054 | 0.09 | 0.471682 | 0.323002 | 1.050848 |
| One bounded critic extension | 0.001 | 0.162 | 0.09 | 0.821544 | — | — |

There were nine unique 16-update screens, two 48-update finalist continuations,
and one 48-update default continuation: 288 actual campaign training updates.
The two-update numerical proof and one resume replay are recorded separately.
All bad outcomes and 16/32/64 packets were retained. The temporary 32-step gains
do not replace the predeclared 64-step comparison.

At 64, pooled full-strength SSE/edit-energy ratios were 0.728397 for defaults,
0.725309 for P 0.03, and 0.865783 for P 0.09.
The similar pooled results and different equal-example means show why raw
per-example values matter. The P 0.03 finalist worsened one example to R 2.118106.
The half-strength means were 0.984312 for defaults,0.803784 for P 0.03, and
1.092491 for P 0.09. Relative bank movement was0.007097,0.046766 and0.127223,
respectively; all 512 bank values changed.

Matched native controls used actual last-token logits and 24-token greedy
continuations. OFF matched the unhooked host logits and complete continuations
exactly; observations preserved the frozen host and game. Half and full
strengths changed the logits and differed from each other on all four examples.
Mean first-token teacher KL moved from 0.645518 at OFF to 0.470293 for defaults,
0.538796 for P 0.03 and0.583004 for P 0.09. This is a narrow next-token diagnostic,
not a generated-language score.

Actual continuations remained invented arithmetic or repetition. Default-rate
museum output largely stayed unchanged, the path changed meters to feet, and
the station became fraction/area arithmetic. The coordinate finalists similarly
produced counts and arithmetic. OFF and the positive-context teacher themselves
also often produced arithmetic or repetition. These four development examples
provide no consistent demonstration of the intended positive/adjective edit.
Preservation evidence covers exact OFF behavior, frozen weights and unchanged
observation state; independent semantic preservation is unqualified.

The bounded comparison therefore closes without a nominee or final-set access.
Further work needs a separately justified training/evaluation change and new
source/data/numerical receipts before another rate or horizon search.
