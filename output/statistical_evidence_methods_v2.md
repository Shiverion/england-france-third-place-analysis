# England–France 6–4: statistical tests, evidence, and method

Analysis date: 19 July 2026  
Primary notebook: `jupyter-notebook/england_france_2026_third_place_analysis_v2.ipynb`

![How we tested the claim](assets/narrative_04_how_we_tested_claim.png)

## What this analysis can and cannot prove

The analysis cannot observe private motivation. No statistical test can prove that players were “having fun,” “not trying,” or deliberately stopped defending.

What it can test is whether the match looked different from carefully chosen serious-match comparisons, whether the scoreline was unusually extreme, and whether the match process showed effort or defensive activity.

The evidence supports this stronger wording:

> **England–France showed a spectacle-first tendency: normal contact and high physical activity coexisted with tournament-leading attack, zero cards, and unusually weak defensive conversion. This supports exhibition-like incentive alignment, not a pre-arranged-score claim.**

## Hypothesis and decision rule

The hypothesis being examined is deliberately stated as a composite:

```text
H1: Compared with serious official matches, the third-place match behaved
    like a low-pressure fun/charity match: less effort and defending,
    more open scoring, and selective individual stat-seeking.

H2: Live Golden Boot, assist, and record incentives influenced selection
    and attacking involvement, giving specific players an opportunity to
    boost personal statistics.

H3: Visible action remained high while the usual collective controls and
    disciplinary consequences weakened: a spectacle-first behavioural
    tendency rather than simple low physical effort.

H4: Across the shared observable metrics, Match 103 was closer to the
    exhibition-match distribution than to the ordinary official-match
    distribution, even when goals were excluded.
```

The competing explanation is that the match had lower team-level stakes and heavy rotation, but physical effort remained; attacking risk, weak coordination, score-state effects, individual incentives, and finishing produced the open score.

There is no single binary test for H1 because it combines selection, physical effort, defensive control, scoring, and private motive. The analysis therefore evaluates components separately:

| Component | Decision rule | Result |
|---|---|---|
| Lower team stakes | Rotation and starter retention | Supported with high confidence |
| Exhibition-like scoring | Historical and matched professional comparisons | Supported descriptively with moderate confidence |
| Broad coasting/no defending | Player effort tests plus same-team ranks | Not supported with moderate confidence |
| Lower contact intensity | Fouls, tackles, blocks, pressures, and high-intensity distance | Not supported with moderate-high confidence |
| Lower disciplinary intensity | Card events conditional on tournament phase, foul band, duration, and referee | Suggestive with low-moderate confidence |
| Defensive control | Pressure-to-turnover conversion and opponent access | Supported with moderate-high confidence |
| H3 spectacle-first tendency | Directional stack across attack, activity, discipline, control, rotation, and incentives | Supported with moderate-high confidence |
| H4 exhibition-profile | 102 official matches vs all 19 complete exhibition matches; strict holdout classifier excluding goals | Supported with moderate-high confidence |
| Individual stat-seeking | Award mechanism plus candidate activity | Supported as incentive/opportunity; intentional attribution suggestive |
| H2 stronger claim: the match was primarily used to boost statistics | Intentional stat-padding or private motive | Not established; low confidence |
| Charity equivalence | Like-for-like roster/rule comparison | Not established; low confidence |

**Overall verdict:** literal H1 is partially supported because broad physical coasting is contradicted. **H3 and H4 are supported with moderate-high confidence.** The lower-stakes, exhibition-profile, and spectacle-first parts fit the evidence. Coordinated pre-arrangement remains outside what match statistics can identify.

## Plain-language guide to the statistics

