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


SAMPLE = "S017"
VIAL = "D5"


def main():
    pl = pd.read_csv(ROOT / "canonical_spectra_0p2nm.csv")
    g = pl.loc[pl.vial == VIAL].sort_values("wavelength_nm")
    if g.sample_id.iloc[0] != SAMPLE:
        raise SystemExit(f"{VIAL} is {g.sample_id.iloc[0]}, expected {SAMPLE}")
    wave = g.wavelength_nm.to_numpy()
    sz = g.shenzhen_pl.to_numpy(float)
    hz = g.hangzhou_pl.to_numpy(float)
    scale = sz.max()
    sz, hz = sz / scale, hz / scale
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    ax.axhline(0, color="#e6e6e6", lw=0.4, zorder=0)
    ax.plot(wave, sz, color=ORANGE, lw=1.2, label="Shenzhen")
    ax.plot(wave, hz, color=BLUE, lw=1.1, ls="--", label="Hangzhou replay")
    ax.set_xlim(400, 700)
    ax.set_xticks([450, 520, 600])
    ax.set_ylim(-0.08, max(1.2, float(hz.max()) * 1.08))
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Intensity / Shenzhen peak")
    ax.set_title(f"{SAMPLE} ({VIAL})")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    path = OUT / f"s4_{SAMPLE}_{VIAL}.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    main()
