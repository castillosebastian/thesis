#!/usr/bin/env python3
"""Genera las figuras de datos de la presentación a partir de los archivos de experimentos.

Uso: ../.venv/bin/python figuras.py
Salida: presentacion/figuras/*.png

Un solo estilo para todas: azul = con aumentación / datos sintéticos,
gris = sin aumentación / datos reales. Cada punto es una corrida completa del AG.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy import stats

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "utnthesis"
OUT = HERE / "figuras"
OUT.mkdir(exist_ok=True)

PAPER = "#FAFAF8"
INK = "#1A1A1A"
GREY = "#6B6B6B"
RULE = "#D8D6D0"
AUM = "#2E6DA4"   # con aumentación / sintéticos
ORI = "#8A8A8A"   # sin aumentación / reales

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 15,
    "axes.edgecolor": GREY,
    "axes.labelcolor": INK,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.facecolor": "none",
    "figure.facecolor": "none",
    "savefig.transparent": True,
    "xtick.color": INK,
    "ytick.color": GREY,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.color": RULE,
    "grid.linewidth": 0.8,
    "axes.axisbelow": True,
    "legend.frameon": False,
})


def coma(dec):
    return FuncFormatter(lambda v, _: f"{v:.{dec}f}".replace(".", ","))


def miles():
    return FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", "."))


def caja(ax, valores, pos, color, ancho=0.5, seed=0):
    """Caja con mediana y cada corrida como punto."""
    valores = np.asarray(valores, dtype=float)
    bp = ax.boxplot(valores, positions=[pos], widths=ancho, patch_artist=True,
                    showfliers=False, whis=(0, 100),
                    medianprops=dict(color=INK, linewidth=2),
                    boxprops=dict(facecolor=color, edgecolor=color, alpha=0.30, linewidth=0),
                    whiskerprops=dict(color=color, linewidth=1.5),
                    capprops=dict(color=color, linewidth=1.5))
    for b in bp["boxes"]:
        ax.add_patch(plt.Polygon(b.get_path().vertices[:4], closed=True, fill=False,
                                 edgecolor=color, linewidth=1.5))
    rng = np.random.default_rng(seed)
    x = pos + rng.uniform(-ancho * 0.28, ancho * 0.28, size=len(valores))
    ax.scatter(x, valores, s=34, color=color, edgecolor=PAPER, linewidth=1.0, zorder=3)


def par(ax, aum, ori, etiquetas=("Con\naumentación", "Sin\naumentación"), seed=0):
    caja(ax, ori, 0, ORI, seed=seed)
    caja(ax, aum, 1, AUM, seed=seed + 1)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([etiquetas[1], etiquetas[0]])
    if "\n" in etiquetas[0]:
        ax.tick_params(axis="x", labelsize=12.5)
    ax.set_xlim(-0.6, 1.6)


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("  ->", nombre)


def welch(a, o):
    a, o = np.asarray(a, float), np.asarray(o, float)
    d = a.mean() - o.mean()
    va, vo = a.var(ddof=1) / len(a), o.var(ddof=1) / len(o)
    se = np.sqrt(va + vo)
    gl = (va + vo) ** 2 / (va ** 2 / (len(a) - 1) + vo ** 2 / (len(o) - 1))
    t = stats.t.ppf(0.975, gl)
    p = stats.ttest_ind(a, o, equal_var=False).pvalue
    return d, d - t * se, d + t * se, p


# ---------------------------------------------------------------- datos
d = pd.read_csv(DATA / "filtered_experiment_data_v2.csv")
eg = d["experiment_group"]


def grupo(mask):
    s = d[mask]
    return s[s["group"] == "aumentados"], s[s["group"] == "original"]


conjuntos = {
    "Leukemia": grupo(eg.str.startswith("leukemia")),
    "Gisette": grupo(eg.str.startswith("gisette")),
    "Madelon": grupo(eg.str.startswith("mandelon")),
    "GCM": grupo(eg.isin(["gcm_base_0061", "gcm_base_0066", "gcm_base_0063", "gcm_base_0065"])),
    "ALL Leukemia": grupo(eg.str.startswith("all_leukemia")),
}

print("Resumen (aumentados / originales):")
for nombre, (a, o) in conjuntos.items():
    dif, lo, hi, p = welch(a["pob_accuracy_avg"], o["pob_accuracy_avg"])
    print(f"  {nombre:13s} n={len(a)}/{len(o)}  acc {o.pob_accuracy_avg.mean():.3f}->{a.pob_accuracy_avg.mean():.3f}"
          f"  dif={dif*100:+.2f} [{lo*100:.2f}, {hi*100:.2f}] p={p:.4f}"
          f"  sd {a.pob_accuracy_avg.std():.3f}/{o.pob_accuracy_avg.std():.3f}"
          f"  ngenes {a.pob_ngenes_avg.mean():.1f}/{o.pob_ngenes_avg.mean():.1f}")

# ------------------------------------------------- 25. MLP reales vs sintéticos
fig, ax = plt.subplots(figsize=(11.5, 4.9))
nombres = ["Leukemia", "Madelon", "Gisette", "GCM"]
reales = [0.81, 0.55, 0.97, 0.54]
sint = [0.95, 0.57, 0.95, 0.54]
x = np.arange(4)
w = 0.30
b1 = ax.bar(x - w / 2 - 0.015, reales, w, color=ORI, label="MLP entrenado con datos reales")
b2 = ax.bar(x + w / 2 + 0.015, sint, w, color=AUM, label="MLP entrenado con datos sintéticos")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.015,
                f"{b.get_height():.2f}".replace(".", ","), ha="center", va="bottom", color=INK)
ax.set_xticks(x); ax.set_xticklabels(nombres)
ax.set_ylim(0, 1.12); ax.set_yticks(np.arange(0, 1.01, 0.2)); ax.yaxis.set_major_formatter(coma(1))
ax.set_ylabel("Exactitud en la partición de testeo")
ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.13))
guardar(fig, "mlp_reales_vs_sinteticos.png")

# ------------------------------------------------- 26. umbral de muestras en GCM
fig, ax = plt.subplots(figsize=(11.5, 4.9))
n = ["190", "400", "3.000", "6.000"]
acc = [0.1228, 0.3860, 0.5439, 0.2105]
bars = ax.bar(np.arange(4), acc, 0.42, color=AUM)
for b in bars:
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.012,
            f"{b.get_height():.2f}".replace(".", ","), ha="center", va="bottom", color=INK)
ax.axhline(0.54, color=ORI, linewidth=1.6, zorder=0)
ax.text(-0.42, 0.555, "MLP entrenado con datos reales: 0,54", ha="left", va="bottom", color=GREY)
ax.set_xticks(np.arange(4)); ax.set_xticklabels(n)
ax.set_xlabel("Muestras sintéticas usadas para entrenar el MLP (GCM)")
ax.set_ylim(0, 0.7); ax.yaxis.set_major_formatter(coma(1))
ax.set_ylabel("Exactitud en la partición de testeo")
guardar(fig, "umbral_muestras_gcm.png")

# ------------------------------------------------- 28. diferencia con IC 95 %
fig, ax = plt.subplots(figsize=(11.5, 4.9))
for i, (nombre, (a, o)) in enumerate(conjuntos.items()):
    dif, lo, hi, p = welch(a["pob_accuracy_avg"], o["pob_accuracy_avg"])
    sig = lo > 0
    c = AUM if sig else ORI
    ax.plot([i, i], [lo * 100, hi * 100], color=c, linewidth=2.5, solid_capstyle="round")
    ax.scatter([i], [dif * 100], s=110, color=c, edgecolor=PAPER, linewidth=1.5, zorder=3)
    cerca = abs(dif * 100) < 1
    ax.text(i + 0.12, dif * 100 + (0.35 if cerca else 0), f"{dif*100:+.1f}".replace(".", ","),
            va="bottom" if cerca else "center", ha="left", color=INK)
ax.axhline(0, color=INK, linewidth=1)
ax.set_xticks(range(5)); ax.set_xticklabels(list(conjuntos))
ax.set_xlim(-0.5, 4.6)
ax.set_ylabel("Diferencia de exactitud\n(puntos porcentuales)")
ax.yaxis.set_major_formatter(coma(0))
guardar(fig, "ic95.png")

# ------------------------------------------------- 29. escala común
fig, axes = plt.subplots(1, 5, figsize=(13.5, 4.9), sharey=True)
for i, (ax, (nombre, (a, o))) in enumerate(zip(axes, conjuntos.items())):
    par(ax, a["pob_accuracy_avg"], o["pob_accuracy_avg"], etiquetas=("Con", "Sin"), seed=i)
    ax.set_title(nombre, fontsize=16, color=INK, pad=10)
    ax.set_ylim(0.4, 1.0)
    ax.yaxis.set_major_formatter(coma(1))
axes[0].set_ylabel("Exactitud en la partición de testeo")
fig.subplots_adjust(wspace=0.12)
guardar(fig, "escala_comun.png")


# ------------------------------------------------- pares exactitud + variables
def dos_paneles(a, o, nombre, dec=2, ylabel2="Variables seleccionadas"):
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 5.0))
    par(axes[0], a["pob_accuracy_avg"], o["pob_accuracy_avg"], seed=1)
    axes[0].set_ylabel("Exactitud en la partición de testeo")
    axes[0].yaxis.set_major_formatter(coma(dec))
    par(axes[1], a["pob_ngenes_avg"], o["pob_ngenes_avg"], seed=3)
    axes[1].set_ylabel(ylabel2)
    axes[1].yaxis.set_major_formatter(miles())
    fig.subplots_adjust(wspace=0.42)
    guardar(fig, nombre)


a, o = conjuntos["Madelon"]
dos_paneles(a, o, "madelon.png")

# GCM primera etapa: experimentos del script graficar_gcm_parte1.py
e = pd.read_csv(DATA / "experiments_results.csv")
e = e[e["experiment_name"].str.contains("gcm")].copy()
e["experiment_group"] = e["experiment_name"].str[:13]
e = e[e["experiment_group"].str.contains("0031|0033|0035|0036|0037|0038|0040")]
orig1 = ["gcm_base_0037", "gcm_base_0038", "gcm_base_0039", "gcm_base_0040"]
o1 = e[e["experiment_group"].isin(orig1)]
a1 = e[~e["experiment_group"].isin(orig1)]
print(f"GCM 1.ª etapa: n={len(a1)}/{len(o1)} acc {o1.pob_accuracy_avg.mean():.3f}->{a1.pob_accuracy_avg.mean():.3f}"
      f" sd {a1.pob_accuracy_avg.std():.3f}/{o1.pob_accuracy_avg.std():.3f}"
      f" ngenes {a1.pob_ngenes_avg.mean():.0f}/{o1.pob_ngenes_avg.mean():.0f}")
dos_paneles(a1, o1, "gcm_etapa1.png")

# ------------------------------------------------- 34. GCM segunda etapa, exactitud
a, o = conjuntos["GCM"]
fig, ax = plt.subplots(figsize=(6.4, 4.9))
par(ax, a["pob_accuracy_avg"], o["pob_accuracy_avg"], seed=5)
ax.set_ylabel("Exactitud en la partición de testeo")
ax.yaxis.set_major_formatter(coma(2))
guardar(fig, "gcm_etapa2.png")


# ------------------------------------------------- 35 y 36. por tamaño de cromosoma
def por_tamano(pares, nombre, dec=2):
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    ticks, labels = [], []
    for i, (rotulo, ga, go) in enumerate(pares):
        va = d[eg == ga]["pob_accuracy_avg"]; vo = d[eg == go]["pob_accuracy_avg"]
        c = i * 2.6
        caja(ax, vo, c, ORI, ancho=0.8, seed=i)
        caja(ax, va, c + 1, AUM, ancho=0.8, seed=i + 10)
        # media de cada grupo: rombo blanco con borde de tinta, para leerla junto a la mediana
        ax.scatter([c, c + 1], [vo.mean(), va.mean()], marker="D", s=52, facecolor=PAPER,
                   edgecolor=INK, linewidth=1.4, zorder=5)
        ticks.append(c + 0.5); labels.append(rotulo)
        _, _, _, p = welch(va, vo)
        print(f"  {nombre} {rotulo}: n={len(va)}/{len(vo)} {vo.mean():.3f}->{va.mean():.3f} p={p:.3f}")
    ax.set_xticks(ticks); ax.set_xticklabels(labels)
    ax.set_xlabel("Genes activos en el cromosoma")
    ax.set_ylabel("Exactitud en la partición de testeo")
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_formatter(coma(dec))
    h = [plt.Rectangle((0, 0), 1, 1, facecolor=ORI, alpha=0.5, edgecolor=ORI),
         plt.Rectangle((0, 0), 1, 1, facecolor=AUM, alpha=0.5, edgecolor=AUM),
         plt.Line2D([], [], linestyle="none", marker="D", markersize=7, markerfacecolor=PAPER,
                    markeredgecolor=INK, markeredgewidth=1.4)]
    ax.legend(h, ["Sin aumentación", "Con aumentación", "Media"], loc="upper left", ncol=3,
              bbox_to_anchor=(0, 1.12))
    guardar(fig, nombre)


por_tamano([("~45", "gcm_base_0064", "gcm_base_0067"),
            ("~200", "gcm_base_0069", "gcm_base_0070"),
            ("~450", "gcm_base_0066", "gcm_base_0065"),
            ("~750", "gcm_base_0061", "gcm_base_0063")], "gcm_cromosoma.png")
por_tamano([("~35", "all_leukemia_base_0079", "all_leukemia_base_0080"),
            ("~180", "all_leukemia_base_0075", "all_leukemia_base_0076"),
            ("~300", "all_leukemia_base_0077", "all_leukemia_base_0078")], "all_cromosoma.png")

# ------------------------------------------------- 37. conjuntos saturados
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))
a, o = conjuntos["Leukemia"]
par(axes[0], a["pob_accuracy_avg"], o["pob_accuracy_avg"], etiquetas=("Con", "Sin"), seed=7)
axes[0].set_title("Leukemia: exactitud", fontsize=16, pad=10)
axes[0].yaxis.set_major_formatter(coma(2))
a, o = conjuntos["Gisette"]
par(axes[1], a["pob_accuracy_avg"], o["pob_accuracy_avg"], etiquetas=("Con", "Sin"), seed=8)
axes[1].set_title("Gisette: exactitud", fontsize=16, pad=10)
axes[1].yaxis.set_major_formatter(coma(3))
par(axes[2], a["pob_ngenes_avg"], o["pob_ngenes_avg"], etiquetas=("Con", "Sin"), seed=9)
axes[2].set_title("Gisette: variables seleccionadas", fontsize=16, pad=10)
q = lambda s: s.quantile(0.75) - s.quantile(0.25)
print(f"Gisette RIC ngenes: {q(a.pob_ngenes_avg):.1f} / {q(o.pob_ngenes_avg):.1f}")
fig.subplots_adjust(wspace=0.30)
guardar(fig, "saturados.png")
