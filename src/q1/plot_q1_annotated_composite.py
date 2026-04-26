"""
Generate annotated Q1 composite figures for the paper.
Left panel: paper pattern with mm-scale coordinate frame, A4 border, cylinder circle.
Right panel: simulated mirror view with theta/z axis labels.
Overwrites q1_monalisa_teammate_result.png and q1_cat_teammate_result.png.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / "outputs" / "figures" / "draft"

CASES = {
    "monalisa": {
        "label": "Mona Lisa",
        "R": 35.0,
        "x_min": -148.5, "x_max": 148.5,
        "y_bot": -80.0,  "y_top": 130.0,
        "theta_deg": 180.0,
        "z_min": 0.2, "z_max": 84.0,
        "clean_img": "p3_2D_clean.png",
        "sim_img":   "p3_mirror_simulated_from_paper.png",
        "out_img":   "q1_monalisa_teammate_result.png",
    },
    "cat": {
        "label": "Cartoon Cat",
        "R": 50.0,
        "x_min": -148.5, "x_max": 148.5,
        "y_bot": -85.0,  "y_top": 125.0,
        "theta_deg": 170.0,
        "z_min": 0.2, "z_max": 80.9,
        "clean_img": "p4_2D_clean.png",
        "sim_img":   "p4_mirror_simulated_from_paper.png",
        "out_img":   "q1_cat_teammate_result.png",
    },
}


def add_paper_axes(ax: plt.Axes, cfg: dict) -> None:
    x0, x1 = cfg["x_min"], cfg["x_max"]
    y0, y1 = cfg["y_bot"], cfg["y_top"]
    R = cfg["R"]

    # A4 boundary
    rect = mpatches.Rectangle(
        (x0, y0), x1 - x0, y1 - y0,
        linewidth=1.4, edgecolor="#333333", facecolor="none",
        linestyle="--", zorder=5,
    )
    ax.add_patch(rect)

    # Coordinate axes through origin
    ax.axhline(0, color="#555555", linewidth=0.9, zorder=4)
    ax.axvline(0, color="#555555", linewidth=0.9, zorder=4)

    # Origin marker
    ax.plot(0, 0, "r+", markersize=9, markeredgewidth=1.6, zorder=6)

    # Cylinder circle
    circle = mpatches.Circle(
        (0, 0), R,
        linewidth=1.6, edgecolor="#d62728", facecolor="none", zorder=6,
    )
    ax.add_patch(circle)
    ax.annotate(
        f"$R={R:.0f}$ mm",
        xy=(R * 0.70, R * 0.70), xytext=(R + 14, R + 10),
        fontsize=7.5, color="#d62728", zorder=7,
        arrowprops=dict(arrowstyle="-", color="#d62728", lw=0.8),
    )

    ax.set_xlim(x0 - 6, x1 + 6)
    ax.set_ylim(y0 - 6, y1 + 6)
    ax.set_aspect("equal", adjustable="box")
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.yaxis.set_major_locator(MultipleLocator(50))
    ax.tick_params(labelsize=7.5)
    ax.set_xlabel("$x$ / mm", fontsize=8.5)
    ax.set_ylabel("$y$ / mm", fontsize=8.5)
    ax.set_title(f"{cfg['label']}: paper pattern (A4, mm)", fontsize=9, pad=5)
    ax.grid(True, alpha=0.18, linewidth=0.5)


def add_sim_axes(ax: plt.Axes, cfg: dict) -> None:
    half_deg = cfg["theta_deg"] / 2.0
    ax.set_xlabel(r"$\theta$ / deg", fontsize=8.5)
    ax.set_ylabel("$z$ / mm", fontsize=8.5)
    ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.tick_params(labelsize=7.5)
    ax.set_xlim(-half_deg, half_deg)
    ax.set_ylim(cfg["z_min"], cfg["z_max"])
    ax.set_title("simulated mirror view", fontsize=9, pad=5)


def make_composite(cfg: dict) -> None:
    clean_path = DRAFT / cfg["clean_img"]
    sim_path   = DRAFT / cfg["sim_img"]
    out_path   = DRAFT / cfg["out_img"]

    if not clean_path.exists():
        print(f"  [skip] {clean_path.name} not found")
        return
    if not sim_path.exists():
        print(f"  [skip] {sim_path.name} not found")
        return

    paper_img = np.asarray(Image.open(clean_path).convert("RGB"))
    sim_img   = np.asarray(Image.open(sim_path).convert("RGB"))

    fig, (ax_paper, ax_sim) = plt.subplots(
        1, 2,
        figsize=(12.5, 5.2),
        dpi=200,
        gridspec_kw={"width_ratios": [1, 1.1]},
    )

    x0, x1 = cfg["x_min"], cfg["x_max"]
    y0, y1 = cfg["y_bot"], cfg["y_top"]
    ax_paper.imshow(
        paper_img,
        extent=[x0, x1, y0, y1],
        origin="upper",
        interpolation="bilinear",
        zorder=1,
    )
    add_paper_axes(ax_paper, cfg)

    half_deg = cfg["theta_deg"] / 2.0
    # sim_img has row 0 = z_max (top); use origin="upper" to preserve that orientation
    ax_sim.imshow(
        sim_img,
        extent=[-half_deg, half_deg, cfg["z_min"], cfg["z_max"]],
        origin="upper",
        interpolation="bilinear",
        aspect="auto",
        zorder=1,
    )
    add_sim_axes(ax_sim, cfg)

    fig.tight_layout(pad=1.4)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved → {out_path.name}")


def main() -> None:
    DRAFT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 8, "font.family": "sans-serif"})
    for cfg in CASES.values():
        print(f"Processing {cfg['label']} ...")
        make_composite(cfg)


if __name__ == "__main__":
    main()
