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


SERIES = [
    ("S001", "F1", "#1B4F72"),
    ("S004", "F4", "#2471A3"),
    ("S008", "E2", "#5DADE2"),
    ("S012", "E6", "#148F77"),
    ("S016", "D4", "#1E8449"),
    ("S020", "C2", "#52BE80"),
    ("S024", "C6", "#7DCEA0"),
    ("S028", "B4", "#D4AC0D"),
    ("S032", "A2", "#F4D03F"),
    ("S036", "A6", "#F7DC6F"),
]


def main():
    pl = pd.read_csv(ROOT / "canonical_spectra_0p2nm.csv")
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    step = 0.145
    for i, (sample, vial, color) in enumerate(SERIES):
        g = pl.loc[pl.vial == vial].sort_values("wavelength_nm")
        if g.sample_id.iloc[0] != sample:
            raise SystemExit(f"{vial} is {g.sample_id.iloc[0]}, expected {sample}")
        y = g.shenzhen_pl.to_numpy(float)
        y = y / y.max() + i * step
        ax.plot(g.wavelength_nm, y, color=color, lw=1.15, label=f"{sample} ({vial})")
    ax.set_xlim(400, 700)
    ax.set_ylim(-0.05, step * 9 + 1.25)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Normalized PL, offset")
    ax.legend(
        loc="upper left", bbox_to_anchor=(1.02, 1.02), frameon=False,
        fontsize=7.5, ncol=2, handlelength=1.6, columnspacing=0.8,
    )
    fig.tight_layout()
    path = OUT / "fig3_offset_spectra.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    main()