- **Mean difference:** how many more goals one setting produced on average. Here, “friendly minus official.”
- **95% confidence interval:** a reasonable uncertainty range around the estimated difference. If it crosses zero, the data are compatible with either side of zero.
- **p-value:** how surprising the observed difference would be if there were no systematic difference between the settings. A large p-value is not proof that the settings are identical; it means the data do not provide strong evidence of a difference.
- **Matched pair:** a friendly and an official match made comparable on team strength, year, neutral venue, and Elo gap. Matching reduces obvious apples-to-oranges bias.
- **Percentile:** where the current match sits relative to the first 102 matches of the same World Cup using the same FIFA report definitions.
- **Holm adjustment:** a correction used when several related outcomes are tested. It raises p-values enough to control the chance of at least one false positive across the family of tests.
- **Empirical tail check:** the current player's rate is ranked against his own earlier matches. With only six or seven earlier appearances, the resulting p-values are necessarily coarse.
- **xG/Poisson check:** a rough calculation of how often a Poisson process with mean equal to aggregate expected goals would score at least the observed number. It is an approximation, not an exact shot-level model.
- **Add-one empirical lower tail:** `(1 + prior matches no higher than observed) / (1 + prior matches)`. It avoids claiming a zero probability when the reference sample is finite.
- **Negative-binomial zero check:** a predictive probability of zero card events that allows card counts to vary more than a Poisson model would permit.
- **Mann–Whitney test:** a rank-based two-sample test asking whether values from one population tend to be higher or lower than values from the other without assuming normality.
- **Cliff's delta:** an effect size from −1 to +1. Positive values mean a random exhibition match is more likely to have a higher value than a random official match; negative values mean lower.
- **Holm correction:** the five common-metric p-values are adjusted together to control the chance of at least one false positive in that test family.
- **AUC:** how often the classifier ranks a randomly selected exhibition match above a randomly selected official match. AUC 0.5 is chance; 1.0 is perfect separation.
- **Exhibition-likeness diagnostic score:** the class-balanced model's output on a 0–1 scale. It is useful for relative profile similarity but is not a real-world probability that the match was fixed, unserious, or intentionally manipulated.

## 1. Primary professional comparison

### Question

Do elite professional friendlies generally produce more goals than serious official tournament matches?

### Design

The primary sample contains **173 matched pairs** from 1991–2023. Each pair contains:

- one senior men's professional friendly;
- one official tournament match;
- neutral venue in both matches;
- teams in the prior-year top 30;
- prior-year Elo difference of no more than 200 points;
- matching on year, average Elo, and Elo gap.

After matching, every recorded covariate had an absolute standardized mean difference below 0.05. The conventional balance warning line is 0.10.

### Test A: paired bootstrap for the mean goal difference

For every pair, the analysis calculated:

```text
goal difference = friendly goals − official goals
```

It then resampled the 173 paired differences with replacement **20,000 times**. The 2.5th and 97.5th percentiles formed the bootstrap 95% interval.

| Result | Value |
|---|---:|
| Friendly average | 2.4509 goals |
| Official average | 2.4913 goals |
| Friendly minus official | −0.0405 goals |
| Bootstrap 95% interval | −0.3526 to +0.2659 |

The estimate is effectively zero relative to the uncertainty. The interval does not support a large general “friendlies become goal festivals” effect.

### Test B: paired sign-flip permutation test

The null hypothesis is that there is no systematic friendly-versus-official difference within matched pairs. Under that null, each pair’s difference can be randomly left as-is or have its sign flipped. The analysis performed **20,000 random sign-flip draws** and calculated a two-sided p-value.

**Result: p = 0.824.**

Interpretation: a difference at least as extreme as −0.04 goals is very unsurprising if the two contexts have no general scoring difference. We do not reject the no-difference hypothesis.

This is not the same as proving that friendlies and official matches are identical. The interval still allows a modest difference in either direction.

## 2. Five-plus-goal threshold test

### Question

Are friendlies more likely to become high-scoring matches, even if their average goal totals are similar?

The matched results were converted into a simple indicator: total goals were either **5 or more** or **below 5**.

| Context | 5+ goal rate |
|---|---:|
| Professional friendlies | 12.1% |
| Official tournament matches | 8.7% |

Because the observations are paired, the analysis used an exact paired **McNemar-style binomial test**. It only counts pairs where one context crosses the threshold and the other does not; pairs where both are high-scoring or both are not do not create directional evidence.

**Result: p = 0.345.**

The friendly rate is descriptively higher, but the paired threshold evidence is not strong enough to rule out ordinary sampling variation.

## 3. Design sensitivity checks

The result should not depend on one arbitrary definition of “elite.” The notebook repeated the primary design using prior-year top-10, top-15, and top-20 teams, plus a larger friendly-versus-qualifier design.

| Design | Pairs | Friendly − official | 95% interval | p-value |
|---|---:|---:|---:|---:|
| Neutral, top 10 | 23 | +0.30 | −0.39 to +1.00 | .472 |
| Neutral, top 15 | 55 | +0.00 | −0.49 to +0.49 | 1.000 |
| Neutral, top 20 | 86 | +0.08 | −0.31 to +0.48 | .726 |
| Neutral, top 30 | 173 | −0.04 | −0.36 to +0.27 | .825 |
| Top 30 friendly vs qualifier | 539 | +0.15 | −0.04 to +0.35 | .127 |

The point estimates move around because the tighter samples are small, but every interval includes zero. The larger design is more precise and still does not establish a statistically reliable friendly scoring advantage.

## 4. How rare was ten goals?

