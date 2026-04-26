from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import font_manager
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "outputs" / "figures" / "draft"


def chinese_font():
    for path in (
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ):
        if Path(path).exists():
            return font_manager.FontProperties(fname=path)
    return None


FONT = chinese_font()


def crop_nonwhite(img, tol=250, pad=70):
    rgb = img.convert("RGB")
    pix = rgb.load()
    w, h = rgb.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b = pix[x, y]
            if not (r >= tol and g >= tol and b >= tol):
                xs.append(x)
                ys.append(y)
    if not xs:
        return rgb
    return rgb.crop(
        (
            max(min(xs) - pad, 0),
            max(min(ys) - pad, 0),
            min(max(xs) + pad, w),
            min(max(ys) + pad, h),
        )
    )


def make_pair(case):
    paper = crop_nonwhite(Image.open(BASE / case["paper"]))
    mirror = Image.open(BASE / case["mirror"]).convert("RGB")

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(11.8, 4.45),
        dpi=220,
        gridspec_kw={"width_ratios": [1.0, 1.28]},
    )

    ax = axes[0]
    ax.imshow(
        paper,
        extent=[case["x_min"], case["x_max"], case["y_top"], case["y_bot"]],
        origin="upper",
    )
    ax.add_patch(
        Circle(
            (0, 0),
            case["R"],
            fill=False,
            color="#d62728",
            linewidth=1.4,
            linestyle="--",
        )
    )
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x / mm")
    ax.set_ylabel("y / mm")
    ax.set_title("(a) A4 纸面畸变图案", fontproperties=FONT)
    ax.grid(color="0.82", linewidth=0.45, alpha=0.55)
    ax.tick_params(labelsize=8)

    ax = axes[1]
    ax.imshow(
        mirror,
        extent=[case["theta_min"], case["theta_max"], case["z_max"], case["z_min"]],
        origin="upper",
        aspect="auto",
    )
    ax.set_xlabel(r"$\theta$ / deg")
    ax.set_ylabel("z / mm")
    ax.set_title("(b) 镜面重建结果", fontproperties=FONT)
    ax.grid(color="0.88", linewidth=0.4, alpha=0.35)
    ax.tick_params(labelsize=8)

    fig.tight_layout(w_pad=1.8)
    fig.savefig(BASE / case["out"], bbox_inches="tight")
    plt.close(fig)
    print(BASE / case["out"])


if __name__ == "__main__":
    make_pair(
        {
            "paper": "monalisa_paper_pattern_teammate.png",
            "mirror": "monalisa_mirror_sim_teammate.png",
            "out": "q1_monalisa_result_final.png",
            "R": 35.0,
            "x_min": -148.5,
            "x_max": 148.5,
            "y_top": 130.0,
            "y_bot": -80.0,
            "theta_min": -90.0,
            "theta_max": 90.0,
            "z_min": 0.2,
            "z_max": 84.0,
        }
    )
    make_pair(
        {
            "paper": "cat_paper_pattern_teammate.png",
            "mirror": "cat_mirror_sim_teammate.png",
            "out": "q1_cat_result_final.png",
            "R": 50.0,
            "x_min": -148.5,
            "x_max": 148.5,
            "y_top": 125.0,
            "y_bot": -85.0,
            "theta_min": -85.0,
            "theta_max": 85.0,
            "z_min": 0.2,
            "z_max": 80.9,
        }
    )
