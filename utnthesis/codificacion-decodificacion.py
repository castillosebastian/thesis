# Genera la Figura 4.2 (diagrama de codificación y decodificación del AG).
# El ejemplo coincide con el texto del Capítulo 4: genotipo 1100101 sobre 7 características.
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

BORDE, RELLENO = "#13867A", "#DFF6F8"
BORDE_C, RELLENO_C = "#9370DB", "#ECECFF"

fig, ax = plt.subplots(figsize=(5.6, 8.2), dpi=200)
ax.set_xlim(0, 10)
ax.set_ylim(0, 15)
ax.axis("off")


def caja(x, y, w, h, texto):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="square,pad=0",
                                lw=1.4, ec=BORDE, fc=RELLENO))
    ax.text(x, y, texto, ha="center", va="center", fontsize=9.5, color="#333333", linespacing=1.5)
    return (x, y, w, h)


def flecha(p, q, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=10, lw=0.9,
                                 color="#444444", connectionstyle=f"arc3,rad={rad}"))


original = caja(4.6, 14.0, 3.6, 1.3, "Espacio original:\nX1, X2, X3, X4, X5, X6, X7")
codif = caja(3.6, 11.9, 3.3, 1.3, "Codificación\n(genotipo): 1100101")
selec = caja(2.6, 9.4, 2.3, 0.9, "Selección")
cruce = caja(2.6, 7.3, 1.8, 0.9, "Cruce")
mutac = caja(2.6, 5.4, 2.2, 0.9, "Mutación")
decod = caja(2.6, 3.3, 3.8, 1.3, "Decodificación\n(fenotipo): X1, X2, X5, X7")
salida = caja(5.4, 1.0, 3.8, 1.3, "Output: características\nseleccionadas")

ax.add_patch(Circle((6.5, 8.9), 1.75, lw=1.2, ec=BORDE_C, fc=RELLENO_C))
for dy, texto, peso in [(1.0, "Genotipo:", "bold"), (0.6, "representación interna", "normal"),
                        (0.1, "Fenotipo:", "bold"), (-0.3, "interpretación externa", "normal"),
                        (-0.9, "Ej.: 1100101 ⇒", "normal"), (-1.3, "X1, X2, X5, X7", "normal")]:
    ax.text(6.5, 8.9 + dy, texto, ha="center", va="center", fontsize=8.5, color="#333333", fontweight=peso)

flecha((4.2, 13.35), (3.8, 12.55), rad=0.2)
flecha((2.9, 11.25), (2.6, 9.85), rad=0.25)
flecha((4.8, 11.25), (6.1, 10.65), rad=-0.2)
flecha((2.6, 8.95), (2.6, 7.75))
flecha((2.6, 6.85), (2.6, 5.85))
flecha((2.6, 4.95), (2.6, 3.95))
flecha((2.6, 2.65), (4.2, 1.65), rad=0.2)
ax.plot([7.3, 9.4, 9.4], [1.0, 1.0, 14.0], color="#444444", lw=0.9)
flecha((9.4, 14.0), (6.4, 14.0))

fig.tight_layout()
fig.savefig("codificacion-decodificacion.png", dpi=200, facecolor="white")
