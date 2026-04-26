"""
Cartoon Cat Cylindrical Mirror Design - Paper Pattern Generator
Based on verified MATLAB formula with parameters optimized for the cat image.

Cat image: 897x489, aspect ratio = 1.834 (landscape/wide)
Optimal parameters found via A4-fit maximization:
  R = 50.0 mm        Cylinder radius (larger = better resolution)
  D = 280.0 mm       Observer horizontal distance
  H_view = 350.0 mm  Observer height
  delta_theta = 85   Half-angle (full 170 deg visible)
  z_max = 80.9 mm    Pattern top height
  y_offset = 20 mm   Cylinder shift toward observer
"""

import numpy as np
from PIL import Image
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

# ============================================================
# 1. Parameters (optimized for cat image, A_r = 1.834)
# ============================================================
R = 50.0           # mm, cylinder radius
D = 280.0          # mm, observer horizontal distance
H_view = 350.0     # mm, observer height (>> z_max for stability)
H_cyl = 86.0       # mm, cylinder height

delta_theta = np.radians(85.0)  # half-angle

z_min = 0.2        # mm, bottom of pattern
z_max = 80.9       # mm, top of pattern (from aspect-ratio constraint)

# ============================================================
# 2. Load Cat Reference Image
# ============================================================
ref_candidates = [
    "huazhongbei-2026/data/reference/图4.png",
    "附件/图4.png",
    "cartoon_cat.jpg",
    "cat.png"
]
ref_path = None
for p in ref_candidates:
    if os.path.exists(p):
        ref_path = p
        break

img = Image.open(ref_path).convert("RGB")
print(f"[INFO] Image: {ref_path}, size: {img.size}")

# Mirror mesh resolution — match cat's aspect ratio
A_r = img.width / img.height
n_theta = 300
n_z = int(n_theta / A_r)
print(f"[INFO] Mesh: {n_theta} x {n_z} (aspect {n_theta/n_z:.3f})")

img_resized = img.resize((n_theta, n_z), Image.LANCZOS)
img_array = np.array(img_resized, dtype=np.float32) / 255.0

# ============================================================
# 3. Compute mapping: Mirror (th, z) -> Paper (x, y)
# ============================================================
th_vals = np.linspace(-delta_theta, delta_theta, n_theta)
z_vals = np.linspace(z_max, z_min, n_z)

TH, Z = np.meshgrid(th_vals, z_vals)

alpha = (H_view - 2 * Z) / (H_view - Z)
beta  = Z / (H_view - Z)

x_paper = alpha * R * np.sin(TH) + beta * D * np.sin(2 * TH)
y_paper = alpha * R * np.cos(TH) + beta * D * np.cos(2 * TH)

points = np.column_stack([x_paper.ravel(), y_paper.ravel()])
colors = img_array.reshape(-1, 3)

x_min, x_max = points[:, 0].min(), points[:, 0].max()
y_min, y_max = points[:, 1].min(), points[:, 1].max()
print(f"[INFO] Pattern range: x=[{x_min:.0f}, {x_max:.0f}]  y=[{y_min:.0f}, {y_max:.0f}] mm")
print(f"[INFO] Pattern size: {x_max-x_min:.0f} x {y_max-y_min:.0f} mm")

# ============================================================
# 4. A4 Paper Layout (Landscape)
#    y_offset = 20 centers the pattern vertically
# ============================================================
A4_W = 297.0   # mm
A4_H = 210.0   # mm

y_offset = 20   # mm, shift cylinder TOWARD observer (positive y)
grid_y_top = A4_H / 2 + y_offset      # 105 + 20 = 125
grid_y_bot = -A4_H / 2 + y_offset     # -105 + 20 = -85

pixel_density = 10  # px/mm (~254 DPI)
nx = int(A4_W * pixel_density)
ny = int(A4_H * pixel_density)

print(f"[INFO] Generating A4 pattern ({nx}x{ny})...")

grid_x = np.linspace(-A4_W/2, A4_W/2, nx)
grid_y = np.linspace(grid_y_top, grid_y_bot, ny)
GX, GY = np.meshgrid(grid_x, grid_y)
grid_pts = np.column_stack([GX.ravel(), GY.ravel()])

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
# 5. Mask Cylinder Base
# ============================================================
dist = np.sqrt(GX**2 + GY**2)
cylinder_mask = dist <= R
for c in range(3):
    paper_img[:, :, c][cylinder_mask] = 1.0

# Flip for correct physical orientation
paper_img_phys = np.flipud(paper_img)

paper_out = (np.clip(paper_img_phys, 0, 1) * 255).astype(np.uint8)
Image.fromarray(paper_out).save("cat_paper_pattern.png")
print("[INFO] Saved: cat_paper_pattern.png")

# ============================================================
# 6. Mirror Simulation
# ============================================================
print("\n[INFO] Generating mirror simulation...")
sampler = LinearNDInterpolator(points, colors, fill_value=1.0)
mirror_colors = sampler(points).reshape(n_z, n_theta, 3)
mirror_colors = np.clip(mirror_colors, 0, 1)

Image.fromarray((mirror_colors * 255).astype(np.uint8)).save("cat_mirror_sim.png")
print("[INFO] Saved: cat_mirror_sim.png")

# ============================================================
# 7. Annotated Paper Pattern
# ============================================================
fig_paper, ax_paper = plt.subplots(1, 1, figsize=(12, 9))

ax_paper.imshow(paper_img_phys, extent=[-A4_W/2, A4_W/2, grid_y_top, grid_y_bot],
                origin='upper')
