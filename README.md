# England vs France: third-place match analysis

Reproducible analysis of whether England 6–4 France played like a relaxed exhibition match or an unusually open, competitive official match.

## Main conclusion

The evidence supports a bolder interpretation than “nobody tried”:

> **Match 103 had an exhibition-like observable profile with moderate-high confidence.** Players kept running, pressing, tackling, and fouling, but the usual collective controls and disciplinary consequences weakened sharply. The match behaved more like it was maximizing visible action and stat opportunity than minimizing defeat—without providing evidence that the score was pre-arranged.

The corrected comparison is no longer one target match against 102 normal matches. It trains on **102 earlier official World Cup matches and all 19 exhibition matches with complete common-core intensity data**, while keeping Match 103 as a strict holdout. The primary model excludes goals and uses shots, shots on target, fouls, and yellow cards. Its held-out exhibition-likeness diagnostic score is about **0.98**, with repeated five-fold cross-validation AUC about **0.958**. Event-family sensitivity spans roughly **0.61–0.99**, so this is strong profile evidence, not a 98% probability of fixing or intent.

The matched professional comparison found no general goal-scoring advantage for elite friendlies over official tournament matches. The current match was still an extreme ten-goal outlier, and the 4–0 score state explains only part of its openness. Player-level FIFA data sharpen the diagnosis: comparable outfielders produced 12% more high-intensity distance and 63% more direct pressures than their own earlier-tournament rates, while both teams conceded their worst opponent xG of the tournament. The raw player tests are exploratory and do not survive correction for four related outcomes, but the same-team rankings strongly reject a simple “everyone jogged” story.

The new contact panel adds **all 103 official FIFA Full Time Match Reports**. Match 103 had **22 fouls** versus **22.39** in earlier regulation-time matches, but **zero cards** versus **2.79**. Across France and England, tackles attempted rose **61%** and direct pressures **52%**, while clearances fell **65%**, aerial duels won **53%**, and possession contests won **53%**. This is high-activity, low-restraint football—not low intensity.

France also retained Kylian Mbappé and Michael Olise—its live goal and assist leaders—among only four retained starters. Their before-and-after totals and observable Match-103 activity support a selective individual-incentive mechanism, without proving private motive or universal stat-padding. Ten goals from 5.33 xG show that exceptional finishing then magnified the open chance environment.

## Hypothesis and confidence

**H1:** compared with serious official matches, the third-place match behaved like a low-pressure fun or charity match: less effort and defending, more open scoring, and selective individual stat-seeking.

**H2:** live Golden Boot, assist, and record incentives influenced selection and attacking involvement, giving specific players an opportunity to boost personal statistics.

**H3:** visible action remained high while defensive conversion and disciplinary consequence weakened—a spectacle-first behavioural tendency.

**H4:** across metrics available for both populations, Match 103 was closer to genuine exhibition matches than to ordinary official World Cup matches, even without using goals.

**Verdict:** literal H1 is partially supported because broad physical coasting is contradicted. **H3 and H4 are supported with moderate-high confidence.** Lower stakes, exhibition-like attacking volume, weak collective control, normal foul volume, and low disciplinary consequence align. Coordinated pre-arrangement is not established.

For H2 specifically: **supported as an incentive/opportunity mechanism with moderate confidence; intentional attribution remains suggestive**. Mbappe and Olise were selectively retained, highly involved, and improved award totals, but match data cannot establish private motive or coordination.

## Expanded charity/exhibition benchmark

To address the original 15-match Soccer Aid limitation, the analysis now adds 26 documented matches from Corazón Classic Match, Match for Hope, Sidemen Charity Match, Football for Hope, Game4Ukraine, and a Manchester United/Pompey legends benefit. The combined file has **41 regulation-score matches**. Results are stratified by event and roster profile because the event means range from roughly 5 to 13 goals; a pooled charity average would be misleading.

- [Expanded benchmark data](data/exhibition_charity_benchmark.csv)
- [Event-level summary and bootstrap intervals](output/tables/v2_exhibition_benchmark_summary.csv)
- [Target-vs-benchmark descriptive checks](output/tables/v2_exhibition_benchmark_tests.csv)

The formal intensity subset adds every Soccer Aid edition and every Sidemen Charity Match for which FotMob exposes the shared statistics. Nineteen of 22 rows have complete goals, shots, shots-on-target, foul, and yellow-card data; three older Sidemen rows remain score-only.

