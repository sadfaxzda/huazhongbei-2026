"""
Mona Lisa Cylindrical Mirror Design - Paper Pattern Generator
Based on verified MATLAB prototype (p3_2D.m) and Paper Q1 model

Key correction: uses MATLAB's verified formula/parameters which differ from
the paper's parameter table (paper table appears to have transcription errors).

MATLAB verified parameters (converted to mm):
  R = 35.0          Cylinder radius
  D = 250.0         Observer horizontal distance
  H_view = 350.0    Observer height
  delta_theta = 90  Half-angle (full 180 deg visible)
  z_range = [0.2, 84.0] mm  Mirror pattern height range
"""

import numpy as np
from PIL import Image
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

# ============================================================
# 1. Parameters (MATLAB prototype verified values)
# ============================================================
R = 35.0           # mm, cylinder radius
D = 250.0          # mm, observer horizontal distance
H_view = 350.0     # mm, observer height (CRITICAL: must be >> z_max for stable mapping)
H_cyl = 90.0       # mm, cylinder height
delta_theta = np.radians(90.0)  # half-angle (mirror covers 180 deg front)

# Mirror pattern z range
z_min = 0.2        # mm, bottom of pattern (slight offset from paper)
z_max = 84.0       # mm, top of pattern (within cylinder height)

# ============================================================
# 2. Load Reference Image
# ============================================================
ref_candidates = [
    "data/reference/图3.png",
    "huazhongbei-2026/data/reference/图3.png",
    "monalisa.jpg",
]
ref_path = next((p for p in ref_candidates if os.path.exists(p)), None)
if ref_path is None:
    raise FileNotFoundError("Cannot find Mona Lisa reference image.")

img = Image.open(ref_path).convert("RGB")
print(f"[INFO] Image size: {img.size}")

# Mirror mesh resolution
n_theta = 240   # angular samples
n_z = 160       # height samples

# Resize to match mesh
img_resized = img.resize((n_theta, n_z), Image.LANCZOS)
img_array = np.array(img_resized, dtype=np.float32) / 255.0

# ============================================================
# 3. Compute mapping: Mirror (th, z) -> Paper (x, y)
# Uses MATLAB verified formula:
#   alpha = (H - 2z) / (H - z)
#   beta  = z / (H - z)
#   x_paper = alpha*R*sin(th) + beta*D*sin(2*th)
#   y_paper = alpha*R*cos(th) + beta*D*cos(2*th)
#   where th=0 is front center (pointing toward observer)
# ============================================================
th_vals = np.linspace(-delta_theta, delta_theta, n_theta)
z_vals = np.linspace(z_max, z_min, n_z)  # top to bottom

TH, Z = np.meshgrid(th_vals, z_vals)

alpha = (H_view - 2 * Z) / (H_view - Z)
beta = Z / (H_view - Z)

x_paper = alpha * R * np.sin(TH) + beta * D * np.sin(2 * TH)
y_paper = alpha * R * np.cos(TH) + beta * D * np.cos(2 * TH)

# Flatten for interpolation
points = np.column_stack([x_paper.ravel(), y_paper.ravel()])
colors = img_array.reshape(-1, 3)

# Report mapping range
x_min, x_max = points[:, 0].min(), points[:, 0].max()
y_min, y_max = points[:, 1].min(), points[:, 1].max()
print(f"[INFO] Mapping range: x=[{x_min:.0f}, {x_max:.0f}] mm, y=[{y_min:.0f}, {y_max:.0f}] mm")

# ============================================================
# 4. A4 Paper Layout
#    Landscape orientation, cylinder center shifted downward
#    MATLAB: grid_y = linspace(16, -5, ...) cm = linspace(160, -50, ...) mm
#    Cylinder at y=0, paper extends 160mm up, 50mm down
# ============================================================
A4_W = 297.0   # mm
A4_H = 210.0   # mm

# Cylinder center shifted below A4 center to make room for upward-mapped pattern
# Pattern maps to y=[-79, +103], so we need grid to cover this range within 210mm A4
# With y_offset=25: grid goes from y=+130 to y=-80, covering [-80, +130] → pattern fits
y_offset = 25   # mm, shift cylinder DOWN relative to A4 center
grid_y_top = A4_H / 2 + y_offset      # 105 + 25 = 130  → top edge of A4
grid_y_bot = -A4_H / 2 + y_offset     # -105 + 25 = -80 → bottom edge of A4
# Paper: 130mm above cylinder, 80mm below.  Cylinder at y=0.

pixel_density = 10  # px/mm (~254 DPI)
nx = int(A4_W * pixel_density)
ny = int(A4_H * pixel_density)

print(f"[INFO] Generating A4 pattern ({nx}x{ny})...")

grid_x = np.linspace(-A4_W/2, A4_W/2, nx)
grid_y = np.linspace(grid_y_top, grid_y_bot, ny)  # top to bottom, cylinder at y=0
GX, GY = np.meshgrid(grid_x, grid_y)
grid_pts = np.column_stack([GX.ravel(), GY.ravel()])

