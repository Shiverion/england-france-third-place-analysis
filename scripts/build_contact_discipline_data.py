from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import fitz
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
BASE_URL = (
    "https://fdp.fifa.org/assetspublic/ce281/"
    "r{asset_id}/pdf/FullTimeMatchReport-English.pdf"
)
ASSET_IDS = range(12449, 12552)  # 103 published reports, matches 1-103.
USER_AGENT = "EnglandFranceMatchAnalysis/2.0 (public reproducibility project)"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def fetch_report(asset_id: int, retries: int = 3) -> tuple[int, str, bytes]:
    url = BASE_URL.format(asset_id=asset_id)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=45) as response:
                payload = response.read()
            if not payload.startswith(b"%PDF"):
                raise ValueError(f"Asset r{asset_id} did not return a PDF")
            return asset_id, url, payload
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            last_error = error
            if attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Unable to fetch r{asset_id}: {last_error}")


def stage_from_match_number(match_number: int) -> str:
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
        return "Bronze final"
    return "Final"


def extract_pair(text: str, label_pattern: str) -> tuple[int, int]:
    match = re.search(rf"(\d+)\s+{label_pattern}\s+(\d+)", text, flags=re.I)
    if not match:
        raise ValueError(f"Could not parse statistic: {label_pattern}")
    return int(match.group(1)), int(match.group(2))


def extract_slash_pair(text: str, label_pattern: str) -> tuple[int, int, int, int]:
    match = re.search(
        rf"(\d+)\s*/\s*(\d+)\s+{label_pattern}\s+(\d+)\s*/\s*(\d+)",
        text,
        flags=re.I,
    )
    if not match:
        raise ValueError(f"Could not parse slash statistic: {label_pattern}")
    return tuple(int(value) for value in match.groups())