The notebook fitted smoothed count models to estimate the probability of reaching at least ten total goals. These are model-based tail probabilities, not direct frequencies and not substitutes for the paired tests.

| Context | Matches | Average goals | Highest saved score | Smoothed P(total ≥ 10) |
|---|---:|---:|---:|---:|
| Matched official tournaments | 173 | 2.49 | 7 | 0.027% |
| Matched professional friendlies | 173 | 2.45 | 7 | 0.076% |
| 2026 World Cup matches 1–102 | 102 | 2.91 | 8 | 0.114% |
| World Cup third-place matches, all eras | 20 | 3.80 | 9 | 0.617% |
| Soccer Aid charity sample | 15 | 5.13 | 9 | 3.69% |
| Expanded charity/exhibition benchmark | 41 | 7.15 | 20 | 25.82% |

England–France scored **10**, exceeding every saved match in the matched professional groups and every saved Soccer Aid match. It did not exceed every row in the expanded benchmark: creator-led formats reached 10–20 regulation-time goals. The expanded modelled tail is therefore much less useful as a single population estimate because the rows mix different event formats.

The charity comparison is useful as a descriptive exhibition-like anchor, but it is not a valid causal control group: it has different rosters, incentives, player experience, substitutions, and match conditions.

### Expanded exhibition benchmark sensitivity

To address the original Soccer Aid sample-size limitation, the notebook adds 26 documented matches from Corazón Classic Match, Match for Hope, Sidemen Charity Match, Football for Hope, Game4Ukraine, and a Manchester United/Pompey legends benefit. Combined with Soccer Aid, the benchmark contains **41 regulation-score matches**.

| Event group | Matches | Mean goals | 95% bootstrap interval | Maximum |
|---|---:|---:|---:|---:|
| Soccer Aid | 15 | 5.13 | 4.20–6.20 | 9 |
| Corazón Classic | 13 | 5.08 | 3.77–6.54 | 11 |
| Match for Hope | 3 | 12.67 | 11.00–15.00 | 15 |
| Sidemen Charity | 7 | 12.14 | 7.71–16.29 | 20 |
| Other benefit events | 3 | 9.00 | 4.00–14.00 | 14 |
| All expanded events | 41 | 7.15 | 5.83–8.61 | 20 |

The current ten-goal match is above all 15 Soccer Aid rows, but **9 of 41** expanded matches reached at least ten goals. With the small-sample +1 correction, the descriptive upper-tail rate is **6.25%** for Soccer Aid alone and **23.81%** for the expanded benchmark. This is not a formal p-value: the expanded rows are not a random sample from one well-defined population, and several event series have only three to thirteen observations.

The correct interpretation is therefore stratified. The added data strengthen the claim that England–France reached an exhibition-like scoring environment, while weakening the claim that it was specifically equivalent to Soccer Aid or to all charity football. The professional matched sample remains the primary serious-versus-friendly comparison.

## 4A. Formal two-population intensity test

### Why the earlier design was incomplete

Comparing Match 103 with 102 earlier World Cup matches establishes that it was unusual for an official match. It does **not** establish that it resembled exhibition football. That requires two labeled reference distributions.

The corrected design uses:

- **102 official World Cup matches** completed before Match 103;
- **19 exhibition matches** with complete common-core metrics: all 15 Soccer Aid editions and four Sidemen Charity Matches;
- **one strict holdout:** England–France, excluded from every training and validation fold.

The source file contains 22 exhibition rows in total. Three older Sidemen matches have documented scores but not the complete intensity core; they remain in the scoring benchmark and are excluded from this model by a pre-declared completeness rule.

### Common metrics and descriptive separation

| Metric | Official median (n=102) | Exhibition median (n=19) | Match 103 | Cliff's delta | Holm-adjusted p |
|---|---:|---:|---:|---:|---:|
| Goals | 3.0 | 6.0 | 10 | +0.674 | 5.12×10⁻⁶ |
| Total shots | 24.0 | 39.0 | 38 | +0.861 | 1.11×10⁻⁸ |
| Shots on target | 8.0 | 17.0 | 20 | +0.878 | 6.04×10⁻⁹ |
| Fouls | 22.5 | 13.0 | 22 | −0.671 | 5.12×10⁻⁶ |
| Yellow cards | 2.5 | 1.0 | 0 | −0.707 | 2.14×10⁻⁶ |

All five population differences remain below 0.05 after Holm correction. The signs are coherent: exhibition matches produce more attacking volume and output, but fewer fouls and cards. These p-values test the **two reference populations**; they are not p-values for the single target match.