# Interpolate per channel (white fill for NaN/outside)
paper_img = np.ones((ny, nx, 3), dtype=np.float32)
print(f"[INFO] Interpolating {len(grid_pts)} grid points...")

for c in range(3):
    print(f"  Channel {c+1}/3 ...")
    interp = LinearNDInterpolator(points, colors[:, c], fill_value=1.0)
    channel = interp(grid_pts).reshape(ny, nx)
    paper_img[:, :, c] = channel
    print(f"    NaN pixels: {np.isnan(channel).sum()}")

paper_img = np.nan_to_num(paper_img, 1.0)

# ============================================================
# 5. Mask Cylinder Base (circle on paper)
# ============================================================
dist = np.sqrt(GX**2 + GY**2)
cylinder_mask = dist <= R
for c in range(3):
    paper_img[:, :, c][cylinder_mask] = 1.0

# Flip data so PNG and display match physical layout:
#   TOP    = far side  (y=-80, away from observer)
#   BOTTOM = near side (y=+130, toward observer)
paper_img_phys = np.flipud(paper_img)

# Save raw PNG (already correctly oriented)
paper_out = (np.clip(paper_img_phys, 0, 1) * 255).astype(np.uint8)
Image.fromarray(paper_out).save("outputs/figures/draft/monalisa_paper_pattern_teammate.png")
print("[INFO] Saved: outputs/figures/draft/monalisa_paper_pattern_teammate.png")

# ============================================================
# 6. Mirror Simulation: what observer sees on the cylinder
# ============================================================
print("\n[INFO] Generating mirror simulation...")
sampler = LinearNDInterpolator(points, colors, fill_value=1.0)
mirror_colors = sampler(points).reshape(n_z, n_theta, 3)
mirror_colors = np.clip(mirror_colors, 0, 1)

Image.fromarray((mirror_colors * 255).astype(np.uint8)).save("outputs/figures/draft/monalisa_mirror_sim_teammate.png")
print("[INFO] Saved: outputs/figures/draft/monalisa_mirror_sim_teammate.png")

# ============================================================
# 7. Annotated Paper Pattern (for the paper / report)
#    Display: far side (y=-80) at top, observer side (y=130) at bottom,
#    matching the physical desk top-view.
# ============================================================
fig_paper, ax_paper = plt.subplots(1, 1, figsize=(12, 9))

# Use pre-flipped data with extent mapping:
#   extent=(left, right, bottom, top) = (-148.5, 148.5, 130, -80)
#   origin='upper': pixel(0,0) at (left, top) = (-148.5, -80)
#   → far side (y=-80) at visual TOP, observer side (y=130) at visual BOTTOM
ax_paper.imshow(paper_img_phys, extent=[-A4_W/2, A4_W/2, grid_y_top, grid_y_bot],
                origin='upper')
ax_paper.set_xlabel("x (mm)", fontsize=11)
ax_paper.set_ylabel("y (mm)", fontsize=11)
ax_paper.set_title("Paper Pattern for Mona Lisa — Top View", fontsize=14, fontweight='bold')

# ---- Cylinder base circle ----
circle = Circle((0, 0), R, fill=False, color='#D32F2F', linewidth=2.5, linestyle='--',
                label=f"Cylinder base (R = {R} mm)")
ax_paper.add_patch(circle)
ax_paper.plot(0, 0, color='#D32F2F', marker='+', markersize=12, linewidth=2)

# ---- Origin O (left side to avoid overlap with radius label) ----
# Using negative x so O label is clearly separate from radius annotation
ax_paper.annotate("O (0, 0)", xy=(0, 0), xytext=(-28, -12),
                  fontsize=11, color='#D32F2F', fontweight='bold',
                  arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.2),
                  bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8))

# ---- Radius dimension (upper-right quadrant, along 45 deg) ----
r_angle = np.radians(45)
rx = R * np.cos(r_angle)
ry = R * np.sin(r_angle)
ax_paper.annotate("", xy=(rx, ry), xytext=(0, 0),
                  arrowprops=dict(arrowstyle='<->', color='#1976D2', lw=2))
mid_rx, mid_ry = rx * 0.45, ry * 0.45
# label above the line at 45 deg
ax_paper.text(mid_rx + 5, mid_ry + 8, f"R = {R} mm", fontsize=11,
              color='#1976D2', fontweight='bold',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# ---- Cylinder height (right side, further out) ----
h_x = R + 30
ax_paper.plot([h_x - 4, h_x + 4], [0, 0], color='#388E3C', lw=1.5)
ax_paper.plot([h_x - 4, h_x + 4], [H_cyl, H_cyl], color='#388E3C', lw=1.5)
ax_paper.annotate("", xy=(h_x, 0), xytext=(h_x, H_cyl),
                  arrowprops=dict(arrowstyle='<->', color='#388E3C', lw=2))
ax_paper.text(h_x + 10, H_cyl / 2, f"H_c = {H_cyl} mm", fontsize=11,
              color='#388E3C', fontweight='bold', rotation=90,
              verticalalignment='center',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# ---- Observer indicator (bottom-center) ----
ax_paper.annotate("", xy=(0, 20), xytext=(0, grid_y_top + 12),
                  arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2.5))
ax_paper.text(0, grid_y_top + 30, f"Observer  E = (0, {D}, {H_view}) mm",
              fontsize=11, color='#7B1FA2', fontweight='bold', ha='center',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=2))

