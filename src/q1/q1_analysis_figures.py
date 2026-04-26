from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "figures" / "draft"

A4_X = (-148.5, 148.5)

CASES = {
    "Mona Lisa": {
        "R": 35.0,
        "D": 250.0,
        "ZE": 350.0,
        "Hc": 90.0,
        "theta_deg": 180.0,
        "z_min": 0.2,
        "z_max": 84.0,
        "a4_y": (-80.0, 130.0),
        "color": "#7b3f00",
    },
    "Cat": {
        "R": 50.0,
        "D": 280.0,
        "ZE": 350.0,
        "Hc": 86.0,
        "theta_deg": 170.0,
        "z_min": 0.2,
        "z_max": 80.9,
        "a4_y": (-85.0, 125.0),
        "color": "#1b7837",
    },
}


def paper_map(
    theta: np.ndarray, z: np.ndarray, case: dict[str, float | tuple[float, float] | str]
) -> tuple[np.ndarray, np.ndarray]:
    r = float(case["R"])
    d = float(case["D"])
    z_e = float(case["ZE"])
    alpha = (z_e - 2.0 * z) / (z_e - z)
    beta = z / (z_e - z)
    x_paper = alpha * r * np.sin(theta) + beta * d * np.sin(2.0 * theta)
    y_paper = alpha * r * np.cos(theta) + beta * d * np.cos(2.0 * theta)
    return x_paper, y_paper


def jacobian(theta: np.ndarray, z: np.ndarray, case: dict[str, float | tuple[float, float] | str]) -> np.ndarray:
    th_grid, z_grid = np.meshgrid(theta, z)
    x, y = paper_map(th_grid, z_grid, case)
    dx_dt = np.gradient(x, theta, axis=1)
    dx_dz = np.gradient(x, z, axis=0)
    dy_dt = np.gradient(y, theta, axis=1)
    dy_dz = np.gradient(y, z, axis=0)
    return dx_dt * dy_dz - dx_dz * dy_dt


def metrics(
    theta_deg: float,
    case: dict[str, float | tuple[float, float] | str],
    n: int = 520,
) -> tuple[float, float, float]:
    theta = np.linspace(-np.deg2rad(theta_deg) / 2.0, np.deg2rad(theta_deg) / 2.0, n)
    z = np.linspace(float(case["z_max"]), float(case["z_min"]), n)
    th_grid, z_grid = np.meshgrid(theta, z)
    x, y = paper_map(th_grid, z_grid, case)
    a4_y = case["a4_y"]
    assert isinstance(a4_y, tuple)
    inside = (
        (x >= A4_X[0])
        & (x <= A4_X[1])
        & (y >= a4_y[0])
        & (y <= a4_y[1])
    )
    j = jacobian(theta, z, case)
    return float(inside.mean()), float(j.min()), float(j.max())


def plot_angle_scan() -> None:
    angles = np.arange(90, 181, 5)

    plt.rcParams.update({"font.size": 9})
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=220)
    for name, case in CASES.items():
        inside = []
        j_min = []
        j_max = []
        for angle in angles:
            r, j0, j1 = metrics(float(angle), case)
            inside.append(r * 100.0)
            j_min.append(j0)
            j_max.append(j1)
        color = str(case["color"])
        axes[0].plot(angles, inside, marker="o", linewidth=1.8, label=name, color=color)
        axes[1].plot(angles, j_min, marker="o", linewidth=1.8, label=f"{name}: min J", color=color)
        axes[1].plot(angles, j_max, linestyle="--", linewidth=1.2, label=f"{name}: max J", color=color, alpha=0.75)

    axes[0].axvline(180, color=CASES["Mona Lisa"]["color"], linestyle=":", linewidth=1.5)
    axes[0].axvline(170, color=CASES["Cat"]["color"], linestyle=":", linewidth=1.5)
    axes[1].axvline(180, color=CASES["Mona Lisa"]["color"], linestyle=":", linewidth=1.5)
    axes[1].axvline(170, color=CASES["Cat"]["color"], linestyle=":", linewidth=1.5)
    axes[0].set_title("A4 coverage under increasing angular span", fontsize=11)
    axes[0].set_xlabel("mirror angular span / degree")
    axes[0].set_ylabel("samples inside A4 / %")
    axes[0].set_ylim(70, 101)
    axes[1].set_title("Jacobian range over mirror domain", fontsize=11)
    axes[1].set_xlabel("mirror angular span / degree")
    axes[1].set_ylabel("Jacobian")
    axes[1].axhline(0, color="black", linewidth=1.0)
    for ax in axes:
        ax.grid(True, alpha=0.25)
        ax.legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.85)
    fig.tight_layout()
    fig.savefig(OUT / "q1_angle_scan.png", bbox_inches="tight")
    plt.close(fig)


