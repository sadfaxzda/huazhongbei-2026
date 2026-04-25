from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "outputs" / "figures" / "draft"

R = 35.0
D = 250.0
ZE = 350.0
THETA_MAX = 13.0 * np.pi / 18.0

PAPER_X_MIN = -148.5
PAPER_X_MAX = 148.5
PAPER_Y_TOP = 160.0
PAPER_Y_BOTTOM = -50.0


def bilinear_sample(image: np.ndarray, col: np.ndarray, row: np.ndarray) -> np.ndarray:
    h, w, channels = image.shape
    valid = (col >= 0) & (col <= w - 1) & (row >= 0) & (row <= h - 1)

    col0 = np.floor(np.clip(col, 0, w - 1)).astype(np.int64)
    row0 = np.floor(np.clip(row, 0, h - 1)).astype(np.int64)
    col1 = np.clip(col0 + 1, 0, w - 1)
    row1 = np.clip(row0 + 1, 0, h - 1)

    dc = (col - col0)[..., None]
    dr = (row - row0)[..., None]

    top = image[row0, col0] * (1.0 - dc) + image[row0, col1] * dc
    bottom = image[row1, col0] * (1.0 - dc) + image[row1, col1] * dc
    sampled = top * (1.0 - dr) + bottom * dr

    out = np.ones((*col.shape, channels), dtype=np.float32)
    out[valid] = sampled[valid]
    return out


def paper_coordinates(theta: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
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


def simulate(case: str, z_min: float, z_max: float, height: int, width: int) -> Path:
    paper_path = FIG_DIR / f"{case}_2D_clean.png"
    if not paper_path.exists():
        paper_path = FIG_DIR / f"{case}_2D_matlab.jpg"
    out_path = FIG_DIR / f"{case}_mirror_simulated_from_paper.png"

    paper = np.asarray(Image.open(paper_path).convert("RGB"), dtype=np.float32) / 255.0
    paper_h, paper_w, _ = paper.shape

    theta = np.linspace(-THETA_MAX / 2.0, THETA_MAX / 2.0, width)
    z = np.linspace(z_max, z_min, height)
    theta_grid, z_grid = np.meshgrid(theta, z)

    x_paper, y_paper = paper_coordinates(theta_grid, z_grid)
    col = (x_paper - PAPER_X_MIN) / (PAPER_X_MAX - PAPER_X_MIN) * (paper_w - 1)
    row = (PAPER_Y_TOP - y_paper) / (PAPER_Y_TOP - PAPER_Y_BOTTOM) * (paper_h - 1)

    mirror = bilinear_sample(paper, col, row)
    mirror_u8 = np.clip(mirror * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(mirror_u8).save(out_path)
    return out_path


def render_perspective(
    case: str, z_min: float, z_max: float, size: int = 1200, supersample: int = 2
) -> Path:
    paper_path = FIG_DIR / f"{case}_2D_clean.png"
    if not paper_path.exists():
        paper_path = FIG_DIR / f"{case}_2D_matlab.jpg"
    out_path = FIG_DIR / f"{case}_mirror_perspective_from_paper.png"

    paper = np.asarray(Image.open(paper_path).convert("RGB"), dtype=np.float32) / 255.0
    paper_h, paper_w, _ = paper.shape

    eye = np.array([0.0, D, ZE], dtype=np.float64)
    look_at = np.array([0.0, 0.0, 0.5 * (z_min + z_max)], dtype=np.float64)
    forward = look_at - eye
    forward /= np.linalg.norm(forward)
    world_up = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    right = np.cross(forward, world_up)
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)

    fov = np.deg2rad(24.0)
    extent = np.tan(fov / 2.0)
    render_size = size * supersample
    screen = np.linspace(-extent, extent, render_size)
    sx, sy = np.meshgrid(screen, -screen)
    dirs = forward + sx[..., None] * right + sy[..., None] * up
    dirs /= np.linalg.norm(dirs, axis=2, keepdims=True)

    # Intersect eye rays with the cylinder x^2 + y^2 = R^2.
    a = dirs[..., 0] ** 2 + dirs[..., 1] ** 2
    b = 2.0 * (eye[0] * dirs[..., 0] + eye[1] * dirs[..., 1])
    c = eye[0] ** 2 + eye[1] ** 2 - R**2
    disc = b**2 - 4.0 * a * c
    hit = disc >= 0
    sqrt_disc = np.sqrt(np.maximum(disc, 0.0))
    t0 = (-b - sqrt_disc) / (2.0 * a)
    t1 = (-b + sqrt_disc) / (2.0 * a)
    t = np.where(t0 > 0, t0, t1)
    hit &= t > 0

    q = eye + dirs * t[..., None]
    theta = np.arctan2(q[..., 0], q[..., 1])
    z = q[..., 2]
    active = (
        hit
        & (z >= z_min)
        & (z <= z_max)
        & (theta >= -THETA_MAX / 2.0)
        & (theta <= THETA_MAX / 2.0)
    )

    x_paper, y_paper = paper_coordinates(theta, z)
    col = (x_paper - PAPER_X_MIN) / (PAPER_X_MAX - PAPER_X_MIN) * (paper_w - 1)
    row = (PAPER_Y_TOP - y_paper) / (PAPER_Y_TOP - PAPER_Y_BOTTOM) * (paper_h - 1)
    sampled = bilinear_sample(paper, col, row)

    light_dir = np.array([0.0, 1.0, 0.35], dtype=np.float64)
    light_dir /= np.linalg.norm(light_dir)
    normal = np.stack((q[..., 0] / R, q[..., 1] / R, np.zeros_like(z)), axis=2)
    shade = np.clip(0.55 + 0.45 * np.sum(normal * light_dir, axis=2), 0.45, 1.0)

    out = np.ones((render_size, render_size, 3), dtype=np.float32)
    cylinder = hit & (z >= 0.0) & (z <= max(150.0, z_max))
    out[cylinder] = np.array([0.88, 0.9, 0.9], dtype=np.float32) * shade[cylinder, None]
    out[active] = sampled[active] * shade[active, None]

    image = Image.fromarray(np.clip(out * 255.0, 0, 255).astype(np.uint8))
    if supersample > 1:
        image = image.resize((size, size), Image.Resampling.LANCZOS)
    image.save(out_path)
    return out_path


def main() -> None:
    outputs = [
        simulate("p3", z_min=2.0, z_max=120.0, height=1200, width=800),
        simulate("p4", z_min=2.0, z_max=90.0, height=800, width=600),
        render_perspective("p3", z_min=2.0, z_max=120.0),
        render_perspective("p4", z_min=2.0, z_max=90.0),
    ]
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