# ---- A4 dimensions (light, on the borders) ----
# Width at the bottom
ax_paper.annotate("", xy=(-A4_W/2, grid_y_top - 6), xytext=(A4_W/2, grid_y_top - 6),
                  arrowprops=dict(arrowstyle='<->', color='#888888', lw=1.2))
ax_paper.text(0, grid_y_top - 16, "297 mm", fontsize=10, color='#888888',
              ha='center', fontweight='bold',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

# Height on the left
ax_paper.annotate("", xy=(-A4_W/2 - 6, grid_y_top), xytext=(-A4_W/2 - 6, grid_y_bot),
                  arrowprops=dict(arrowstyle='<->', color='#888888', lw=1.2))
ax_paper.text(-A4_W/2 - 16, (grid_y_top + grid_y_bot) / 2, "210 mm",
              fontsize=10, color='#888888', ha='center', va='center',
              fontweight='bold', rotation=90,
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

plt.tight_layout()
plt.savefig("outputs/figures/draft/monalisa_annotated_paper_teammate.png", dpi=350)
print("[INFO] Saved: outputs/figures/draft/monalisa_annotated_paper_teammate.png")
plt.close()

# ============================================================
# 8. Composite Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
theta_deg = np.degrees(th_vals)

# Top-left: Paper pattern (same orientation as annotated figure)
axes[0, 0].imshow(paper_img_phys, extent=[-A4_W/2, A4_W/2, grid_y_top, grid_y_bot], origin='upper')
c = Circle((0, 0), R, fill=False, color='red', linewidth=2, linestyle='--',
           label=f'Cylinder R={R}mm')
axes[0, 0].add_patch(c)
axes[0, 0].plot(0, 0, 'r+', markersize=12, linewidth=2)
axes[0, 0].legend(fontsize=9)
axes[0, 0].set_title("Paper Pattern (Distorted)", fontsize=13)
axes[0, 0].set_xlabel("x (mm)")
axes[0, 0].set_ylabel("y (mm)")

# Top-right: Reference image
axes[0, 1].imshow(img_resized)
axes[0, 1].set_title(f"Mirror Reference\n({n_theta}x{n_z})", fontsize=13)
axes[0, 1].axis('off')

# Bottom-left: Mirror simulation
axes[1, 0].imshow(mirror_colors, extent=[theta_deg[0], theta_deg[-1], z_max, z_min],
                  aspect='auto')
axes[1, 0].set_xlabel("Angle from front theta (deg)")
axes[1, 0].set_ylabel("Height z (mm)")
axes[1, 0].set_title("Mirror Reflection Simulation (Unwrapped)", fontsize=13)

# Bottom-right: Info
axes[1, 1].axis('off')
info = (
    f"DESIGN PARAMETERS\n"
    f"{'-'*22}\n"
    f"Cylinder radius  R  = {R:.0f} mm\n"
    f"Cylinder height  Hc = {H_cyl:.0f} mm\n"
    f"Half-angle      dth = {np.degrees(delta_theta):.0f} deg\n"
    f"Observer dist    D  = {D:.0f} mm\n"
    f"Observer height  H  = {H_view:.0f} mm\n"
    f"Mirror z range      = [{z_min:.0f}, {z_max:.0f}] mm\n"
    f"{'-'*22}\n"
    f"Image size   = {img.size}\n"
    f"Paper res    = {pixel_density} px/mm\n"
    f"Map range    = [{x_min:.0f},{x_max:.0f}] x "
    f"[{y_min:.0f},{y_max:.0f}]"
)
axes[1, 1].text(0.1, 0.9, info, transform=axes[1, 1].transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig("outputs/figures/draft/monalisa_composite_teammate.png", dpi=200)
print("[INFO] Saved: outputs/figures/draft/monalisa_composite_teammate.png")
plt.close()

# ============================================================
# 8. Statistics
# ============================================================
total_pixels = nx * ny
non_white = (paper_img[:, :, 0] < 0.99) | (paper_img[:, :, 1] < 0.99) | (paper_img[:, :, 2] < 0.99)
coverage = non_white.sum() / total_pixels * 100
print(f"\n[INFO] Stats:")
print(f"  Paper pixels (total): {total_pixels}")
print(f"  Image coverage: {coverage:.1f}%")
print(f"  Output files:")
print(f"    monalisa_paper_pattern.png  (paper pattern)")
print(f"    monalisa_mirror_sim.png     (mirror simulation)")
print(f"    monalisa_composite.png      (composite figure)")
