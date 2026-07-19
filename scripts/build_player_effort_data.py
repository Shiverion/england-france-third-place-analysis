"""Build compact player-level FIFA PMSR data for France and England.

The official reports are large PDFs. Reports already present in ``data/fifa``
are read locally; missing reports are fetched in memory from FIFA and are not
persisted. The output CSVs are therefore compact enough to version while every
row retains its official source URL.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import re
from urllib.request import Request, urlopen

import fitz
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIFA_DIR = ROOT / "data" / "fifa"
PROCESSED_DIR = ROOT / "data" / "processed"
SOURCE_BASE = "https://www.fifatrainingcentre.com/media/native/tournaments/fifa-world-cup/2026"
USER_AGENT = "Mozilla/5.0 (compatible; reproducible-football-analysis/1.0)"


@dataclass(frozen=True)
class MatchSpec:
    match_number: int
    filename: str
    left_team: str
    right_team: str
    stage: str

    @property
    def source_url(self) -> str:
        return f"{SOURCE_BASE}/{self.filename}"


MATCH_SPECS = [
    MatchSpec(17, "PMSR-M17-FRA-V-SEN.pdf", "France", "Senegal", "Group stage"),
    MatchSpec(22, "PMSR-M22-ENG-V-CRO.pdf", "England", "Croatia", "Group stage"),
    MatchSpec(42, "PMSR-M42-FRA-V-IRQ.pdf", "France", "Iraq", "Group stage"),
    MatchSpec(45, "PMSR-M45-ENG-V-GHA.pdf", "England", "Ghana", "Group stage"),
    MatchSpec(61, "PMSR-M61-NOR-V-FRA.pdf", "Norway", "France", "Group stage"),
    MatchSpec(67, "PMSR-M67-PAN-V-ENG.pdf", "Panama", "England", "Group stage"),
    MatchSpec(77, "PMSR-M77-FRA-V-SWE.pdf", "France", "Sweden", "Round of 32"),
    MatchSpec(80, "PMSR-M80-ENG-V-COD.pdf", "England", "Congo DR", "Round of 32"),
    MatchSpec(89, "PMSR-M89-PAR-V-FRA.pdf", "Paraguay", "France", "Round of 16"),
    MatchSpec(92, "PMSR-M92-MEX-V-ENG.pdf", "Mexico", "England", "Round of 16"),
    MatchSpec(97, "PMSR-M97-FRA-V-MAR.pdf", "France", "Morocco", "Quarter-final"),
    MatchSpec(99, "PMSR-M99-NOR-V-ENG.pdf", "Norway", "England", "Quarter-final"),
    MatchSpec(101, "PMSR-M101-FRA-V-ESP.pdf", "France", "Spain", "Semi-final"),
    MatchSpec(102, "PMSR-M102-ENG-V-ARG.pdf", "England", "Argentina", "Semi-final"),
    MatchSpec(103, "PMSR-M103-FRA-V-ENG.pdf", "France", "England", "Third-place"),
]

# Match 61's summary row uses all visible event slots for Dembele's hat-trick,
# so his substitution time is not recoverable from that row. FIFA's own match
# article explicitly states that he left in the 65th minute.
MINUTE_OVERRIDES = {
    (61, "France", 7): {
        "minutes": 65.0,
        "source_url": (
            "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/"
            "articles/ousmane-dembele-hat-trick-norway"
        ),
        "note": "Official FIFA article states that Dembele left in the 65th minute.",
    }
}


TABLE_CONFIG = {
    "distribution": {
        "marker": "In Possession - Distributions {team}",
        "rename": {
            "passes_attempted": "passes_attempted",
            "passes_completed": "passes_completed",
            "pass_completion": "pass_completion_pct",
            "switches_of_play": "switches_of_play",
            "crosses_attempted": "crosses_attempted",
            "crosses_completed": "crosses_completed",
            "line_breaks_attempted": "line_breaks_attempted",
            "line_breaks_completed": "line_breaks_completed",
            "line_break_completion": "line_break_completion_pct",
            "ball_progressions": "ball_progressions",
            "take_ons": "take_ons",
            "step_ins": "step_ins",
            "attempts_at_goal": "attempts_at_goal",
            "goals": "goals",
        },
    },
    "offers": {
        "marker": "In Possession - Offers & Receptions {team}",
        "rename": {
            "total_offers": "total_offers",
            "in_front": "offers_in_front",
            "in_between": "offers_in_between",
            "out_to_in": "offers_out_to_in",
            "in_to_out": "offers_in_to_out",
            "in_behind": "offers_in_behind",
            "no_movement": "offers_no_movement",
            "offers_received": "offers_received",
        },
    },
    "defending": {
        "marker": "Out of Possession {team}",
        "rename": {
            "blocks": "blocks",
            "interceptions": "interceptions",
            "pressing_direct": "pressures_direct",
            "pressing_indirect": "pressures_indirect",
            "duels_won_aerial": "duels_won_aerial",
            "duels_won_physical": "duels_won_physical",
            "possession_contests_won": "possession_contests_won",
            "clearances": "clearances",
            "loose_ball_receptions": "loose_ball_receptions",
            "pushing_on": "pushing_on",
            "pushing_on_into_pressing": "pushing_on_into_pressing",
            "possession_regains": "possession_regains",
            "possession_interrupted": "possession_interrupted",
        },
    },
    "physical": {
        "marker": "Physical Data {team}",
        "rename": {
            "total_distance_m": "total_distance_m",
            "zone_1_0_7_km_h_m": "zone1_distance_m",
            "zone_2_7_15_km_h_m": "zone2_distance_m",
            "zone_3_15_20_km_h_m": "zone3_distance_m",
            "zone_4_20_25_km_h_m": "zone4_distance_m",
            "zone_5_25_km_h_m": "zone5_distance_m",
            "high_speed_runs_zone_3": "high_speed_runs",
            "sprints_zone_4_5": "sprints",
            "top_speed_km_h": "top_speed_kmh",
        },
    },
}


def load_pdf(spec: MatchSpec) -> bytes:
    local_path = FIFA_DIR / spec.filename
    if local_path.exists():
        return local_path.read_bytes()

    request = Request(
        spec.source_url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*"},
    )
    with urlopen(request, timeout=120) as response:
        payload = response.read()
    if not payload.startswith(b"%PDF"):
        raise ValueError(f"FIFA source did not return a PDF: {spec.source_url}")
    return payload


def compact_text(page: fitz.Page) -> str:
    return " ".join(page.get_text().split())


def find_page(document: fitz.Document, marker: str) -> fitz.Page:
    for page in document:
        if marker in compact_text(page)[:250]:
            return page
    raise ValueError(f"Could not locate FIFA PMSR page: {marker}")


def header_key(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("%", "").replace("&", " ")
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def numeric_value(value: str) -> float:
    cleaned = value.replace("%", "").replace(",", "").strip()
    if not cleaned:
        return 0.0
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(match.group()) if match else 0.0


def table_header(page: fitz.Page) -> tuple[list[str], list[tuple[float, float, float, float]], float]:
    found = page.find_tables()
    for table in found.tables:
        extracted = table.extract()
        for row_index, row_values in enumerate(extracted):
            cleaned = ["" if value is None else str(value) for value in row_values]
            if "Player" not in cleaned:
                continue
            cells = table.rows[row_index].cells
            if any(cell is None for cell in cells):
                continue
            typed_cells = [tuple(cell) for cell in cells]
            return cleaned, typed_cells, max(cell[3] for cell in typed_cells)
    raise ValueError("Could not identify a complete player-table header.")


def parse_player_table(page: fitz.Page, table_kind: str) -> pd.DataFrame:
    header_names, header_cells, header_bottom = table_header(page)
    keys = [header_key(name) for name in header_names]
    first_cell = header_cells[0]
    words = page.get_text("words", sort=True)

    anchors: list[tuple[float, int]] = []
    for word in words:
        x0, y0, x1, _y1, text, *_ = word
        center = (x0 + x1) / 2
        if y0 <= header_bottom + 2 or not (first_cell[0] <= center <= first_cell[2]):
            continue
        if text.isdigit() and 1 <= int(text) <= 30:
            anchors.append((y0, int(text)))

    rows: list[dict[str, object]] = []
    for row_y, shirt_number in anchors:
        row_words = [word for word in words if abs(word[1] - row_y) <= 1.25]
        values: list[str] = []
        for cell in header_cells:
            tokens = []
            for word in row_words:
                x0, _y0, x1, _y1, text, *_ = word
                center = (x0 + x1) / 2
                if cell[0] <= center <= cell[2]:
                    tokens.append((x0, text))
            values.append(" ".join(text for _x, text in sorted(tokens)))

        raw = dict(zip(keys, values))
        player_name = raw.get("player", "").strip()
        if not player_name:
            continue
        row: dict[str, object] = {
            "shirt_number": shirt_number,
            "player": " ".join(part.capitalize() for part in player_name.split()),
        }

        if table_kind == "defending":
            tackles = raw.get("tackles_made_won", "")
            tackle_values = [int(value) for value in re.findall(r"\d+", tackles)]
            row["tackles_made"] = tackle_values[0] if tackle_values else 0
            row["tackles_won"] = tackle_values[1] if len(tackle_values) > 1 else 0

        rename = TABLE_CONFIG[table_kind]["rename"]
        for raw_name, output_name in rename.items():
            row[output_name] = numeric_value(raw.get(raw_name, ""))
        rows.append(row)

    frame = pd.DataFrame(rows)
    if frame.empty or frame["shirt_number"].duplicated().any():
        raise ValueError(f"Invalid {table_kind} player table on page {page.number + 1}.")
    return frame


TIME_PATTERN = re.compile(r"^(\d+)(?:\+(\d+))?'$")
POSITION_PATTERN = re.compile(r"^(GK|DF|MF|FW)(\d*)$")


def clock_minute(value: str, duration: int) -> int:
    match = TIME_PATTERN.match(value)
    if not match:
        raise ValueError(value)
    base = int(match.group(1))
    extra = int(match.group(2) or 0)
    return min(base + extra, duration)


def parse_lineup_minutes(
    page: fitz.Page,
    left_team: str,
    right_team: str,
) -> tuple[pd.DataFrame, int]:
    words = page.get_text("words", sort=True)
    duration = 120 if any(
        word[4] == "120" and 300 <= (word[0] + word[2]) / 2 <= 660 for word in words
    ) else 90

    substitute_labels = [word for word in words if word[4] == "SUBSTITUTES"]
    if len(substitute_labels) < 2:
        raise ValueError("Could not locate both substitute lists.")
    left_sub_y = min(word[1] for word in substitute_labels if word[0] < 300)
    right_sub_y = min(word[1] for word in substitute_labels if word[0] > 700)

    player_rows: list[dict[str, object]] = []
    for side, team, position_x_min, position_x_max, sub_y in [
        ("left", left_team, 65, 86, left_sub_y),
        ("right", right_team, 878, 915, right_sub_y),
    ]:
        for word in words:
            x0, y0, x1, _y1, text, *_ = word
            if not (position_x_min <= x0 <= position_x_max):
                continue
            position_match = POSITION_PATTERN.match(text)
            if not position_match or not (125 <= y0 <= 510):
                continue

            same_line = [candidate for candidate in words if abs(candidate[1] - y0) <= 1.25]
            if side == "left":
                jersey_words = [candidate for candidate in same_line if candidate[2] <= 65 and candidate[4].isdigit()]
                name_candidates = [
                    candidate for candidate in words
                    if abs(candidate[1] - y0) <= 7
                    and 85 <= candidate[0] < 230
                    and not TIME_PATTERN.match(candidate[4])
                ]
                event_words = [
                    candidate for candidate in same_line
                    if 160 <= candidate[0] <= 300 and TIME_PATTERN.match(candidate[4])
                ]
            else:
                embedded_number = position_match.group(2)
                jersey_words = [candidate for candidate in same_line if candidate[0] >= 897 and candidate[4].isdigit()]
                name_candidates = [
                    candidate for candidate in words
                    if abs(candidate[1] - y0) <= 7
                    and 760 <= candidate[0]
                    and candidate[2] <= 876
                    and not TIME_PATTERN.match(candidate[4])
                ]
                event_words = [
                    candidate for candidate in same_line
                    if 690 <= candidate[0] <= 810 and TIME_PATTERN.match(candidate[4])
                ]
                if embedded_number and not jersey_words:
                    jersey_words = [(0, 0, 0, 0, embedded_number)]

            if name_candidates:
                closest_name_y = min(name_candidates, key=lambda item: abs(item[1] - y0))[1]
                name_words = [
                    candidate for candidate in name_candidates
                    if abs(candidate[1] - closest_name_y) <= 1.25
                ]
            else:
                name_words = []

            if not jersey_words or not name_words:
                continue
            shirt_number = int(jersey_words[0][4])
            player_name = " ".join(
                candidate[4] for candidate in sorted(name_words, key=lambda item: item[0])
            )
            event_times = sorted({clock_minute(candidate[4], duration) for candidate in event_words})
            player_rows.append({
                "team": team,
                "shirt_number": shirt_number,
                "player_lineup": " ".join(part.capitalize() for part in player_name.split()),
                "position": position_match.group(1),
                "started": y0 < sub_y,
                "event_times": event_times,
            })

    lineup = pd.DataFrame(player_rows)
    if lineup.duplicated(["team", "shirt_number"]).any():
        duplicates = lineup[lineup.duplicated(["team", "shirt_number"], keep=False)]
        raise ValueError(f"Duplicate lineup rows:\n{duplicates}")

    for team in (left_team, right_team):
        team_rows = lineup[lineup["team"].eq(team)]
        starter_times = {
            time
            for times in team_rows.loc[team_rows["started"], "event_times"]
            for time in times
        }
        substitute_times = {
            time
            for times in team_rows.loc[~team_rows["started"], "event_times"]
            for time in times
        }
        shared_times = starter_times & substitute_times
        for index in team_rows.index:
            row_times = [time for time in lineup.at[index, "event_times"] if time in shared_times]
            if lineup.at[index, "started"]:
                lineup.at[index, "minutes"] = min(row_times) if row_times else duration
            else:
                lineup.at[index, "minutes"] = duration - min(row_times) if row_times else 0

    lineup["minutes"] = lineup["minutes"].astype(float)
    return lineup.drop(columns="event_times"), duration


def parse_match(spec: MatchSpec, payload: bytes) -> tuple[pd.DataFrame, pd.DataFrame]:
    document = fitz.open(stream=BytesIO(payload), filetype="pdf")
    lineup_page = find_page(document, "Match Summary - Teams")
    lineup, duration = parse_lineup_minutes(lineup_page, spec.left_team, spec.right_team)

    player_frames: list[pd.DataFrame] = []
    for team in (spec.left_team, spec.right_team):
        tables: dict[str, pd.DataFrame] = {}
        for table_kind, config in TABLE_CONFIG.items():
            page = find_page(document, config["marker"].format(team=team))
            tables[table_kind] = parse_player_table(page, table_kind)

        merged = tables["physical"]
        for table_kind in ("distribution", "offers", "defending"):
            addition = tables[table_kind].drop(columns="player")
            merged = merged.merge(addition, on="shirt_number", how="left", validate="one_to_one")

        merged.insert(0, "match_number", spec.match_number)
        merged.insert(1, "stage", spec.stage)
        merged.insert(2, "team", team)
        merged.insert(3, "opponent", spec.right_team if team == spec.left_team else spec.left_team)
        merged.insert(4, "match_duration", duration)
        merged = merged.merge(
            lineup[lineup["team"].eq(team)].drop(columns="team"),
            on="shirt_number",
            how="left",
            validate="one_to_one",
        )
        merged["source_url"] = spec.source_url
        merged["minutes_source_url"] = spec.source_url
        merged["minutes_note"] = "Paired substitution times on the FIFA PMSR team-summary page."
        for (match_number, override_team, shirt_number), override in MINUTE_OVERRIDES.items():
            if match_number != spec.match_number or override_team != team:
                continue
            mask = merged["shirt_number"].eq(shirt_number)
            if mask.sum() != 1:
                raise ValueError(f"Minute override key did not resolve uniquely: {(match_number, team, shirt_number)}")
            merged.loc[mask, "minutes"] = override["minutes"]
            merged.loc[mask, "minutes_source_url"] = override["source_url"]
            merged.loc[mask, "minutes_note"] = override["note"]
        if merged[["minutes", "position", "started"]].isna().any().any():
            missing = merged.loc[merged["minutes"].isna(), ["shirt_number", "player"]]
            raise ValueError(f"Lineup join failed for match {spec.match_number}, {team}:\n{missing}")
        player_frames.append(merged)

    players = pd.concat(player_frames, ignore_index=True)
    players["high_intensity_distance_m"] = players["zone4_distance_m"] + players["zone5_distance_m"]

    aggregation = {
        "total_distance_m": "sum",
        "zone3_distance_m": "sum",
        "zone4_distance_m": "sum",
        "zone5_distance_m": "sum",
        "high_intensity_distance_m": "sum",
        "high_speed_runs": "sum",
        "sprints": "sum",
        "attempts_at_goal": "sum",
        "goals": "sum",
        "pressures_direct": "sum",
        "pressures_indirect": "sum",
        "offers_in_behind": "sum",
        "minutes": "sum",
    }
    teams = players.groupby(
        ["match_number", "stage", "team", "opponent", "match_duration", "source_url"],
        as_index=False,
    ).agg(aggregation)
    for column in [
        "total_distance_m",
        "zone3_distance_m",
        "zone4_distance_m",
        "zone5_distance_m",
        "high_intensity_distance_m",
        "high_speed_runs",
        "sprints",
        "pressures_direct",
        "pressures_indirect",
        "offers_in_behind",
    ]:
        teams[f"{column}_per90"] = teams[column] / teams["match_duration"] * 90

    return players, teams


def build() -> tuple[pd.DataFrame, pd.DataFrame]:
    all_players: list[pd.DataFrame] = []
    all_teams: list[pd.DataFrame] = []
    for spec in MATCH_SPECS:
        print(f"Parsing match {spec.match_number}: {spec.left_team} v {spec.right_team}")
        players, teams = parse_match(spec, load_pdf(spec))
        focal_players = players[players["team"].isin(["France", "England"])].copy()
        focal_teams = teams[teams["team"].isin(["France", "England"])].copy()
        all_players.append(focal_players)
        all_teams.append(focal_teams)

    player_data = pd.concat(all_players, ignore_index=True)
    team_data = pd.concat(all_teams, ignore_index=True)

    numeric_columns = player_data.select_dtypes(include=np.number).columns
    player_data[numeric_columns] = player_data[numeric_columns].fillna(0)
    player_data = player_data.sort_values(["team", "match_number", "shirt_number"], kind="stable")
    team_data = team_data.sort_values(["team", "match_number"], kind="stable")

    expected_matches = {"France": 8, "England": 8}
    observed_matches = player_data.groupby("team")["match_number"].nunique().to_dict()
    if observed_matches != expected_matches:
        raise ValueError(f"Unexpected focal match coverage: {observed_matches}")
    if player_data.duplicated(["match_number", "team", "shirt_number"]).any():
        raise ValueError("Player-match-shirt key is not unique.")
    minute_totals = player_data.groupby(["match_number", "team", "match_duration"])["minutes"].sum()
    expected_minute_totals = minute_totals.index.get_level_values("match_duration") * 11
    if not np.allclose(minute_totals.to_numpy(), expected_minute_totals):
        raise ValueError("Parsed player minutes do not reconcile to eleven players on the pitch.")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    player_path = PROCESSED_DIR / "fifa_2026_france_england_player_match.csv"
    team_path = PROCESSED_DIR / "fifa_2026_france_england_team_physical.csv"
    player_data.to_csv(player_path, index=False)
    team_data.to_csv(team_path, index=False)
    print(f"Wrote {len(player_data)} player-match rows to {player_path}")
    print(f"Wrote {len(team_data)} team-match rows to {team_path}")
    return player_data, team_data


if __name__ == "__main__":
    build()
