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


import numpy as np

VIAL_ORDER = [f"{r}{c}" for r in "ABCDEF" for c in range(1, 7)]


def main():
    pl = pd.read_csv(ROOT / "canonical_spectra_0p2nm.csv")
    meta = (
        pl.groupby("vial", sort=False)
        .agg(peak_sz=("peak_shenzhen_nm", "first"), peak_hz=("peak_hangzhou_nm", "first"))
        .reindex(VIAL_ORDER)
    )
    diff = meta.peak_hz - meta.peak_sz
    sd = float(diff.std(ddof=1))
    x = np.arange(len(VIAL_ORDER))
    fig, ax = plt.subplots(figsize=(6.4, 4.15))
    ax.axhline(0, color="#b0b0b0", lw=0.8, zorder=0)
    ax.errorbar(
        x, diff, yerr=sd, fmt="o", color="#2E9B45", ecolor="#9a9a9a",
        elinewidth=0.8, capsize=2.2, capthick=0.8, ms=4.2, zorder=2,
    )
    ax.set_xlim(-0.6, len(VIAL_ORDER) - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(VIAL_ORDER, rotation=90, fontsize=6.5)
    ax.set_ylim(-4.2, 4.2)
    ax.set_yticks(np.arange(-4, 5, 1))
    ax.set_ylabel("Hangzhou − Shenzhen peak (nm)")
    ax.set_title("(A) Peak-center agreement", loc="left", fontsize=11, fontweight="bold")
    ax.text(
        0.03, 0.96, f"SD = {sd:.2f} nm", transform=ax.transAxes,
        va="top", ha="left", fontsize=8,
        bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="#c8c8c8", lw=0.6),
    )
    fig.tight_layout()
    path = OUT / "s5_peak_center.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    main()
