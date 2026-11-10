"""Capturas de conjuntos de datos reales para la diapositiva 2 (datos y dimensionalidad).

Genera en figuras/:
  datos_adn.png       matriz de expresión génica de Leukemia (72 pacientes x 7.129 genes),
                      a partir de ../ealab/data/leukemia_{train_38x7129,test_34x7129}.arff
  datos_finanzas.png  precios de cierre normalizados del S&P 500 (505 acciones x 1.259 días),
                      a partir de all_stocks_5yr.csv (plotly/datasets, origen Kaggle "S&P 500 stock data")
  datos_video.png     cuatro fotogramas de Big Buck Bunny (Blender Foundation, CC BY 3.0),
                      extraídos con ffmpeg desde archive.org

Uso:
  ../.venv/bin/python figuras_datos.py DIRECTORIO_DESCARGAS
donde DIRECTORIO_DESCARGAS contiene:
  dl_fin/all_stocks_5yr.csv   https://raw.githubusercontent.com/plotly/datasets/master/all_stocks_5yr.csv
  dl_vid/f_*.png              ffmpeg -ss HH:MM:SS -i https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4 -frames:v 1 f_HHMMSS.png
                              (instantes usados: 00:01:05, 00:03:20, 00:05:40, 00:07:15)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "figuras"
DESCARGAS = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None

AZUL = "#1F4E79"
GRIS = "#6B6B6B"
AZULES = LinearSegmentedColormap.from_list("azules", ["#F4F7FA", "#B9CBDD", "#5B86AE", AZUL, "#102B45"])

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": "#D8D6D0",
                     "savefig.transparent": True})


def leer_arff(path: Path) -> pd.DataFrame:
    lineas = path.read_text(encoding="utf-8", errors="replace").splitlines()
    inicio = next(i for i, l in enumerate(lineas) if l.strip().upper() == "@DATA") + 1
    nombres = [l.split()[1] for l in lineas[:inicio] if l.upper().startswith("@ATTRIBUTE")]
    filas = [l.split(",") for l in lineas[inicio:] if l.strip() and not l.startswith("%")]
    return pd.DataFrame(filas, columns=nombres)


def matriz(m, salida):
    """Matriz sin rótulos: las dimensiones van en el pie de la diapositiva."""
    fig, ax = plt.subplots(figsize=(6.4, 2.7))
    ax.imshow(m, aspect="auto", cmap=AZULES, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(OUT / salida, dpi=170)
    plt.close(fig)


def adn():
    base = HERE.parent / "ealab" / "data"
    df = pd.concat([leer_arff(base / "leukemia_train_38x7129.arff"),
                    leer_arff(base / "leukemia_test_34x7129.arff")], ignore_index=True)
    clase = df["CLASS"]
    x = df.drop(columns="CLASS").astype(float).to_numpy()
    x = np.log2(np.clip(x, 20, None))                       # preprocesamiento habitual de Golub: piso 20 y log2
    x = (x - x.mean(0)) / (x.std(0) + 1e-9)                 # estandarizar por gen
    c = clase.to_numpy()
    orden_p = np.argsort(c, kind="stable")                  # pacientes: ALL primero, AML después
    orden_g = np.argsort(x[c == "ALL"].mean(0) - x[c == "AML"].mean(0))  # genes por diferencia entre clases
    x = np.clip(x[orden_p][:, orden_g], -2.5, 2.5)
    matriz(x, "datos_adn.png")
    return x.shape


def finanzas():
    df = pd.read_csv(DESCARGAS / "dl_fin" / "all_stocks_5yr.csv", usecols=["date", "close", "Name"])
    p = df.pivot(index="Name", columns="date", values="close")
    p = p.dropna(axis=0, thresh=int(0.98 * p.shape[1])).ffill(axis=1).bfill(axis=1)
    r = np.log(p.div(p.iloc[:, 0], axis=0))                 # log del precio relativo al primer día
    r = r.loc[r.iloc[:, -1].sort_values().index]            # acciones ordenadas por rendimiento final
    m = np.clip(r.to_numpy(), -1.2, 1.6)
    matriz(m, "datos_finanzas.png")
    return m.shape


def video():
    cuadros = sorted((DESCARGAS / "dl_vid").glob("f_*.png"))
    assert len(cuadros) >= 4, "faltan fotogramas"
    ancho, alto, sep = 300, 169, 10
    tira = Image.new("RGBA", (4 * ancho + 3 * sep, alto), (0, 0, 0, 0))
    for i, c in enumerate(cuadros[:4]):
        im = Image.open(c).convert("RGB").resize((ancho, alto), Image.LANCZOS)
        tira.paste(im, (i * (ancho + sep), 0))
    tira.save(OUT / "datos_video.png")
    w, h = Image.open(cuadros[0]).size
    return (w, h, len(cuadros))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    print("adn", adn())
    if DESCARGAS:
        print("finanzas", finanzas())
        print("video", video())