Match 103 combines the classes rather than copying either one perfectly. Its 22 fouls sit at the official median, while 38 shots, 20 shots on target, and zero yellow cards sit on the exhibition side. This is the statistical form of the “not contactless—brakeless” interpretation.

### Primary classifier: goals deliberately excluded

The pre-specified primary classifier uses only:

```text
total shots + shots on target + total fouls + yellow cards
```

The pipeline standardizes the four features and fits a class-balanced logistic regression with fixed regularization `C=1`. Class weighting prevents the 102-to-19 sample imbalance from making “official” the automatic answer. No feature selection or threshold tuning uses Match 103.

Validation repeats stratified five-fold cross-validation **50 times**. In each repeat, every labeled match receives a prediction from a model that did not train on it. The model is then fitted once to all 121 labeled rows and applied to the untouched target.

| Result | Value |
|---|---:|
| Repeated-CV AUC | 0.958 |
| Repeated-CV balanced accuracy | 0.887 |
| Repeated-CV Brier score | 0.087 |
| Match-103 exhibition-likeness score | 0.980 |
| Match-bootstrap 95% interval | 0.876–0.996 |

The key result is that the model reaches this conclusion **without seeing total goals**. Adding goals raises the target score only slightly, to about 0.990. A rate-based sensitivity model using shot accuracy and cards per ten fouls gives about 0.969.

### Event-family sensitivity

The exhibition class contains two formats with different scoring geometry. The primary model was therefore refitted twice, each time retaining all 102 official rows but using only one exhibition family:

| Exhibition family used | Complete matches | Match-103 score |
|---|---:|---:|
| Soccer Aid only | 15 | 0.989 |
| Sidemen Charity only | 4 | 0.612 |

The Sidemen-only score is lower because those four matches are exceptionally extreme—13 to 20 goals and 23 to 39 shots on target—so England–France is less similar to that creator-led format. The result stays above 0.5, but the wide **0.61–0.99** family range is why confidence is graded moderate-high rather than “near certain.”

### Decision

**H4 is supported with moderate-high confidence as an observable-profile claim.** England–France was not merely a goal outlier. Its non-goal attacking and disciplinary pattern falls on the exhibition side of a classifier that separates the two labeled populations well.

This does not identify intent. FIFA supplies the official-match metrics while FotMob supplies the exhibition metrics, so provider definitions may contribute some separation. Roster quality, substitutions, match format, and event incentives also differ. The score is therefore a diagnostic similarity index—not a posterior probability of fixing, coordination, or deliberate stat-padding.

## 5. Score-state analysis

### Question

Could an early 4–0 lead explain why the match became so open?

The analysis used **964 regulation-time World Cup matches through 2022**. For each minute, it recorded the absolute score gap at the start of that minute and estimated historical goals per 90 minutes:

| Score state | Historical goals per 90 |
|---|---:|
| Level | 2.36 |
| One-goal gap | 2.76 |
| Two-goal gap | 3.55 |
| Three-plus gap | 4.71 |

Those rates were applied to two counterfactual paths:

- **Level-state path:** expected 2.452 goals.
- **Actual England–France score-state path:** expected 3.297 goals, with a match-cluster bootstrap interval of 3.011–3.618.
- **Observed result:** 10 goals.

The score path raised expected scoring by approximately **0.85 goals, or 34%**, but it did not explain the scale of the final score.

The notebook used **5,000 match-cluster bootstrap resamples**, so whole historical matches—not individual minutes—were resampled together.

Important limitation: score state is endogenous. A big lead is related to team strength, matchups, and the events that already happened. This is an explanatory decomposition, not a causal experiment saying that the 4–0 score independently caused exactly 0.85 extra goals.

## 6. FIFA process evidence: effort versus control

The process comparison uses the same FIFA Post-Match Summary Report format for World Cup matches 1–103. Match 103 is England–France; matches 1–102 are the reference distribution.

| Metric | England–France | Position among matches 1–102 |
|---|---:|---:|
| Goals | 10 | 100th percentile |
| Total xG | 5.33 | 100th percentile |
| Attempts | 38 | 95th percentile |
| Shots on target | 20 | 100th percentile |
| Completed line breaks | 221 | 91st percentile |
| Direct pressures | 119 | 98th percentile |
| Forced turnovers | 62 | 5th percentile |
| Forced turnovers per 100 pressures | 11.1 | Below all earlier matches |

This is not a formal hypothesis test because the FIFA process sample is a single current match compared with a tournament reference distribution. It is strong descriptive evidence of the pattern:

- very active attacking and pressure attempts;
- unusually poor conversion of pressure into forced turnovers;
- unusually high access, chance creation, and defensive instability.

That pattern is more consistent with **active but ineffective defending** than with “nobody tried.”

