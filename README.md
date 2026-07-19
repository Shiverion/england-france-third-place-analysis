# England vs France: third-place match analysis

Reproducible analysis of whether England 6–4 France played like a relaxed exhibition match or an unusually open, competitive official match.

## Main conclusion

The evidence supports a more precise interpretation than “nobody tried”:

> A lower-stakes, heavily rotated official match in which live individual rewards preserved strong attacking incentives. It combined high attacking risk and aggressive pressure attempts with unusually weak defensive control. Its scoring looked exhibition-like, but the process data do not look passive.

The matched professional comparison found no general goal-scoring advantage for elite friendlies over official tournament matches. The current match was still an extreme ten-goal outlier, and the 4–0 score state explains only part of its openness. Player-level FIFA data sharpen the diagnosis: comparable outfielders produced 12% more high-intensity distance and 63% more direct pressures than their own earlier-tournament rates, while both teams conceded their worst opponent xG of the tournament. The raw player tests are exploratory and do not survive correction for four related outcomes, but the same-team rankings strongly reject a simple “everyone jogged” story.

France also retained Kylian Mbappé and Michael Olise—its live goal and assist leaders—among only four retained starters. Their before-and-after totals and observable Match-103 activity support a selective individual-incentive mechanism, without proving private motive or universal stat-padding. Ten goals from 5.33 xG show that exceptional finishing then magnified the open chance environment.

## Hypothesis and confidence

**H1:** compared with serious official matches, the third-place match behaved like a low-pressure fun or charity match: less effort and defending, more open scoring, and selective individual stat-seeking.

**H2:** live Golden Boot, assist, and record incentives influenced selection and attacking involvement, giving specific players an opportunity to boost personal statistics.

**Verdict: partially supported, with moderate overall confidence.** Lower team-level stakes and exhibition-like openness are supported. Broad physical coasting and “no defending” are not supported; the player tests are exploratory and none survives Holm correction. Individual award incentives are plausible and selectively supported, but the samples are small and private motivation cannot be observed. Exact equivalence to a charity match is not established.

For H2 specifically: **suggestive but underpowered, with low-moderate confidence**. Mbappe and Olise were selectively retained and highly involved, but the small within-player samples cannot establish intentional stat-padding or prove that the match was primarily played to boost statistics.

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
- [Lower team stakes, live individual rewards](output/assets/v2_individual_incentives.png)
- [High physical intensity, weak collective control](output/assets/v2_effort_vs_control.png)
- [They ran, they pressed, they lost control](output/assets/narrative_05_effort_without_control.png)
- [Award-leader activity and finishing decomposition](output/assets/v2_player_behavior_and_finishing.png)

## Methods in brief

- 173 neutral matched friendly–official pairs from 1991–2023.
- Pair matching on year, average prior-year Elo, Elo gap, neutral venue, and prior-year top-30 eligibility.
- Paired bootstrap and sign-flip permutation test for the mean goal difference.
- Exact paired threshold test for five-plus goals.
- Sensitivity checks using top-10, top-15, top-20, and friendly-versus-qualifier designs.
- Smoothed count-model tail probabilities for ten-goal rarity.
- World Cup score-state decomposition using 964 regulation-time matches and match-cluster bootstrap resampling.
- FIFA Post-Match Summary Report process comparison for matches 1–103.
- Timestamped before/after audit of live player awards, selection, match contributions, and changed standings.
- Player-level physical and pressing extraction from all eight France and all eight England matches.
- Within-player per-90 comparison for 19 eligible outfielders, using bootstrap intervals, sign-flip tests, and Holm correction across four effort metrics.
- Small-sample empirical tail checks for award-candidate activity; treated as descriptive because each player has only six or seven prior appearances.
- Aggregate-xG finishing decomposition with a clearly labelled Poisson approximation.
- Component-by-component hypothesis verdict with separate confidence grades, because the broad “fun match” claim is composite rather than a single testable statistic.

Statistical tests describe the match’s observable scoring and process profile. They cannot prove private player motivation or intent.

## Reproduction notes

The notebook was executed top-to-bottom successfully before publication. To rerun the analysis, use a Python environment with pandas, NumPy, SciPy, matplotlib, PyMuPDF, and nbclient installed, then run:

```powershell
python scripts/build_player_effort_data.py
python scripts/build_v2_notebook.py
python scripts/execute_notebook.py
python scripts/build_narrative_effort_control_image.py
```

The compact processed player CSVs are included, so the first command is only needed to refresh them. It reads saved official reports where available and fetches missing FIFA reports in memory.

The international-results source is tracked as a submodule at the pinned commit listed in `data/source_manifest_v2.json`. The team-strength and World Cup-history inputs are external source snapshots from the sibling `Argentina Comeback Analysis` project; their repositories and pinned commits are recorded in the manifest.

## Data and provenance

The project combines public international match results, soccer Elo ratings, World Cup history, FIFA Post-Match Summary Reports, player physical and event tables from 15 official reports, a current-match goal timeline, manually transcribed starting lineups, timestamped player-award evidence, and a small charity-match benchmark. The charity sample is used only as a descriptive external anchor, not as a like-for-like professional control.

See `data/source_manifest_v2.json` for source URLs, pinned commits, coverage, and known limitations.