def parse_report(asset_id: int, url: str, payload: bytes) -> tuple[dict, list[dict]]:
    document = fitz.open(stream=BytesIO(payload), filetype="pdf")
    if len(document) < 4:
        raise ValueError(f"r{asset_id}: expected at least four pages, found {len(document)}")

    cover_text = normalize(document[0].get_text("text", sort=True))
    stats_page_text = next(
        (
            page.get_text("text", sort=True)
            for page in document
            if "Statistics" in page.get_text("text", sort=True)
            and "Fouls Against" in page.get_text("text", sort=True)
        ),
        "",
    )
    if not stats_page_text:
        raise ValueError(f"r{asset_id}: statistics page not found")
    stats_text = normalize(stats_page_text)
    stats_lines = [normalize(line) for line in stats_page_text.splitlines() if normalize(line)]

    match_number_match = re.search(r"#(\d+)\s*\|", stats_text)
    if not match_number_match:
        raise ValueError(f"r{asset_id}: match number not found")
    match_number = int(match_number_match.group(1))

    team_line = next(
        (line for line in stats_lines if " Statistics " in f" {line} "),
        "",
    )
    team_match = re.match(
        r"^(.+?)\s*\(([A-Z]{3})\)\s+Statistics\s+(.+?)\s*\(([A-Z]{3})\)$",
        team_line,
    )
    if not team_match:
        raise ValueError(f"r{asset_id}: team names not found")
    left_team, left_code, right_team, right_code = (
        value.strip() for value in team_match.groups()
    )

    score_line = next(
        (line for line in stats_lines if " v. " in line and re.search(r"\d+-\d+", line)),
        "",
    )
    score_match = re.search(
        rf"{re.escape(left_team)}\s+v\.\s+{re.escape(right_team)}\s+"
        r"(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?",
        score_line,
        flags=re.I,
    )
    if not score_match:
        raise ValueError(f"r{asset_id}: score not found")
    left_goals, right_goals = (int(value) for value in score_match.groups()[:2])
    left_half = int(score_match.group(3)) if score_match.group(3) is not None else 0
    right_half = int(score_match.group(4)) if score_match.group(4) is not None else 0

    referee_match = re.search(r"Referee:\s*(.*?)\s+VAR:", cover_text, flags=re.I)
    if not referee_match:
        raise ValueError(f"r{asset_id}: referee not found")
    referee = referee_match.group(1).strip()
    went_to_extra_time = bool(re.search(r"\bAET\b", cover_text))
    penalty_shootout = bool(re.search(r"\bPSO\b", cover_text))
    match_duration_minutes = 120 if went_to_extra_time else 90

    attempts = extract_slash_pair(
        stats_text, r"Attempts at Goal \(Total/On Target\)"
    )
    penalties = extract_slash_pair(stats_text, r"Penalties \(total/scored\)")
    blocked = extract_pair(stats_text, r"Attempts at Goal blocked")
    fouls = extract_pair(stats_text, r"Fouls Against")
    corners = extract_pair(stats_text, r"Corners")
    direct_free_kicks = extract_pair(stats_text, r"Direct free kicks")
    indirect_free_kicks = extract_pair(stats_text, r"Indirect free kicks")
    offsides = extract_pair(stats_text, r"Offsides")
    own_goals = extract_pair(stats_text, r"Own goals")
    yellow_cards = extract_pair(stats_text, r"Yellow cards")
    second_yellow_reds = extract_pair(stats_text, r"Red Cards for second caution")
    direct_reds = extract_pair(stats_text, r"Direct red cards")

    possession_match = re.search(
        r"(\d+)%\s+Ball possession\s+(\d+)%", stats_text, flags=re.I
    )
    if not possession_match:
        raise ValueError(f"r{asset_id}: possession not found")
    possession = tuple(int(value) for value in possession_match.groups())

    stage = stage_from_match_number(match_number)
    match_row = {
        "match_number": match_number,
        "stage": stage,
        "left_team": left_team,
        "left_code": left_code,
        "right_team": right_team,
        "right_code": right_code,
        "left_goals": left_goals,
        "right_goals": right_goals,
        "total_goals": left_goals + right_goals,
        "half_time_total_goals": left_half + right_half,
        "went_to_extra_time": went_to_extra_time,
        "penalty_shootout": penalty_shootout,
        "match_duration_minutes": match_duration_minutes,
        "referee": referee,
        "went_to_extra_time": went_to_extra_time,
        "penalty_shootout": penalty_shootout,
        "match_duration_minutes": match_duration_minutes,
        "total_fouls": fouls[0] + fouls[1],
        "total_yellow_cards": yellow_cards[0] + yellow_cards[1],
        "total_second_yellow_reds": second_yellow_reds[0] + second_yellow_reds[1],
        "total_direct_reds": direct_reds[0] + direct_reds[1],
        "total_card_events": sum(yellow_cards) + sum(second_yellow_reds) + sum(direct_reds),
        "fair_play_penalty_points": (
            sum(yellow_cards) + 3 * sum(second_yellow_reds) + 4 * sum(direct_reds)
        ),
        "cards_per_10_fouls": (
            10 * (sum(yellow_cards) + sum(second_yellow_reds) + sum(direct_reds))
            / (fouls[0] + fouls[1])
        ),
        "asset_id": asset_id,
        "source_url": url,
    }

    shared = {
        "match_number": match_number,
        "stage": stage,
        "referee": referee,
        "asset_id": asset_id,
        "source_url": url,
    }
    values = [
        {
            "team": left_team,
            "team_code": left_code,
            "opponent": right_team,
            "opponent_code": right_code,
            "side": "left",
            "goals_for": left_goals,
            "goals_against": right_goals,
            "possession_pct": possession[0],
            "attempts_at_goal": attempts[0],
            "shots_on_target": attempts[1],
            "attempts_blocked": blocked[0],
            "fouls_committed": fouls[0],
            "fouls_suffered": fouls[1],
            "corners": corners[0],
            "direct_free_kicks_awarded": direct_free_kicks[0],
            "indirect_free_kicks_awarded": indirect_free_kicks[0],
            "penalties_awarded": penalties[0],
            "penalties_scored": penalties[1],
            "offsides": offsides[0],
            "own_goals": own_goals[0],
            "yellow_cards": yellow_cards[0],
            "second_yellow_reds": second_yellow_reds[0],
            "direct_reds": direct_reds[0],
        },
        {
            "team": right_team,
            "team_code": right_code,
            "opponent": left_team,
            "opponent_code": left_code,
            "side": "right",
            "goals_for": right_goals,
            "goals_against": left_goals,
            "possession_pct": possession[1],
            "attempts_at_goal": attempts[2],
            "shots_on_target": attempts[3],
            "attempts_blocked": blocked[1],
            "fouls_committed": fouls[1],
            "fouls_suffered": fouls[0],
            "corners": corners[1],
            "direct_free_kicks_awarded": direct_free_kicks[1],
            "indirect_free_kicks_awarded": indirect_free_kicks[1],
            "penalties_awarded": penalties[2],
            "penalties_scored": penalties[3],
            "offsides": offsides[1],
            "own_goals": own_goals[1],
            "yellow_cards": yellow_cards[1],
            "second_yellow_reds": second_yellow_reds[1],
            "direct_reds": direct_reds[1],
        },
    ]
    team_rows: list[dict] = []
    for row in values:
        row.update(shared)
        row["card_events"] = (
            row["yellow_cards"] + row["second_yellow_reds"] + row["direct_reds"]
        )
        row["fair_play_penalty_points"] = (
            row["yellow_cards"]
            + 3 * row["second_yellow_reds"]
            + 4 * row["direct_reds"]
        )
        row["cards_per_10_fouls"] = (
            10 * row["card_events"] / row["fouls_committed"]
            if row["fouls_committed"]
            else 0.0
        )
        row["fouls_committed_per90"] = (
            90 * row["fouls_committed"] / match_duration_minutes
        )
        row["card_events_per90"] = 90 * row["card_events"] / match_duration_minutes
        team_rows.append(row)

    return match_row, team_rows


