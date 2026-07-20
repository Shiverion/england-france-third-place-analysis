from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "jupyter-notebook" / "england_france_2026_third_place_analysis_v2.ipynb"


def markdown(source: str):
    return nbf.v4.new_markdown_cell(dedent(source).strip())


def code(source: str):
    return nbf.v4.new_code_cell(dedent(source).strip())


def build_notebook() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    }

    nb["cells"] = [
        markdown(
            """
            # England 6–4 France: competitive match or low-pressure spectacle?

            ## tl;dr

            This version replaces the weak charity-only comparison with several stronger layers of evidence and an expanded, stratified exhibition benchmark.

            - **Lower selection pressure is visible:** France and England each changed **7 of 11 starters** from their semi-finals.
            - **Individual stakes remained live:** France retained Kylian Mbappe and Michael Olise—its live goal and assist leaders—among only four retained starters. Mbappe moved from **8 to 10 goals**, Olise from **5 to 7 assists**, and substitute Jude Bellingham from **6 to 7 goals**.
            - **The players did not broadly coast:** among **19 comparable outfield players**, Match 103 total distance per 90 was slightly lower than their own earlier-tournament rates (**−3.2%**), but high-intensity distance was **12.0% higher** and direct pressures were **63.2% higher**. Raw exploratory p-values were approximately 0.09, 0.05, and 0.04; none remained below 0.05 after Holm correction across four effort metrics.
            - **Elite friendlies are not normally much more open:** in **173 matched neutral pairs** of elite men's internationals (1991–2023), friendlies averaged **2.45 goals** and official tournament matches averaged **2.49**. The paired difference was **−0.04 goals** (bootstrap 95% CI about **−0.35 to +0.27**; sign-flip permutation **p≈0.82**).
            - **The match process was extraordinarily open:** against the first 102 matches of the 2026 World Cup using the same official FIFA provider, England–France set new highs for **goals (10), total xG (5.33), and shots on target (20)**.
            - **“No defensive effort” is too simple:** the match was at the **98th percentile for direct pressures**, but produced only **62 forced turnovers** (about the 5th percentile). Its derived turnover yield—**11.1 per 100 pressures**—was below all 102 earlier matches.
            - **The new contact evidence reveals the sharper anomaly:** Match 103 had **22 fouls**, almost identical to the first-102 mean of **23**, but **zero cards** versus an earlier mean of **2.86**. It was only the second cardless knockout match through Match 103. The all-match empirical lower tail is **p≈0.097** and the knockout-only tail **p≈0.065**—suggestive, not conclusive by itself.
            - **The corrected all-versus-all test is much stronger:** the comparison now uses **102 official matches versus 19 exhibition matches with complete intensity data**, with Match 103 held out. A classifier using shots, shots on target, fouls, and yellow cards—but **not goals**—assigns the target an exhibition-likeness diagnostic score of about **0.98**; repeated-CV AUC is about **0.958**.
            - **Activity rose while control outcomes collapsed:** across the two teams, tackles attempted were **61% above** their own earlier-tournament baselines, direct pressures **52% above**, and high-intensity distance **16% above**. Yet clearances were **65% lower**, possession contests won **53% lower**, and aerial duels won **53% lower**.
            - **The 4–0 game state mattered but does not explain everything:** historical World Cup minute rates imply about **2.45 goals** for a level-state path and **3.30** for the score-state path actually experienced. Ten goals remain roughly three times the state-conditioned expectation.
            - **Exceptional finishing amplified exceptional openness:** ten goals came from **5.33 xG**. A rough Poisson check gives about a **4.5%** chance of at least ten goals at that expectation; England alone scored six from 2.34 xG.

            **Best verdict:** Match 103 had an **exhibition-like observable profile with moderate-high confidence**, even after goals were excluded. Players still ran, pressed, tackled, and fouled, so this was not passive football. It was a spectacle-first official match in which attacking output surged while collective control and disciplinary consequence weakened. That does not establish a pre-arranged score.
            """
        ),
        markdown(
            """
            ## Context & Methods

            The target idea—“they played it like a fun match”—is not directly observable. This notebook therefore tests an operational question:

            > Was the match's selection and observable playing behaviour more consistent with high-stakes official football, elite professional friendlies, or an exhibition-style scoring environment?

            ### Hypotheses and decision rule

            **H1 (composite fun-match hypothesis):** compared with serious official matches, the third-place match behaved like a low-pressure exhibition or charity match—lower physical and defensive effort, unusually open scoring, and selective attacking behaviour aimed at individual statistics.

            **H2 (individual-stat boost hypothesis):** live Golden Boot, assist, and record incentives influenced selection and attacking involvement, so the match gave specific players an unusual opportunity to add to their personal statistics.

            **H3 (spectacle-first tendency):** observable behaviour shifted toward maximizing visible action—shots, goals, assists, runs, and pressure attempts—rather than minimizing defeat, producing normal contact volume but unusually weak defensive conversion and disciplinary consequence.

            **H4 (exhibition-profile hypothesis):** on match-level measures available for both populations, Match 103 should sit closer to the distribution of genuine exhibition matches than to ordinary official World Cup matches—even when goals are excluded from the classifier.

            **H0 / competing explanation:** the match was lower-stakes and heavily rotated, but players still worked physically; the open score was produced by ordinary tactical variance, score-state effects, referee style, and exceptional finishing rather than a systematic spectacle-first shift.

            This is a composite hypothesis, so one p-value cannot answer it. The notebook evaluates each component separately and reports a graded verdict: **supported**, **not supported**, **suggestive but underpowered**, or **descriptive only**. Private motivation and “fun” are not directly observable.

            ### Comparison hierarchy

            1. **Primary professional control:** neutral senior men's friendlies matched 1:1 to neutral major official tournament matches on year, average prior-year Elo, and Elo gap. Both teams must be prior-year top 30 and no more than 200 Elo points apart.
            2. **Duration sensitivity:** elite friendlies matched to official qualifiers, which normally avoid knockout extra time.
            3. **Individual-incentive mechanism audit:** timestamped pre-match award standings, selection decisions, match contributions, and post-match changes.
            4. **Player effort-versus-control audit:** official FIFA physical, pressing, movement, and shooting tables for all eight France and all eight England matches, with each player compared with his own earlier-tournament rate.
            5. **Same-provider process benchmark:** official FIFA Post-Match Summary Report metrics for 102 earlier 2026 World Cup matches.
            6. **Game-state benchmark:** regulation-time goal hazards from 964 men's World Cup matches through 2022.
            7. **Expanded exhibition benchmark:** 41 regulation-score charity/exhibition matches are reported by event and roster profile. This improves descriptive coverage while preserving the warning that charity formats are not like-for-like professional controls.
            8. **Two-population intensity test:** 102 earlier official World Cup matches are compared with all 19 exhibition matches that have the complete common core of shots, shots on target, fouls, and yellow cards. Match 103 is a strict holdout, never a training row.

            ### Statistical plan

            - The pre-specified primary outcome is total goals.
            - Matched outcomes use a paired bootstrap confidence interval and paired sign-flip permutation test. A paired exact McNemar test checks the five-plus-goal threshold.
            - Tail probabilities use a method-of-moments negative-binomial model, falling back to Poisson when overdispersion is absent. These are descriptive predictive checks, not causal estimates.
            - FIFA process metrics are empirical percentiles; only metrics from the same provider are compared.
            - Contact and discipline use all 103 official FIFA Full Time Match Reports. Match 103 is compared with the first 102 matches, the first 30 knockout matches, a ±3-foul band, the same referee's earlier matches, and each focal team's seven earlier matches. Add-one empirical tails avoid zero-probability estimates.
            - The formal exhibition-profile test uses Mann–Whitney rank tests with Cliff's delta and Holm correction across five common metrics. A class-balanced regularized logistic model is evaluated with 50 repeated five-fold splits. The primary model deliberately excludes goals; its output is a diagnostic similarity score, not a causal probability or an integrity verdict.
            - Score-state rates are bootstrapped by World Cup match. Because score state is endogenous, the decomposition is explanatory context, not a causal claim.
            - The individual-incentive audit is mechanism triangulation rather than a hypothesis test: a live award stake, selection, a match contribution, and a material change in the standing must all be visible.
            - Player effort tests compare Match 103 per-90 rates with each outfielder's pooled prior-tournament rate. Eligibility requires at least 45 Match 103 minutes, two prior appearances, and 90 prior minutes. Player bootstrap intervals and sign-flip tests are exploratory because teammates are not fully independent.
            - The finishing check treats total xG as a Poisson scoring mean. It is an approximation because shot-level xG values are not published in the saved report.

            ### Key assumptions and limitations

            - “Seriousness” is latent. Rotation, pressure, attacking volume, defensive outcomes, and scoring are proxies.
            - The international-results source stores full-time scores including extra time. The neutral official-tournament design is therefore paired with a qualifier sensitivity analysis.
            - The large results backbone has no stage field outside the World Cup source. Other competitions' third-place games are not fabricated or silently pooled.
            - Year-end Elo from year Y−1 is used for matches in year Y, preventing look-ahead but measuring strength less precisely than a match-day rating.
            - Charity and exhibition matches differ in roster quality, rules, substitutions, duration, and incentives. The expanded benchmark is stratified by event rather than collapsed into one supposedly homogeneous population.
            - Shared metrics come from two providers: FIFA for official World Cup matches and FotMob for exhibition matches. Event-family sensitivity and a rate-based model are reported, but residual provider-definition bias remains possible.
            - Before/after award movement establishes that an incentive existed and the match changed the outcome; it cannot establish the player's private motive for any action.
            - Physical totals include stoppage time while per-90 denominators use the regulation clock. This is applied consistently across reports; one crowded match-summary row required a separately sourced official substitution time.
            - Fouls and cards are aggregate match totals. They cannot isolate tactical fouls by score state, and card issuance depends partly on referee thresholds. The cardless result is supporting evidence, not a standalone test of intent.

            ### Sources

            - [Mart Jürisoo senior men's international results](https://github.com/martj42/international_results)
            - [JGravier yearly World Football Elo compilation](https://github.com/JGravier/soccer-elo)
            - [Fjelstul World Cup Database](https://github.com/jfjelstul/worldcup)
            - [FIFA Training Centre Post-Match Summary Reports](https://www.fifatrainingcentre.com/)
            - [StatsBomb Open Data attribution for the reused sibling pipeline](https://github.com/statsbomb/open-data)
            - [FotMob Soccer Aid archive and statistics](https://www.fotmob.com/en-GB/leagues/11648/stats/soccer-aid)
            - [FotMob Sidemen Charity Match archive and statistics](https://www.fotmob.com/leagues/10312/stats/sidemen-charity-match/teams?season=2025)
            """
        ),
        code(
            """
            # Setup, paths, and a restrained visual system
            from pathlib import Path
            from collections import defaultdict
            import json
            import math
            import sys
            import unicodedata
            import warnings

            import matplotlib.pyplot as plt
            import matplotlib.ticker as mtick
            import numpy as np
            import pandas as pd
            from IPython.display import display
            from scipy import stats
            from scipy.optimize import linear_sum_assignment
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import balanced_accuracy_score, brier_score_loss, roc_auc_score
            from sklearn.model_selection import StratifiedKFold
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import StandardScaler

            warnings.filterwarnings("ignore", category=FutureWarning)
            SEED = 20260719
            rng = np.random.default_rng(SEED)

            cwd = Path.cwd().resolve()
            candidates = [cwd, cwd.parent, cwd.parent.parent]
            ROOT = next(path for path in candidates if (path / "data").exists() and (path / "output").exists())
            SIBLING = ROOT.parent / "Argentina Comeback Analysis"
            ASSETS = ROOT / "output" / "assets"
            TABLES = ROOT / "output" / "tables"
            PROCESSED = ROOT / "data" / "processed"
            for directory in (ASSETS, TABLES, PROCESSED):
                directory.mkdir(parents=True, exist_ok=True)

            BLUE = "#2F6BFF"
            BLUE_LIGHT = "#BFD0FF"
            ORANGE = "#E28A2B"
            ORANGE_LIGHT = "#F7D9B2"
            INK = "#1F2937"
            MUTED = "#667085"
            GRID = "#D9DEE7"
            BG = "#FCFCFD"

            plt.rcParams.update({
                "figure.facecolor": BG,
                "axes.facecolor": BG,
                "axes.edgecolor": INK,
                "axes.labelcolor": INK,
                "axes.titlecolor": INK,
                "xtick.color": MUTED,
                "ytick.color": MUTED,
                "font.size": 10,
                "axes.titlesize": 13,
                "axes.titleweight": "bold",
                "axes.grid": True,
                "grid.color": GRID,
                "grid.alpha": 0.65,
                "grid.linewidth": 0.7,
                "legend.frameon": False,
            })

            print(f"Workspace: {ROOT}")
            print(f"Reusable sibling project: {SIBLING}")
            """
        ),
        markdown("## Data"),
        code(
            """
            # Load source manifest and input datasets
            with open(ROOT / "data" / "source_manifest_v2.json", encoding="utf-8") as handle:
                source_manifest = json.load(handle)

            results = pd.read_csv(ROOT / "data" / "international_results_raw" / "results.csv")
            ratings = pd.read_csv(SIBLING / "data" / "raw" / "jgravier" / "ranking_soccer_1901-2023.csv")
            matches_raw = pd.read_csv(SIBLING / "data" / "raw" / "fjelstul" / "matches.csv", encoding="utf-8-sig")
            goals_raw = pd.read_csv(SIBLING / "data" / "raw" / "fjelstul" / "goals.csv", encoding="utf-8-sig")
            pmsr_base = pd.read_csv(SIBLING / "data" / "processed" / "pmsr_2026_match_features.csv")
            current_goals = pd.read_csv(ROOT / "data" / "current_match_goals.csv")
            soccer_aid = pd.read_csv(ROOT / "data" / "soccer_aid_results.csv")
            exhibition_benchmark = pd.read_csv(ROOT / "data" / "exhibition_charity_benchmark.csv")
            exhibition_intensity = pd.read_csv(ROOT / "data" / "exhibition_match_intensity_benchmark.csv")
            lineups = pd.read_csv(ROOT / "data" / "lineup_starters.csv")
            player_incentives = pd.read_csv(ROOT / "data" / "player_incentive_evidence.csv")
            player_match = pd.read_csv(PROCESSED / "fifa_2026_france_england_player_match.csv")
            team_physical = pd.read_csv(PROCESSED / "fifa_2026_france_england_team_physical.csv")
            match_discipline = pd.read_csv(PROCESSED / "fifa_2026_match_contact_discipline.csv")
            team_discipline = pd.read_csv(PROCESSED / "fifa_2026_team_contact_discipline.csv")

            source_table = pd.DataFrame([
                ("Senior internationals", len(results), "one row per match", "1872–2026 file; analysis uses complete 1991–2023 rows"),
                ("Yearly Elo", len(ratings), "one row per team-year", "through 2023"),
                ("Men's World Cups", int(matches_raw["tournament_name"].str.contains("Men's World Cup", regex=False, na=False).sum()), "one row per match", "1930–2022"),
                ("FIFA PMSR baseline", pmsr_base["match_number"].nunique(), "two team rows per match", "2026 matches 1–96"),
                ("Current goal timeline", len(current_goals), "one row per goal", "match 103"),
                ("Soccer Aid", len(soccer_aid), "one row per match", "2006–2026"),
                ("Expanded charity/exhibition benchmark", len(exhibition_benchmark), "one row per match", "2005–2026; 26 additional matches"),
                ("Exhibition match-intensity benchmark", len(exhibition_intensity), "one row per match", "22 Soccer Aid/Sidemen matches; 19 complete common-core rows"),
                ("Starter audit", len(lineups), "one row per starter", "semi-finals and match 103"),
                ("Individual incentive audit", len(player_incentives), "one row per player-metric", "timestamped pre/post standings"),
                ("FIFA player-match audit", len(player_match), "one row per player-match", "all 8 France and all 8 England matches"),
                ("FIFA team physical audit", len(team_physical), "one row per team-match", "16 focal team-matches"),
                ("FIFA contact/discipline matches", len(match_discipline), "one row per match", "all completed matches 1–103"),
                ("FIFA contact/discipline teams", len(team_discipline), "one row per team-match", "206 rows from 103 official reports"),
            ], columns=["source", "rows_or_matches", "grain", "coverage"])
            display(source_table)
            """
        ),
        code(
            """
            # Data-quality audit: grain, uniqueness, completeness, and source reconciliation
            results["date"] = pd.to_datetime(results["date"], errors="coerce")
            men = matches_raw[matches_raw["tournament_name"].str.contains("Men's World Cup", regex=False, na=False)].copy()
            men_goal_events = goals_raw[goals_raw["match_id"].isin(men["match_id"])].copy()

            all_event_goals = men_goal_events.groupby("match_id").size()
            men["event_goal_count"] = men["match_id"].map(all_event_goals).fillna(0).astype(int)
            men["score_goal_count"] = pd.to_numeric(men["home_team_score"]) + pd.to_numeric(men["away_team_score"])

            lineup_sizes = lineups.groupby(["match_number", "team"]).size()
            incentive_arithmetic = (
                player_incentives["pre_match_value"] + player_incentives["match_added"]
            ).eq(player_incentives["post_match_value"])
            current_result_row = results[
                results["date"].eq(pd.Timestamp("2026-07-18"))
                & results["home_team"].eq("France")
                & results["away_team"].eq("England")
            ]
            player_key_duplicates = int(player_match.duplicated(["match_number", "team", "shirt_number"]).sum())
            player_match_coverage = player_match.groupby("team")["match_number"].nunique()
            minute_totals = player_match.groupby(["match_number", "team", "match_duration"])["minutes"].sum()
            minute_expected = minute_totals.index.get_level_values("match_duration") * 11
            minute_groups_reconciled = int(np.isclose(minute_totals.to_numpy(), minute_expected).sum())
            discipline_team_sizes = team_discipline.groupby("match_number").size()
            discipline_foul_reconciliation = team_discipline.merge(
                team_discipline[["match_number", "team", "fouls_committed"]],
                left_on=["match_number", "opponent"],
                right_on=["match_number", "team"],
                suffixes=("", "_opponent"),
                validate="one_to_one",
            )
            discipline_fouls_reconciled = discipline_foul_reconciliation[
                "fouls_suffered"
            ].eq(discipline_foul_reconciliation["fouls_committed_opponent"])
            exhibition_core_metrics = [
                "total_goals", "total_shots", "shots_on_target", "total_fouls", "yellow_cards"
            ]
            exhibition_complete = exhibition_intensity["coverage_status"].eq("complete_core")
            exhibition_complete_rows = exhibition_intensity.loc[exhibition_complete]

            quality_checks = pd.DataFrame([
                ("International result dates parse", int(results["date"].notna().sum()), len(results), "pass" if results["date"].notna().all() else "review"),
                ("Elo team-year key unique", int(ratings.duplicated(["year", "team"]).sum()), 0, "pass" if not ratings.duplicated(["year", "team"]).any() else "fail"),
                ("Men's World Cup match ID unique", int(men["match_id"].nunique()), len(men), "pass" if men["match_id"].is_unique else "fail"),
                ("World Cup goal events reconcile final scores", int((men["event_goal_count"] == men["score_goal_count"]).sum()), len(men), "pass" if (men["event_goal_count"] == men["score_goal_count"]).all() else "fail"),
                ("PMSR baseline has two team rows per match", int(pmsr_base.groupby("match_number").size().eq(2).sum()), 96, "pass"),
                ("Starter groups contain exactly 11 players", int(lineup_sizes.eq(11).sum()), len(lineup_sizes), "pass" if lineup_sizes.eq(11).all() else "fail"),
                ("Current timeline contains ten goals", len(current_goals), 10, "pass" if len(current_goals) == 10 else "fail"),
                ("Expanded benchmark has 26 additional matches", len(exhibition_benchmark), 26, "pass" if len(exhibition_benchmark) == 26 else "fail"),
                ("Expanded benchmark source URLs present", int(exhibition_benchmark["source_url"].notna().sum()), len(exhibition_benchmark), "pass" if exhibition_benchmark["source_url"].notna().all() else "fail"),
                ("Expanded benchmark regulation scores are nonnegative", int(((exhibition_benchmark["team_a_goals"] >= 0) & (exhibition_benchmark["team_b_goals"] >= 0)).sum()), len(exhibition_benchmark), "pass" if ((exhibition_benchmark["team_a_goals"] >= 0) & (exhibition_benchmark["team_b_goals"] >= 0)).all() else "fail"),
                ("Exhibition intensity event-year key unique", int(exhibition_intensity.duplicated(["event", "year"]).sum()), 0, "pass" if not exhibition_intensity.duplicated(["event", "year"]).any() else "fail"),
                ("Exhibition intensity source URLs present", int(exhibition_intensity["source_url"].notna().sum()), len(exhibition_intensity), "pass" if exhibition_intensity["source_url"].notna().all() else "fail"),
                ("Exhibition complete-core rows available", int(exhibition_complete.sum()), 19, "pass" if exhibition_complete.sum() == 19 else "fail"),
                ("Exhibition complete-core metrics populated", int(exhibition_complete_rows[exhibition_core_metrics].notna().all(axis=1).sum()), 19, "pass" if exhibition_complete_rows[exhibition_core_metrics].notna().all(axis=1).sum() == 19 else "fail"),
                ("Individual incentive rows reconcile pre + match = post", int(incentive_arithmetic.sum()), len(player_incentives), "pass" if incentive_arithmetic.all() else "fail"),
                ("FIFA player-match-shirt key unique", player_key_duplicates, 0, "pass" if player_key_duplicates == 0 else "fail"),
                ("Focal teams each cover eight matches", int(player_match_coverage.eq(8).sum()), 2, "pass" if player_match_coverage.eq(8).all() else "fail"),
                ("Player minutes reconcile eleven on-field slots", minute_groups_reconciled, len(minute_totals), "pass" if minute_groups_reconciled == len(minute_totals) else "fail"),
                ("Full Time reports cover matches 1–103 exactly", int(set(match_discipline["match_number"]) == set(range(1, 104))), 1, "pass" if set(match_discipline["match_number"]) == set(range(1, 104)) else "fail"),
                ("Full Time reports have two team rows per match", int(discipline_team_sizes.eq(2).sum()), 103, "pass" if discipline_team_sizes.eq(2).all() else "fail"),
                ("Fouls suffered reconcile to opponent fouls", int(discipline_fouls_reconciled.sum()), len(team_discipline), "pass" if discipline_fouls_reconciled.all() else "fail"),
                ("Full Time report supplies Match-103 ten-goal score", int(match_discipline.loc[match_discipline["match_number"].eq(103), "total_goals"].iloc[0]), 10, "pass"),
                ("Results backbone current score populated", int(current_result_row[["home_score", "away_score"]].notna().all(axis=1).sum()), 1, "expected gap"),
            ], columns=["check", "observed", "expected", "status"])

            assert ratings[["year", "team"]].drop_duplicates().shape[0] == len(ratings)
            assert men["match_id"].is_unique
            assert (men["event_goal_count"] == men["score_goal_count"]).all()
            assert pmsr_base.groupby("match_number").size().eq(2).all()
            assert lineup_sizes.eq(11).all()
            assert len(current_goals) == 10
            assert len(exhibition_benchmark) == 26
            assert exhibition_benchmark["source_url"].notna().all()
            assert ((exhibition_benchmark["team_a_goals"] >= 0) & (exhibition_benchmark["team_b_goals"] >= 0)).all()
            assert not exhibition_intensity.duplicated(["event", "year"]).any()
            assert exhibition_intensity["source_url"].notna().all()
            assert exhibition_complete.sum() == 19
            assert exhibition_complete_rows[exhibition_core_metrics].notna().all(axis=1).all()
            assert not player_incentives.duplicated(["player", "metric"]).any()
            assert incentive_arithmetic.all()
            assert player_key_duplicates == 0
            assert player_match_coverage.eq(8).all()
            assert minute_groups_reconciled == len(minute_totals)
            assert set(match_discipline["match_number"]) == set(range(1, 104))
            assert discipline_team_sizes.eq(2).all()
            assert discipline_fouls_reconciled.all()
            assert match_discipline.loc[match_discipline["match_number"].eq(103), "total_goals"].iloc[0] == 10
            display(quality_checks)

            print("Known freshness gap: the cloned results backbone still stores match 103 as an unscored fixture; official FIFA data supplies the result and process metrics.")
            """
        ),
        code(
            """
            # Extend the official FIFA PMSR panel from match 96 through match 103
            sibling_src = SIBLING / "src"
            if str(sibling_src) not in sys.path:
                sys.path.insert(0, str(sibling_src))
            from research_etl.pmsr_stats import parse_pmsr_match_summary

            pmsr_specs = [
                (97, "FRA-V-MAR", ["France", "Morocco"]),
                (98, "ESP-V-BEL", ["Spain", "Belgium"]),
                (99, "NOR-V-ENG", ["Norway", "England"]),
                (100, "ARG-V-SUI", ["Argentina", "Switzerland"]),
                (101, "FRA-V-ESP", ["France", "Spain"]),
                (102, "ENG-V-ARG", ["England", "Argentina"]),
                (103, "FRA-V-ENG", ["France", "England"]),
            ]

            extension_rows = []
            for match_number, code_name, teams in pmsr_specs:
                pdf_path = ROOT / "data" / "fifa" / f"PMSR-M{match_number}-{code_name}.pdf"
                assert pdf_path.exists(), f"Missing {pdf_path}"
                parsed = parse_pmsr_match_summary(pdf_path.read_bytes(), teams)
                source_url = f"https://www.fifatrainingcentre.com/media/native/tournaments/fifa-world-cup/2026/PMSR-M{match_number}-{code_name}.pdf"
                for team_name in teams:
                    opponent = next(team for team in teams if team != team_name)
                    extension_rows.append({
                        "match_number": match_number,
                        "tournament_name": "2026 FIFA World Cup",
                        "year": 2026,
                        "team_name": team_name,
                        "opponent_team_name": opponent,
                        "penalties_awarded": np.nan,
                        **parsed[team_name],
                        "source_name": "FIFA Post-Match Summary Report",
                        "source_version": "pmsr_match_summary_v1",
                        "source_url": source_url,
                    })

            pmsr_extension = pd.DataFrame(extension_rows)
            missing_extension_columns = set(pmsr_base.columns) - set(pmsr_extension.columns)
            assert not missing_extension_columns, missing_extension_columns
            pmsr = pd.concat([pmsr_base, pmsr_extension[pmsr_base.columns]], ignore_index=True)
            pmsr = pmsr.sort_values(["match_number", "team_name"], kind="stable").reset_index(drop=True)

            def fifa_stage(match_number: int) -> str:
                if match_number <= 72:
                    return "Group stage"
                if match_number <= 88:
                    return "Round of 32"
                if match_number <= 96:
                    return "Round of 16"
                if match_number <= 100:
                    return "Quarter-final"
                if match_number <= 102:
                    return "Semi-final"
                if match_number == 103:
                    return "Third-place"
                return "Final"

            pmsr["stage"] = pmsr["match_number"].map(fifa_stage)
            assert pmsr["match_number"].nunique() == 103
            assert pmsr.groupby("match_number").size().eq(2).all()
            pmsr.to_csv(PROCESSED / "fifa_2026_match_features_m1_m103.csv", index=False)

            print(f"Official same-provider panel: {pmsr['match_number'].nunique()} matches, {len(pmsr)} team-match rows.")
            display(pmsr.tail(6)[["match_number", "stage", "team_name", "goals", "xg", "attempts_at_goal", "shots_on_target", "defensive_pressures", "forced_turnovers"]])
            """
        ),
        markdown("## Results"),
        code(
            """
            # Build a leakage-safe elite international comparison frame
            def ascii_text(value: object) -> str:
                return "".join(
                    character for character in unicodedata.normalize("NFKD", str(value))
                    if not unicodedata.combining(character)
                )

            aliases = {
                "Republic of Ireland": "Ireland",
                "Czech Republic": "Czechia",
                "North Macedonia": "Macedonia",
                "Eswatini": "Swaziland",
                "DR Congo": "Congo DR",
                "United States Virgin Islands": "US Virgin Islands",
                "Timor-Leste": "East Timor",
            }

            complete = results[
                results["date"].dt.year.between(1991, 2023)
                & results["home_score"].notna()
                & results["away_score"].notna()
            ].copy()
            complete["rating_year"] = complete["date"].dt.year - 1
            for side in ("home", "away"):
                complete[f"{side}_rating_team"] = complete[f"{side}_team"].replace(aliases)
                lookup = ratings[["year", "team", "rating", "rank"]].rename(columns={
                    "year": "rating_year",
                    "team": f"{side}_rating_team",
                    "rating": f"{side}_rating",
                    "rank": f"{side}_rank",
                })
                complete = complete.merge(
                    lookup,
                    on=["rating_year", f"{side}_rating_team"],
                    how="left",
                    validate="many_to_one",
                )

            complete["tournament_normalized"] = complete["tournament"].map(ascii_text)
            complete["neutral_bool"] = complete["neutral"].astype(str).str.upper().eq("TRUE")
            complete["year"] = complete["date"].dt.year
            complete["avg_elo"] = (complete["home_rating"] + complete["away_rating"]) / 2
            complete["elo_gap"] = (complete["home_rating"] - complete["away_rating"]).abs()
            complete["worst_rank"] = complete[["home_rank", "away_rank"]].max(axis=1)
            complete["total_goals"] = complete["home_score"] + complete["away_score"]

            major_finals = {
                "FIFA World Cup", "UEFA Euro", "Copa America", "African Cup of Nations",
                "AFC Asian Cup", "CONCACAF Gold Cup", "Gold Cup", "Oceania Nations Cup",
                "UEFA Nations League", "CONCACAF Nations League", "FIFA Confederations Cup",
                "Confederations Cup",
            }
            complete["analysis_context"] = np.select(
                [
                    complete["tournament_normalized"].eq("Friendly"),
                    complete["tournament_normalized"].isin(major_finals),
                ],
                ["Elite professional friendly", "Official tournament match"],
                default="Other",
            )

            rating_coverage = complete[["home_rating", "away_rating"]].notna().all(axis=1).mean()
            eligible = complete[
                complete["analysis_context"].ne("Other")
                & complete[["home_rating", "away_rating"]].notna().all(axis=1)
                & complete["worst_rank"].le(30)
                & complete["elo_gap"].le(200)
            ].copy()
            primary_pool = eligible[eligible["neutral_bool"]].copy()

            coverage_table = pd.DataFrame([
                ("All complete 1991–2023 rows", len(complete), rating_coverage * 100),
                ("Elite friendly/official-tournament candidates", len(eligible), eligible[["home_rating", "away_rating"]].notna().all(axis=1).mean() * 100),
                ("Neutral primary pool", len(primary_pool), 100.0),
            ], columns=["population", "matches", "prior-year Elo coverage_pct"])
            display(coverage_table.round(1))
            display(primary_pool.groupby("analysis_context").size().rename("matches").to_frame())
            """
        ),
        code(
            """
            # Optimal 1:1 matching without replacement and balance diagnostics
            MATCH_FEATURES = ["year", "avg_elo", "elo_gap"]

            def standardized_mean_difference(left: pd.Series, right: pd.Series) -> float:
                denominator = math.sqrt((left.var(ddof=1) + right.var(ddof=1)) / 2)
                return 0.0 if denominator == 0 else float((left.mean() - right.mean()) / denominator)

            def optimal_pair_match(
                frame: pd.DataFrame,
                left_label: str,
                right_label: str,
                *,
                caliper: float = 1.25,
                exact_neutral: bool = True,
            ) -> tuple[pd.DataFrame, pd.DataFrame]:
                pair_rows = []
                pair_id = 0
                groups = frame.groupby("neutral_bool", dropna=False) if exact_neutral else [("all", frame)]
                for _, stratum in groups:
                    left = stratum[stratum["analysis_context"].eq(left_label)].copy()
                    right = stratum[stratum["analysis_context"].eq(right_label)].copy()
                    if left.empty or right.empty:
                        continue
                    center = pd.concat([left[MATCH_FEATURES], right[MATCH_FEATURES]]).mean()
                    scale = pd.concat([left[MATCH_FEATURES], right[MATCH_FEATURES]]).std(ddof=0).replace(0, 1)
                    left_matrix = ((left[MATCH_FEATURES] - center) / scale).to_numpy()
                    right_matrix = ((right[MATCH_FEATURES] - center) / scale).to_numpy()
                    costs = np.sqrt(((left_matrix[:, None, :] - right_matrix[None, :, :]) ** 2).sum(axis=2))
                    left_idx, right_idx = linear_sum_assignment(costs)
                    for left_pos, right_pos in zip(left_idx, right_idx):
                        distance = float(costs[left_pos, right_pos])
                        if distance > caliper:
                            continue
                        pair_id += 1
                        left_row = left.iloc[left_pos].copy()
                        right_row = right.iloc[right_pos].copy()
                        left_row["pair_id"] = pair_id
                        right_row["pair_id"] = pair_id
                        left_row["match_distance"] = distance
                        right_row["match_distance"] = distance
                        pair_rows.extend([left_row, right_row])
                matched_long = pd.DataFrame(pair_rows)
                left_matched = matched_long[matched_long["analysis_context"].eq(left_label)].sort_values("pair_id")
                right_matched = matched_long[matched_long["analysis_context"].eq(right_label)].sort_values("pair_id")
                paired = pd.DataFrame({
                    "pair_id": left_matched["pair_id"].to_numpy(),
                    "friendly_goals": left_matched["total_goals"].to_numpy(),
                    "official_goals": right_matched["total_goals"].to_numpy(),
                    "distance": left_matched["match_distance"].to_numpy(),
                })
                return matched_long, paired

            FRIENDLY = "Elite professional friendly"
            OFFICIAL = "Official tournament match"
            matched_primary, paired_primary = optimal_pair_match(primary_pool, FRIENDLY, OFFICIAL)
            primary_friendly = matched_primary[matched_primary["analysis_context"].eq(FRIENDLY)].sort_values("pair_id")
            primary_official = matched_primary[matched_primary["analysis_context"].eq(OFFICIAL)].sort_values("pair_id")

            raw_friendly = primary_pool[primary_pool["analysis_context"].eq(FRIENDLY)]
            raw_official = primary_pool[primary_pool["analysis_context"].eq(OFFICIAL)]
            balance_rows = []
            for feature in MATCH_FEATURES:
                balance_rows.append({
                    "feature": feature,
                    "before": standardized_mean_difference(raw_friendly[feature], raw_official[feature]),
                    "after": standardized_mean_difference(primary_friendly[feature], primary_official[feature]),
                })
            balance = pd.DataFrame(balance_rows)

            assert len(paired_primary) >= 150
            assert balance["after"].abs().max() < 0.10
            matched_primary.to_csv(PROCESSED / "matched_neutral_elite_friendlies_vs_officials.csv", index=False)
            balance.to_csv(TABLES / "v2_matching_balance.csv", index=False)

            print(f"Matched neutral pairs: {len(paired_primary)}")
            display(balance.assign(before_abs=balance["before"].abs(), after_abs=balance["after"].abs()).round(3))

            fig, ax = plt.subplots(figsize=(8.5, 4.4))
            y = np.arange(len(balance))
            ax.hlines(y, balance["before"].abs(), balance["after"].abs(), color=GRID, linewidth=3)
            ax.scatter(balance["before"].abs(), y, s=80, facecolor=BG, edgecolor=ORANGE, linewidth=2, label="Before")
            ax.scatter(balance["after"].abs(), y, s=80, color=BLUE, edgecolor=INK, linewidth=0.6, label="After")
            ax.axvline(0.10, color=INK, linestyle="--", linewidth=1, label="|SMD| = 0.10")
            ax.set_yticks(y, ["Match year", "Average prior-year Elo", "Prior-year Elo gap"])
            ax.set_xlabel("Absolute standardized mean difference")
            ax.set_title("Covariate balance before and after 1:1 matching", loc="left", pad=30)
            ax.text(0, 1.01, f"Neutral top-30 internationals, 1991–2023; n={len(paired_primary)} pairs", transform=ax.transAxes, color=MUTED)
            ax.legend(loc="upper right", ncol=3)
            ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_matching_balance.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        code(
            """
            # Primary paired inference, five-goal threshold, and design sensitivities
            def paired_inference(differences: np.ndarray, *, draws: int = 20_000, seed: int = SEED) -> dict[str, float]:
                local_rng = np.random.default_rng(seed)
                differences = np.asarray(differences, dtype=float)
                observed = float(differences.mean())
                bootstrap = np.array([
                    local_rng.choice(differences, size=len(differences), replace=True).mean()
                    for _ in range(draws)
                ])
                permutations = np.array([
                    (differences * local_rng.choice([-1, 1], size=len(differences))).mean()
                    for _ in range(draws)
                ])
                return {
                    "mean_difference": observed,
                    "ci_low": float(np.quantile(bootstrap, 0.025)),
                    "ci_high": float(np.quantile(bootstrap, 0.975)),
                    "permutation_p": float((np.sum(np.abs(permutations) >= abs(observed)) + 1) / (draws + 1)),
                }

            primary_differences = paired_primary["friendly_goals"].to_numpy() - paired_primary["official_goals"].to_numpy()
            primary_test = paired_inference(primary_differences)

            friendly_high = paired_primary["friendly_goals"].ge(5).to_numpy()
            official_high = paired_primary["official_goals"].ge(5).to_numpy()
            friendly_only = int(np.sum(friendly_high & ~official_high))
            official_only = int(np.sum(~friendly_high & official_high))
            mcnemar_p = float(stats.binomtest(friendly_only, friendly_only + official_only, 0.5).pvalue)

            primary_summary = pd.DataFrame([
                ("Matched pairs", len(paired_primary)),
                ("Friendly mean goals", paired_primary["friendly_goals"].mean()),
                ("Official mean goals", paired_primary["official_goals"].mean()),
                ("Friendly − official mean difference", primary_test["mean_difference"]),
                ("Bootstrap 95% CI low", primary_test["ci_low"]),
                ("Bootstrap 95% CI high", primary_test["ci_high"]),
                ("Paired sign-flip permutation p", primary_test["permutation_p"]),
                ("Friendly five-plus rate", friendly_high.mean()),
                ("Official five-plus rate", official_high.mean()),
                ("Exact paired five-plus p", mcnemar_p),
            ], columns=["measure", "value"])
            display(primary_summary.round(4))

            # Target-quality sensitivity: repeat neutral matching at stricter rank cutoffs.
            rank_sensitivity = []
            for rank_cutoff in (10, 15, 20, 30):
                pool = eligible[eligible["neutral_bool"] & eligible["worst_rank"].le(rank_cutoff)].copy()
                matched_rank, paired_rank = optimal_pair_match(pool, FRIENDLY, OFFICIAL)
                if paired_rank.empty:
                    continue
                rank_result = paired_inference(
                    paired_rank["friendly_goals"].to_numpy() - paired_rank["official_goals"].to_numpy(),
                    draws=5_000,
                    seed=SEED + rank_cutoff,
                )
                rank_sensitivity.append({
                    "rank_cutoff": rank_cutoff,
                    "pairs": len(paired_rank),
                    "friendly_mean": paired_rank["friendly_goals"].mean(),
                    "official_mean": paired_rank["official_goals"].mean(),
                    **rank_result,
                })
            rank_sensitivity = pd.DataFrame(rank_sensitivity)

            # Extra-time sensitivity: use official qualifiers and exact-match venue status.
            qualifier_names = {
                "FIFA World Cup qualification", "UEFA Euro qualification",
                "African Cup of Nations qualification", "AFC Asian Cup qualification",
                "Gold Cup qualification", "Oceania Nations Cup qualification",
                "Copa America qualification", "CONCACAF Nations League qualification",
            }
            qualifier_pool = complete[
                complete[["home_rating", "away_rating"]].notna().all(axis=1)
                & complete["worst_rank"].le(30)
                & complete["elo_gap"].le(200)
                & (complete["tournament_normalized"].eq("Friendly") | complete["tournament_normalized"].isin(qualifier_names))
            ].copy()
            qualifier_pool["analysis_context"] = np.where(
                qualifier_pool["tournament_normalized"].eq("Friendly"), FRIENDLY, "Elite official qualifier"
            )
            _, paired_qualifier = optimal_pair_match(qualifier_pool, FRIENDLY, "Elite official qualifier")
            qualifier_test = paired_inference(
                paired_qualifier["friendly_goals"].to_numpy() - paired_qualifier["official_goals"].to_numpy(),
                seed=SEED + 100,
            )

            sensitivity_table = pd.concat([
                rank_sensitivity.assign(design=lambda frame: "Neutral top-" + frame["rank_cutoff"].astype(str))[
                    ["design", "pairs", "friendly_mean", "official_mean", "mean_difference", "ci_low", "ci_high", "permutation_p"]
                ],
                pd.DataFrame([{
                    "design": "Top-30 friendly vs qualifier",
                    "pairs": len(paired_qualifier),
                    "friendly_mean": paired_qualifier["friendly_goals"].mean(),
                    "official_mean": paired_qualifier["official_goals"].mean(),
                    **qualifier_test,
                }]),
            ], ignore_index=True)
            sensitivity_table.to_csv(TABLES / "v2_professional_control_sensitivity.csv", index=False)
            display(sensitivity_table.round(3))

            fig, ax = plt.subplots(figsize=(8.8, 5.3))
            positions = [1, 2]
            data = [paired_primary["official_goals"], paired_primary["friendly_goals"]]
            box = ax.boxplot(data, positions=positions, widths=0.45, patch_artist=True, showfliers=False, medianprops={"color": INK, "linewidth": 1.5})
            for patch, color in zip(box["boxes"], [BLUE_LIGHT, ORANGE_LIGHT]):
                patch.set_facecolor(color)
                patch.set_edgecolor(INK)
            local_rng = np.random.default_rng(SEED)
            for position, values, color in zip(positions, data, [BLUE, ORANGE]):
                jitter = local_rng.normal(0, 0.055, len(values))
                ax.scatter(np.full(len(values), position) + jitter, values, s=16, alpha=0.38, color=color, edgecolors="none")
                ax.text(position, 7.65, f"mean {np.mean(values):.2f}\\nn={len(values)}", ha="center", va="bottom", color=MUTED)
            ax.axhline(10, color=INK, linestyle="--", linewidth=1.2)
            ax.text(2.37, 10, "England–France: 10", va="center", color=INK, fontweight="bold")
            ax.set_xticks(positions, ["Official tournament matches", "Professional friendlies"])
            ax.set_ylabel("Total goals")
            ax.set_ylim(-0.2, 10.8)
            ax.set_title("Total goals in matched neutral elite internationals", loc="left", pad=30)
            ax.text(0, 1.01, f"Top-30 teams, Elo gap ≤200, 1991–2023; {len(paired_primary)} matched pairs", transform=ax.transAxes, color=MUTED)
            ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_matched_goal_distribution.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        code(
            """
            # Smoothed probability of a ten-goal match across contexts
            men["total_goals"] = pd.to_numeric(men["home_team_score"]) + pd.to_numeric(men["away_team_score"])
            title_path_stages = {"round of 16", "quarter-finals", "semi-finals", "final"}
            world_cup_title = men.loc[men["stage_name"].isin(title_path_stages), "total_goals"].to_numpy()
            world_cup_third = men.loc[men["stage_name"].eq("third-place match"), "total_goals"].to_numpy()
            soccer_aid_goals = (soccer_aid["team_a_goals"] + soccer_aid["team_b_goals"]).to_numpy()
            exhibition_benchmark["total_goals"] = exhibition_benchmark["team_a_goals"] + exhibition_benchmark["team_b_goals"]
            additional_exhibition_goals = exhibition_benchmark["total_goals"].to_numpy()
            expanded_exhibition_goals = np.concatenate([soccer_aid_goals, additional_exhibition_goals])

            pmsr_match = pmsr.groupby("match_number").agg(
                total_goals=("goals", "sum"),
                total_xg=("xg", "sum"),
                attempts=("attempts_at_goal", "sum"),
                shots_on_target=("shots_on_target", "sum"),
                line_breaks=("completed_line_breaks", "sum"),
                pressures=("defensive_pressures", "sum"),
                direct_pressures=("direct_pressures", "sum"),
                forced_turnovers=("forced_turnovers", "sum"),
            )
            pmsr_match["turnovers_per_100_pressures"] = 100 * pmsr_match["forced_turnovers"] / pmsr_match["pressures"]
            pmsr_match["direct_pressure_share_pct"] = 100 * pmsr_match["direct_pressures"] / pmsr_match["pressures"]
            pmsr_match["goals_per_xg"] = pmsr_match["total_goals"] / pmsr_match["total_xg"]

            def count_tail(values: np.ndarray, threshold: int = 10) -> dict[str, float | str]:
                values = np.asarray(values, dtype=float)
                mean = float(values.mean())
                variance = float(values.var(ddof=1))
                if variance <= mean * 1.001:
                    tail = float(stats.poisson.sf(threshold - 1, mean))
                    model = "Poisson"
                    dispersion = 0.0
                else:
                    dispersion = (variance - mean) / mean**2
                    size = 1 / dispersion
                    probability = size / (size + mean)
                    tail = float(stats.nbinom.sf(threshold - 1, size, probability))
                    model = "Negative binomial"
                return {
                    "matches": len(values),
                    "mean_goals": mean,
                    "sd_goals": math.sqrt(variance),
                    "empirical_10_plus": float(np.mean(values >= threshold)),
                    "max_goals": float(values.max()),
                    "tail_probability": tail,
                    "tail_model": model,
                    "dispersion": dispersion,
                }

            tail_contexts = {
                "Matched official tournaments": paired_primary["official_goals"].to_numpy(),
                "Matched professional friendlies": paired_primary["friendly_goals"].to_numpy(),
                "World Cup title-path · all eras": world_cup_title,
                "World Cup third-place · all eras": world_cup_third,
                "Soccer Aid charity · regulation": soccer_aid_goals,
                "Expanded charity/exhibition · regulation": expanded_exhibition_goals,
                "2026 World Cup 1–102 · FIFA": pmsr_match.loc[:102, "total_goals"].to_numpy(),
            }
            tail_table = pd.DataFrame([
                {"context": context, **count_tail(values)} for context, values in tail_contexts.items()
            ]).sort_values("tail_probability")
            tail_table["tail_probability_pct"] = 100 * tail_table["tail_probability"]
            tail_table.to_csv(TABLES / "v2_ten_goal_tail_probabilities.csv", index=False)
            display(tail_table[["context", "matches", "mean_goals", "max_goals", "empirical_10_plus", "tail_model", "tail_probability_pct"]].round(4))

            fig, ax = plt.subplots(figsize=(9.0, 5.4))
            plot_tail = tail_table.sort_values("tail_probability", ascending=True).reset_index(drop=True)
            colors = [ORANGE if ("Soccer Aid" in name or "Expanded charity" in name) else BLUE for name in plot_tail["context"]]
            bars = ax.barh(plot_tail["context"], plot_tail["tail_probability_pct"], color=colors, edgecolor=INK, linewidth=0.5)
            ax.set_xscale("log")
            ax.set_xlabel("Modelled probability of at least 10 goals (%) — log scale")
            ax.set_title("Smoothed ten-goal tail probability by comparison context", loc="left", pad=30)
            ax.text(0, 1.01, "Negative-binomial method of moments; Poisson when estimated overdispersion is absent", transform=ax.transAxes, color=MUTED)
            for bar, probability, sample in zip(bars, plot_tail["tail_probability_pct"], plot_tail["matches"]):
                ax.text(probability * 1.10, bar.get_y() + bar.get_height()/2, f"{probability:.3f}% · n={sample}", va="center", fontsize=9, color=INK)
            ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_predictive_tail.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        markdown(
            """
            ## The expanded charity benchmark is larger—but not one homogeneous population

            The original Soccer Aid sample had only 15 matches. The expanded file adds 26 documented charity or exhibition matches from other formats. The important result is not a single larger average: the event groups have different roster profiles and scoring levels.

            We therefore report the event means, uncertainty around each mean, the raw score spread, and the current match's position. The benchmark is a descriptive context check. It cannot establish that an official World Cup third-place match was causally equivalent to a celebrity, legends, or benefit game.
            """
        ),
        code(
            """
            # Expanded event-level charity/exhibition benchmark
            soccer_aid_std = soccer_aid.copy()
            soccer_aid_std["benchmark_group"] = "soccer_aid"
            soccer_aid_std["roster_profile"] = "celebrities_and_former_pros"
            soccer_aid_std["source_tier"] = np.where(soccer_aid_std["year"].ge(2024), "official", "secondary")
            soccer_aid_std["total_goals"] = soccer_aid_std["team_a_goals"] + soccer_aid_std["team_b_goals"]
            benchmark_all = pd.concat([
                soccer_aid_std[["year", "competition", "benchmark_group", "roster_profile", "team_a", "team_b", "team_a_goals", "team_b_goals", "penalty_shootout", "source_tier", "total_goals"]],
                exhibition_benchmark[["year", "competition", "benchmark_group", "roster_profile", "team_a", "team_b", "team_a_goals", "team_b_goals", "penalty_shootout", "source_tier", "total_goals"]],
            ], ignore_index=True)

            group_labels = {
                "soccer_aid": "Soccer Aid",
                "corazon_classic": "Corazón Classic",
                "match_for_hope": "Match for Hope",
                "sidemen": "Sidemen Charity",
                "benefit_all_star": "Other benefit events",
            }
            group_order = ["soccer_aid", "corazon_classic", "match_for_hope", "sidemen", "benefit_all_star"]

            def mean_bootstrap_interval(values: np.ndarray, draws: int = 20_000) -> tuple[float, float]:
                values = np.asarray(values, dtype=float)
                draws_values = rng.choice(values, size=(draws, len(values)), replace=True).mean(axis=1)
                return float(np.quantile(draws_values, 0.025)), float(np.quantile(draws_values, 0.975))

            summary_rows = []
            for group in group_order:
                values = benchmark_all.loc[benchmark_all["benchmark_group"].eq(group), "total_goals"].to_numpy()
                ci_low, ci_high = mean_bootstrap_interval(values)
                summary_rows.append({
                    "benchmark_group": group,
                    "label": group_labels[group],
                    "matches": len(values),
                    "mean_goals": float(values.mean()),
                    "median_goals": float(np.median(values)),
                    "sd_goals": float(values.std(ddof=1)),
                    "min_goals": int(values.min()),
                    "max_goals": int(values.max()),
                    "five_plus_rate": float(np.mean(values >= 5)),
                    "ten_plus_count": int(np.sum(values >= 10)),
                    "mean_bootstrap_ci_low": ci_low,
                    "mean_bootstrap_ci_high": ci_high,
                })
            expanded_values = benchmark_all["total_goals"].to_numpy()
            expanded_ci_low, expanded_ci_high = mean_bootstrap_interval(expanded_values)
            summary_rows.append({
                "benchmark_group": "expanded_all",
                "label": "All expanded events",
                "matches": len(expanded_values),
                "mean_goals": float(expanded_values.mean()),
                "median_goals": float(np.median(expanded_values)),
                "sd_goals": float(expanded_values.std(ddof=1)),
                "min_goals": int(expanded_values.min()),
                "max_goals": int(expanded_values.max()),
                "five_plus_rate": float(np.mean(expanded_values >= 5)),
                "ten_plus_count": int(np.sum(expanded_values >= 10)),
                "mean_bootstrap_ci_low": expanded_ci_low,
                "mean_bootstrap_ci_high": expanded_ci_high,
            })
            exhibition_summary = pd.DataFrame(summary_rows)
            target_goals = 10
            benchmark_tests = pd.DataFrame([
                {
                    "comparison": "Target vs Soccer Aid",
                    "matches": len(soccer_aid_goals),
                    "benchmark_mean_goals": float(soccer_aid_goals.mean()),
                    "target_minus_mean": float(target_goals - soccer_aid_goals.mean()),
                    "benchmark_max_goals": int(soccer_aid_goals.max()),
                    "benchmark_matches_at_least_target": int(np.sum(soccer_aid_goals >= target_goals)),
                    "empirical_upper_tail_with_correction": float((1 + np.sum(soccer_aid_goals >= target_goals)) / (len(soccer_aid_goals) + 1)),
                    "interpretation": "Descriptive only; small single-event sample",
                },
                {
                    "comparison": "Target vs all expanded events",
                    "matches": len(expanded_values),
                    "benchmark_mean_goals": float(expanded_values.mean()),
                    "target_minus_mean": float(target_goals - expanded_values.mean()),
                    "benchmark_max_goals": int(expanded_values.max()),
                    "benchmark_matches_at_least_target": int(np.sum(expanded_values >= target_goals)),
                    "empirical_upper_tail_with_correction": float((1 + np.sum(expanded_values >= target_goals)) / (len(expanded_values) + 1)),
                    "interpretation": "Descriptive only; event formats are heterogeneous",
                },
            ])
            exhibition_summary.to_csv(TABLES / "v2_exhibition_benchmark_summary.csv", index=False)
            benchmark_tests.to_csv(TABLES / "v2_exhibition_benchmark_tests.csv", index=False)
            display(exhibition_summary.round(3))
            display(benchmark_tests.round(3))

            fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.0), gridspec_kw={"width_ratios": [1.1, 1.55]})
            plot_summary = exhibition_summary[exhibition_summary["benchmark_group"].isin(group_order)].copy()
            x = np.arange(len(plot_summary))
            palette = [BLUE, BLUE_LIGHT, ORANGE, "#8A9BB8", "#C7A86B"]
            axes[0].bar(x, plot_summary["mean_goals"], color=palette, edgecolor=INK, linewidth=0.6)
            axes[0].errorbar(x, plot_summary["mean_goals"], yerr=[plot_summary["mean_goals"] - plot_summary["mean_bootstrap_ci_low"], plot_summary["mean_bootstrap_ci_high"] - plot_summary["mean_goals"]], fmt="none", ecolor=INK, capsize=4, linewidth=1.2)
            axes[0].axhline(target_goals, color=INK, linestyle="--", linewidth=1.2)
            axes[0].text(0.05, target_goals + 0.25, "England–France: 10", ha="left", color=INK, fontweight="bold")
            axes[0].set_xticks(x, plot_summary["label"], rotation=25, ha="right")
            axes[0].set_ylabel("Average regulation-time goals")
            axes[0].set_ylim(0, max(14, target_goals + 2))
            axes[0].set_title("Average goals by exhibition format", loc="left", pad=30)
            axes[0].text(0, 1.01, "Bars show means; whiskers show bootstrap 95% intervals", transform=axes[0].transAxes, color=MUTED)
            for xi, value, n in zip(x, plot_summary["mean_goals"], plot_summary["matches"]):
                axes[0].text(xi, value + 0.45, f"{value:.1f}\\nn={n}", ha="center", va="bottom", fontsize=9, color=INK)

            sorted_benchmark = benchmark_all.sort_values(["total_goals", "year"], kind="stable").reset_index(drop=True)
            color_map = dict(zip(group_order, palette))
            axes[1].scatter(np.arange(len(sorted_benchmark)), sorted_benchmark["total_goals"], c=sorted_benchmark["benchmark_group"].map(color_map), s=42, edgecolor=INK, linewidth=0.4, alpha=0.9)
            axes[1].axhline(target_goals, color=INK, linestyle="--", linewidth=1.2)
            axes[1].text(len(sorted_benchmark) - 0.5, target_goals + 0.35, "Target = 10", ha="right", color=INK, fontweight="bold")
            axes[1].set_xlabel("41 benchmark matches sorted from fewest to most goals")
            axes[1].set_ylabel("Regulation-time goals")
            axes[1].set_title("The expanded sample is highly heterogeneous", loc="left", pad=30)
            axes[1].text(0, 1.01, "Some creator formats reached 18–20 goals; legends and Soccer Aid were lower", transform=axes[1].transAxes, color=MUTED)
            axes[1].set_xlim(-1, len(sorted_benchmark))
            for ax in axes:
                ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "narrative_06_expanded_exhibition_benchmark.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        markdown(
            """
            ## The missing test: all usable exhibition matches versus all earlier official matches

            The earlier analysis asked whether Match 103 was unusual relative to **102 official World Cup matches**. That is an anomaly test, not a serious-versus-exhibition classification test. This section fixes the denominator:

            - **Official class:** all 102 World Cup matches completed before the bronze final.
            - **Exhibition class:** all 19 Soccer Aid or Sidemen Charity matches with a complete shared core of goals, shots, shots on target, fouls, and yellow cards.
            - **Strict holdout:** England-France is excluded from model fitting and validation, then scored once at the end.

            The primary classifier intentionally excludes goals. It asks whether the *way the match generated action and discipline* looked exhibition-like, rather than merely rediscovering the 6-4 score. The 22-row exhibition file also retains three older Sidemen matches with score-only coverage; they remain in the 41-match scoring analysis but cannot enter this intensity model.
            """
        ),
        code(
            """
            # Two-population common-core comparison with Match 103 as a strict holdout
            common_features = [
                "total_goals", "total_shots", "shots_on_target", "total_fouls", "yellow_cards"
            ]
            common_labels = {
                "total_goals": "Goals",
                "total_shots": "Total shots",
                "shots_on_target": "Shots on target",
                "total_fouls": "Fouls",
                "yellow_cards": "Yellow cards",
            }

            official_common = (
                pmsr_match.loc[1:102, ["total_goals", "attempts", "shots_on_target"]]
                .rename(columns={"attempts": "total_shots"})
                .reset_index()
                .merge(
                    match_discipline.loc[
                        match_discipline["match_number"].le(102),
                        ["match_number", "total_fouls", "total_yellow_cards"],
                    ],
                    on="match_number",
                    how="inner",
                    validate="one_to_one",
                )
                .rename(columns={"total_yellow_cards": "yellow_cards"})
            )
            official_common["sample_type"] = "Official World Cup"
            official_common["event_family"] = "2026 FIFA World Cup"
            official_common["source_provider"] = "FIFA"
            official_common["is_holdout"] = False

            exhibition_common = exhibition_intensity.loc[
                exhibition_intensity["coverage_status"].eq("complete_core"),
                ["event", "year", "source_provider", *common_features],
            ].copy()
            exhibition_common = exhibition_common.rename(columns={"event": "event_family"})
            exhibition_common["match_number"] = pd.NA
            exhibition_common["sample_type"] = "Exhibition"
            exhibition_common["is_holdout"] = False

            holdout_common = (
                pmsr_match.loc[[103], ["total_goals", "attempts", "shots_on_target"]]
                .rename(columns={"attempts": "total_shots"})
                .reset_index()
                .merge(
                    match_discipline.loc[
                        match_discipline["match_number"].eq(103),
                        ["match_number", "total_fouls", "total_yellow_cards"],
                    ],
                    on="match_number",
                    how="inner",
                    validate="one_to_one",
                )
                .rename(columns={"total_yellow_cards": "yellow_cards"})
            )
            holdout_common["sample_type"] = "Match 103 holdout"
            holdout_common["event_family"] = "England 6-4 France"
            holdout_common["source_provider"] = "FIFA"
            holdout_common["is_holdout"] = True

            official_train = official_common[["sample_type", "event_family", "source_provider", "match_number", "is_holdout", *common_features]].copy()
            exhibition_train = exhibition_common[["sample_type", "event_family", "source_provider", "match_number", "is_holdout", *common_features]].copy()
            target_row = holdout_common.iloc[0]
            comparison_panel = pd.concat([
                official_train,
                exhibition_train,
                holdout_common[["sample_type", "event_family", "source_provider", "match_number", "is_holdout", *common_features]],
            ], ignore_index=True)

            assert len(official_train) == 102
            assert len(exhibition_train) == 19
            assert comparison_panel["is_holdout"].sum() == 1
            assert comparison_panel.loc[~comparison_panel["is_holdout"], "match_number"].dropna().astype(int).max() == 102
            assert official_train[common_features].notna().all(axis=1).all()
            assert exhibition_train[common_features].notna().all(axis=1).all()

            comparison_summary_rows = []
            for sample_name, frame in (("Official World Cup", official_train), ("Exhibition", exhibition_train)):
                for metric in common_features:
                    values = frame[metric].astype(float)
                    comparison_summary_rows.append({
                        "sample_type": sample_name,
                        "metric": metric,
                        "label": common_labels[metric],
                        "matches": len(values),
                        "mean": float(values.mean()),
                        "median": float(values.median()),
                        "q1": float(values.quantile(0.25)),
                        "q3": float(values.quantile(0.75)),
                        "sd": float(values.std(ddof=1)),
                    })
            comparison_summary = pd.DataFrame(comparison_summary_rows)

            test_rows = []
            for metric in common_features:
                exhibition_values = exhibition_train[metric].astype(float).to_numpy()
                official_values = official_train[metric].astype(float).to_numpy()
                u_stat, p_value = stats.mannwhitneyu(
                    exhibition_values,
                    official_values,
                    alternative="two-sided",
                    method="asymptotic",
                )
                cliffs_delta = 2 * u_stat / (len(exhibition_values) * len(official_values)) - 1
                test_rows.append({
                    "metric": metric,
                    "label": common_labels[metric],
                    "official_median": float(np.median(official_values)),
                    "exhibition_median": float(np.median(exhibition_values)),
                    "target_value": float(target_row[metric]),
                    "mann_whitney_u": float(u_stat),
                    "raw_p": float(p_value),
                    "cliffs_delta_exhibition_minus_official": float(cliffs_delta),
                    "target_percentile_within_official": float(stats.percentileofscore(official_values, target_row[metric], kind="weak")),
                    "target_percentile_within_exhibition": float(stats.percentileofscore(exhibition_values, target_row[metric], kind="weak")),
                })
            common_tests = pd.DataFrame(test_rows)
            raw_common_p = common_tests["raw_p"].to_numpy()
            common_p_order = np.argsort(raw_common_p)
            common_p_sorted_adjusted = np.maximum.accumulate(
                (len(raw_common_p) - np.arange(len(raw_common_p))) * raw_common_p[common_p_order]
            )
            common_p_adjusted = np.empty_like(raw_common_p)
            common_p_adjusted[common_p_order] = np.minimum(common_p_sorted_adjusted, 1.0)
            common_tests["holm_adjusted_p"] = common_p_adjusted

            model_train = pd.concat([
                official_train.assign(exhibition_label=0),
                exhibition_train.assign(exhibition_label=1),
            ], ignore_index=True)

            def add_comparison_rates(frame: pd.DataFrame) -> pd.DataFrame:
                enriched = frame.copy()
                enriched["shot_accuracy"] = enriched["shots_on_target"] / enriched["total_shots"]
                enriched["goal_conversion"] = enriched["total_goals"] / enriched["total_shots"]
                enriched["cards_per_10_fouls"] = 10 * enriched["yellow_cards"] / enriched["total_fouls"]
                return enriched

            model_train = add_comparison_rates(model_train)
            target_model = add_comparison_rates(pd.DataFrame([target_row]))

            model_specs = {
                "Process only (no goals)": ["total_shots", "shots_on_target", "total_fouls", "yellow_cards"],
                "Process rates (no goals)": ["total_shots", "shot_accuracy", "total_fouls", "cards_per_10_fouls"],
                "Process plus goals": common_features,
            }

            def new_exhibition_model():
                return make_pipeline(
                    StandardScaler(),
                    LogisticRegression(
                        C=1.0,
                        class_weight="balanced",
                        solver="liblinear",
                        random_state=SEED,
                    ),
                )

            y_model = model_train["exhibition_label"].astype(int).to_numpy()
            model_validation_rows = []
            model_oof_scores = {}
            fitted_models = {}
            for model_name, model_features in model_specs.items():
                X_model = model_train[model_features]
                repeat_metrics = []
                repeated_oof = []
                for repeat in range(50):
                    fold_predictions = np.zeros(len(model_train), dtype=float)
                    splitter = StratifiedKFold(
                        n_splits=5,
                        shuffle=True,
                        random_state=SEED + repeat,
                    )
                    for train_index, test_index in splitter.split(X_model, y_model):
                        fold_model = new_exhibition_model()
                        fold_model.fit(X_model.iloc[train_index], y_model[train_index])
                        fold_predictions[test_index] = fold_model.predict_proba(X_model.iloc[test_index])[:, 1]
                    repeat_metrics.append({
                        "auc": roc_auc_score(y_model, fold_predictions),
                        "balanced_accuracy": balanced_accuracy_score(y_model, fold_predictions >= 0.5),
                        "brier_score": brier_score_loss(y_model, fold_predictions),
                    })
                    repeated_oof.append(fold_predictions)

                repeat_metrics = pd.DataFrame(repeat_metrics)
                average_oof = np.mean(np.vstack(repeated_oof), axis=0)
                fitted_model = new_exhibition_model().fit(X_model, y_model)
                target_score = float(fitted_model.predict_proba(target_model[model_features])[:, 1][0])
                fitted_models[model_name] = fitted_model
                model_oof_scores[model_name] = average_oof
                model_validation_rows.append({
                    "model": model_name,
                    "features": ", ".join(model_features),
                    "official_matches": int((y_model == 0).sum()),
                    "exhibition_matches": int((y_model == 1).sum()),
                    "repeated_cv_auc_mean": float(repeat_metrics["auc"].mean()),
                    "repeated_cv_auc_p05": float(repeat_metrics["auc"].quantile(0.05)),
                    "repeated_cv_auc_p95": float(repeat_metrics["auc"].quantile(0.95)),
                    "repeated_cv_balanced_accuracy_mean": float(repeat_metrics["balanced_accuracy"].mean()),
                    "repeated_cv_brier_mean": float(repeat_metrics["brier_score"].mean()),
                    "target_exhibition_likeness_score": target_score,
                })
            model_validation = pd.DataFrame(model_validation_rows)

            primary_model_name = "Process only (no goals)"
            primary_features = model_specs[primary_model_name]
            primary_target_score = float(
                model_validation.loc[
                    model_validation["model"].eq(primary_model_name),
                    "target_exhibition_likeness_score",
                ].iloc[0]
            )

            bootstrap_rng = np.random.default_rng(SEED + 404)
            official_model_rows = model_train[model_train["exhibition_label"].eq(0)].reset_index(drop=True)
            exhibition_model_rows = model_train[model_train["exhibition_label"].eq(1)].reset_index(drop=True)
            target_bootstrap_scores = []
            for _ in range(2_000):
                official_indices = bootstrap_rng.integers(0, len(official_model_rows), len(official_model_rows))
                exhibition_indices = bootstrap_rng.integers(0, len(exhibition_model_rows), len(exhibition_model_rows))
                bootstrap_sample = pd.concat([
                    official_model_rows.iloc[official_indices],
                    exhibition_model_rows.iloc[exhibition_indices],
                ], ignore_index=True)
                bootstrap_model = new_exhibition_model().fit(
                    bootstrap_sample[primary_features],
                    bootstrap_sample["exhibition_label"].astype(int),
                )
                target_bootstrap_scores.append(float(
                    bootstrap_model.predict_proba(target_model[primary_features])[:, 1][0]
                ))
            target_bootstrap_scores = np.asarray(target_bootstrap_scores)
            primary_score_ci = np.quantile(target_bootstrap_scores, [0.025, 0.975])
            classifier_uncertainty = pd.DataFrame([{
                "model": primary_model_name,
                "bootstrap_draws": len(target_bootstrap_scores),
                "target_score_median": float(np.median(target_bootstrap_scores)),
                "target_score_p025": float(primary_score_ci[0]),
                "target_score_p975": float(primary_score_ci[1]),
            }])

            event_sensitivity_rows = []
            for event_family in ["Soccer Aid", "Sidemen Charity Match"]:
                event_rows = model_train[
                    model_train["sample_type"].eq("Exhibition")
                    & model_train["event_family"].eq(event_family)
                ]
                event_training = pd.concat([official_model_rows, event_rows], ignore_index=True)
                event_model = new_exhibition_model().fit(
                    event_training[primary_features],
                    event_training["exhibition_label"].astype(int),
                )
                event_sensitivity_rows.append({
                    "exhibition_family_used": event_family,
                    "exhibition_matches": len(event_rows),
                    "official_matches": len(official_model_rows),
                    "target_exhibition_likeness_score": float(
                        event_model.predict_proba(target_model[primary_features])[:, 1][0]
                    ),
                })
            event_sensitivity = pd.DataFrame(event_sensitivity_rows)

            comparison_panel.to_csv(TABLES / "v2_official_vs_exhibition_common_core.csv", index=False)
            comparison_summary.to_csv(TABLES / "v2_official_vs_exhibition_summary.csv", index=False)
            common_tests.to_csv(TABLES / "v2_official_vs_exhibition_tests.csv", index=False)
            model_validation.to_csv(TABLES / "v2_exhibition_classifier_validation.csv", index=False)
            event_sensitivity.to_csv(TABLES / "v2_exhibition_classifier_event_sensitivity.csv", index=False)
            classifier_uncertainty.to_csv(TABLES / "v2_exhibition_classifier_uncertainty.csv", index=False)

            display(comparison_summary.pivot(index="label", columns="sample_type", values=["matches", "mean", "median"]).round(2))
            display(common_tests.round(5))
            display(model_validation.round(4))
            display(event_sensitivity.round(4))
            print(
                f"Primary holdout score (goals excluded): {primary_target_score:.3f}; "
                f"match-bootstrap 95% interval {primary_score_ci[0]:.3f} to {primary_score_ci[1]:.3f}."
            )

            # Technical visual: distributions plus the held-out classifier score
            plot_rng = np.random.default_rng(SEED + 505)
            fig, axes = plt.subplots(2, 3, figsize=(14.8, 8.6))
            for ax, metric in zip(axes.flat[:5], common_features):
                official_values = official_train[metric].astype(float).to_numpy()
                exhibition_values = exhibition_train[metric].astype(float).to_numpy()
                boxes = ax.boxplot(
                    [official_values, exhibition_values],
                    positions=[0, 1],
                    widths=0.48,
                    patch_artist=True,
                    showfliers=False,
                    medianprops={"color": INK, "linewidth": 1.5},
                    whiskerprops={"color": MUTED},
                    capprops={"color": MUTED},
                )
                boxes["boxes"][0].set(facecolor=BLUE_LIGHT, edgecolor=BLUE)
                boxes["boxes"][1].set(facecolor=ORANGE_LIGHT, edgecolor=ORANGE)
                ax.scatter(plot_rng.normal(0, 0.055, len(official_values)), official_values, color=BLUE, s=14, alpha=0.42, linewidth=0)
                ax.scatter(plot_rng.normal(1, 0.055, len(exhibition_values)), exhibition_values, color=ORANGE, s=25, alpha=0.72, linewidth=0)
                ax.scatter([2], [target_row[metric]], marker="D", s=82, color=INK, edgecolor="white", linewidth=0.9, zorder=5)
                ax.set_xticks([0, 1, 2], ["Official\\nn=102", "Exhibition\\nn=19", "Match 103\\nholdout"])
                ax.set_title(common_labels[metric], loc="left")
                ax.grid(axis="x", visible=False)
                ax.spines[["top", "right"]].set_visible(False)

            score_ax = axes.flat[5]
            primary_oof = model_oof_scores[primary_model_name]
            official_scores = primary_oof[y_model == 0]
            exhibition_scores = primary_oof[y_model == 1]
            score_boxes = score_ax.boxplot(
                [official_scores, exhibition_scores],
                positions=[0, 1],
                widths=0.48,
                patch_artist=True,
                showfliers=False,
                medianprops={"color": INK, "linewidth": 1.5},
            )
            score_boxes["boxes"][0].set(facecolor=BLUE_LIGHT, edgecolor=BLUE)
            score_boxes["boxes"][1].set(facecolor=ORANGE_LIGHT, edgecolor=ORANGE)
            score_ax.scatter(plot_rng.normal(0, 0.055, len(official_scores)), official_scores, color=BLUE, s=14, alpha=0.42, linewidth=0)
            score_ax.scatter(plot_rng.normal(1, 0.055, len(exhibition_scores)), exhibition_scores, color=ORANGE, s=25, alpha=0.72, linewidth=0)
            score_ax.scatter([2], [primary_target_score], marker="D", s=82, color=INK, edgecolor="white", linewidth=0.9, zorder=5)
            score_ax.vlines(2, primary_score_ci[0], primary_score_ci[1], color=INK, linewidth=2)
            score_ax.set_xticks([0, 1, 2], ["Official\\nOOF", "Exhibition\\nOOF", "Match 103\\nholdout"])
            score_ax.set_ylim(-0.04, 1.04)
            score_ax.set_ylabel("Exhibition-likeness diagnostic score")
            score_ax.set_title("Primary model - goals excluded", loc="left")
            score_ax.text(
                0.02,
                0.96,
                f"Repeated-CV AUC {model_validation.loc[model_validation['model'].eq(primary_model_name), 'repeated_cv_auc_mean'].iloc[0]:.3f}",
                transform=score_ax.transAxes,
                va="top",
                color=MUTED,
            )
            score_ax.grid(axis="x", visible=False)
            score_ax.spines[["top", "right"]].set_visible(False)

            fig.suptitle("One held-out match against two labeled populations", x=0.06, ha="left", fontsize=18, fontweight="bold", color=INK)
            fig.text(0.06, 0.925, "Five common metrics; black diamonds are England-France and were never used to train the classifier", color=MUTED, fontsize=11)
            fig.tight_layout(rect=[0, 0, 1, 0.91])
            fig.savefig(ASSETS / "v2_official_vs_exhibition_holdout.png", dpi=180, bbox_inches="tight")
            plt.show()

            # Reader-facing narrative card
            from matplotlib.patches import FancyBboxPatch

            narrative_fig, narrative_ax = plt.subplots(figsize=(16, 9), facecolor="#08111F")
            narrative_ax.set_facecolor("#08111F")
            narrative_ax.axis("off")
            narrative_ax.text(0.055, 0.92, "BUKAN LAGI 1 PERTANDINGAN vs 102 NORMAL", color="white", fontsize=25, fontweight="bold", transform=narrative_ax.transAxes)
            narrative_ax.text(0.055, 0.865, "Sekarang: 102 laga resmi vs 19 exhibition lengkap | England-France murni holdout", color="#AFC2DB", fontsize=14, transform=narrative_ax.transAxes)

            official_medians = official_train[common_features].median()
            exhibition_medians = exhibition_train[common_features].median()
            cards = [
                (0.055, "LAGA RESMI", "n=102 | median", BLUE, official_medians),
                (0.365, "ENGLAND 6-4 FRANCE", "holdout | aktual", "#F4C95D", target_row),
                (0.675, "EXHIBITION", "n=19 | median", ORANGE, exhibition_medians),
            ]
            for x0, title, subtitle, color, values in cards:
                narrative_ax.add_patch(FancyBboxPatch(
                    (x0, 0.36), 0.27, 0.41,
                    boxstyle="round,pad=0.012,rounding_size=0.018",
                    facecolor="#101D30", edgecolor=color, linewidth=2,
                    transform=narrative_ax.transAxes,
                ))
                narrative_ax.text(x0 + 0.02, 0.715, title, color=color, fontsize=16, fontweight="bold", transform=narrative_ax.transAxes)
                narrative_ax.text(x0 + 0.02, 0.675, subtitle, color="#8FA6C2", fontsize=11, transform=narrative_ax.transAxes)
                narrative_lines = [
                    ("Gol", values["total_goals"]),
                    ("Tembakan", values["total_shots"]),
                    ("Tepat sasaran", values["shots_on_target"]),
                    ("Foul", values["total_fouls"]),
                    ("Kartu kuning", values["yellow_cards"]),
                ]
                for line_no, (label, value) in enumerate(narrative_lines):
                    y0 = 0.61 - line_no * 0.052
                    narrative_ax.text(x0 + 0.02, y0, label, color="#B7C7DA", fontsize=12, transform=narrative_ax.transAxes)
                    narrative_ax.text(x0 + 0.235, y0, f"{value:g}", color="white", fontsize=14, fontweight="bold", ha="right", transform=narrative_ax.transAxes)

            auc_value = model_validation.loc[model_validation["model"].eq(primary_model_name), "repeated_cv_auc_mean"].iloc[0]
            family_low = event_sensitivity["target_exhibition_likeness_score"].min()
            family_high = event_sensitivity["target_exhibition_likeness_score"].max()
            narrative_ax.add_patch(FancyBboxPatch(
                (0.055, 0.12), 0.89, 0.16,
                boxstyle="round,pad=0.014,rounding_size=0.018",
                facecolor="#172A43", edgecolor="#345A84", linewidth=1.4,
                transform=narrative_ax.transAxes,
            ))
            narrative_ax.text(0.075, 0.225, "Bahkan tanpa gol: skor exhibition-like = {:.2f}/1".format(primary_target_score), color="white", fontsize=21, fontweight="bold", transform=narrative_ax.transAxes)
            narrative_ax.text(0.075, 0.177, f"Validasi silang AUC {auc_value:.2f} | sensitivitas keluarga event {family_low:.2f}-{family_high:.2f}", color="#AFC2DB", fontsize=13, transform=narrative_ax.transAxes)
            narrative_ax.text(0.075, 0.138, "Bold insight: aksi exhibition-like - foul normal, serangan meledak, kartu lenyap.", color="#F4C95D", fontsize=13.5, fontweight="bold", transform=narrative_ax.transAxes)
            narrative_ax.text(0.055, 0.055, "Skor diagnostik bukan probabilitas settingan. Ini menguji kemiripan perilaku observabel, bukan niat atau koordinasi.", color="#7F96B3", fontsize=11.5, transform=narrative_ax.transAxes)
            narrative_fig.savefig(ASSETS / "narrative_08_two_population_verdict.png", dpi=180, bbox_inches="tight", facecolor=narrative_fig.get_facecolor())
            plt.show()
            """
        ),
        markdown(
            """
            ### Two-population verdict

            This is the direct answer the earlier design could not provide. The exhibition and official distributions differ in all five shared metrics after Holm correction. Exhibition matches had more shots, more shots on target, and more goals, but fewer fouls and fewer yellow cards. Englandâ€“France combined an exhibition-level attacking profile with an ordinary official-match foul count and an exhibition-side card profile.

            The primary **no-goals** model produced a held-out exhibition-likeness score of about **0.98**. Its repeated five-fold validation AUC was about **0.958** with balanced accuracy about **0.887**. Adding goals barely changed the conclusion. Event-family sensitivity was widerâ€”about **0.61** when Sidemen alone defined exhibition and **0.99** when Soccer Aid alone didâ€”because only four Sidemen matches have complete intensity data and their scoring is much more extreme.

            **H4 verdict: supported with moderate-high confidence as an observable match profile.** The match did not merely have an exhibition-like score; its non-goal action-and-discipline geometry was also on the exhibition side. This does not mean the teams were physically idle, and the diagnostic score is not a probability of fixing, coordination, or private intent.
            """
        ),
        code(
            """
            # Official FIFA process metrics and lineup rotation
            current_process = pmsr_match.loc[103]
            earlier_process = pmsr_match.loc[:102]
            metric_labels = {
                "total_goals": "Goals",
                "total_xg": "Total xG",
                "attempts": "Attempts",
                "shots_on_target": "Shots on target",
                "line_breaks": "Completed line breaks",
                "pressures": "Defensive pressures",
                "direct_pressures": "Direct pressures",
                "forced_turnovers": "Forced turnovers",
                "turnovers_per_100_pressures": "Turnovers per 100 pressures",
            }
            process_rows = []
            for metric, label in metric_labels.items():
                value = float(current_process[metric])
                process_rows.append({
                    "metric": metric,
                    "label": label,
                    "current_value": value,
                    "earlier_median": float(earlier_process[metric].median()),
                    "earlier_min": float(earlier_process[metric].min()),
                    "earlier_max": float(earlier_process[metric].max()),
                    "percentile": 100 * float((earlier_process[metric] < value).mean()),
                })
            process_percentiles = pd.DataFrame(process_rows)

            rotation_rows = []
            semifinal_match = {"France": 101, "England": 102}
            for team in ("France", "England"):
                semifinal_starters = set(lineups.loc[(lineups["team"].eq(team)) & (lineups["match_number"].eq(semifinal_match[team])), "player"])
                third_place_starters = set(lineups.loc[(lineups["team"].eq(team)) & (lineups["match_number"].eq(103)), "player"])
                retained = sorted(semifinal_starters & third_place_starters)
                rotation_rows.append({
                    "team": team,
                    "retained_starters": len(retained),
                    "starter_changes": 11 - len(retained),
                    "retained_players": ", ".join(retained),
                })
            rotation = pd.DataFrame(rotation_rows)
            assert rotation["starter_changes"].eq(7).all()

            team_process_rows = []
            for team in ("France", "England"):
                prior = pmsr[(pmsr["team_name"].eq(team)) & pmsr["match_number"].lt(103)]
                current = pmsr[(pmsr["team_name"].eq(team)) & pmsr["match_number"].eq(103)].iloc[0]
                for metric in ("xg", "attempts_at_goal", "shots_on_target", "defensive_pressures", "direct_pressures", "forced_turnovers"):
                    team_process_rows.append({
                        "team": team,
                        "metric": metric,
                        "current": float(current[metric]),
                        "prior_tournament_mean": float(prior[metric].mean()),
                        "prior_matches": len(prior),
                    })
            team_process = pd.DataFrame(team_process_rows)

            process_percentiles.to_csv(TABLES / "v2_fifa_process_percentiles.csv", index=False)
            rotation.to_csv(TABLES / "v2_lineup_rotation.csv", index=False)
            team_process.to_csv(TABLES / "v2_same_team_process.csv", index=False)
            display(process_percentiles.round(2))
            display(rotation)
            display(team_process.pivot(index=["team", "prior_matches"], columns="metric", values=["current", "prior_tournament_mean"]).round(2))

            fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.1), gridspec_kw={"width_ratios": [1.65, 1]})
            process_plot = process_percentiles.iloc[::-1].reset_index(drop=True)
            y = np.arange(len(process_plot))
            point_colors = [ORANGE if metric in {"forced_turnovers", "turnovers_per_100_pressures"} else BLUE for metric in process_plot["metric"]]
            axes[0].hlines(y, 0, process_plot["percentile"], color=GRID, linewidth=3)
            axes[0].scatter(process_plot["percentile"], y, s=85, c=point_colors, edgecolor=INK, linewidth=0.6, zorder=3)
            axes[0].axvline(50, color=INK, linestyle="--", linewidth=1)
            axes[0].set_yticks(y, process_plot["label"])
            axes[0].set_xlim(0, 110)
            axes[0].set_xlabel("Percentile among matches 1–102")
            axes[0].set_title("Match 103 process percentiles", loc="left", pad=30)
            axes[0].text(0, 1.01, "Official FIFA PMSR; current match excluded from reference", transform=axes[0].transAxes, color=MUTED)
            for yi, percentile, value in zip(y, process_plot["percentile"], process_plot["current_value"]):
                axes[0].text(min(percentile + 2, 100), yi, f"{percentile:.0f}th · {value:.1f}", va="center", fontsize=8.5, color=INK)

            teams = rotation["team"].tolist()
            retained = rotation["retained_starters"].to_numpy()
            changed = rotation["starter_changes"].to_numpy()
            axes[1].barh(teams, retained, color=BLUE_LIGHT, edgecolor=INK, label="Retained")
            axes[1].barh(teams, changed, left=retained, color=ORANGE, edgecolor=INK, label="Changed")
            for idx, (keep, change) in enumerate(zip(retained, changed)):
                axes[1].text(keep / 2, idx, f"{keep}\\nretained", ha="center", va="center", fontweight="bold")
                axes[1].text(keep + change / 2, idx, f"{change}\\nchanged", ha="center", va="center", color="white", fontweight="bold")
            axes[1].set_xlim(0, 11)
            axes[1].set_xlabel("Starting XI players")
            axes[1].set_title("Starter retention from semi-final", loc="left", pad=30)
            axes[1].text(0, 1.01, "Official FIFA team-summary pages", transform=axes[1].transAxes, color=MUTED)
            for ax in axes:
                ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_fifa_process_and_rotation.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        markdown(
            """
            ## Individual stakes can survive lower team stakes

            The bronze match counted fully toward official player awards. Immediately before kick-off, FIFA listed Lionel Messi and Kylian Mbappe on eight goals, with Messi ahead on the assist tie-break; Michael Olise led the tournament assist table with five. France then retained **Mbappe and Olise among only four semi-final starters**.

            The match materially changed those individual outcomes:

            - Mbappe scored twice: **8 → 10 tournament goals**, moving into the provisional Golden Boot lead and reaching 22 career World Cup goals.
            - Olise was credited with both Mbappe assists: **5 → 7 tournament assists**, extending his lead and passing FIFA's listed single-tournament benchmark of six.
            - Bellingham began on the bench but scored after entering: **6 → 7 tournament goals**, setting an England single-World-Cup record.
            - Kane also began on the bench and stayed at six, which is an important counterexample to a universal stat-padding explanation.

            This completes part of the incentive puzzle: **team-level pressure can fall while individual attacking incentives remain high**. It does not prove that any player chose a selfish action, and the pattern is selective rather than shared by everyone.

            Sources: [FIFA pre-match Golden Boot table and criteria](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/adidas-golden-boot-race-top-scorer), [FIFA pre-match assist table](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/most-assists-top-assisters), [AP post-match report](https://apnews.com/article/world-cup-england-france-third-place-score-52f94eda6ff6d268d38aaefbc446c525), and [reported Olise assist update](https://as.com/us/futbol/mundial/michael-olise-supera-a-pele-y-rompe-record-historico-de-asistencias-en-un-mundial-f202607-n/).
            """
        ),
        code(
            """
            # Before-versus-after audit of individual award incentives
            incentive_plot = player_incentives.copy()
            incentive_plot["display_label"] = incentive_plot["player"] + "\\n" + incentive_plot["metric"]
            incentive_plot.to_csv(TABLES / "v2_player_incentive_evidence.csv", index=False)

            france_semi = set(lineups.loc[(lineups["team"].eq("France")) & lineups["match_number"].eq(101), "player"])
            france_bronze = set(lineups.loc[(lineups["team"].eq("France")) & lineups["match_number"].eq(103), "player"])
            england_bronze = set(lineups.loc[(lineups["team"].eq("England")) & lineups["match_number"].eq(103), "player"])
            assert {"Kylian Mbappe", "Michael Olise"}.issubset(france_semi & france_bronze)
            assert {"Harry Kane", "Jude Bellingham"}.isdisjoint(england_bronze)

            display(incentive_plot[[
                "player", "team", "metric", "pre_match_value", "match_added",
                "post_match_value", "selection_status", "post_match_consequence", "evidence_strength"
            ]])

            fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.3), gridspec_kw={"width_ratios": [1.45, 1]})
            ordered = incentive_plot.iloc[::-1].reset_index(drop=True)
            y = np.arange(len(ordered))
            pre = ordered["pre_match_value"].to_numpy()
            added = ordered["match_added"].to_numpy()

            axes[0].barh(y, pre, color=BLUE_LIGHT, edgecolor=INK, label="Before match")
            axes[0].barh(y, added, left=pre, color=ORANGE, edgecolor=INK, label="Added in match")
            axes[0].set_yticks(y, ordered["display_label"])
            axes[0].set_xlim(0, 11)
            axes[0].set_xlabel("Tournament goals or assists")
            axes[0].set_title("The bronze match changed individual standings", loc="left", pad=30)
            axes[0].text(0, 1.01, "Timestamped pre-match total + match contribution = post-match total", transform=axes[0].transAxes, color=MUTED)
            for yi, before, gain, after in zip(y, pre, added, ordered["post_match_value"]):
                axes[0].text(after + 0.18, yi, f"{before:.0f} + {gain:.0f} = {after:.0f}", va="center", color=INK, fontweight="bold")
            axes[0].legend(loc="lower right")
            axes[0].spines[["top", "right"]].set_visible(False)

            axes[1].axis("off")
            axes[1].set_title("Selection makes the mechanism selective", loc="left", pad=30)
            axes[1].text(0.02, 0.88, "FRANCE", color=BLUE, fontsize=14, fontweight="bold", transform=axes[1].transAxes)
            axes[1].text(0.02, 0.78, "7 starter changes", fontsize=18, fontweight="bold", color=INK, transform=axes[1].transAxes)
            axes[1].text(0.02, 0.62, "Mbappe + Olise retained\\n2 of only 4 retained starters\\nwere live individual-award leaders", fontsize=12, color=INK, linespacing=1.5, transform=axes[1].transAxes)
            axes[1].text(0.02, 0.42, "ENGLAND", color=ORANGE, fontsize=14, fontweight="bold", transform=axes[1].transAxes)
            axes[1].text(0.02, 0.32, "7 starter changes", fontsize=18, fontweight="bold", color=INK, transform=axes[1].transAxes)
            axes[1].text(0.02, 0.16, "Kane + Bellingham began on bench\\nBellingham entered late and scored;\\nKane made no statistical gain", fontsize=12, color=INK, linespacing=1.5, transform=axes[1].transAxes)
            axes[1].text(0.02, 0.01, "Conclusion: plausible attacking incentive,\\nnot a universal stat-padding pact.", fontsize=11, color=MUTED, fontstyle="italic", transform=axes[1].transAxes)

            fig.tight_layout()
            fig.savefig(ASSETS / "v2_individual_incentives.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        markdown(
            """
            ## Did the players physically coast—or did coordination fail?

            FIFA's player tables allow a cleaner separation between **individual work** and **collective control**. This section uses all eight France matches and all eight England matches. Match 103 is compared with each player's own earlier-tournament rate rather than with a different squad or competition.

            The primary player comparison includes 19 outfielders who played at least 45 minutes in Match 103 and had at least two earlier appearances totalling 90 minutes. It is an observational, exploratory comparison: teammates share tactics and score states, so the player rows are not perfectly independent.
            """
        ),
        code(
            """
            # Player-level effort, attacking behaviour, and finishing decomposition
            focal_process = pmsr[[
                "match_number", "team_name", "opponent_team_name", "goals", "xg",
                "attempts_at_goal", "shots_on_target", "completed_line_breaks",
                "defensive_pressures", "direct_pressures", "forced_turnovers",
            ]].rename(columns={
                "team_name": "team",
                "opponent_team_name": "opponent",
                "goals": "fifa_goals",
                "xg": "team_xg",
                "attempts_at_goal": "fifa_attempts",
                "shots_on_target": "team_shots_on_target",
                "completed_line_breaks": "team_completed_line_breaks",
                "direct_pressures": "fifa_direct_pressures",
            })
            effort_control = team_physical.merge(
                focal_process,
                on=["match_number", "team", "opponent"],
                how="left",
                validate="one_to_one",
            )
            opponent_process = pmsr[[
                "match_number", "team_name", "xg", "shots_on_target", "completed_line_breaks"
            ]].rename(columns={
                "team_name": "opponent",
                "xg": "opponent_xg",
                "shots_on_target": "opponent_shots_on_target",
                "completed_line_breaks": "opponent_completed_line_breaks",
            })
            effort_control = effort_control.merge(
                opponent_process,
                on=["match_number", "opponent"],
                how="left",
                validate="many_to_one",
            )
            effort_control["turnovers_per_100_pressures"] = (
                100 * effort_control["forced_turnovers"] / effort_control["defensive_pressures"]
            )
            effort_control["high_intensity_km_per90"] = (
                effort_control["high_intensity_distance_m_per90"] / 1_000
            )

            # Independent parser reconciliation against FIFA's match-summary totals.
            assert effort_control["goals"].eq(effort_control["fifa_goals"]).all()
            assert effort_control["attempts_at_goal"].eq(effort_control["fifa_attempts"]).all()
            assert effort_control["pressures_direct"].eq(effort_control["fifa_direct_pressures"]).all()
            player_team_reconciliations = int(
                effort_control["goals"].eq(effort_control["fifa_goals"]).sum()
                + effort_control["attempts_at_goal"].eq(effort_control["fifa_attempts"]).sum()
                + effort_control["pressures_direct"].eq(effort_control["fifa_direct_pressures"]).sum()
            )
            quality_checks = pd.concat([
                quality_checks,
                pd.DataFrame([{
                    "check": "Player-derived goals, attempts, and direct pressures reconcile FIFA team totals",
                    "observed": player_team_reconciliations,
                    "expected": 48,
                    "status": "pass" if player_team_reconciliations == 48 else "fail",
                }]),
            ], ignore_index=True)

            rank_metrics = {
                "total_distance_m_per90": ("Total distance per 90", False),
                "high_intensity_distance_m_per90": ("Distance at 20+ km/h per 90", False),
                "sprints_per90": ("Sprints per 90", False),
                "fifa_direct_pressures": ("Direct pressures", False),
                "turnovers_per_100_pressures": ("Turnovers per 100 pressures", False),
                "opponent_xg": ("Opponent xG", True),
                "opponent_completed_line_breaks": ("Opponent completed line breaks", True),
            }
            team_rank_rows = []
            for team in ("France", "England"):
                team_matches = effort_control[effort_control["team"].eq(team)].copy()
                current_row = team_matches[team_matches["match_number"].eq(103)].iloc[0]
                for metric, (label, higher_is_worse) in rank_metrics.items():
                    descending_rank = int(
                        team_matches[metric].rank(method="min", ascending=False)
                        .loc[team_matches["match_number"].eq(103)].iloc[0]
                    )
                    team_rank_rows.append({
                        "team": team,
                        "metric": metric,
                        "label": label,
                        "current_value": float(current_row[metric]),
                        "rank_high_to_low": descending_rank,
                        "matches": len(team_matches),
                        "higher_is_worse": higher_is_worse,
                        "empirical_percentile": 100 * float((team_matches[metric] <= current_row[metric]).mean()),
                    })
            effort_ranks = pd.DataFrame(team_rank_rows)

            player_work = player_match.copy()
            player_work["high_intensity_distance_m"] = (
                player_work["zone4_distance_m"] + player_work["zone5_distance_m"]
            )
            effort_metrics = {
                "total_distance_m": "Total distance per 90",
                "high_intensity_distance_m": "Distance at 20+ km/h per 90",
                "sprints": "Sprints per 90",
                "pressures_direct": "Direct pressures per 90",
            }
            current_players = player_work[
                player_work["match_number"].eq(103)
                & player_work["position"].ne("GK")
                & player_work["minutes"].ge(45)
            ].copy()
            prior_players = player_work[
                player_work["match_number"].lt(103)
                & player_work["position"].ne("GK")
                & player_work["minutes"].ge(15)
            ].copy()

            prior_baseline = prior_players.groupby(["team", "player"]).agg(
                prior_minutes=("minutes", "sum"),
                prior_matches=("match_number", "nunique"),
                **{f"prior_{metric}": (metric, "sum") for metric in effort_metrics},
            )
            for metric in effort_metrics:
                prior_baseline[f"{metric}_baseline_p90"] = (
                    prior_baseline[f"prior_{metric}"] / prior_baseline["prior_minutes"] * 90
                )
                current_players[f"{metric}_current_p90"] = (
                    current_players[metric] / current_players["minutes"] * 90
                )
            player_effort = current_players.merge(
                prior_baseline.reset_index(),
                on=["team", "player"],
                how="left",
                validate="one_to_one",
            )
            player_effort = player_effort[
                player_effort["prior_minutes"].ge(90)
                & player_effort["prior_matches"].ge(2)
            ].copy()
            assert len(player_effort) == 19

            test_rng = np.random.default_rng(SEED + 103)
            player_test_rows = []
            for metric, label in effort_metrics.items():
                current_values = player_effort[f"{metric}_current_p90"].to_numpy()
                baseline_values = player_effort[f"{metric}_baseline_p90"].to_numpy()
                differences = current_values - baseline_values
                n_players = len(differences)
                bootstrap_indices = test_rng.integers(0, n_players, size=(20_000, n_players))
                bootstrap_means = differences[bootstrap_indices].mean(axis=1)
                signs = test_rng.choice([-1, 1], size=(100_000, n_players))
                null_means = (signs * differences).mean(axis=1)
                observed_delta = float(differences.mean())
                permutation_p = float(
                    (1 + (np.abs(null_means) >= abs(observed_delta)).sum()) / (len(null_means) + 1)
                )
                player_test_rows.append({
                    "metric": metric,
                    "label": label,
                    "players": n_players,
                    "current_mean": float(current_values.mean()),
                    "prior_mean": float(baseline_values.mean()),
                    "mean_delta": observed_delta,
                    "relative_delta_pct": 100 * observed_delta / float(baseline_values.mean()),
                    "bootstrap_ci_low": float(np.quantile(bootstrap_means, 0.025)),
                    "bootstrap_ci_high": float(np.quantile(bootstrap_means, 0.975)),
                    "sign_flip_p": permutation_p,
                    "players_above_baseline": int((differences > 0).sum()),
                })
            player_effort_tests = pd.DataFrame(player_test_rows)
            # Four related outcomes are examined. Holm adjustment controls the
            # family-wise error rate and keeps the exploratory interpretation honest.
            raw_player_p = player_effort_tests["sign_flip_p"].to_numpy()
            player_p_order = np.argsort(raw_player_p)
            player_p_sorted_adjusted = np.maximum.accumulate(
                (len(raw_player_p) - np.arange(len(raw_player_p))) * raw_player_p[player_p_order]
            )
            player_p_adjusted = np.empty_like(raw_player_p)
            player_p_adjusted[player_p_order] = np.minimum(player_p_sorted_adjusted, 1.0)
            player_effort_tests["holm_adjusted_p"] = player_p_adjusted

            # Award-candidate behaviour: counts, per-90 rates, and team shot share.
            team_attempt_totals = player_work.groupby(
                ["match_number", "team"], as_index=False
            )["attempts_at_goal"].sum().rename(columns={"attempts_at_goal": "team_attempts"})
            player_with_team = player_work.merge(
                team_attempt_totals,
                on=["match_number", "team"],
                validate="many_to_one",
            )
            candidate_rows = []
            for candidate in ("Kylian Mbappe", "Michael Olise", "Bukayo Saka", "Jude Bellingham", "Harry Kane"):
                candidate_matches = player_with_team[player_with_team["player"].eq(candidate)]
                current_candidate = candidate_matches[candidate_matches["match_number"].eq(103)]
                prior_candidate = candidate_matches[
                    candidate_matches["match_number"].lt(103)
                    & candidate_matches["minutes"].ge(15)
                ]
                row = {
                    "player": candidate,
                    "team": "France" if candidate in {"Kylian Mbappe", "Michael Olise"} else "England",
                    "appeared": not current_candidate.empty,
                    "minutes": float(current_candidate["minutes"].iloc[0]) if not current_candidate.empty else 0.0,
                    "prior_matches": int(prior_candidate["match_number"].nunique()),
                }
                for metric in ("attempts_at_goal", "offers_in_behind", "pressures_direct", "high_intensity_distance_m"):
                    current_count = float(current_candidate[metric].iloc[0]) if not current_candidate.empty else 0.0
                    prior_rate = (
                        float(prior_candidate[metric].sum() / prior_candidate["minutes"].sum() * 90)
                        if prior_candidate["minutes"].sum() > 0 else np.nan
                    )
                    current_rate = (
                        float(current_count / current_candidate["minutes"].iloc[0] * 90)
                        if not current_candidate.empty and current_candidate["minutes"].iloc[0] > 0 else np.nan
                    )
                    row[f"{metric}_current"] = current_count
                    row[f"{metric}_current_p90"] = current_rate
                    row[f"{metric}_prior_p90"] = prior_rate
                    row[f"{metric}_index"] = 100 * current_rate / prior_rate if prior_rate > 0 else np.nan
                    prior_match_rates = prior_candidate[metric] / prior_candidate["minutes"] * 90
                    row[f"{metric}_rank_high_to_low"] = (
                        int(1 + (prior_match_rates > current_rate).sum())
                        if np.isfinite(current_rate) else np.nan
                    )
                    row[f"{metric}_empirical_one_sided_p"] = (
                        float((1 + (prior_match_rates >= current_rate).sum()) / (len(prior_match_rates) + 1))
                        if np.isfinite(current_rate) and len(prior_match_rates) else np.nan
                    )
                row["shot_share_current"] = (
                    float(current_candidate["attempts_at_goal"].iloc[0] / current_candidate["team_attempts"].iloc[0])
                    if not current_candidate.empty else 0.0
                )
                row["shot_share_prior"] = (
                    float(prior_candidate["attempts_at_goal"].sum() / prior_candidate["team_attempts"].sum())
                    if prior_candidate["team_attempts"].sum() > 0 else np.nan
                )
                row["rate_stability"] = "unstable: under 30 minutes" if 0 < row["minutes"] < 30 else "usable"
                candidate_rows.append(row)
            candidate_behavior = pd.DataFrame(candidate_rows)

            current_fifa_teams = focal_process[
                focal_process["match_number"].eq(103)
                & focal_process["team"].isin(["France", "England"])
            ]
            finishing_rows = []
            for team in ("France", "England"):
                team_row = current_fifa_teams[current_fifa_teams["team"].eq(team)].iloc[0]
                finishing_rows.append({
                    "scope": team,
                    "xg": float(team_row["team_xg"]),
                    "goals": int(team_row["fifa_goals"]),
                })
            finishing_rows.append({
                "scope": "Combined",
                "xg": float(current_fifa_teams["team_xg"].sum()),
                "goals": int(current_fifa_teams["fifa_goals"].sum()),
            })
            finishing = pd.DataFrame(finishing_rows)
            finishing["goals_above_xg"] = finishing["goals"] - finishing["xg"]
            finishing["goals_to_xg_ratio"] = finishing["goals"] / finishing["xg"]
            finishing["poisson_tail_p"] = [
                float(stats.poisson.sf(goals - 1, expected))
                for expected, goals in zip(finishing["xg"], finishing["goals"])
            ]

            effort_control.to_csv(TABLES / "v2_effort_control_team_matches.csv", index=False)
            effort_ranks.to_csv(TABLES / "v2_effort_control_ranks.csv", index=False)
            player_effort.to_csv(TABLES / "v2_player_effort_comparison.csv", index=False)
            player_effort_tests.to_csv(TABLES / "v2_player_effort_tests.csv", index=False)
            candidate_behavior.to_csv(TABLES / "v2_candidate_behavior.csv", index=False)
            finishing.to_csv(TABLES / "v2_finishing_decomposition.csv", index=False)

            display(effort_ranks.round(2))
            display(player_effort_tests.round(3))
            display(candidate_behavior[[
                "player", "minutes", "attempts_at_goal_current", "attempts_at_goal_current_p90",
                "attempts_at_goal_prior_p90", "attempts_at_goal_empirical_one_sided_p",
                "shot_share_current", "shot_share_prior", "offers_in_behind_current",
                "offers_in_behind_prior_p90", "offers_in_behind_empirical_one_sided_p",
                "pressures_direct_current", "pressures_direct_prior_p90",
                "pressures_direct_empirical_one_sided_p", "rate_stability",
            ]].round(3))
            display(finishing.round(3))

            # Chart contract: 16 equal-grain team-match points; scatter shows whether
            # high-intensity output translated into pressure outcomes. Team colors are
            # reinforced by labels and filled current-match markers.
            fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.0), gridspec_kw={"width_ratios": [1.5, 1]})
            team_colors = {"France": BLUE, "England": ORANGE}
            prior_effort = effort_control[effort_control["match_number"].lt(103)]
            axes[0].axvline(prior_effort["high_intensity_km_per90"].median(), color=GRID, linestyle="--", linewidth=1)
            axes[0].axhline(prior_effort["turnovers_per_100_pressures"].median(), color=GRID, linestyle="--", linewidth=1)
            for team, color in team_colors.items():
                prior_points = effort_control[
                    effort_control["team"].eq(team) & effort_control["match_number"].lt(103)
                ]
                current_point = effort_control[
                    effort_control["team"].eq(team) & effort_control["match_number"].eq(103)
                ].iloc[0]
                axes[0].scatter(
                    prior_points["high_intensity_km_per90"],
                    prior_points["turnovers_per_100_pressures"],
                    s=58, facecolor=BG, edgecolor=color, linewidth=1.5, label=f"{team} earlier"
                )
                axes[0].scatter(
                    current_point["high_intensity_km_per90"],
                    current_point["turnovers_per_100_pressures"],
                    s=150, marker="*", color=color, edgecolor=INK, linewidth=0.8,
                    label=f"{team} Match 103", zorder=5,
                )
                axes[0].annotate(
                    f"{team}\\n{current_point['high_intensity_km_per90']:.1f} km · {current_point['turnovers_per_100_pressures']:.1f} turnovers/100",
                    (current_point["high_intensity_km_per90"], current_point["turnovers_per_100_pressures"]),
                    xytext=(8, -4 if team == "France" else 8), textcoords="offset points",
                    fontsize=8.5, color=INK,
                )
            axes[0].set_xlabel("Team distance at 20+ km/h per 90 (km)")
            axes[0].set_ylabel("Forced turnovers per 100 defensive pressures")
            axes[0].set_title("Physical intensity versus pressure outcome", loc="left", pad=30)
            axes[0].text(0, 1.01, "France and England at the 2026 World Cup; 16 team-matches", transform=axes[0].transAxes, color=MUTED)
            axes[0].legend(loc="upper left", ncol=2, fontsize=8)
            axes[0].spines[["top", "right"]].set_visible(False)

            axes[1].axis("off")
            axes[1].set_title("Match 103 ranks within each team's eight matches", loc="left", pad=30)
            rank_lookup = effort_ranks.set_index(["team", "metric"])
            axes[1].text(0.02, 0.90, "FRANCE", color=BLUE, fontsize=14, fontweight="bold", transform=axes[1].transAxes)
            axes[1].text(
                0.02, 0.72,
                f"High-intensity distance  #{int(rank_lookup.loc[('France', 'high_intensity_distance_m_per90'), 'rank_high_to_low'])} of 8\\n"
                f"Direct pressures             #{int(rank_lookup.loc[('France', 'fifa_direct_pressures'), 'rank_high_to_low'])} of 8\\n"
                f"Turnover yield               #{int(rank_lookup.loc[('France', 'turnovers_per_100_pressures'), 'rank_high_to_low'])} of 8\\n"
                f"Opponent xG                  #{int(rank_lookup.loc[('France', 'opponent_xg'), 'rank_high_to_low'])} of 8 (worst)",
                fontsize=11.5, linespacing=1.55, color=INK, transform=axes[1].transAxes,
            )
            axes[1].text(0.02, 0.48, "ENGLAND", color=ORANGE, fontsize=14, fontweight="bold", transform=axes[1].transAxes)
            axes[1].text(
                0.02, 0.30,
                f"High-intensity distance  #{int(rank_lookup.loc[('England', 'high_intensity_distance_m_per90'), 'rank_high_to_low'])} of 8\\n"
                f"Direct pressures             #{int(rank_lookup.loc[('England', 'fifa_direct_pressures'), 'rank_high_to_low'])} of 8\\n"
                f"Opponent xG                  #{int(rank_lookup.loc[('England', 'opponent_xg'), 'rank_high_to_low'])} of 8 (worst)\\n"
                f"Line breaks conceded     #{int(rank_lookup.loc[('England', 'opponent_completed_line_breaks'), 'rank_high_to_low'])} of 8",
                fontsize=11.5, linespacing=1.55, color=INK, transform=axes[1].transAxes,
            )
            axes[1].text(
                0.02, 0.04,
                "Interpretation: substantial fast running and pressing,\\nbut unusually weak collective control.",
                fontsize=11, color=MUTED, fontstyle="italic", transform=axes[1].transAxes,
            )
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_effort_vs_control.png", dpi=180, bbox_inches="tight")
            plt.show()

            # Chart contract: indexed grouped comparison for two award leaders plus
            # an absolute xG/goals comparison. Exact values and baseline=100 prevent
            # the index from being mistaken for raw event counts.
            spotlight = candidate_behavior[
                candidate_behavior["player"].isin(["Kylian Mbappe", "Michael Olise"])
            ].copy()
            behavior_rows = []
            behavior_specs = [
                ("attempts_at_goal", "Attempts at goal / 90"),
                ("offers_in_behind", "Offers in behind / 90"),
                ("pressures_direct", "Direct pressures / 90"),
            ]
            for row in spotlight.itertuples():
                for metric, label in behavior_specs:
                    behavior_rows.append({
                        "player": row.player,
                        "metric": metric,
                        "label": f"{row.player.replace('Kylian ', '').replace('Michael ', '')}\\n{label}",
                        "index": getattr(row, f"{metric}_index"),
                        "current_rate": getattr(row, f"{metric}_current_p90"),
                        "prior_rate": getattr(row, f"{metric}_prior_p90"),
                    })
            behavior_index = pd.DataFrame(behavior_rows)

            fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.8), gridspec_kw={"width_ratios": [1.55, 1]})
            behavior_plot = behavior_index.iloc[::-1].reset_index(drop=True)
            y = np.arange(len(behavior_plot))
            colors = [BLUE if player == "Kylian Mbappe" else ORANGE for player in behavior_plot["player"]]
            bars = axes[0].barh(y, behavior_plot["index"], color=colors, edgecolor=INK, linewidth=0.6)
            axes[0].axvline(100, color=INK, linestyle="--", linewidth=1.2, label="Own earlier rate = 100")
            axes[0].set_yticks(y, behavior_plot["label"])
            axes[0].set_xlabel("Match 103 activity index (own prior tournament rate = 100)")
            axes[0].set_xlim(0, max(360, behavior_plot["index"].max() * 1.18))
            axes[0].set_title("Award leaders' observable Match 103 activity", loc="left", pad=30)
            axes[0].text(0, 1.01, "Rates per 90; descriptive comparison with seven earlier matches per player", transform=axes[0].transAxes, color=MUTED)
            for bar, row in zip(bars, behavior_plot.itertuples()):
                axes[0].text(
                    bar.get_width() + 7, bar.get_y() + bar.get_height() / 2,
                    f"{row.current_rate:.1f} vs {row.prior_rate:.1f}",
                    va="center", fontsize=8.5, color=INK,
                )
            axes[0].legend(loc="upper right", fontsize=8.5)
            axes[0].spines[["top", "right"]].set_visible(False)

            x = np.arange(len(finishing))
            width = 0.36
            xg_bars = axes[1].bar(x - width / 2, finishing["xg"], width, color=BLUE_LIGHT, edgecolor=INK, label="xG")
            goal_bars = axes[1].bar(x + width / 2, finishing["goals"], width, color=ORANGE, edgecolor=INK, label="Goals")
            axes[1].set_xticks(x, finishing["scope"])
            axes[1].set_ylabel("Expected or observed goals")
            axes[1].set_title("Chance quality versus finishing", loc="left", pad=30)
            axes[1].text(0, 1.01, "Poisson tail is an approximation from aggregate xG", transform=axes[1].transAxes, color=MUTED)
            axes[1].bar_label(xg_bars, fmt="%.2f", padding=3, fontsize=8.5)
            axes[1].bar_label(goal_bars, fmt="%.0f", padding=3, fontsize=8.5)
            combined_finishing = finishing[finishing["scope"].eq("Combined")].iloc[0]
            axes[1].text(
                0.04, 0.90,
                f"10 from 5.33 xG\\n+{combined_finishing['goals_above_xg']:.2f} above xG\\nP(10+) ≈ {100 * combined_finishing['poisson_tail_p']:.1f}%",
                transform=axes[1].transAxes, va="top", fontsize=11, color=INK,
                bbox={"facecolor": BG, "edgecolor": GRID, "pad": 6},
            )
            axes[1].legend(loc="upper center", ncol=2)
            axes[1].spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_player_behavior_and_finishing.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        markdown(
            """
            ### Interpretation

            The new evidence separates **work rate** from **defensive organisation**:

            - Across 19 comparable outfielders, total distance per 90 was **3.2% below** their own earlier rates (bootstrap CI includes zero; sign-flip p≈0.09). That is compatible with a slightly less continuous game.
            - Distance at 20+ km/h was **12.0% above** baseline (bootstrap interval roughly +9 to +176 metres per player-90; raw p≈0.05). Direct pressures were **63.2% above** baseline (raw p≈0.04). Sprints were essentially unchanged. Neither raw result survives Holm correction across the four related effort metrics, so the pattern is exploratory rather than confirmatory.
            - France produced its **second-highest high-intensity distance** and **highest direct-pressure count** in eight matches, yet its **worst turnover yield**, while conceding its highest opponent xG and most completed line breaks.
            - England's high-intensity distance ranked **third of eight**, but it also conceded its highest opponent xG.

            This is stronger evidence for **active but poorly coordinated defending** than for players simply jogging through the match. The p-values remain exploratory because player observations share the same match environment and several related metrics were examined.

            The individual-incentive story also gains behavioural support, selectively. Mbappe took **8 shots versus a prior rate of 4.88 per 90**, accounting for 42% of France's attempts. Olise made **17 offers in behind versus 8.34 per 90** and applied **11 direct pressures versus 3.37 per 90**. With only seven earlier matches per player, the empirical one-sided p-values are coarse (Mbappe attempts p=0.25; Olise offers and pressures p=0.125). These are observable changes consistent with aggressive attacking involvement, not standalone proof or evidence of private motive.

            Finally, the score was not only about openness. Match 103 generated a tournament-high **5.33 xG**, but ten goals were **4.67 above xG**. Under a rough aggregate-Poisson check, ten or more goals had probability about **4.5%**; England's six goals from 2.34 xG had a corresponding tail near **3.2%**. Structural openness created the opportunity, and exceptional finishing magnified it.
            """
        ),
        markdown(
            """
            ## Contact, discipline, and the spectacle-first hypothesis

            **H3:** Match 103 shifted toward maximizing visible action—shots, goals, assists, runs, tackles, and pressure attempts—rather than minimizing defeat. The predicted signature is not necessarily fewer actions. It is **normal or high engagement paired with unusually weak defensive conversion and disciplinary consequence**.

            This distinction matters. A genuinely low-effort match would show less running, pressing, tackling, and contact. A spectacle-first match can instead be frantic: players keep producing visible actions while teams accept risks that serious knockout football normally suppresses.
            """
        ),
        code(
            """
            # Official contact, disciplinary intensity, and defensive-control outcomes
            reference_matches = match_discipline[match_discipline["match_number"].lt(103)].copy()
            reference_90 = reference_matches[~reference_matches["went_to_extra_time"]].copy()
            knockout_reference = reference_matches[~reference_matches["stage"].eq("Group stage")].copy()
            knockout_90_reference = knockout_reference[~knockout_reference["went_to_extra_time"]].copy()
            current_discipline = match_discipline[match_discipline["match_number"].eq(103)].iloc[0]
            foul_band_reference = reference_90[
                reference_90["total_fouls"].between(
                    current_discipline["total_fouls"] - 3,
                    current_discipline["total_fouls"] + 3,
                )
            ].copy()
            same_referee_reference = reference_matches[
                reference_matches["referee"].eq(current_discipline["referee"])
            ].copy()

            def add_one_lower_tail(reference: pd.Series, observed: float) -> float:
                return float((1 + reference.le(observed).sum()) / (len(reference) + 1))

            def negative_binomial_zero_probability(values: pd.Series) -> float:
                values = values.astype(float)
                mean = float(values.mean())
                variance = float(values.var(ddof=1))
                if mean <= 0:
                    return 1.0
                if variance <= mean:
                    return float(np.exp(-mean))
                size = mean ** 2 / (variance - mean)
                probability = size / (size + mean)
                return float(stats.nbinom.pmf(0, size, probability))

            discipline_summary = pd.DataFrame([
                {
                    "metric": "Total fouls",
                    "current": float(current_discipline["total_fouls"]),
                    "first_102_mean": float(reference_matches["total_fouls"].mean()),
                    "first_102_median": float(reference_matches["total_fouls"].median()),
                    "regulation_only_mean": float(reference_90["total_fouls"].mean()),
                    "knockout_90_mean": float(knockout_90_reference["total_fouls"].mean()),
                    "rank_low_to_high_vs_first_102": int(1 + reference_matches["total_fouls"].lt(current_discipline["total_fouls"]).sum()),
                },
                {
                    "metric": "Card events",
                    "current": float(current_discipline["total_card_events"]),
                    "first_102_mean": float(reference_matches["total_card_events"].mean()),
                    "first_102_median": float(reference_matches["total_card_events"].median()),
                    "regulation_only_mean": float(reference_90["total_card_events"].mean()),
                    "knockout_90_mean": float(knockout_90_reference["total_card_events"].mean()),
                    "rank_low_to_high_vs_first_102": int(1 + reference_matches["total_card_events"].lt(current_discipline["total_card_events"]).sum()),
                },
                {
                    "metric": "Card events per 10 fouls",
                    "current": float(current_discipline["cards_per_10_fouls"]),
                    "first_102_mean": float(reference_matches["cards_per_10_fouls"].mean()),
                    "first_102_median": float(reference_matches["cards_per_10_fouls"].median()),
                    "regulation_only_mean": float(reference_90["cards_per_10_fouls"].mean()),
                    "knockout_90_mean": float(knockout_90_reference["cards_per_10_fouls"].mean()),
                    "rank_low_to_high_vs_first_102": int(1 + reference_matches["cards_per_10_fouls"].lt(current_discipline["cards_per_10_fouls"]).sum()),
                },
            ])

            discipline_test_specs = [
                ("All first 102 matches", reference_matches),
                ("Regulation-only first 102", reference_90),
                ("All earlier knockout matches", knockout_reference),
                ("Regulation-only knockout matches", knockout_90_reference),
                ("Regulation matches within ±3 fouls", foul_band_reference),
                ("Same referee's earlier matches", same_referee_reference),
            ]
            discipline_tests = pd.DataFrame([
                {
                    "reference": label,
                    "matches": len(frame),
                    "mean_fouls": float(frame["total_fouls"].mean()),
                    "mean_card_events": float(frame["total_card_events"].mean()),
                    "zero_card_matches": int(frame["total_card_events"].eq(0).sum()),
                    "raw_zero_frequency": float(frame["total_card_events"].eq(0).mean()),
                    "add_one_empirical_lower_tail_p": add_one_lower_tail(
                        frame["total_card_events"], current_discipline["total_card_events"]
                    ),
                    "negative_binomial_p_zero": negative_binomial_zero_probability(
                        frame["total_card_events"]
                    ) if len(frame) >= 10 else np.nan,
                }
                for label, frame in discipline_test_specs
            ])

            # Aggregate player events to equal-grain team-match rates. These outcomes
            # separate activity from whether the defensive action restored control.
            contact_control_metrics = [
                "tackles_made", "tackles_won", "blocks", "interceptions",
                "pressures_direct", "duels_won_aerial", "duels_won_physical",
                "possession_contests_won", "clearances", "possession_regains",
                "possession_interrupted", "high_intensity_distance_m", "sprints",
            ]
            team_contact_control = player_match.groupby(
                ["match_number", "team", "match_duration"], as_index=False
            )[contact_control_metrics].sum()
            for metric in contact_control_metrics:
                team_contact_control[f"{metric}_per90"] = (
                    90 * team_contact_control[metric] / team_contact_control["match_duration"]
                )

            metric_metadata = {
                "tackles_made": ("Tackles attempted", "activity"),
                "tackles_won": ("Tackles won", "control outcome"),
                "blocks": ("Blocks", "activity"),
                "interceptions": ("Interceptions", "control outcome"),
                "pressures_direct": ("Direct pressures", "activity"),
                "duels_won_aerial": ("Aerial duels won", "control outcome"),
                "duels_won_physical": ("Physical duels won", "control outcome"),
                "possession_contests_won": ("Possession contests won", "control outcome"),
                "clearances": ("Clearances", "control outcome"),
                "possession_regains": ("Possession regains", "control outcome"),
                "possession_interrupted": ("Possession interrupted", "control outcome"),
                "high_intensity_distance_m": ("Distance at 20+ km/h", "activity"),
                "sprints": ("Sprints", "activity"),
            }
            team_contact_rows = []
            for team in ("France", "England"):
                team_matches = team_contact_control[team_contact_control["team"].eq(team)]
                current_team = team_matches[team_matches["match_number"].eq(103)].iloc[0]
                prior_team = team_matches[team_matches["match_number"].lt(103)]
                for metric, (label, category) in metric_metadata.items():
                    value_column = f"{metric}_per90"
                    current_value = float(current_team[value_column])
                    prior_mean = float(prior_team[value_column].mean())
                    team_contact_rows.append({
                        "team": team,
                        "metric": metric,
                        "label": label,
                        "category": category,
                        "current_per90": current_value,
                        "prior_mean_per90": prior_mean,
                        "relative_delta_pct": 100 * (current_value / prior_mean - 1) if prior_mean else np.nan,
                        "rank_high_to_low": int(1 + prior_team[value_column].gt(current_value).sum()),
                        "rank_low_to_high": int(1 + prior_team[value_column].lt(current_value).sum()),
                    })
            contact_control_team_ranks = pd.DataFrame(team_contact_rows)

            contact_control_split = contact_control_team_ranks.groupby(
                ["metric", "label", "category"], as_index=False
            ).agg(
                current_per90=("current_per90", "sum"),
                prior_mean_per90=("prior_mean_per90", "sum"),
            )
            contact_control_split["relative_delta_pct"] = 100 * (
                contact_control_split["current_per90"]
                / contact_control_split["prior_mean_per90"] - 1
            )

            # Independent reconciliation with the already-built PMSR panel.
            discipline_scores = match_discipline[["match_number", "total_goals"]]
            pmsr_scores = pmsr.groupby("match_number", as_index=False)["goals"].sum().rename(
                columns={"goals": "pmsr_total_goals"}
            )
            discipline_score_check = discipline_scores.merge(
                pmsr_scores, on="match_number", validate="one_to_one"
            )
            assert discipline_score_check["total_goals"].eq(
                discipline_score_check["pmsr_total_goals"]
            ).all()
            quality_checks = pd.concat([
                quality_checks,
                pd.DataFrame([(
                    "Full Time report goals reconcile PMSR totals",
                    int(discipline_score_check["total_goals"].eq(discipline_score_check["pmsr_total_goals"]).sum()),
                    len(discipline_score_check),
                    "pass",
                )], columns=quality_checks.columns),
            ], ignore_index=True)

            discipline_summary.to_csv(TABLES / "v2_contact_discipline_summary.csv", index=False)
            discipline_tests.to_csv(TABLES / "v2_contact_discipline_tests.csv", index=False)
            contact_control_team_ranks.to_csv(TABLES / "v2_contact_control_team_ranks.csv", index=False)
            contact_control_split.to_csv(TABLES / "v2_contact_control_split.csv", index=False)

            display(discipline_summary.round(3))
            display(discipline_tests.round(3))
            display(contact_control_team_ranks[
                contact_control_team_ranks["metric"].isin([
                    "tackles_made", "tackles_won", "interceptions", "duels_won_aerial",
                    "possession_contests_won", "clearances", "pressures_direct",
                    "high_intensity_distance_m",
                ])
            ].round(2))

            # Chart contract: panel 1 compares two match-level metrics with a common
            # baseline index; panel 2 shows same-team deltas at one team-match grain.
            fig, axes = plt.subplots(1, 2, figsize=(14.8, 6.8), gridspec_kw={"width_ratios": [0.8, 1.45]})
            baseline_fouls = float(reference_90["total_fouls"].mean())
            baseline_cards = float(reference_90["total_card_events"].mean())
            context_rows = pd.DataFrame([
                ("Total fouls", float(current_discipline["total_fouls"]), baseline_fouls, BLUE),
                ("Card events", float(current_discipline["total_card_events"]), baseline_cards, ORANGE),
            ], columns=["metric", "current", "baseline", "color"])
            context_rows["index"] = 100 * context_rows["current"] / context_rows["baseline"]
            y_context = np.arange(len(context_rows))
            axes[0].barh(y_context, [100, 100], color="#E9EDF5", edgecolor=GRID, height=0.56)
            current_bars = axes[0].barh(
                y_context, context_rows["index"], color=context_rows["color"],
                edgecolor=INK, linewidth=0.6, height=0.56,
            )
            axes[0].axvline(100, color=INK, linestyle="--", linewidth=1.1)
            axes[0].set_yticks(y_context, context_rows["metric"])
            axes[0].invert_yaxis()
            axes[0].set_xlim(0, 125)
            axes[0].set_xlabel("Match 103 index (90-minute tournament mean = 100)")
            axes[0].set_title("Contact and discipline", loc="left", pad=30)
            axes[0].text(0, 1.01, "Match 103 versus 94 earlier regulation-time matches", transform=axes[0].transAxes, color=MUTED)
            for bar, row in zip(current_bars, context_rows.itertuples()):
                axes[0].text(
                    min(max(bar.get_width() + 4, 4), 112),
                    bar.get_y() + bar.get_height() / 2,
                    f"{row.current:g} vs {row.baseline:.2f}",
                    va="center", fontsize=9, color=INK,
                )
            axes[0].spines[["top", "right"]].set_visible(False)

            plot_metric_order = [
                "tackles_made", "blocks", "pressures_direct", "high_intensity_distance_m",
                "tackles_won", "interceptions", "duels_won_aerial",
                "possession_contests_won", "clearances",
            ]
            split_plot = contact_control_split.set_index("metric").loc[plot_metric_order].reset_index()
            split_plot["display_label"] = [
                f"{label}  [{category}]"
                for label, category in zip(split_plot["label"], split_plot["category"])
            ]
            split_colors = [BLUE if category == "activity" else ORANGE for category in split_plot["category"]]
            y_split = np.arange(len(split_plot))
            split_bars = axes[1].barh(
                y_split, split_plot["relative_delta_pct"], color=split_colors,
                edgecolor=INK, linewidth=0.5,
            )
            axes[1].axvline(0, color=INK, linewidth=1.1)
            axes[1].set_yticks(y_split, split_plot["display_label"])
            axes[1].invert_yaxis()
            axes[1].set_xlim(-85, 85)
            axes[1].set_xlabel("Change versus sum of each team's prior-match mean (%)")
            axes[1].set_title("Defensive activity and control outcomes", loc="left", pad=30)
            axes[1].text(0, 1.01, "France + England; per-90 rates versus their own previous seven matches", transform=axes[1].transAxes, color=MUTED)
            for bar, value in zip(split_bars, split_plot["relative_delta_pct"]):
                axes[1].text(
                    value + (2.2 if value >= 0 else -2.2),
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:+.0f}%",
                    ha="left" if value >= 0 else "right", va="center", fontsize=8.8, color=INK,
                )
            axes[1].spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_contact_discipline_and_control.png", dpi=180, bbox_inches="tight")
            plt.show()

            # Narrative image for non-technical readers.
            fig, ax = plt.subplots(figsize=(16, 9), facecolor="#0B132B")
            ax.set_facecolor("#0B132B")
            ax.axis("off")
            ax.text(0.055, 0.92, "MATCH 103 · FRANCE 4–6 ENGLAND", color=BLUE_LIGHT, fontsize=16, fontweight="bold", transform=ax.transAxes)
            ax.text(0.055, 0.79, "Bukan tanpa kontak.\\nYang hilang adalah rem.", color="white", fontsize=34, fontweight="bold", linespacing=1.05, transform=ax.transAxes)
            ax.text(0.055, 0.65, "Pemain tetap aktif—tetapi permainan tidak lagi meminimalkan risiko kebobolan.", color="#CBD5E1", fontsize=16, transform=ax.transAxes)

            ax.add_patch(plt.Rectangle((0.055, 0.25), 0.40, 0.32, facecolor="#14213D", edgecolor=BLUE, linewidth=2, transform=ax.transAxes))
            ax.text(0.085, 0.52, "AKTIVITAS TETAP TINGGI", color=BLUE_LIGHT, fontsize=17, fontweight="bold", transform=ax.transAxes)
            ax.text(0.085, 0.43, "22 foul", color="white", fontsize=25, fontweight="bold", transform=ax.transAxes)
            ax.text(0.25, 0.43, "≈ normal turnamen", color="#CBD5E1", fontsize=14, transform=ax.transAxes)
            ax.text(0.085, 0.35, "+61% tekel dicoba", color="white", fontsize=19, transform=ax.transAxes)
            ax.text(0.085, 0.28, "+52% tekanan langsung", color="white", fontsize=19, transform=ax.transAxes)

            ax.add_patch(plt.Rectangle((0.545, 0.25), 0.40, 0.32, facecolor="#261B24", edgecolor=ORANGE, linewidth=2, transform=ax.transAxes))
            ax.text(0.575, 0.52, "KONTROL & KONSEKUENSI TURUN", color=ORANGE_LIGHT, fontsize=17, fontweight="bold", transform=ax.transAxes)
            ax.text(0.575, 0.43, "0 kartu", color="white", fontsize=25, fontweight="bold", transform=ax.transAxes)
            ax.text(0.73, 0.43, "vs 2,79 normal", color="#CBD5E1", fontsize=14, transform=ax.transAxes)
            ax.text(0.575, 0.35, "−65% clearance", color="white", fontsize=19, transform=ax.transAxes)
            ax.text(0.575, 0.28, "yield tekanan terendah", color="white", fontsize=19, transform=ax.transAxes)

            ax.text(0.055, 0.15, "SPECTACLE-FIRST TENDENCY", color=ORANGE, fontsize=22, fontweight="bold", transform=ax.transAxes)
            ax.text(0.055, 0.095, "Pola konsisten dengan insentif exhibition/stat-padding—bukan bukti skor disepakati.", color="#CBD5E1", fontsize=14, transform=ax.transAxes)
            fig.savefig(ASSETS / "narrative_07_spectacle_without_brakes.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.show()
            """
        ),
        markdown(
            """
            ### Contact verdict: not softer, but less consequential

            Match 103 recorded **22 fouls**, almost identical to the **22.39** average in the 94 earlier regulation-time matches. Contact therefore did not disappear. The sharper anomaly is that those 22 fouls produced **zero yellow or red cards**, compared with **2.79 card events** in the regulation-time reference and **3.27** in regulation-time knockout matches.

            Zero cards are unusual but not independently decisive. The add-one empirical lower-tail probability is **0.097** against all first 102 matches, **0.065** against all earlier knockout matches, **0.087** after removing extra-time knockout matches, **0.140** among regulation matches within three fouls of Match 103, and **0.250** against the same referee's three earlier tournament matches. A negative-binomial model gives a roughly **6%** zero-card probability in the regulation-time knockout reference. Referee style and ordinary variation therefore remain credible alternatives.

            The stronger evidence comes from the **directional stack**. Across France and England, tackles attempted rose **61%**, direct pressures **52%**, blocks **38%**, and high-intensity distance **16%** versus their own earlier matches. Tackles won also rose **53%**, an important counter-signal showing genuine engagement. Yet interceptions fell **25%**, aerial duels won **53%**, possession contests won **53%**, and clearances **65%**. Both teams recorded their fewest clearances in eight tournament matches, while pressure-to-turnover yield was already below every earlier World Cup match.

            > **Bold insight:** this was not low-intensity football. It was **high-activity, low-restraint football**—closer to a match maximizing spectacle and individual output than to teams optimizing the probability of avoiding defeat.

            **H3 verdict: supported with moderate-high confidence as a behavioural tendency.** The evidence supports a spectacle-first incentive pattern. It does not establish coordination, a pre-arranged score, or private intent; those are different hypotheses requiring communications, betting, or integrity evidence that match statistics cannot supply.

            ![Contact stayed normal while cards and collective control fell](../assets/narrative_07_spectacle_without_brakes.png)
            """
        ),
        code(
            """
            # Regulation-time score-state exposure and World Cup goal hazards
            regulation_goals = men_goal_events[
                ~men_goal_events["match_period"].str.startswith("extra time", na=False)
            ].copy()
            regulation_goals["minute"] = pd.to_numeric(regulation_goals["minute_regulation"], errors="coerce").clip(1, 90).astype(int)

            event_map: defaultdict[str, defaultdict[int, list[str]]] = defaultdict(lambda: defaultdict(list))
            for row in regulation_goals.itertuples():
                event_map[row.match_id][row.minute].append(row.team_name)

            time_labels = ["1–15", "16–30", "31–45", "46–60", "61–75", "76–90"]
            panel_rows = []
            for match in men.itertuples():
                home_score = 0
                away_score = 0
                for minute in range(1, 91):
                    absolute_gap = abs(home_score - away_score)
                    gap_bin = "3+" if absolute_gap >= 3 else str(absolute_gap)
                    goals_this_minute = event_map[match.match_id].get(minute, [])
                    panel_rows.append((match.match_id, minute, time_labels[(minute - 1) // 15], gap_bin, len(goals_this_minute)))
                    for scoring_team in goals_this_minute:
                        if scoring_team == match.home_team_name:
                            home_score += 1
                        else:
                            away_score += 1

            score_panel = pd.DataFrame(panel_rows, columns=["match_id", "minute", "time_bin", "gap_bin", "goals"])
            score_rates = score_panel.groupby(["time_bin", "gap_bin"], observed=True).agg(
                goals=("goals", "sum"), exposure_minutes=("goals", "size")
            ).reset_index()
            score_rates["goals_per_minute"] = score_rates["goals"] / score_rates["exposure_minutes"]

            current_goals["minute_int"] = np.floor(current_goals["minute_decimal"]).clip(1, 90).astype(int)
            current_event_map: defaultdict[int, list[str]] = defaultdict(list)
            for row in current_goals.itertuples():
                current_event_map[row.minute_int].append(row.team)

            france_score = 0
            england_score = 0
            current_path_rows = []
            for minute in range(1, 91):
                absolute_gap = abs(france_score - england_score)
                gap_bin = "3+" if absolute_gap >= 3 else str(absolute_gap)
                time_bin = time_labels[(minute - 1) // 15]
                goals_this_minute = current_event_map.get(minute, [])
                current_path_rows.append((minute, time_bin, gap_bin, len(goals_this_minute)))
                for scoring_team in goals_this_minute:
                    if scoring_team == "France":
                        france_score += 1
                    else:
                        england_score += 1

            current_path = pd.DataFrame(current_path_rows, columns=["minute", "time_bin", "gap_bin", "observed_goals"])
            current_path = current_path.merge(
                score_rates[["time_bin", "gap_bin", "goals_per_minute"]],
                on=["time_bin", "gap_bin"],
                validate="many_to_one",
            )
            level_path = current_path[["minute", "time_bin"]].merge(
                score_rates[score_rates["gap_bin"].eq("0")][["time_bin", "goals_per_minute"]],
                on="time_bin",
                validate="many_to_one",
            )

            # Cluster bootstrap by historical match using compact cell matrices.
            cell_order = pd.MultiIndex.from_frame(score_rates[["time_bin", "gap_bin"]])
            match_cell = score_panel.groupby(["match_id", "time_bin", "gap_bin"]).agg(
                goals=("goals", "sum"), exposure=("goals", "size")
            )
            goal_matrix = match_cell["goals"].unstack(["time_bin", "gap_bin"]).reindex(columns=cell_order, fill_value=0).fillna(0).to_numpy()
            exposure_matrix = match_cell["exposure"].unstack(["time_bin", "gap_bin"]).reindex(columns=cell_order, fill_value=0).fillna(0).to_numpy()
            current_cell_counts = current_path.groupby(["time_bin", "gap_bin"]).size().reindex(cell_order, fill_value=0).to_numpy()
            level_cell_counts = pd.Series(0, index=cell_order, dtype=float)
            for time_bin in time_labels:
                level_cell_counts.loc[(time_bin, "0")] = 15

            bootstrap_counts = rng.multinomial(len(goal_matrix), np.repeat(1 / len(goal_matrix), len(goal_matrix)), size=5_000)
            bootstrap_goals = bootstrap_counts @ goal_matrix
            bootstrap_exposure = bootstrap_counts @ exposure_matrix
            bootstrap_rates = np.divide(bootstrap_goals, bootstrap_exposure, out=np.zeros_like(bootstrap_goals, dtype=float), where=bootstrap_exposure > 0)
            current_expected_boot = bootstrap_rates @ current_cell_counts
            level_expected_boot = bootstrap_rates @ level_cell_counts.to_numpy()

            current_expected = float(current_path["goals_per_minute"].sum())
            level_expected = float(level_path["goals_per_minute"].sum())
            state_increase = current_expected - level_expected

            first_half_goals = regulation_goals[regulation_goals["minute"].le(45)].groupby("match_id").size().reindex(men["match_id"], fill_value=0)
            second_half_goals = regulation_goals[regulation_goals["minute"].gt(45)].groupby("match_id").size().reindex(men["match_id"], fill_value=0)
            rarity_table = pd.DataFrame([
                ("At least four first-half goals", int((first_half_goals >= 4).sum()), len(men), float((first_half_goals >= 4).mean())),
                ("At least six second-half goals", int((second_half_goals >= 6).sum()), len(men), float((second_half_goals >= 6).mean())),
                ("At least ten regulation goals", int(((first_half_goals + second_half_goals) >= 10).sum()), len(men), float(((first_half_goals + second_half_goals) >= 10).mean())),
            ], columns=["event", "historical_matches", "denominator", "rate"])

            state_summary = pd.DataFrame([
                ("Level-state path", level_expected, *np.quantile(level_expected_boot, [0.025, 0.975])),
                ("Observed score-state path", current_expected, *np.quantile(current_expected_boot, [0.025, 0.975])),
                ("Actual England–France", 10.0, np.nan, np.nan),
            ], columns=["scenario", "goals", "ci_low", "ci_high"])
            state_summary.to_csv(TABLES / "v2_score_state_decomposition.csv", index=False)
            rarity_table.to_csv(TABLES / "v2_world_cup_regulation_rarity.csv", index=False)
            score_rates.to_csv(TABLES / "v2_score_state_rates.csv", index=False)
            display(score_rates.pivot(index="time_bin", columns="gap_bin", values="goals_per_minute").round(4))
            display(state_summary.round(3))
            display(rarity_table.assign(rate_pct=100 * rarity_table["rate"]).round(3))

            aggregate_gap = score_panel.groupby("gap_bin").agg(goals=("goals", "sum"), exposure=("goals", "size")).reset_index()
            aggregate_gap["goals_per_90"] = 90 * aggregate_gap["goals"] / aggregate_gap["exposure"]
            gap_order = ["0", "1", "2", "3+"]
            aggregate_gap["gap_bin"] = pd.Categorical(aggregate_gap["gap_bin"], gap_order, ordered=True)
            aggregate_gap = aggregate_gap.sort_values("gap_bin")

            fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.1))
            bars = axes[0].bar(aggregate_gap["gap_bin"].astype(str), aggregate_gap["goals_per_90"], color=BLUE, edgecolor=INK, linewidth=0.5)
            axes[0].set_xlabel("Absolute score gap at start of minute")
            axes[0].set_ylabel("Historical goals per 90 match-minutes")
            axes[0].set_title("World Cup goal rate by score gap", loc="left", pad=30)
            axes[0].text(0, 1.01, f"Regulation time, men's World Cups 1930–2022; n={len(men)} matches", transform=axes[0].transAxes, color=MUTED)
            axes[0].bar_label(bars, fmt="%.2f", padding=3, color=INK)

            scenario_colors = [BLUE_LIGHT, BLUE, ORANGE]
            scenario_bars = axes[1].bar(state_summary["scenario"], state_summary["goals"], color=scenario_colors, edgecolor=INK, linewidth=0.5)
            error_low = state_summary["goals"] - state_summary["ci_low"]
            error_high = state_summary["ci_high"] - state_summary["goals"]
            axes[1].errorbar([0, 1], state_summary.loc[:1, "goals"], yerr=np.vstack([error_low[:2], error_high[:2]]), fmt="none", ecolor=INK, capsize=4, linewidth=1)
            axes[1].set_ylabel("Expected or observed goals")
            axes[1].set_title("Score-state decomposition of match 103", loc="left", pad=30)
            axes[1].text(0, 1.01, "Intervals: match-cluster bootstrap; observed bar is not an estimate", transform=axes[1].transAxes, color=MUTED)
            axes[1].tick_params(axis="x", rotation=12)
            axes[1].bar_label(scenario_bars, fmt="%.2f", padding=3, color=INK)
            for ax in axes:
                ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()
            fig.savefig(ASSETS / "v2_score_state_decomposition.png", dpi=180, bbox_inches="tight")
            plt.show()
            """
        ),
        code(
            """
            # Evidence scorecard and machine-readable handoff
            evidence_scorecard = pd.DataFrame([
                ("Lower selection priority", "Supported", "Each team changed 7 of 11 semi-final starters."),
                ("Individual attacking incentives remained live", "Supported selectively", "France retained Mbappe and Olise; their totals moved 8→10 goals and 5→7 assists. England began with Kane and Bellingham on the bench, so the mechanism was not universal."),
                ("Players broadly coasted physically", "Not supported", f"Among {len(player_effort)} comparable outfielders, high-intensity distance was {player_effort_tests.loc[player_effort_tests['metric'].eq('high_intensity_distance_m'), 'relative_delta_pct'].iloc[0]:+.1f}% and direct pressures were {player_effort_tests.loc[player_effort_tests['metric'].eq('pressures_direct'), 'relative_delta_pct'].iloc[0]:+.1f}% versus their own prior rates; total distance was slightly lower. Raw tests are exploratory and none remains below 0.05 after Holm correction."),
                ("Award leaders showed unusually aggressive activity", "Suggestive, not conclusive", "Mbappe took 8 shots versus 4.88 per prior player-90; Olise made 17 offers in behind versus 8.34 and 11 direct pressures versus 3.37. Seven-match empirical p-values are coarse (0.25 and 0.125)."),
                ("Elite friendlies normally score much more", "Not supported", f"Matched difference {primary_test['mean_difference']:+.2f}; 95% CI {primary_test['ci_low']:+.2f} to {primary_test['ci_high']:+.2f}; p={primary_test['permutation_p']:.3f}."),
                ("Charity-like scoring spectacle", "Supported descriptively", f"Ten goals exceeded every Soccer Aid row; the expanded {len(benchmark_all)}-match benchmark shows that creator-led formats can also reach 10+ goals, so event stratification matters."),
                ("Non-goal match profile was exhibition-like", "Supported", f"The strict-holdout process model used 102 official and 19 exhibition matches, excluded goals, and scored Match 103 at {primary_target_score:.3f}; repeated-CV AUC was {model_validation.loc[model_validation['model'].eq(primary_model_name), 'repeated_cv_auc_mean'].iloc[0]:.3f}."),
                ("Teams made no defensive effort", "Contradicted", f"Direct pressures were at the {process_percentiles.loc[process_percentiles['metric'].eq('direct_pressures'), 'percentile'].iloc[0]:.0f}th percentile, while high-intensity player distance was above individual baselines."),
                ("Contact intensity disappeared", "Contradicted", f"Match 103 had {current_discipline['total_fouls']:.0f} fouls versus {reference_90['total_fouls'].mean():.2f} in earlier regulation-time matches; tackles attempted were {contact_control_split.loc[contact_control_split['metric'].eq('tackles_made'), 'relative_delta_pct'].iloc[0]:+.0f}% versus the focal teams' own prior rates."),
                ("Disciplinary consequence weakened", "Supported as a secondary signal", f"Zero cards versus {reference_90['total_card_events'].mean():.2f} earlier regulation-time mean; add-one empirical p={discipline_tests.loc[discipline_tests['reference'].eq('All earlier knockout matches'), 'add_one_empirical_lower_tail_p'].iloc[0]:.3f} for all earlier knockout matches and {discipline_tests.loc[discipline_tests['reference'].eq('Regulation-only knockout matches'), 'add_one_empirical_lower_tail_p'].iloc[0]:.3f} after excluding extra time."),
                ("Defensive control was unusually ineffective", "Supported", f"Only {current_process['forced_turnovers']:.0f} turnovers and {current_process['turnovers_per_100_pressures']:.1f} per 100 pressures; the latter was below all 102 earlier matches."),
                ("Spectacle-first behavioural tendency", "Supported", "Normal contact and high activity coexisted with zero cards, tournament-leading attack, bottom-ranked pressure yield, and collapsed clearance/duel outcomes. This supports an incentive tendency, not pre-arrangement."),
                ("Ten goals came only from chance volume", "Not supported", f"Observed goals exceeded 5.33 xG by 4.67; aggregate-Poisson P(10+)≈{100 * finishing.loc[finishing['scope'].eq('Combined'), 'poisson_tail_p'].iloc[0]:.1f}%."),
                ("The 4–0 state explains all ten goals", "Contradicted", f"State-conditioned expectation {current_expected:.2f} versus 10 observed; level-state expectation {level_expected:.2f}."),
                ("Current match fits an ordinary elite friendly", "Not supported", "Ten-goal model tail is below 0.1% in both matched professional contexts."),
            ], columns=["claim", "assessment", "evidence"])
            display(evidence_scorecard)

            hypothesis_verdict = pd.DataFrame([
                ("Overall H1: the match behaved like a fun/charity match", "Partially supported", "Lower selection priority and exhibition-like openness are supported; broad coasting and no defending are contradicted.", "Moderate"),
                ("Lower team-level stakes", "Supported", "Both teams changed seven of eleven semi-final starters.", "High"),
                ("Players broadly reduced physical/defensive effort", "Not supported", "High-intensity distance and direct pressures rose; player tests are exploratory and Holm-adjusted p-values exceed 0.05.", "Moderate"),
                ("Collective defensive control weakened", "Supported", "Pressure-to-turnover yield and opponent chance quality were unusually poor.", "Moderate-high"),
                ("Contact intensity was broadly lower", "Not supported", "Twenty-two fouls were normal and tackles attempted, blocks, pressure attempts, and high-intensity distance were elevated.", "Moderate-high"),
                ("Disciplinary intensity was lower", "Suggestive", "The match was cardless despite normal foul volume; knockout empirical tails are about 0.065–0.087 and referee/foul-band sensitivities are weaker.", "Low-moderate"),
                ("H3: spectacle-first behavioural tendency", "Supported", "Visible activity remained high while attacking output peaked and collective defensive conversion, clearances, duel control, and card consequence fell.", "Moderate-high"),
                ("H4: observable profile was closer to exhibition football", "Supported", f"All 19 complete-core exhibition matches were compared with 102 official matches; the no-goals holdout score was {primary_target_score:.3f}, with repeated-CV AUC {model_validation.loc[model_validation['model'].eq(primary_model_name), 'repeated_cv_auc_mean'].iloc[0]:.3f}. Cross-provider and event-family sensitivity limit causal interpretation.", "Moderate-high"),
                ("H2: individual rewards affected selection and attacking involvement", "Supported as an incentive/opportunity mechanism; player attribution remains suggestive", "Mbappe and Olise were selectively retained, highly involved, and materially changed award standings; small within-player samples and unobserved motive limit attribution.", "Moderate"),
                ("H2 stronger claim: the match was primarily used to farm statistics", "Not established", "Award totals changed, but the evidence cannot distinguish intentional stat-seeking from normal attacking opportunity or private motive.", "Low"),
                ("The match was equivalent to a charity match", "Not established", "The scoring was charity-like descriptively, but roster quality, incentives, and rules are not comparable.", "Low"),
            ], columns=["hypothesis_component", "verdict", "evidence", "confidence"])
            display(hypothesis_verdict)

            summary_payload = {
                "analysis_as_of": "2026-07-19",
                "primary_matched_pairs": int(len(paired_primary)),
                "primary_friendly_mean_goals": float(paired_primary["friendly_goals"].mean()),
                "primary_official_mean_goals": float(paired_primary["official_goals"].mean()),
                "primary_mean_difference": float(primary_test["mean_difference"]),
                "primary_ci_low": float(primary_test["ci_low"]),
                "primary_ci_high": float(primary_test["ci_high"]),
                "primary_permutation_p": float(primary_test["permutation_p"]),
                "primary_mcnemar_p": mcnemar_p,
                "france_starter_changes": int(rotation.loc[rotation["team"].eq("France"), "starter_changes"].iloc[0]),
                "england_starter_changes": int(rotation.loc[rotation["team"].eq("England"), "starter_changes"].iloc[0]),
                "mbappe_tournament_goals_before": int(player_incentives.loc[player_incentives["player"].eq("Kylian Mbappe"), "pre_match_value"].iloc[0]),
                "mbappe_tournament_goals_after": int(player_incentives.loc[player_incentives["player"].eq("Kylian Mbappe"), "post_match_value"].iloc[0]),
                "olise_tournament_assists_before": int(player_incentives.loc[player_incentives["player"].eq("Michael Olise"), "pre_match_value"].iloc[0]),
                "olise_tournament_assists_after": int(player_incentives.loc[player_incentives["player"].eq("Michael Olise"), "post_match_value"].iloc[0]),
                "bellingham_tournament_goals_before": int(player_incentives.loc[player_incentives["player"].eq("Jude Bellingham"), "pre_match_value"].iloc[0]),
                "bellingham_tournament_goals_after": int(player_incentives.loc[player_incentives["player"].eq("Jude Bellingham"), "post_match_value"].iloc[0]),
                "comparable_outfield_players": int(len(player_effort)),
                "player_total_distance_delta_pct": float(player_effort_tests.loc[player_effort_tests["metric"].eq("total_distance_m"), "relative_delta_pct"].iloc[0]),
                "player_total_distance_sign_flip_p": float(player_effort_tests.loc[player_effort_tests["metric"].eq("total_distance_m"), "sign_flip_p"].iloc[0]),
                "player_total_distance_holm_p": float(player_effort_tests.loc[player_effort_tests["metric"].eq("total_distance_m"), "holm_adjusted_p"].iloc[0]),
                "player_high_intensity_distance_delta_pct": float(player_effort_tests.loc[player_effort_tests["metric"].eq("high_intensity_distance_m"), "relative_delta_pct"].iloc[0]),
                "player_high_intensity_distance_sign_flip_p": float(player_effort_tests.loc[player_effort_tests["metric"].eq("high_intensity_distance_m"), "sign_flip_p"].iloc[0]),
                "player_high_intensity_distance_holm_p": float(player_effort_tests.loc[player_effort_tests["metric"].eq("high_intensity_distance_m"), "holm_adjusted_p"].iloc[0]),
                "player_direct_pressure_delta_pct": float(player_effort_tests.loc[player_effort_tests["metric"].eq("pressures_direct"), "relative_delta_pct"].iloc[0]),
                "player_direct_pressure_sign_flip_p": float(player_effort_tests.loc[player_effort_tests["metric"].eq("pressures_direct"), "sign_flip_p"].iloc[0]),
                "player_direct_pressure_holm_p": float(player_effort_tests.loc[player_effort_tests["metric"].eq("pressures_direct"), "holm_adjusted_p"].iloc[0]),
                "mbappe_match_attempts": int(candidate_behavior.loc[candidate_behavior["player"].eq("Kylian Mbappe"), "attempts_at_goal_current"].iloc[0]),
                "mbappe_prior_attempts_per90": float(candidate_behavior.loc[candidate_behavior["player"].eq("Kylian Mbappe"), "attempts_at_goal_prior_p90"].iloc[0]),
                "mbappe_attempts_empirical_p": float(candidate_behavior.loc[candidate_behavior["player"].eq("Kylian Mbappe"), "attempts_at_goal_empirical_one_sided_p"].iloc[0]),
                "olise_match_offers_in_behind": int(candidate_behavior.loc[candidate_behavior["player"].eq("Michael Olise"), "offers_in_behind_current"].iloc[0]),
                "olise_prior_offers_in_behind_per90": float(candidate_behavior.loc[candidate_behavior["player"].eq("Michael Olise"), "offers_in_behind_prior_p90"].iloc[0]),
                "olise_offers_in_behind_empirical_p": float(candidate_behavior.loc[candidate_behavior["player"].eq("Michael Olise"), "offers_in_behind_empirical_one_sided_p"].iloc[0]),
                "soccer_aid_matches": int(len(soccer_aid_goals)),
                "soccer_aid_mean_goals": float(soccer_aid_goals.mean()),
                "expanded_exhibition_matches": int(len(expanded_exhibition_goals)),
                "expanded_exhibition_mean_goals": float(expanded_exhibition_goals.mean()),
                "expanded_exhibition_ten_plus_count": int(np.sum(expanded_exhibition_goals >= 10)),
                "expanded_exhibition_empirical_upper_tail": float((1 + np.sum(expanded_exhibition_goals >= 10)) / (len(expanded_exhibition_goals) + 1)),
                "exhibition_intensity_rows": int(len(exhibition_intensity)),
                "exhibition_intensity_complete_rows": int(len(exhibition_train)),
                "official_classifier_training_matches": int(len(official_train)),
                "exhibition_classifier_training_matches": int(len(exhibition_train)),
                "primary_exhibition_classifier_features": primary_features,
                "primary_exhibition_likeness_score": primary_target_score,
                "primary_exhibition_likeness_bootstrap_ci_low": float(primary_score_ci[0]),
                "primary_exhibition_likeness_bootstrap_ci_high": float(primary_score_ci[1]),
                "primary_exhibition_classifier_cv_auc": float(model_validation.loc[model_validation["model"].eq(primary_model_name), "repeated_cv_auc_mean"].iloc[0]),
                "primary_exhibition_classifier_cv_balanced_accuracy": float(model_validation.loc[model_validation["model"].eq(primary_model_name), "repeated_cv_balanced_accuracy_mean"].iloc[0]),
                "exhibition_event_family_sensitivity_low": float(event_sensitivity["target_exhibition_likeness_score"].min()),
                "exhibition_event_family_sensitivity_high": float(event_sensitivity["target_exhibition_likeness_score"].max()),
                "exhibition_profile_hypothesis_verdict": "Supported as an observable profile",
                "exhibition_profile_hypothesis_confidence": "Moderate-high",
                "current_total_xg": float(current_process["total_xg"]),
                "goals_above_xg": float(finishing.loc[finishing["scope"].eq("Combined"), "goals_above_xg"].iloc[0]),
                "aggregate_poisson_ten_plus_p": float(finishing.loc[finishing["scope"].eq("Combined"), "poisson_tail_p"].iloc[0]),
                "current_shots_on_target": int(current_process["shots_on_target"]),
                "current_direct_pressures": int(current_process["direct_pressures"]),
                "current_forced_turnovers": int(current_process["forced_turnovers"]),
                "current_turnovers_per_100_pressures": float(current_process["turnovers_per_100_pressures"]),
                "current_total_fouls": int(current_discipline["total_fouls"]),
                "regulation_reference_mean_fouls": float(reference_90["total_fouls"].mean()),
                "current_total_card_events": int(current_discipline["total_card_events"]),
                "regulation_reference_mean_card_events": float(reference_90["total_card_events"].mean()),
                "knockout_cardless_empirical_p": float(discipline_tests.loc[discipline_tests["reference"].eq("All earlier knockout matches"), "add_one_empirical_lower_tail_p"].iloc[0]),
                "regulation_knockout_cardless_empirical_p": float(discipline_tests.loc[discipline_tests["reference"].eq("Regulation-only knockout matches"), "add_one_empirical_lower_tail_p"].iloc[0]),
                "tackles_made_delta_pct": float(contact_control_split.loc[contact_control_split["metric"].eq("tackles_made"), "relative_delta_pct"].iloc[0]),
                "clearances_delta_pct": float(contact_control_split.loc[contact_control_split["metric"].eq("clearances"), "relative_delta_pct"].iloc[0]),
                "possession_contests_won_delta_pct": float(contact_control_split.loc[contact_control_split["metric"].eq("possession_contests_won"), "relative_delta_pct"].iloc[0]),
                "spectacle_first_hypothesis_verdict": "Supported as a behavioural tendency",
                "spectacle_first_hypothesis_confidence": "Moderate-high",
                "level_state_expected_goals": level_expected,
                "observed_state_expected_goals": current_expected,
                "observed_goals": 10,
                "overall_hypothesis_verdict": "Partially supported",
                "overall_hypothesis_confidence": "Moderate",
                "hypothesis_note": "The literal low-effort claim is only partial, but the revised spectacle-first hypothesis is supported: visible activity stayed high while attack, risk acceptance, stat opportunity, and defensive-control failure aligned.",
                "individual_stats_hypothesis_verdict": "Supported as an incentive/opportunity mechanism; intentional attribution remains suggestive",
                "individual_stats_hypothesis_confidence": "Moderate",
                "individual_stats_strong_claim_verdict": "Not established",
            }
            with open(TABLES / "v2_summary_metrics.json", "w", encoding="utf-8") as handle:
                json.dump(summary_payload, handle, indent=2)
            evidence_scorecard.to_csv(TABLES / "v2_evidence_scorecard.csv", index=False)
            hypothesis_verdict.to_csv(TABLES / "v2_hypothesis_verdict.csv", index=False)
            quality_checks.to_csv(TABLES / "v2_data_quality_checks.csv", index=False)

            print("Saved analysis tables:", TABLES)
            print("Saved figures:", ASSETS)
            """
        ),
        markdown(
            """
            ## Takeaways

            1. **The stronger professional sample removes the original power problem for the friendly comparison.** With 173 neutral matched pairs, there is no evidence of a large general scoring difference between elite friendlies and official tournament matches. The result remains small and unstable across stricter rank cutoffs.
            2. **The corrected two-population test answers the actual question.** Across 102 official matches and all 19 exhibition matches with complete intensity data, the no-goals model scored Match 103 at about 0.98 on the exhibition side. Repeated-CV AUC was about 0.958, and all five common metrics differed after Holm correction.
            3. **Selection clearly signalled lower priority.** Both teams replaced seven semi-final starters, consistent with fatigue management, experimentation, and reduced consequence.
            4. **Individual rewards survived the fall in team-level pressure.** France retained Mbappe and Olise despite seven changes; both materially improved live award positions. Bellingham also set an England record after coming off the bench. Kane's unchanged total prevents this from becoming a universal stat-padding claim.
            5. **The new physical data reject a simple coasting explanation.** Comparable outfielders covered slightly less total distance, but 12% more distance at 20+ km/h and applied 63% more direct pressures than their own prior rates. France's high-intensity distance ranked second of eight and England's third. The player-level tests are exploratory; none remains below 0.05 after Holm correction.
            6. **Effort and control separated.** France produced its highest direct-pressure count but worst turnover yield; both teams conceded their highest opponent xG of the tournament. The players ran and pressed, but the collective defensive system did not convert that work into control.
            7. **Contact did not disappear; consequence did.** Match 103 had 22 fouls versus 22.39 in earlier regulation-time matches, but zero cards versus 2.79. The cardless knockout tail is suggestive rather than conclusive (empirical p≈0.065–0.087), especially after referee and foul-band sensitivity checks.
            8. **The action-to-control split is the boldest insight.** Across both teams, tackles attempted rose 61%, direct pressures 52%, and high-intensity distance 16%; clearances fell 65%, possession contests won 53%, and aerial duels won 53%. Tackles won rose 53%, showing reactive engagement rather than passivity.
            9. **The individual-incentive mechanism now has behavioural evidence.** Mbappe's eight attempts were 64% above his prior per-90 rate, while Olise doubled his prior rate of in-behind offers and more than tripled his direct-pressure rate. This supports a stat-opportunity mechanism, not proof of conscious intent.
            10. **The game was open from process and amplified by finishing.** It exceeded every earlier 2026 match in total xG and shots on target, then produced ten goals from 5.33 xG. England supplied most of the finishing overperformance with six goals from 2.34 xG.
            11. **Game state amplified the spectacle.** The 4–0 lead raised the historical scoring expectation by roughly one-third, but the state-conditioned expectation remained far below ten.
            12. **The expanded benchmark improves context but weakens the shortcut.** England–France's ten goals exceeded all 15 Soccer Aid rows, but creator-led formats in the expanded 41-match file reached 10–20 regulation-time goals. The event-level spread shows why there is no single “charity average” that proves equivalence.

            ### Final interpretation

            The evidence supports calling England–France an **exhibition-profile, spectacle-first official match**. The all-versus-all classifier reaches that conclusion without using goals: attacking action and disciplinary restraint sit on the exhibition side, while the normal foul count and high physical activity show that players did not simply stop working. They stopped behaving as if preventing the next goal was the dominant objective. This is not evidence of a pre-arranged score.

            ### Hypothesis verdict

            **Overall: literal H1 is partially supported because broad physical coasting is contradicted. H4—the observable exhibition-profile hypothesis—is supported with moderate-high confidence, as is H3's spectacle-first tendency. H2 is supported as an incentive/opportunity mechanism with moderate confidence, while intentional stat-padding remains suggestive.** The statistics show a coherent direction—more visible action and personal-output opportunity, less collective control and disciplinary consequence. They do not prove coordination, an agreed score, or private motive.

            ### Remaining data gap

            Minute-by-minute foul locations, tactical-foul labels, and positional tracking would show whether the disappearance of restraint occurred before or only after the 4–0 score. Integrity evidence—communications, unusual betting patterns, or an official investigation—would be required to test coordination or pre-arrangement. Match statistics alone can identify the spectacle-first tendency, not its private origin.
            """
        ),
    ]
    return nb


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    notebook = build_notebook()
    nbf.write(notebook, OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