## 7. Contact and disciplinary-intensity test

### Source and grain

`scripts/build_contact_discipline_data.py` fetches official FIFA Full Time Match Reports in memory for asset ids `r12449` through `r12551`, then parses the match number from each report. The resulting files contain:

- **103 match rows**, exactly matches 1–103;
- **206 team-match rows**, exactly two per match;
- fouls, cards, free kicks, penalties, offsides, referee, possession, attempts, and shots on target;
- official report URL and asset id on every row.

FIFA labels the committed-foul field “Fouls Against.” The parser uses it as `fouls_committed`; opponent-team reconciliation confirms that it equals the opposing row's fouls suffered in all 206 rows. Final-score totals reconcile with the independent PMSR panel in 103 of 103 matches.

`card_events` is the sum of single-yellow cards, second-yellow red events, and direct-red events. It counts disciplinary sanctions, not FIFA fair-play penalty points. Match 103 had no cards of any type, so alternate weighting does not change its result.

### Primary observable pattern

| Metric | Match 103 | Earlier 90-minute mean | Earlier 90-minute knockout mean |
|---|---:|---:|---:|
| Total fouls | 22 | 22.394 | 22.636 |
| Card events | 0 | 2.787 | 3.273 |
| Card events per 10 fouls | 0.000 | 1.249 | 1.426 |

This directly rejects **H3a: contact broadly disappeared**. Fouls were normal, and the separate player-event panel shows more tackles, blocks, and pressure attempts.

### One-sided cardless tests

The pre-specified lower-tail statistic is:

```text
p_empirical = (1 + count(reference card events <= 0)) / (1 + reference matches)
```

The add-one term prevents a finite reference from returning zero. The test is one-sided because H3 specifically predicts lower disciplinary consequence.

| Reference | n | Zero-card matches | Add-one empirical p | Method-of-moments NB P(0) |
|---|---:|---:|---:|---:|
| All first 102 | 102 | 9 | 0.097 | 0.081 |
| Regulation-only first 102 | 94 | 9 | 0.105 | 0.082 |
| All earlier knockout matches | 30 | 1 | 0.065 | 0.062 |
| Regulation-only knockout matches | 22 | 1 | 0.087 | 0.064 |
| Regulation matches within ±3 fouls | 42 | 5 | 0.140 | 0.082 |
| Same referee's earlier matches | 3 | 0 | 0.250 | Not estimated |

No empirical result crosses 0.05. The correct formal judgment is **suggestive, not conventionally significant**. The knockout references provide the strongest signal, while foul-band and same-referee checks show that contact volume and referee style weaken it. The negative-binomial checks return roughly 6% probability of zero cards in knockout references, but they are predictive model checks rather than causal tests.

### Defensive action versus defensive control

Player events are summed to the team-match grain, divided by match duration, and multiplied by 90. Match 103 for France and England is compared with each team's own previous-seven-match mean; the two current values and two baseline means are then summed before calculating the percentage change.

Activity metrics were specified as tackles attempted, blocks, direct pressures, high-intensity distance, and sprints. Outcome/control metrics were tackles won, interceptions, aerial and physical duels won, possession contests won, clearances, possession regains, and possession interrupted. Reporting the full set prevents selection of only metrics that fit the narrative.

The critical counterexample is **tackles won, +53%**. It demonstrates genuine reactive defending. Yet interceptions fell 25%, aerial duels won 53%, possession contests won 53%, and clearances 65%. The evidence therefore supports **high activity with weak anticipatory and collective control**, not universal defensive failure on every action.

### H3 decision rule

H3 is not accepted because one card p-value crosses an arbitrary threshold; none does. It is graded from a multi-layer directional stack:

1. Goals, xG, and shots on target were tournament highs.
2. Direct pressures and fast running were high.
3. Total fouls were normal, rejecting low contact.
4. Card consequence was unusually low, though only suggestive after sensitivities.
5. Pressure yield was below all 102 earlier matches.
6. Clearance, aerial-duel, and possession-contest outcomes collapsed versus both teams' own baselines.
7. Team-level stakes fell while individual attacking rewards remained live.

These components are correlated, so their p-values are **not combined with Fisher's method or treated as independent experiments**. The verdict is a structured evidence judgment: **spectacle-first tendency supported with moderate-high confidence; coordinated pre-arrangement not tested**.

## 8. Player-level effort-versus-control test

### Question

Did the selected players reduce physical effort, or did substantial effort fail to produce collective defensive control?

### Source and extraction