def main() -> None:
    fetched: dict[int, tuple[str, bytes]] = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_report, asset_id): asset_id for asset_id in ASSET_IDS}
        for index, future in enumerate(as_completed(futures), start=1):
            asset_id, url, payload = future.result()
            fetched[asset_id] = (url, payload)
            if index % 20 == 0 or index == len(ASSET_IDS):
                print(f"Fetched {index}/{len(ASSET_IDS)} official reports")

    match_rows: list[dict] = []
    team_rows: list[dict] = []
    for asset_id in sorted(fetched):
        url, payload = fetched[asset_id]
        match_row, parsed_team_rows = parse_report(asset_id, url, payload)
        match_rows.append(match_row)
        team_rows.extend(parsed_team_rows)

    matches = pd.DataFrame(match_rows).sort_values("match_number").reset_index(drop=True)
    teams = pd.DataFrame(team_rows).sort_values(["match_number", "side"]).reset_index(drop=True)

    expected_matches = set(range(1, 104))
    parsed_matches = set(matches["match_number"])
    if parsed_matches != expected_matches:
        missing = sorted(expected_matches - parsed_matches)
        extra = sorted(parsed_matches - expected_matches)
        raise ValueError(f"Match coverage mismatch; missing={missing}, extra={extra}")
    if matches["match_number"].duplicated().any():
        raise ValueError("Duplicate match numbers in match-level output")
    if not teams.groupby("match_number").size().eq(2).all():
        raise ValueError("Every match must produce exactly two team rows")
    reconciliation = teams.merge(
        teams[["match_number", "team", "fouls_committed"]],
        left_on=["match_number", "opponent"],
        right_on=["match_number", "team"],
        suffixes=("", "_opponent"),
    )
    if not reconciliation["fouls_suffered"].eq(
        reconciliation["fouls_committed_opponent"]
    ).all():
        raise ValueError("Fouls suffered do not reconcile to opponent fouls committed")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    match_path = PROCESSED / "fifa_2026_match_contact_discipline.csv"
    team_path = PROCESSED / "fifa_2026_team_contact_discipline.csv"
    matches.to_csv(match_path, index=False)
    teams.to_csv(team_path, index=False)
    print(f"Saved {len(matches)} match rows to {match_path}")
    print(f"Saved {len(teams)} team rows to {team_path}")


if __name__ == "__main__":
    main()