def plot_footprint() -> None:
    plt.rcParams.update({"font.size": 9})
    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=220)
    for name, case in CASES.items():
        theta_deg = float(case["theta_deg"])
        theta = np.linspace(-np.deg2rad(theta_deg) / 2.0, np.deg2rad(theta_deg) / 2.0, 520)
        z = np.linspace(float(case["z_max"]), float(case["z_min"]), 420)
        th_grid, z_grid = np.meshgrid(theta, z)
        x, y = paper_map(th_grid, z_grid, case)
        ax.scatter(x[::5, ::5], y[::5, ::5], s=0.7, alpha=0.28, color=str(case["color"]), label=f"{name} ({theta_deg:.0f} deg)")

    for name, case in CASES.items():
        a4_y = case["a4_y"]
        assert isinstance(a4_y, tuple)
        rect_x = [A4_X[0], A4_X[1], A4_X[1], A4_X[0], A4_X[0]]
        rect_y = [a4_y[0], a4_y[0], a4_y[1], a4_y[1], a4_y[0]]
        ax.plot(rect_x, rect_y, linewidth=1.3, linestyle="--", color=str(case["color"]), label=f"{name} A4 window")
    circle = plt.Circle((0, 0), float(CASES["Cat"]["R"]), color="white", ec="black", lw=1.2, zorder=5)
    ax.add_patch(circle)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Projected paper footprint under final Q1 parameters", fontsize=11)
    ax.set_xlabel("paper x / mm")
    ax.set_ylabel("paper y / mm")
    ax.grid(True, alpha=0.2)
    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="none",
        framealpha=0.9,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        borderaxespad=0.0,
    )
    fig.tight_layout()
    fig.savefig(OUT / "q1_paper_footprint.png", bbox_inches="tight")
    plt.close(fig)


def plot_jacobian(name: str, case: dict[str, float | tuple[float, float] | str]) -> None:
    theta_deg = float(case["theta_deg"])
    theta = np.linspace(-np.deg2rad(theta_deg) / 2.0, np.deg2rad(theta_deg) / 2.0, 700)
    z = np.linspace(float(case["z_max"]), float(case["z_min"]), 620)
    j = jacobian(theta, z, case)
    vmax = np.percentile(np.abs(j), 98)

    fig, ax = plt.subplots(figsize=(6.2, 4.6), dpi=220)
    im = ax.imshow(
        j,
        extent=[-theta_deg / 2.0, theta_deg / 2.0, float(case["z_min"]), float(case["z_max"])],
        origin="lower",
        aspect="auto",
        cmap="coolwarm",
        vmin=-vmax,
        vmax=vmax,
    )
    ax.set_title(f"{name}: Jacobian heatmap at {theta_deg:.0f} degrees")
    ax.set_xlabel("theta / degree")
    ax.set_ylabel("z / mm")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Jacobian")
    fig.tight_layout()
    fig.savefig(OUT / f"q1_jacobian_{name.lower().replace(' ', '_')}.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plot_angle_scan()
    plot_footprint()
    plot_jacobian("Mona Lisa", CASES["Mona Lisa"])
    plot_jacobian("Cat", CASES["Cat"])


if __name__ == "__main__":
    main()
