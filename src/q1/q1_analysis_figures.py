from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "figures" / "draft"

R = 35.0
D = 250.0
ZE = 350.0
A4_X = (-148.5, 148.5)
A4_Y = (-50.0, 160.0)


def paper_map(theta: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    alpha = (ZE - 2.0 * z) / (ZE - z)
    beta = z / (ZE - z)
    rho = np.sqrt(
        (alpha * R) ** 2
        + (beta * D) ** 2
        + 2.0 * alpha * beta * R * D * np.cos(theta)
    )
    y_term = alpha * R * np.sin(theta) + beta * D * np.sin(2.0 * theta)
    x_term = alpha * R * np.cos(theta) + beta * D * np.cos(2.0 * theta)
    phi = np.arctan2(y_term, x_term)
    return rho * np.sin(phi), rho * np.cos(phi)


def metrics(theta_deg: float, z_max: float, n: int = 600) -> tuple[float, float]:
    theta = np.linspace(-np.deg2rad(theta_deg) / 2.0, np.deg2rad(theta_deg) / 2.0, n)
    z = np.linspace(z_max, 2.0, n)
    th_grid, z_grid = np.meshgrid(theta, z)
    x, y = paper_map(th_grid, z_grid)
    inside = (
        (x >= A4_X[0])
        & (x <= A4_X[1])
        & (y >= A4_Y[0])
        & (y <= A4_Y[1])
    )
    dx_dt = np.gradient(x, theta, axis=1)
    dx_dz = np.gradient(x, z, axis=0)
    dy_dt = np.gradient(y, theta, axis=1)
    dy_dz = np.gradient(y, z, axis=0)
    jacobian = dx_dt * dy_dz - dx_dz * dy_dt
    return float(inside.mean()), float(jacobian.min())


def plot_angle_scan() -> None:
    angles = np.arange(90, 181, 5)
    cases = {"Mona Lisa": 120.0, "Cat": 90.0}

    plt.rcParams.update({"font.size": 9})
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=220)
    for name, z_max in cases.items():
        inside = []
        j_min = []
        for angle in angles:
            r, j = metrics(float(angle), z_max)
            inside.append(r * 100.0)
            j_min.append(j)
        axes[0].plot(angles, inside, marker="o", linewidth=1.8, label=name)
        axes[1].plot(angles, j_min, marker="o", linewidth=1.8, label=name)

    axes[0].axvline(130, color="#b3261e", linestyle="--", linewidth=1.4)
    axes[1].axvline(130, color="#b3261e", linestyle="--", linewidth=1.4)
    axes[0].set_title("A4 coverage under increasing angular span", fontsize=11)
    axes[0].set_xlabel("mirror angular span / degree")
    axes[0].set_ylabel("samples inside A4 / %")
    axes[0].set_ylim(84, 101)
    axes[1].set_title("Local monotonicity margin", fontsize=11)
    axes[1].set_xlabel("mirror angular span / degree")
    axes[1].set_ylabel("minimum Jacobian")
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
    for name, z_max, color in [
        ("Mona Lisa", 120.0, "#7b3f00"),
        ("Cat", 90.0, "#1b7837"),
    ]:
        theta = np.linspace(-np.deg2rad(130) / 2.0, np.deg2rad(130) / 2.0, 420)
        z = np.linspace(z_max, 2.0, 420)
        th_grid, z_grid = np.meshgrid(theta, z)
        x, y = paper_map(th_grid, z_grid)
        ax.scatter(x[::5, ::5], y[::5, ::5], s=0.7, alpha=0.28, color=color, label=name)

    rect_x = [A4_X[0], A4_X[1], A4_X[1], A4_X[0], A4_X[0]]
    rect_y = [A4_Y[0], A4_Y[0], A4_Y[1], A4_Y[1], A4_Y[0]]
    ax.plot(rect_x, rect_y, color="black", linewidth=1.6, label="A4 canvas")
    circle = plt.Circle((0, 0), R, color="white", ec="black", lw=1.2, zorder=5)
    ax.add_patch(circle)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Projected paper footprint at 130 degrees", fontsize=11)
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


def plot_jacobian(case: str, z_max: float) -> None:
    theta = np.linspace(-np.deg2rad(130) / 2.0, np.deg2rad(130) / 2.0, 600)
    z = np.linspace(z_max, 2.0, 600)
    th_grid, z_grid = np.meshgrid(theta, z)
    x, y = paper_map(th_grid, z_grid)
    dx_dt = np.gradient(x, theta, axis=1)
    dx_dz = np.gradient(x, z, axis=0)
    dy_dt = np.gradient(y, theta, axis=1)
    dy_dz = np.gradient(y, z, axis=0)
    jacobian = dx_dt * dy_dz - dx_dz * dy_dt

    fig, ax = plt.subplots(figsize=(6.2, 4.6), dpi=220)
    im = ax.imshow(
        jacobian,
        extent=[-65, 65, 2, z_max],
        origin="lower",
        aspect="auto",
        cmap="viridis",
    )
    ax.set_title(f"{case}: Jacobian heatmap at 130 degrees")
    ax.set_xlabel("theta / degree")
    ax.set_ylabel("z / mm")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Jacobian")
    fig.tight_layout()
    fig.savefig(OUT / f"q1_jacobian_{case.lower().replace(' ', '_')}.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plot_angle_scan()
    plot_footprint()
    plot_jacobian("Mona Lisa", 120.0)
    plot_jacobian("Cat", 90.0)


if __name__ == "__main__":
    main()