The parser in `scripts/build_player_effort_data.py` reads official FIFA Post-Match Summary Reports for all 15 matches needed to cover France's eight and England's eight tournament appearances; Match 103 is shared. It extracts player physical data, direct pressure, attempts, offers in behind, lineup position, and minutes. Reports already saved in `data/fifa` are read locally; missing reports are fetched in memory. Compact processed rows retain the official report URL.

The parser validates:

- one unique row per match, team, and shirt number;
- eight matches for each focal team;
- total player minutes equal to 11 on-field slots for all 16 team-matches; and
- team goals, attempts, and direct-pressure totals against independently extracted FIFA team-summary values.

One PDF-layout exception is documented. Ousmane Dembele's Match-61 row used all visible event slots for three goals, hiding his substitution minute. FIFA's official match article states that he left in the 65th minute, so that minute is supplied as an explicit source-linked override.

### Eligibility and estimand

The analysis excludes goalkeepers and includes a Match-103 player only when he played at least 45 minutes, had at least two earlier appearances of 15 or more minutes, and accumulated at least 90 earlier minutes. Nineteen outfielders meet those rules.

For each metric and player:

```text
current rate = Match-103 count or distance / Match-103 minutes × 90
prior rate   = pooled earlier count or distance / pooled earlier minutes × 90
difference   = current rate − prior rate
```

The target is the mean within-player difference among these 19 eligible players. This avoids comparing a rotated lineup with a different set of players.

### Uncertainty and test

- **Bootstrap interval:** resample the 19 player differences with replacement 20,000 times; use the 2.5th and 97.5th percentiles.
- **Sign-flip test:** independently multiply each difference by +1 or −1 under a zero-centered null, calculate 100,000 simulated mean differences, and report the two-sided tail proportion.
- **Multiple outcomes:** apply Holm correction across total distance, high-intensity distance, sprints, and direct pressures.

| Metric per player-90 | Mean change | Bootstrap 95% CI | Raw sign-flip p | Holm p |
|---|---:|---:|---:|---:|
| Total distance | −333.6 m (−3.2%) | −680.7 to +27.0 m | 0.089 | 0.179 |
| Distance at 20+ km/h | +92.2 m (+12.0%) | +8.7 to +175.7 m | 0.050 | 0.150 |
| Sprints | +0.84 (+2.0%) | −3.63 to +5.42 | 0.727 | 0.727 |
| Direct pressures | +2.32 (+63.2%) | +0.45 to +4.36 | 0.035 | 0.141 |

The raw results suggest more explosive work and more pressure activity, but no p-value remains below 0.05 after Holm adjustment. The appropriate judgment is **exploratory evidence against broad coasting**, strengthened by the descriptive team ranks: France ranked second of eight for high-intensity distance and first for direct pressures but last for turnover yield; both teams conceded their highest opponent xG.

### Dependence and interpretation limit

The 19 rows are not fully independent: teammates share tactics, opposition, substitutions, and score state. With only two team clusters, a cluster-robust player test would not be credible. The analysis therefore reports raw and multiplicity-adjusted values, calls the tests exploratory, and uses same-team match ranks as triangulation. The test does not estimate a causal effect of “lower stakes.”

## 9. Candidate behavior and finishing checks

### Candidate behavior

For Mbappe, Olise, Saka, Bellingham, and Kane, the notebook compares Match-103 attempts, offers in behind, direct pressure, and high-intensity distance with each player's earlier per-90 rates. It also reports current and earlier team shot shares.

The empirical one-sided p-value is:

```text
(1 + number of earlier match-rates at least as high as Match 103) / (1 + earlier matches)
```

The added 1 prevents a zero estimate. It also exposes the power limit: with seven earlier matches the smallest possible value is 1/8 = 0.125; with six it is 1/7 = 0.143. Mbappe's attempt p-value is 0.25 because an earlier match matched his per-90 rate. Olise's in-behind offers and direct pressures each return 0.125. Saka's raw count was his highest, but one shorter earlier appearance had a higher per-90 rate, giving p=0.286. These are descriptive behavioral signals, not confirmatory tests of motive. Bellingham's 11-minute rate is explicitly marked unstable, and Kane did not appear.

### Finishing decomposition

The official report gives aggregate xG but not shot-level probabilities. The notebook therefore uses a simple conditional approximation:

```text
Goals | aggregate xG ~ Poisson(aggregate xG)
```

| Scope | xG | Goals | Goals above xG | One-sided Poisson tail |
|---|---:|---:|---:|---:|
| France | 2.99 | 4 | +1.01 | P(4+) = 0.351 |
| England | 2.34 | 6 | +3.66 | P(6+) = 0.032 |
| Combined | 5.33 | 10 | +4.67 | P(10+) = 0.045 |

