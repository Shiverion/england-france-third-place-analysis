# England 6–4 France: deeper third-place-match analysis

Analysis date: 19 July 2026  
Primary notebook: `output/jupyter-notebook/england_france_2026_third_place_analysis_v2.ipynb`

Statistical tests, evidence definitions, assumptions, and reproducibility notes: [statistical evidence and methods appendix](statistical_evidence_methods_v2.md)

## Executive conclusion

England–France was not statistically similar to an ordinary elite friendly, and “the teams did not try to defend” is too simple.

The stronger evidence supports a more precise description:

> **A lower-stakes, heavily rotated official match played with extreme attacking risk, aggressive pressing, and unusually weak defensive control. Its openness looked exhibition-like, but its effort profile did not look passive.**

Both countries changed seven starters from their semi-finals. The match then produced more goals, expected goals, and shots on target than any of the first 102 matches of the 2026 World Cup. At the same time, FIFA recorded an exceptionally high number of direct pressures but exceptionally few forced turnovers relative to those pressures. That combination indicates failed or poorly protected pressure—not an absence of defensive activity.

The 4–0 score state materially opened the second half, but historical World Cup rates suggest it increased the expected total only from about 2.45 to 3.30 goals. Ten goals remain extreme after accounting for the path of the score.

## Visual story for general audiences

These three illustrated explainers summarize the evidence without statistical jargon. The detailed charts and tests remain in the sections below.

### 1. Rotated, not relaxed

Both teams changed seven starters, showing lower selection priority. Yet the very high number of direct pressures shows that the players were still actively competing. The problem was control: those pressure attempts produced unusually few forced turnovers.

![Rotated, not relaxed: seven changes for each team, high pressing, and low control](assets/narrative_01_rotated_not_relaxed.png)

### 2. The score opened the game

The 4–0 lead encouraged risk and made the match more open. Historical scoring rates raise the expectation from 2.45 to 3.30 goals along this score path—a meaningful increase, but nowhere near the ten actually scored.

![The score opened the game but does not explain all ten goals](assets/narrative_02_score_opened_game.png)

### 3. Not an ordinary friendly

Matched elite friendlies averaged almost exactly the same number of goals as matched official games. Historical third-place matches and the charity sample were higher-scoring, but this match still sat far above every comparison.

![Ten goals compared with elite official matches, elite friendlies, World Cup third-place matches, and the charity sample](assets/narrative_03_not_ordinary_friendly.png)

## What the larger professional comparison changes

The original comparison had only 20 historical World Cup third-place matches and 15 Soccer Aid matches. Version 2 adds a professional score backbone and constructs a primary sample of **173 neutral matched pairs** from 1991–2023.

Every pair contains:

- One senior men's professional friendly.
- One official tournament match.
- Two teams ranked in the prior-year top 30.
- A prior-year Elo difference of no more than 200 points.
- Matching on year, average Elo, and Elo gap, with neutral venue held exact.

After matching, every covariate had an absolute standardized mean difference below 0.05, comfortably inside the conventional 0.10 balance boundary.

![Matching balance](assets/v2_matching_balance.png)

### Primary result

| Metric | Professional friendly | Official tournament |
|---|---:|---:|
| Matched matches | 173 | 173 |
| Average total goals | 2.45 | 2.49 |
| Five-plus-goal rate | 12.1% | 8.7% |
| Maximum total goals | 7 | 7 |

The paired mean difference was **−0.04 goals per match** for friendly minus official:

- Bootstrap 95% CI: **−0.35 to +0.27**
- Paired sign-flip permutation test: **p = 0.824**
- Exact paired test for the five-plus threshold: **p = 0.345**

This does not show that the contexts are identical. It shows that the data rule out a large, general “elite friendlies become goal festivals” effect. England–France's ten goals were above every score in both matched groups.

![Matched goal distributions](assets/v2_matched_goal_distribution.png)

The conclusion was stable when eligibility was tightened to prior-year top 10, top 15, and top 20 teams. Those smaller samples produced uncertain estimates on both sides of zero. A separate 539-pair friendly-versus-qualifier design estimated **+0.15 goals** for friendlies, but its CI still crossed zero (**−0.04 to +0.35; p = 0.127**).

### Predictive interpretation

A smoothed count model estimated the probability of at least ten goals as:

- **0.027%** in matched official tournament matches.
- **0.076%** in matched professional friendlies.
- **0.114%** in the first 102 matches of the 2026 World Cup.
- **3.69%** in the small Soccer Aid benchmark.

The friendly estimate is about 2.8 times the matched official estimate, but both are below one-tenth of one percent. Therefore, ten goals are slightly more compatible with the friendly model in relative terms while remaining far outside an ordinary elite-friendly range in absolute terms.

The all-era World Cup tail estimates are sensitive to old, high-variance matches and extra time; they are historical context, not the primary classification result.

![Ten-goal tail probabilities](assets/v2_predictive_tail.png)

## Selection evidence: both teams rotated heavily

Official FIFA team-summary pages show that both teams retained only four semi-final starters.

| Team | Semi-final starters retained | Starter changes | Retained players |
|---|---:|---:|---|
| France | 4 | 7 | Adrien Rabiot, Kylian Mbappe, Michael Olise, Mike Maignan |
| England | 4 | 7 | Declan Rice, Djed Spence, Marc Guehi, Morgan Rogers |

Seven changes each are strong evidence that the bronze match had lower selection priority than the semi-finals. Rotation can represent fatigue management, squad reward, experimentation, or reduced consequence. It does not prove that the selected players lacked competitive intent.

## Official FIFA process evidence

