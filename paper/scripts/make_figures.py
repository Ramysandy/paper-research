"""Regenerate every figure and derived statistic used in the paper.

Inputs are the aggregate tables in ../data/, transcribed verbatim from the A10 repository
(see ../data/SOURCES.md). No number in the paper is produced anywhere else.

Usage:  python3 scripts/make_figures.py      (run from paper/)
Outputs: figures/*.pdf and data/derived_stats.txt
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from scipy.stats import binomtest, spearmanr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

plt.rcParams.update({
    "text.usetex": True,  # Type 1 Times fonts, matching the AAAI body font
    "text.latex.preamble": r"\usepackage{times}",
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "pdf.fonttype": 42,
    "axes.spines.top": False,
    "axes.spines.right": False,
})
COL = 3.3  # AAAI column width in inches


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return centre - half, centre + half


def load(name: str) -> list[dict]:
    with open(DATA / name, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


pilot = load("security_pilot_v2_per_key.csv")
keys = [r for r in pilot if r["key"] != "UNWATERMARKED"]
base = next(r for r in pilot if r["key"] == "UNWATERMARKED")
cal = load("calibration_v1_mean_z.csv")
lines: list[str] = []

# ---------------------------------------------------------------- sanity checks
for r in pilot:
    n = int(r["n"])
    assert int(r["secure_true"]) + int(r["secure_false"]) + int(r["secure_null"]) == n, r
pooled_sf = sum(int(r["secure_and_functional"]) for r in keys)
assert pooled_sf == 231, pooled_sf
assert sum(int(r["z_ge_4"]) for r in keys) == 21
lines.append(f"pooled watermarked secure-and-functional = {pooled_sf}/720 = {pooled_sf/720:.4f}")

# ---------------------------------------------------------------- per-key derived stats
lines.append("key  func  func_CI          SF    SF_CI            sec|decisive")
for r in pilot:
    n = int(r["n"])
    f, sf = int(r["functional"]), int(r["secure_and_functional"])
    st, sfl = int(r["secure_true"]), int(r["secure_false"])
    flo, fhi = wilson(f, n)
    slo, shi = wilson(sf, n)
    lines.append(
        f"{r['key']:<13} {f/n:6.2%} [{flo:6.2%},{fhi:6.2%}]  {sf/n:6.2%} [{slo:6.2%},{shi:6.2%}]"
        f"  {st/(st+sfl):6.2%}"
    )
func = [int(r["functional"]) / 72 for r in keys]
sf = [int(r["secure_and_functional"]) / 72 for r in keys]
mz = [float(r["mean_z"]) for r in keys]
lines.append(f"functional range {min(func):.4f}-{max(func):.4f} spread {100*(max(func)-min(func)):.2f} pp")
lines.append(f"SF range {min(sf):.4f}-{max(sf):.4f} spread {100*(max(sf)-min(sf)):.2f} pp")
rho_fz = spearmanr(mz, func)
rho_sz = spearmanr(mz, sf)
lines.append(f"Spearman(mean z, functional) over 10 keys rho={rho_fz.statistic:.3f} p={rho_fz.pvalue:.3f}")
lines.append(f"Spearman(mean z, SF) over 10 keys rho={rho_sz.statistic:.3f} p={rho_sz.pvalue:.3f}")
neg = sum(z < 0 for z in mz)
lines.append(f"keys with negative mean z: {neg}/10")

# exact McNemar for K0000 vs baseline (discordant 5 WM-only, 2 baseline-only)
mc = binomtest(2, 7, 0.5, alternative="two-sided")
lines.append(f"K0000 exact McNemar p = {mc.pvalue:.4f}")

# implied green fraction from mean z and mean length (first-order, illustrative)
gamma = 0.25
sd = math.sqrt(gamma * (1 - gamma))
for r in keys:
    t, z = float(r["mean_tokens"]), float(r["mean_z"])
    lines.append(f"{r['key']} implied green fraction ~ {gamma + z*sd/math.sqrt(t):.3f}")


def t_min(p: float, z_star: float = 4.0, g: float = gamma) -> float:
    return z_star**2 * g * (1 - g) / (p - g) ** 2


for p in (0.30, 0.35, 0.40, 0.45):
    lines.append(f"T_min(z*=4, gamma=.25, p={p:.2f}) = {t_min(p):.1f} tokens")

# runtime projection from full-calibration wall clock (720 generations per array task)
lo, hi = 1 * 3600 + 59 * 60 + 24, 2 * 3600 + 16 * 60 + 56
lines.append(f"seconds/generation: {lo/720:.2f}-{hi/720:.2f}")
lines.append(f"projected 72,720-generation main run: {72720*lo/720/3600:.0f}-{72720*hi/720/3600:.0f} GPU-hours")
(DATA / "derived_stats.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))

# ---------------------------------------------------------------- Figure: dose response
fig, ax = plt.subplots(figsize=(COL, 2.0))
for g, marker, style in (("0.25", "o", "-"), ("0.50", "s", "--")):
    rows = [r for r in cal if r["gamma"] == g]
    ax.plot([float(r["bias"]) for r in rows], [float(r["mean_z"]) for r in rows],
            linestyle=style, marker=marker, color="black", markerfacecolor="white" if g == "0.50" else "black",
            label=rf"$\gamma={float(g):.2f}$")
ax.axhline(4.0, color="0.45", linestyle=":", linewidth=1)
ax.text(3.0, 3.85, r"decision threshold $z^\star=4$", fontsize=9, color="0.3", va="top", ha="right")
ax.annotate("preregistered cell", xy=(2.0, 1.743), xytext=(1.05, 2.6), fontsize=9,
            arrowprops={"arrowstyle": "->", "lw": 0.7})
ax.set_xlabel(r"logit bias $\delta$")
ax.set_ylabel(r"mean detector $z$")
ax.set_xticks([1, 2, 3])
ax.set_ylim(0, 4.3)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout(pad=0.3)
fig.savefig(FIG / "dose_response.pdf")
plt.close(fig)

# ---------------------------------------------------------------- Figure: per-key outcomes
fig, ax = plt.subplots(figsize=(COL, 2.55))
labels = [r["key"].replace("K000", "K") for r in keys]
xs = list(range(len(keys)))
for offset, field, marker, face, name in (
    (-0.15, "functional", "o", "black", "functional"),
    (0.15, "secure_and_functional", "s", "white", "secure-and-functional"),
):
    vals, los, his = [], [], []
    for r in keys:
        k = int(r[field])
        lo_, hi_ = wilson(k, 72)
        vals.append(100 * k / 72)
        los.append(100 * (k / 72 - lo_))
        his.append(100 * (hi_ - k / 72))
    ax.errorbar([x + offset for x in xs], vals, yerr=[los, his], fmt=marker, color="black",
                markerfacecolor=face, markersize=4, capsize=1.5, elinewidth=0.7, label=name)
ax.axhline(100 * int(base["functional"]) / 72, color="black", linestyle="-", linewidth=0.6,
           label="baseline functional")
ax.axhline(100 * int(base["secure_and_functional"]) / 72, color="black", linestyle="--", linewidth=0.6,
           label="baseline sec.-and-func.")
ax.set_xticks(xs)
ax.set_xticklabels(labels)
ax.set_xlabel("watermark key")
ax.set_ylabel(r"rate (\%)")
ax.set_ylim(0, 100)
ax.legend(frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.26), handletextpad=0.3,
          columnspacing=0.8, handlelength=1.6)
fig.tight_layout(pad=0.3)
fig.savefig(FIG / "per_key_outcomes.pdf")
plt.close(fig)

# ---------------------------------------------------------------- Figure: detection vs function
fig, ax = plt.subplots(figsize=(COL, 1.95))
for r, lab in zip(keys, labels):
    hit = int(r["z_ge_4"]) > 0
    ax.scatter(float(r["mean_z"]), 100 * int(r["functional"]) / 72, marker="^" if hit else "o",
               s=22, color="black", facecolors="black" if hit else "white", linewidths=0.8)
    off = {"K0": (-12, 4), "K7": (-14, -5), "K9": (3, 3)}.get(lab, (3, 2))
    ax.annotate(lab, (float(r["mean_z"]), 100 * int(r["functional"]) / 72), xytext=off,
                textcoords="offset points", fontsize=9)
ax.axvline(0, color="0.5", linestyle=":", linewidth=0.8)
ax.set_xlabel(r"mean detector $z$ (security pilot)")
ax.set_ylabel(r"functional (\%)")
ax.set_xlim(-1.4, 3.1)
ax.set_ylim(0, 85)
fig.tight_layout(pad=0.3)
fig.savefig(FIG / "z_vs_functional.pdf")
plt.close(fig)
print("figures written to", FIG)

# ---------------------------------------------------------------- naive between-key variance
# Method-of-moments (DerSimonian-Laird-style) estimate: observed variance of per-key rates minus
# the mean binomial sampling variance. Treats the 72 rows of a key as independent, which ignores
# task/seed clustering; reported only as an illustration of the estimator.
extra: list[str] = []
for field in ("functional", "secure_and_functional"):
    rates = [int(r[field]) / 72 for r in keys]
    mean = sum(rates) / len(rates)
    s2 = sum((x - mean) ** 2 for x in rates) / (len(rates) - 1)
    within = sum(x * (1 - x) / 72 for x in rates) / len(rates)
    tau2 = max(0.0, s2 - within)
    extra.append(
        f"{field}: mean {mean:.4f}, sd_between_obs {math.sqrt(s2):.4f}, "
        f"mean_within_se {math.sqrt(within):.4f}, tau_hat {math.sqrt(tau2):.4f} "
        f"({100*math.sqrt(tau2):.1f} pp), share {tau2/s2:.2f}"
    )
with open(DATA / "derived_stats.txt", "a", encoding="utf-8") as handle:
    handle.write("\n".join(extra) + "\n")
print("\n".join(extra))