This check separates chance environment from conversion: high xG shows structural openness, while goals above xG show that finishing enlarged the score. It is rough because shot outcomes can be dependent, xG is estimated, and the aggregate mean loses shot-level information. It should not be read as a test of seriousness.

## 10. Selection evidence

Official FIFA team summaries show that both countries retained only four semi-final starters and changed seven:

| Team | Semi-final starters retained | Starter changes |
|---|---:|---:|
| France | 4 | 7 |
| England | 4 | 7 |

This is strong descriptive evidence that the bronze match had lower selection priority than the semi-finals. It does not identify whether the reason was fatigue, squad rotation, experimentation, reward, or lower competitive pressure.

## 11. Individual incentive mechanism

This section evaluates **H2**: whether live individual rewards plausibly influenced selection and attacking involvement. It is not another p-value. It is a timestamped mechanism audit designed to avoid turning a plausible story into an unsupported claim. The mechanism is considered supported only when four observable links are present:

1. An individual award or record was live before kick-off.
2. The player was selected or deliberately retained despite team rotation.
3. The player added to the relevant statistic in the match.
4. The contribution materially changed the player's standing or record.

| Player | Before match | Selection evidence | Match contribution | After match |
|---|---:|---|---:|---:|
| Kylian Mbappe | 8 goals; second on tie-break | Started; retained from semi-final | +2 | 10 goals; provisional Golden Boot lead |
| Michael Olise | 5 assists; tournament leader | Started; retained from semi-final | +2 | 7 assists; extended lead |
| Jude Bellingham | 6 goals; fourth in FIFA table | Began on bench; entered at 79' | +1 | 7 goals; England single-tournament record |
| Harry Kane | 6 goals; fifth in FIFA table | Began on bench | +0 | 6 goals; no gain |

The France evidence is especially strong because Mbappe and Olise were two of only four semi-final starters retained. The England evidence limits the claim: Kane and Bellingham did not start, so individual stat accumulation was not the sole or universal selection principle.

The supported conclusion is **selective individual attacking incentives remained active while collective stakes were lower**. The evidence does not identify private motivation, prove selfish decision-making, or show that players agreed to trade defensive effort for statistics.

The distinction matters: H2's moderate version—**individual rewards were live, changed selection/involvement incentives, and created a concrete stat-boost opportunity**—is supported as a mechanism with moderate confidence. Player-specific intentional attribution remains suggestive and underpowered. The strong version—**the match was coordinated primarily to boost statistics**—is not established.

## 12. Data-quality checks

The notebook ran consistency checks before promoting results into the report:

| Check | Result |
|---|---:|
| International result rows with parseable dates | 49,520 / 49,520 |
| Unique men's World Cup match IDs | 964 / 964 |
| World Cup goal events reconcile to final scores | 964 / 964 |
| FIFA baseline has two team rows per match | 96 / 96 |
| Starter groups contain exactly 11 players | 4 / 4 |
| Current match timeline contains ten goals | 10 / 10 |
| Exhibition intensity event-year duplicates | 0 / 0 |
| Exhibition intensity source URLs present | 22 / 22 |
| Exhibition complete-core rows | 19 / 19 |
| Complete-core rows with all five shared metrics | 19 / 19 |
| Individual-incentive rows reconcile before + match = after | 4 / 4 |
| Duplicate FIFA player match/team/shirt keys | 0 / 0 |
| Focal teams cover eight matches each | 2 / 2 |
| Player minutes reconcile to 11 on-field slots | 16 / 16 |
| Parsed goals, attempts, and direct pressures reconcile to FIFA team totals | 48 / 48 |
| Full Time reports cover matches 1–103 exactly | 103 / 103 |
| Full Time report team rows | 206 / 206 |
| Fouls suffered reconcile to opponent fouls committed | 206 / 206 |
| Full Time report goals reconcile to PMSR totals | 103 / 103 |

One expected gap remains: the current match is held in a separate current-match source rather than being fully populated in the historical results backbone. The current score, timeline, FIFA process data, and lineup data are nevertheless checked separately and reconciled in the notebook.

## Final evidence judgment

