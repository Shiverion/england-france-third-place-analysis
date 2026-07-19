"""Build a plain-language infographic for the effort-versus-control finding."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "output" / "assets" / "narrative_05_effort_without_control.png"
TABLES = ROOT / "output" / "tables"

BLUE = "#2F6BFF"
BLUE_LIGHT = "#DCE6FF"
ORANGE = "#E28A2B"
ORANGE_LIGHT = "#FBE6C9"
INK = "#1F2937"
MUTED = "#667085"
GRID = "#D9DEE7"
BG = "#FCFCFD"


def card(ax, x: float, y: float, width: float, height: float, face: str) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            linewidth=1.2,
            edgecolor=GRID,
            facecolor=face,
            transform=ax.transAxes,
        )
    )


def main() -> None:
    tests = pd.read_csv(TABLES / "v2_player_effort_tests.csv")
    ranks = pd.read_csv(TABLES / "v2_effort_control_ranks.csv")

    high_intensity = float(tests.loc[tests["metric"].eq("high_intensity_distance_m"), "relative_delta_pct"].iloc[0])
    direct_pressures = float(tests.loc[tests["metric"].eq("pressures_direct"), "relative_delta_pct"].iloc[0])
    total_distance = float(tests.loc[tests["metric"].eq("total_distance_m"), "relative_delta_pct"].iloc[0])
    france_pressure_rank = int(ranks.loc[(ranks["team"].eq("France")) & ranks["metric"].eq("fifa_direct_pressures"), "rank_high_to_low"].iloc[0])
    france_yield_rank = int(ranks.loc[(ranks["team"].eq("France")) & ranks["metric"].eq("turnovers_per_100_pressures"), "rank_high_to_low"].iloc[0])

    fig = plt.figure(figsize=(16, 9), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    ax.text(0.06, 0.90, "THEY RAN. THEY PRESSED. THEY LOST CONTROL.", fontsize=28, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(
        0.06, 0.845,
        "The 6–4 match looked relaxed because the defensive system stopped working together—not because everyone stopped working.",
        fontsize=14, color=MUTED, transform=ax.transAxes,
    )

    card(ax, 0.06, 0.755, 0.88, 0.065, ORANGE_LIGHT)
    ax.text(
        0.08, 0.785,
        "HYPOTHESIS H1: this official match behaved like a low-pressure fun/charity match — less effort and defending, more open scoring",
        fontsize=10.5, fontweight="bold", color=INK, transform=ax.transAxes,
    )
    ax.text(
        0.08, 0.767,
        "HYPOTHESIS H2: award leaders used the match to boost goals, assists, or records",
        fontsize=10.5, fontweight="bold", color=INK, transform=ax.transAxes,
    )

    card(ax, 0.06, 0.28, 0.27, 0.47, BLUE_LIGHT)
    card(ax, 0.67, 0.28, 0.27, 0.47, ORANGE_LIGHT)

    ax.text(0.085, 0.69, "WHAT THE PLAYERS DID", fontsize=15, fontweight="bold", color=BLUE, transform=ax.transAxes)
    ax.text(0.085, 0.59, f"+{high_intensity:.0f}%", fontsize=34, fontweight="bold", color=BLUE, transform=ax.transAxes)
    ax.text(0.085, 0.55, "fast running", fontsize=15, color=INK, transform=ax.transAxes)
    ax.text(0.085, 0.46, f"+{direct_pressures:.0f}%", fontsize=34, fontweight="bold", color=BLUE, transform=ax.transAxes)
    ax.text(0.085, 0.42, "direct pressure", fontsize=15, color=INK, transform=ax.transAxes)
    ax.text(0.085, 0.34, f"{total_distance:+.0f}%", fontsize=26, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.19, 0.345, "total distance", fontsize=13, color=INK, transform=ax.transAxes)
    ax.text(0.085, 0.305, "19 comparable outfielders vs their own earlier tournament rates", fontsize=9.5, color=MUTED, transform=ax.transAxes)

    ax.text(0.695, 0.69, "WHAT THE TEAM COULD NOT DO", fontsize=15, fontweight="bold", color=ORANGE, transform=ax.transAxes)
    ax.text(0.695, 0.59, f"#{france_pressure_rank} of 8", fontsize=26, fontweight="bold", color=ORANGE, transform=ax.transAxes)
    ax.text(0.695, 0.55, "France for pressure attempts", fontsize=14, color=INK, transform=ax.transAxes)
    ax.text(0.695, 0.46, f"#{france_yield_rank} of 8", fontsize=26, fontweight="bold", color=ORANGE, transform=ax.transAxes)
    ax.text(0.695, 0.42, "France for turning pressure into takeaways", fontsize=14, color=INK, transform=ax.transAxes)
    ax.text(0.695, 0.34, "#1 worst", fontsize=26, fontweight="bold", color=ORANGE, transform=ax.transAxes)
    ax.text(0.695, 0.30, "opponent chance quality for both teams", fontsize=13, color=INK, transform=ax.transAxes)

    # A deliberately interrupted connector: the visual metaphor is the failed
    # conversion from individual activity to collective defensive control.
    ax.add_patch(FancyArrowPatch((0.36, 0.515), (0.445, 0.515), transform=ax.transAxes, arrowstyle="-|>", mutation_scale=18, linewidth=3, color=BLUE))
    ax.add_patch(FancyArrowPatch((0.555, 0.515), (0.64, 0.515), transform=ax.transAxes, arrowstyle="-|>", mutation_scale=18, linewidth=3, color=ORANGE))
    ax.text(0.50, 0.60, "THE LINK FAILED", ha="center", fontsize=13, fontweight="bold", color=ORANGE, transform=ax.transAxes)
    ax.text(0.50, 0.555, "RUN  →  PRESS  →  ✕  CONTROL", ha="center", fontsize=14, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.50, 0.46, "active effort did not become collective protection", ha="center", fontsize=11, color=MUTED, transform=ax.transAxes)

    ax.text(0.06, 0.20, "H1: PARTIALLY SUPPORTED (MODERATE)  |  H2: SUGGESTIVE, UNDERPOWERED (LOW-MODERATE)", fontsize=12.5, fontweight="bold", color=ORANGE, transform=ax.transAxes)
    ax.text(0.06, 0.16, "BOTTOM LINE", fontsize=13, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.06, 0.105, "This was not simply a fun match with no defending. It was a lower-stakes match where effort remained high,", fontsize=17, color=INK, transform=ax.transAxes)
    ax.text(0.06, 0.065, "but coordination, defensive protection, and finishing discipline broke down.", fontsize=17, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.06, 0.025, "Official FIFA Post-Match Summary Reports · 8 matches per team · player-level tests are exploratory", fontsize=9.5, color=MUTED, transform=ax.transAxes)

    fig.savefig(ASSET, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Wrote {ASSET}")


if __name__ == "__main__":
    main()
