# England vs France: third-place match analysis

Reproducible analysis of whether England 6–4 France played like a relaxed exhibition match or an unusually open, competitive official match.

## Main conclusion

The evidence supports a more precise interpretation than “nobody tried”:

> A lower-stakes, heavily rotated official match with high attacking risk, aggressive pressure attempts, and unusually weak defensive control. Its scoring looked exhibition-like, but the process data do not look passive.

The matched professional comparison found no general goal-scoring advantage for elite friendlies over official tournament matches. The current match was still an extreme ten-goal outlier, and the 4–0 score state explains only part of its openness.

## Start here

- [Reader-friendly insight report](output/england_france_2026_third_place_insights_v2.md)
- [Statistical tests, evidence, and methods](output/statistical_evidence_methods_v2.md)
- [Executed Jupyter notebook](output/jupyter-notebook/england_france_2026_third_place_analysis_v2.ipynb)
- [Source manifest](data/source_manifest_v2.json)

## Narrative visuals

- [Rotated, not relaxed](output/assets/narrative_01_rotated_not_relaxed.png)
- [The score opened the game](output/assets/narrative_02_score_opened_game.png)
- [Not an ordinary friendly](output/assets/narrative_03_not_ordinary_friendly.png)
- [How we tested the claim](output/assets/narrative_04_how_we_tested_claim.png)

## Methods in brief

- 173 neutral matched friendly–official pairs from 1991–2023.
- Pair matching on year, average prior-year Elo, Elo gap, neutral venue, and prior-year top-30 eligibility.
- Paired bootstrap and sign-flip permutation test for the mean goal difference.
- Exact paired threshold test for five-plus goals.
- Sensitivity checks using top-10, top-15, top-20, and friendly-versus-qualifier designs.
- Smoothed count-model tail probabilities for ten-goal rarity.
- World Cup score-state decomposition using 964 regulation-time matches and match-cluster bootstrap resampling.
- FIFA Post-Match Summary Report process comparison for matches 1–103.

Statistical tests describe the match’s observable scoring and process profile. They cannot prove private player motivation or intent.

## Reproduction notes

The notebook was executed top-to-bottom successfully before publication. To rerun the analysis, use a Python environment with Jupyter, pandas, NumPy, SciPy, matplotlib, and PyMuPDF installed, then run:

```powershell
python scripts/build_v2_notebook.py
python -m jupyter nbconvert --execute --to notebook --inplace output/jupyter-notebook/england_france_2026_third_place_analysis_v2.ipynb
```

The international-results source is tracked as a submodule at the pinned commit listed in `data/source_manifest_v2.json`. The team-strength and World Cup-history inputs are external source snapshots from the sibling `Argentina Comeback Analysis` project; their repositories and pinned commits are recorded in the manifest.

## Data and provenance

The project combines public international match results, soccer Elo ratings, World Cup history, FIFA Post-Match Summary Reports, a current-match goal timeline, manually transcribed starting lineups, and a small charity-match benchmark. The charity sample is used only as a descriptive external anchor, not as a like-for-like professional control.

See `data/source_manifest_v2.json` for source URLs, pinned commits, coverage, and known limitations.