| Claim | Evidence judgment |
|---|---|
| The match had lower selection priority than the semi-finals | Supported by seven changes for both teams |
| Individual attacking incentives remained meaningful | Supported selectively by pre/post award movement and France retaining Mbappe and Olise |
| Players broadly coasted physically | Not supported by high-intensity distance, pressure activity, and same-team ranks; player p-values remain exploratory after Holm correction |
| Contact intensity broadly disappeared | Contradicted by normal foul volume and higher tackles, blocks, pressures, and high-intensity distance |
| Disciplinary intensity was lower | Suggestive: zero cards, but empirical sensitivity p-values range from 0.065 to 0.250 |
| Award-candidate activity proves stat-padding | Not supported; activity is suggestive but empirical tests are underpowered and motive is unobserved |
| Individual rewards created an unusual stat-boost opportunity | Supported as an incentive/opportunity mechanism; intentional attribution remains suggestive |
| Elite friendlies are normally much more goal-heavy | Not supported by matched mean or threshold tests |
| The match looked exhibition-like in its scoring | Supported descriptively; ten goals exceeded all saved professional matches and all Soccer Aid rows, but not every expanded creator-format match |
| The non-goal common-core profile was exhibition-like (H4) | Supported with moderate-high confidence; strict-holdout score 0.980, repeated-CV AUC 0.958, and event-family sensitivity 0.612–0.989 |
| The teams made no defensive effort | Not supported; direct pressure was at the 98th percentile |
| Defensive control was unusually poor | Supported by very low forced-turnover yield and high attacking access |
| Match 103 showed a spectacle-first behavioural tendency | Supported with moderate-high confidence by the aligned attack/activity/control/discipline/incentive stack |
| Match 103 was coordinated or pre-arranged | Not established and not testable from match statistics alone |
| Chance creation alone explains all ten goals | Not supported; ten goals exceeded 5.33 xG by 4.67, with England six from 2.34 xG |
| The 4–0 state explains all ten goals | Not supported; expected scoring rose to about 3.30, not 10 |
| The match was an ordinary elite friendly | Not supported; ten goals were an extreme professional-model tail event |

## Reproducibility files

- Notebook: `output/jupyter-notebook/england_france_2026_third_place_analysis_v2.ipynb`
- Source manifest: `data/source_manifest_v2.json`
- Matched pairs: `data/processed/matched_neutral_elite_friendlies_vs_officials.csv`
- Individual incentive audit: `data/player_incentive_evidence.csv`
- FIFA player extraction script: `scripts/build_player_effort_data.py`
- FIFA foul/card extraction script: `scripts/build_contact_discipline_data.py`
- FIFA player-match extract: `data/processed/fifa_2026_france_england_player_match.csv`
- FIFA team physical extract: `data/processed/fifa_2026_france_england_team_physical.csv`
- FIFA match contact/discipline extract: `data/processed/fifa_2026_match_contact_discipline.csv`
- FIFA team contact/discipline extract: `data/processed/fifa_2026_team_contact_discipline.csv`
- Player-effort tests: `output/tables/v2_player_effort_tests.csv`
- Team effort/control ranks: `output/tables/v2_effort_control_ranks.csv`
- Candidate behavior: `output/tables/v2_candidate_behavior.csv`
- Finishing decomposition: `output/tables/v2_finishing_decomposition.csv`
- Contact/discipline summary: `output/tables/v2_contact_discipline_summary.csv`
- Contact/discipline tests: `output/tables/v2_contact_discipline_tests.csv`
- Contact/control team ranks: `output/tables/v2_contact_control_team_ranks.csv`
- Contact/control split: `output/tables/v2_contact_control_split.csv`
- Summary metrics: `output/tables/v2_summary_metrics.json`
- Evidence scorecard: `output/tables/v2_evidence_scorecard.csv`
- Hypothesis verdict table: `output/tables/v2_hypothesis_verdict.csv`
- Score-state decomposition: `output/tables/v2_score_state_decomposition.csv`
- Tail probabilities: `output/tables/v2_ten_goal_tail_probabilities.csv`
- Expanded charity/exhibition benchmark: `data/exhibition_charity_benchmark.csv`
- Expanded benchmark summary: `output/tables/v2_exhibition_benchmark_summary.csv`
- Expanded benchmark descriptive checks: `output/tables/v2_exhibition_benchmark_tests.csv`
- Exhibition intensity source: `data/exhibition_match_intensity_benchmark.csv`
- Official/exhibition common-core panel: `output/tables/v2_official_vs_exhibition_common_core.csv`
- Population summaries: `output/tables/v2_official_vs_exhibition_summary.csv`
- Mann–Whitney tests, Cliff's delta, and Holm adjustment: `output/tables/v2_official_vs_exhibition_tests.csv`
- Classifier validation: `output/tables/v2_exhibition_classifier_validation.csv`
- Match-bootstrap uncertainty summary: `output/tables/v2_exhibition_classifier_uncertainty.csv`
- Exhibition-family sensitivity: `output/tables/v2_exhibition_classifier_event_sensitivity.csv`

The notebook was executed top-to-bottom successfully before these results were documented.