The strongest process comparison uses the same provider and metric definitions: official FIFA Post-Match Summary Reports for matches 1–103.

| Match-103 metric | England–France | Earlier median | Earlier maximum | Percentile vs matches 1–102 |
|---|---:|---:|---:|---:|
| Goals | 10 | 3 | 8 | 100th |
| Total xG | 5.33 | 2.45 | 4.57 | 100th |
| Attempts | 38 | 24 | 41 | 95th |
| Shots on target | 20 | 8 | 18 | 100th |
| Completed line breaks | 221 | 183 | 252 | 91st |
| Defensive pressures | 558 | 521 | 704 | 68th |
| Direct pressures | 119 | 88 | 124 | 98th |
| Forced turnovers | 62 | 83 | 109 | 5th |
| Turnovers per 100 pressures | 11.1 | 15.6 | 27.8 | Below all earlier matches |

![FIFA process and lineup rotation](assets/v2_fifa_process_and_rotation.png)

### What this means tactically

The teams were not standing off and allowing attacks without resistance:

- Direct pressures were at the **98th percentile**.
- The direct-pressure share was at the **91st percentile**.
- France applied 335 pressures compared with its prior-tournament average of approximately 234 pressures per match.

But those actions did not restore control:

- Forced turnovers were at only the **5th percentile**.
- The derived turnover yield was lower than all 102 earlier matches.
- Completed line breaks were at the **91st percentile**.
- Total xG and shots on target set tournament highs.

The most defensible interpretation is **active but ineffective defending**: aggressive pressure attempts, inadequate protection around those attempts, and repeated access through or beyond the defensive structure.

This ratio is a derived analytical proxy, not an official FIFA “pressing efficiency” statistic. A forced turnover is not mechanically attributable to one specific pressure.

## How much did the 4–0 score state matter?

The score-state analysis uses regulation-time goal events from 964 men's World Cup matches through 2022.

Historical scoring accelerated as the existing lead increased:

| Absolute lead at start of minute | Historical goals per 90 match-minutes |
|---|---:|
| Level | 2.36 |
| One goal | 2.76 |
| Two goals | 3.55 |
| Three or more | 4.71 |

Applying those rates to England–France gives:

| Scenario | Expected/observed goals | Match-cluster bootstrap 95% CI |
|---|---:|---:|
| Match remains level throughout | 2.45 | 2.30–2.61 |
| Actual England–France score-state path | 3.30 | 3.01–3.62 |
| Actual result | 10.00 | Not an estimate |

The evolving score therefore raised the historical expectation by approximately **0.85 goals, or 34%**. It explains part of the openness, especially France's need to chase, but not the scale of the final score. This is an associative decomposition: large leads also occur more often in team-strength mismatches, so the difference should not be read as a purely causal score-state effect.

![Score-state decomposition](assets/v2_score_state_decomposition.png)

Further historical context:

- Four or more first-half goals occurred in **42 of 964 matches (4.36%)**.
- Six or more second-half goals occurred in **7 of 964 (0.73%)**.
- Ten or more regulation-time goals occurred in **4 of 964 (0.41%)**.

The match was already unusually open by half-time, before the entire second-half chase could explain the spectacle.

## Role of the charity comparison

Soccer Aid averaged 5.13 goals across 15 saved matches and had a previous maximum of nine. England–France exceeded all of them.

This remains useful as a face-validity anchor: the bronze match reached an exhibition-like scoring level. It is not evidence that the football itself was equivalent. Soccer Aid combines celebrities and former professionals, uses different roster construction, and has different incentives. Adding more unrelated charity games would improve the precision of the charity average but would not fix that validity problem.

## Final evidence scorecard

| Claim | Assessment |
|---|---|
| The match had lower selection priority than the semi-finals | **Supported** |
| Elite friendlies normally score much more than official tournament matches | **Not supported** |
| The scoreline was exhibition-like | **Supported descriptively** |
| The teams made no defensive effort | **Contradicted by pressure activity** |
| Defensive control was exceptionally poor | **Supported** |
| The 4–0 game state explains all ten goals | **Contradicted** |
| The match fits an ordinary elite friendly | **Not supported** |

## Confidence assessment

**Overall status: share with caveats.**

- **High confidence:** score, lineup rotation, official FIFA process metrics, and the match's 2026 percentile positions.
- **Moderate confidence:** matched professional score comparison and historical score-state decomposition.
- **Low confidence:** any statement about private player motivation or exact equivalence to charity football.

The most important remaining data gap is a same-provider event dataset for elite professional friendlies. That would allow pressure, transition, line-break, and defensive-structure classification across contexts—not merely score comparisons. Other competitions' placement matches also require a reliable stage-labelled source before hierarchical pooling is defensible.

## Source notes

- [FIFA match-103 Post-Match Summary Report](https://www.fifatrainingcentre.com/media/native/tournaments/fifa-world-cup/2026/PMSR-M103-FRA-V-ENG.pdf)
- [Mart Jürisoo international-results repository](https://github.com/martj42/international_results), pinned locally at commit `80f408d2c93ba4f9e06a2c7cdc5effb05fea9680`
- [JGravier soccer-Elo repository](https://github.com/JGravier/soccer-elo), pinned sibling data at commit `a24d031e0ed81cbb4206ff84a2209bbf000ee6d6`
- [Fjelstul World Cup Database](https://github.com/jfjelstul/worldcup), pinned sibling data at commit `35a8667f518b07469182ae16d35574dd0e7a00fb`
- Source paths, coverage rules, and known gaps are recorded in `data/source_manifest_v2.json`.
