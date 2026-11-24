from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(r"E:\PL4test")
OUT = ROOT / "figures" / "subplots"
OUT.mkdir(parents=True, exist_ok=True)
ORANGE = "#E69F00"
BLUE = "#0072B2"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.unicode_minus": False,
    "axes.linewidth": 0.6,
})


SAMPLE = "S036"
VIAL = "A6"
YMAX = 6800


def main():
    xrd = pd.read_csv(ROOT / "xrd_cross_location_reference.csv")
    g = xrd.loc[xrd.vial == VIAL].sort_values("two_theta_deg")
    if g.sample_id.iloc[0] != SAMPLE:
        raise SystemExit(f"{VIAL} is {g.sample_id.iloc[0]}, expected {SAMPLE}")
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    for site, color, ls in (("Shenzhen", ORANGE, "-"), ("Hangzhou", BLUE, "--")):
        s = g.loc[g.site == site]
        ax.plot(s.two_theta_deg, s.intensity_counts, color=color, ls=ls, lw=0.95, label=site)
    ax.set_xlim(10, 60)
    ax.set_ylim(0, YMAX)
    ax.set_xticks([10, 20, 30, 40, 50, 60])
    ax.set_xlabel(r"2$\theta$ (degree, Cu K$\alpha$)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_title(f"{SAMPLE} ({VIAL})", loc="left")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    path = OUT / f"xrd_{SAMPLE}_{VIAL}.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    main()