ax_paper.set_xlabel("x (mm)", fontsize=11)
ax_paper.set_ylabel("y (mm)", fontsize=11)
ax_paper.set_title("Paper Pattern for Cartoon Cat — Top View", fontsize=14, fontweight='bold')

# Cylinder base
circle = Circle((0, 0), R, fill=False, color='#D32F2F', linewidth=2.5, linestyle='--',
                label=f"Cylinder base (R = {R} mm)")
ax_paper.add_patch(circle)
ax_paper.plot(0, 0, color='#D32F2F', marker='+', markersize=12, linewidth=2)

# Origin O (left side)
ax_paper.annotate("O (0, 0)", xy=(0, 0), xytext=(-30, -12),
                  fontsize=11, color='#D32F2F', fontweight='bold',
                  arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.2),
                  bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8))

# Radius (45 deg upper-right)
r_angle = np.radians(45)
rx = R * np.cos(r_angle)
ry = R * np.sin(r_angle)
ax_paper.annotate("", xy=(rx, ry), xytext=(0, 0),
                  arrowprops=dict(arrowstyle='<->', color='#1976D2', lw=2))
mid_rx, mid_ry = rx * 0.45, ry * 0.45
ax_paper.text(mid_rx + 5, mid_ry + 8, f"R = {R} mm", fontsize=11,
              color='#1976D2', fontweight='bold',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# Cylinder height (right side, further out)
h_x = R + 30
ax_paper.plot([h_x - 4, h_x + 4], [0, 0], color='#388E3C', lw=1.5)
ax_paper.plot([h_x - 4, h_x + 4], [H_cyl, H_cyl], color='#388E3C', lw=1.5)
ax_paper.annotate("", xy=(h_x, 0), xytext=(h_x, H_cyl),
                  arrowprops=dict(arrowstyle='<->', color='#388E3C', lw=2))
ax_paper.text(h_x + 10, H_cyl / 2, f"H_c = {H_cyl} mm", fontsize=11,
              color='#388E3C', fontweight='bold', rotation=90,
              verticalalignment='center',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# Observer (bottom-center)
ax_paper.annotate("", xy=(0, 20), xytext=(0, grid_y_top + 12),
                  arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2.5))
ax_paper.text(0, grid_y_top + 30, f"Observer  E = (0, {D}, {H_view}) mm",
              fontsize=11, color='#7B1FA2', fontweight='bold', ha='center',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=2))

# A4 dimensions
ax_paper.annotate("", xy=(-A4_W/2, grid_y_top - 6), xytext=(A4_W/2, grid_y_top - 6),
                  arrowprops=dict(arrowstyle='<->', color='#888888', lw=1.2))
ax_paper.text(0, grid_y_top - 16, "297 mm", fontsize=10, color='#888888',
              ha='center', fontweight='bold',
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

ax_paper.annotate("", xy=(-A4_W/2 - 6, grid_y_top), xytext=(-A4_W/2 - 6, grid_y_bot),
                  arrowprops=dict(arrowstyle='<->', color='#888888', lw=1.2))
ax_paper.text(-A4_W/2 - 16, (grid_y_top + grid_y_bot) / 2, "210 mm",
              fontsize=10, color='#888888', ha='center', va='center',
              fontweight='bold', rotation=90,
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

plt.tight_layout()
plt.savefig("cat_annotated_paper.png", dpi=350)
print("[INFO] Saved: cat_annotated_paper.png")
plt.close()

# ============================================================
# 8. Composite Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
theta_deg = np.degrees(th_vals)

axes[0, 0].imshow(paper_img_phys, extent=[-A4_W/2, A4_W/2, grid_y_top, grid_y_bot], origin='upper')
c = Circle((0, 0), R, fill=False, color='red', linewidth=2, linestyle='--',
           label=f'Cylinder R={R}mm')
axes[0, 0].add_patch(c)
axes[0, 0].plot(0, 0, 'r+', markersize=12, linewidth=2)
axes[0, 0].legend(fontsize=9)
axes[0, 0].set_title("Paper Pattern (Distorted)", fontsize=13)
axes[0, 0].set_xlabel("x (mm)")
axes[0, 0].set_ylabel("y (mm)")

axes[0, 1].imshow(img_resized)
axes[0, 1].set_title(f"Mirror Reference\n({n_theta}x{n_z})", fontsize=13)
axes[0, 1].axis('off')

axes[1, 0].imshow(mirror_colors, extent=[theta_deg[0], theta_deg[-1], z_max, z_min],
                  aspect='auto')
axes[1, 0].set_xlabel("Angle from front theta (deg)")
axes[1, 0].set_ylabel("Height z (mm)")
axes[1, 0].set_title("Mirror Reflection Simulation (Unwrapped)", fontsize=13)

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
plt.savefig("cat_composite.png", dpi=200)
print("[INFO] Saved: cat_composite.png")
plt.close()

# ============================================================
# 9. Statistics
# ============================================================
total_pixels = nx * ny
non_white = (paper_img[:, :, 0] < 0.99) | (paper_img[:, :, 1] < 0.99) | (paper_img[:, :, 2] < 0.99)
coverage = non_white.sum() / total_pixels * 100
print(f"\n[INFO] Stats:")
print(f"  Paper pixels (total): {total_pixels}")
print(f"  Image coverage: {coverage:.1f}%")
print(f"  Output files:")
print(f"    cat_paper_pattern.png      (paper pattern)")
print(f"    cat_mirror_sim.png         (mirror simulation)")
print(f"    cat_annotated_paper.png    (annotated for paper)")
print(f"    cat_composite.png          (composite figure)")