- [Exhibition intensity data](data/exhibition_match_intensity_benchmark.csv)
- [Official-vs-exhibition common-core panel](output/tables/v2_official_vs_exhibition_common_core.csv)
- [Distribution tests and effect sizes](output/tables/v2_official_vs_exhibition_tests.csv)
- [Held-out classifier validation](output/tables/v2_exhibition_classifier_validation.csv)

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
- [The expanded charity benchmark](output/assets/narrative_06_expanded_exhibition_benchmark.png)
- [Not contactless—brakeless](output/assets/narrative_07_spectacle_without_brakes.png)
- [Contact, discipline, and control](output/assets/v2_contact_discipline_and_control.png)
- [Two labeled populations and one holdout](output/assets/v2_official_vs_exhibition_holdout.png)
- [Plain-language two-population verdict](output/assets/narrative_08_two_population_verdict.png)

## Methods in brief

- 173 neutral matched friendly–official pairs from 1991–2023.
- Pair matching on year, average prior-year Elo, Elo gap, neutral venue, and prior-year top-30 eligibility.
- Paired bootstrap and sign-flip permutation test for the mean goal difference.
- Exact paired threshold test for five-plus goals.
- Sensitivity checks using top-10, top-15, top-20, and friendly-versus-qualifier designs.
- Smoothed count-model tail probabilities for ten-goal rarity.
- Expanded charity/exhibition benchmark with event-level means, bootstrap intervals, empirical tails, and source-tier labels.
- All-versus-all common-core comparison: 102 official matches versus 19 complete exhibition matches, with Match 103 held out.
- Mann–Whitney tests, Cliff's delta, Holm correction, repeated stratified cross-validation, match bootstrap, and event-family sensitivity.
- World Cup score-state decomposition using 964 regulation-time matches and match-cluster bootstrap resampling.
- FIFA Post-Match Summary Report process comparison for matches 1–103.
- FIFA Full Time Match Report foul/card panel for all 103 completed matches, with knockout, regulation-only, foul-band, and same-referee sensitivity checks.
- Same-team defensive action/control comparison covering tackles, blocks, interceptions, duels, possession contests, clearances, pressures, sprints, and high-intensity distance.
- Timestamped before/after audit of live player awards, selection, match contributions, and changed standings.
- Player-level physical and pressing extraction from all eight France and all eight England matches.
- Within-player per-90 comparison for 19 eligible outfielders, using bootstrap intervals, sign-flip tests, and Holm correction across four effort metrics.
- Small-sample empirical tail checks for award-candidate activity; treated as descriptive because each player has only six or seven prior appearances.
- Aggregate-xG finishing decomposition with a clearly labelled Poisson approximation.
- Component-by-component hypothesis verdict with separate confidence grades, because the broad “fun match” claim is composite rather than a single testable statistic.

Statistical tests describe the match’s observable scoring and process profile. They cannot prove private player motivation or intent.

## Reproduction notes

The notebook was executed top-to-bottom successfully before publication. To rerun the analysis, use a Python environment with pandas, NumPy, SciPy, scikit-learn, matplotlib, PyMuPDF, and nbclient installed, then run:

```powershell
python scripts/build_player_effort_data.py
python scripts/build_contact_discipline_data.py
python scripts/build_v2_notebook.py
python scripts/execute_notebook.py
python scripts/build_narrative_effort_control_image.py
```

The compact processed player and contact/discipline CSVs are included, so the first two commands are only needed to refresh them. The extraction scripts fetch missing official FIFA reports in memory.

The international-results source is tracked as a submodule at the pinned commit listed in `data/source_manifest_v2.json`. The team-strength and World Cup-history inputs are external source snapshots from the sibling `Argentina Comeback Analysis` project; their repositories and pinned commits are recorded in the manifest.

## Data and provenance

The project combines public international match results, soccer Elo ratings, World Cup history, FIFA Post-Match Summary Reports, player physical and event tables from 15 official reports, foul/card/contact data from **103 official Full Time Match Reports**, a current-match goal timeline, manually transcribed starting lineups, timestamped player-award evidence, a 41-match scoring benchmark, and a 22-match exhibition-intensity file with 19 complete common-core rows. Cross-provider definitions remain a documented limitation.

See `data/source_manifest_v2.json` for source URLs, pinned commits, coverage, and known limitations.
