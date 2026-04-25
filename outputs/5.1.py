# -*- coding: utf-8 -*-
"""
Q3 Operator Mapping Diagram -- Paper / Mirror Dual Space
Uses real images: cat.jpg and monalisa.jpg
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# No Chinese fonts needed now, but keep a safe fallback
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(16, 7))
ax.set_xlim(-2, 14)
ax.set_ylim(-2, 8)
ax.set_aspect('equal')
ax.axis('off')

# Colors
color_left  = '#E8F0FE'
color_right = '#FCE8E6'
color_border_left  = '#1A73E8'
color_border_right = '#D93025'
color_j1 = '#1A73E8'
color_j2 = '#D93025'
color_arrow = '#444444'

# ===================== LEFT P-Space =====================
rect_left = FancyBboxPatch((0.3, 0.8), 5.0, 5.2,
                           boxstyle="round,pad=0.15",
                           facecolor=color_left, edgecolor=color_border_left,
                           linewidth=2.5)
ax.add_patch(rect_left)
ax.text(2.8, 6.3, r'$\mathcal{P}$-Space (Paper)',
        ha='center', va='center', fontsize=14, fontweight='bold',
        color=color_border_left)
ax.text(2.8, 5.85, r'Target $P^*$ : Paper Image',
        ha='center', va='center', fontsize=11, color='#555555')

# Cat image (horizontal)
cat_img = plt.imread('cat.jpg')
cat_h, cat_w = cat_img.shape[:2]
max_cat_width = 2.5
cat_scale = max_cat_width / cat_w
cat_disp_w = cat_w * cat_scale
cat_disp_h = cat_h * cat_scale
cat_left   = 2.8 - cat_disp_w / 2
cat_right  = 2.8 + cat_disp_w / 2
cat_bottom = 3.8 - cat_disp_h / 2
cat_top    = 3.8 + cat_disp_h / 2
ax.imshow(cat_img, extent=[cat_left, cat_right, cat_bottom, cat_top],
          aspect='auto', zorder=5)
ax.text(2.8, 2.2, r'$P^*$ (Cat)', ha='center', va='center',
        fontsize=12, fontweight='bold', color='black')

# J1 circle
circle_j1 = Circle((2.8, 3.8), 1.8, fill=False, edgecolor=color_j1,
                   linewidth=2.5, linestyle='--')
ax.add_patch(circle_j1)
ax.annotate(r'$\mathcal{J}_1$ Paper Loss',
            xy=(1.2, 2.2), fontsize=11, color=color_j1, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=color_j1, alpha=0.85))

# ===================== RIGHT M-Space =====================
rect_right = FancyBboxPatch((8.7, 0.8), 5.0, 5.2,
                            boxstyle="round,pad=0.15",
                            facecolor=color_right, edgecolor=color_border_right,
                            linewidth=2.5)
ax.add_patch(rect_right)
ax.text(11.2, 6.3, r'$\mathcal{M}$-Space (Mirror)',
        ha='center', va='center', fontsize=14, fontweight='bold',
        color=color_border_right)
ax.text(11.2, 5.85, r'Target $M^*$ : Mirror Image',
        ha='center', va='center', fontsize=11, color='#555555')

# Mona Lisa (vertical)
mona_img = plt.imread('monalisa.jpg')
mona_h, mona_w = mona_img.shape[:2]
max_mona_height = 3.0
mona_scale = max_mona_height / mona_h
mona_disp_h = mona_h * mona_scale
mona_disp_w = mona_w * mona_scale
mona_left   = 11.2 - mona_disp_w / 2
mona_right  = 11.2 + mona_disp_w / 2
mona_bottom = 3.8 - mona_disp_h / 2
mona_top    = 3.8 + mona_disp_h / 2
ax.imshow(mona_img, extent=[mona_left, mona_right, mona_bottom, mona_top],
          aspect='auto', zorder=5)
ax.text(11.2, 2.2, r'$M^*$ (Mona Lisa)', ha='center', va='center',
        fontsize=12, fontweight='bold', color='#5D4037')

# J2 circle
circle_j2 = Circle((11.2, 3.8), 1.8, fill=False, edgecolor=color_j2,
                   linewidth=2.5, linestyle='--')
ax.add_patch(circle_j2)
ax.annotate(r'$\mathcal{J}_2$ Mirror Loss',
            xy=(9.6, 2.2), fontsize=11, color=color_j2, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=color_j2, alpha=0.85))

# ===================== Arrows =====================
arrow_T = FancyArrowPatch((5.5, 4.8), (8.5, 4.8),
                          arrowstyle='->', mutation_scale=25,
                          linewidth=3, color=color_arrow, zorder=10)
ax.add_patch(arrow_T)
ax.text(7.0, 5.4, r'$\mathbf{T}$ (Reflection Mapping)',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=color_arrow)
ax.text(7.0, 5.05, 'Ray Tracing / Geometric Optics',
        ha='center', va='center', fontsize=9, color='#777777')

arrow_Tinv = FancyArrowPatch((8.5, 3.0), (5.5, 3.0),
                             arrowstyle='->', mutation_scale=25,
                             linewidth=3, color=color_arrow, zorder=10,
                             linestyle=(0, (5, 3)))
ax.add_patch(arrow_Tinv)
ax.text(7.0, 2.35, r'$\mathbf{T}^{-1}$ (Inverse Mapping)',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=color_arrow)

ax.text(7.0, 3.7, 'Bidirectional Constraint\nApproximation',
        ha='center', va='center', fontsize=10, fontweight='bold',
        color='#555555',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFDE7',
                  edgecolor='#AAAAAA', alpha=0.9))

# ===================== Bottom Formula (plain text, no LaTeX) =====================
formula = (
    r'min $\; J(P) = $'
    r'$||P - P^*||^2$  (Paper Fidelity) '
    r'$+ \lambda \; ||\mathbf{T}(P) - M^*||^2$  (Mirror Fidelity)'
)
ax.text(7.0, 0.3, formula, ha='center', va='center',
        fontsize=13, color='#333333',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#FAFAFA',
                  edgecolor='#CCCCCC', linewidth=1.2))
ax.text(7.0, -0.5,
        r'$\lambda$ : trade-off coefficient balancing the two objectives',
        ha='center', va='center', fontsize=10, color='#888888', style='italic')

# Decorative lines
ax.plot([4.6, 9.4], [3.8, 3.8], linestyle=':', color='#999999', linewidth=1.2, alpha=0.7)
ax.plot([4.6, 9.4], [3.3, 3.3], linestyle=':', color='#999999', linewidth=1.0, alpha=0.5)
ax.text(7.0, 3.15, 'Joint Optimization', ha='center', va='center',
        fontsize=8, color='#999999')

# ----------------- Save & Show -----------------
plt.tight_layout(pad=0.8)
plt.savefig('Q3_operator_diagram_real.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('Q3_operator_diagram_real.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()
print("Image saved as Q3_operator_diagram_real.png and .pdf")