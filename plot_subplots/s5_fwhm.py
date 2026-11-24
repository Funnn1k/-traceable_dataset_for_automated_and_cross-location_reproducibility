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
        .agg(fwhm_sz=("fwhm_shenzhen_nm", "first"), fwhm_hz=("fwhm_hangzhou_nm", "first"))
        .reindex(VIAL_ORDER)
    )
    mad = float((meta.fwhm_hz - meta.fwhm_sz).abs().mean())
    x = np.arange(len(VIAL_ORDER))
    fig, ax = plt.subplots(figsize=(6.4, 4.15))
    ax.plot(x, meta.fwhm_sz, color=ORANGE, lw=1.15, marker="o", ms=4.0, label="Shenzhen")
    ax.plot(x, meta.fwhm_hz, color=BLUE, lw=1.05, ls="--", marker="s", ms=3.4, label="Hangzhou")
    ax.set_xlim(-0.6, len(VIAL_ORDER) - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(VIAL_ORDER, rotation=90, fontsize=6.5)
    ax.set_ylim(15, 70)
    ax.set_ylabel("FWHM (nm)")
    ax.set_title("(B) FWHM reproducibility", loc="left", fontsize=11, fontweight="bold")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.text(
        0.03, 0.96, f"mean abs. difference = {mad:.2f} nm", transform=ax.transAxes,
        va="top", ha="left", fontsize=8,
        bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="#c8c8c8", lw=0.6),
    )
    fig.tight_layout()
    path = OUT / "s5_fwhm.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    main()
