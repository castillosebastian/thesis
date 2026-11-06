#!/usr/bin/env python3
"""Construye la presentación formal de la defensa.

Entradas
  defensa_formal.src.html  diseño y contenido visible de cada diapositiva
  guion_defensa.md         títulos y notas de orador (fuente única)
  figuras/*.png            figuras de datos (las genera figuras.py)

Salidas
  defensa_formal.html          para proyectar: notas ocultas tras la tecla N
  defensa_formal_entrega.html  sin notas, para entregar
  defensa_formal.pdf           sin notas, una diapositiva por página (si hay Chrome)

Cada <section class="slide" data-n="12"> recibe el título y las notas de la
diapositiva 12 del guion. Para cambiar un título o una nota se edita el guion;
para cambiar lo que se ve, el fuente HTML. Después: python build_formal.py
"""
import base64
import html
import mimetypes
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "defensa_formal.src.html"
GUION = HERE / "guion_defensa.md"

SECCIONES = [
    ("Introducción", "motivación, selección de características, estado del arte, propuesta y objetivos"),
    ("Marco teórico", "autocodificadores variacionales, algoritmos genéticos, métricas"),
    ("Materiales y métodos", "conjuntos de datos, línea base, modelos, diseño experimental"),
    ("Resultados", "calidad de los datos sintéticos, resultados globales, análisis por conjunto"),
    ("Conclusiones y trabajos futuros", "conclusiones, limitaciones, trabajos futuros"),
]
PIE = "C. S. Castillo · Defensa de tesis · Maestría en Minería de Datos, UTN FRP"


def md_inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s)
    return s


def leer_guion() -> dict:
    """Devuelve {numero: (titulo, notas_html)} a partir del guion."""
    texto = GUION.read_text(encoding="utf-8")
    texto = texto.split("\n## Decisiones de construcción")[0]
    out = {}
    for m in re.finditer(r"^### (R?\d+)\. (.+?)\n(.*?)(?=^### |^## |\Z)", texto, re.S | re.M):
        n, titulo, cuerpo = m.group(1), m.group(2).strip(), m.group(3)
        titulo = re.sub(r"\s*\(sección \d resaltada\)", "", titulo)
        nm = re.search(r"\*\*Notas\.\*\*\s*(.+?)(?=\n\n|\n---|\Z)", cuerpo, re.S)
        notas = f"<p>{md_inline(nm.group(1).strip())}</p>" if nm else ""
        out[n] = (md_inline(titulo), notas)
    return out


def barra(activa) -> str:
    items = []
    for i, (nombre, _) in enumerate(SECCIONES, 1):
        cls = ' class="on"' if activa == i else ""
        items.append(f"<span{cls}>{i}. {nombre}</span>")
    if activa == "R":
        items.append('<span class="on">Respaldo</span>')
    return '<nav class="secbar">' + "".join(items) + "</nav>"


def organizacion(activa) -> str:
    filas = []
    for i, (nombre, temas) in enumerate(SECCIONES, 1):
        cls = "on" if activa == i else ("off" if activa else "")
        filas.append(f'<li class="{cls}"><span class="sec">{nombre}</span><span class="temas">{temas}</span></li>')
    return '<ol class="org">' + "".join(filas) + "</ol>"


def inline_img(match: re.Match) -> str:
    rel = match.group(1)
    path = (HERE / rel).resolve()
    if not path.exists():
        raise SystemExit(f"falta la figura: {rel}")
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'src="data:{mime};base64,{data}"'


def construir(con_notas: bool) -> str:
    guion = leer_guion()
    src = SRC.read_text(encoding="utf-8")
    principales = [n for n in guion if not n.startswith("R")]
    total = max(int(n) for n in principales)
    vistos = []

    def slide(m: re.Match) -> str:
        attrs, cuerpo = m.group(1), m.group(2)
        n = re.search(r'data-n="([^"]+)"', attrs).group(1)
        if n not in guion:
            raise SystemExit(f"la diapositiva {n} no está en el guion")
        vistos.append(n)
        titulo, notas = guion[n]
        sec = re.search(r'data-sec="([^"]+)"', attrs)
        activa = None
        if sec:
            activa = "R" if sec.group(1) == "R" else int(sec.group(1))
        org = re.search(r'data-org="(\d)"', attrs)
        if org:
            cuerpo = organizacion(int(org.group(1))) + cuerpo
        cuerpo = cuerpo.replace("<!--ORG-->", organizacion(None))
        plain = "plain" in attrs
        partes = [f"<section{attrs}>"]
        if not plain:
            partes.append(barra(activa))
            partes.append(f'<div class="content"><h2>{titulo}</h2>{cuerpo}</div>')
            num = n if n.startswith("R") else f"{n} / {total}"
            partes.append(f'<footer><span>{PIE}</span><span class="num">{num}</span></footer>')
        else:
            partes.append(cuerpo)
        if con_notas and notas:
            partes.append(f'<aside class="notes">{notas}</aside>')
        partes.append("</section>")
        return "\n".join(partes)

    out = re.sub(r'<section((?:\s[^>]*)?class="slide[^>]*)>(.*?)</section>', slide, src, flags=re.S)
    faltan = [n for n in guion if n not in vistos]
    if faltan:
        raise SystemExit(f"diapositivas del guion sin maqueta: {faltan}")
    if not con_notas:
        out = out.replace("· N notas ", "")
    out, k = re.subn(r'src="((?:\.\./|figuras/)[^"]+)"', inline_img, out)
    return out, len(vistos), k


def main():
    for nombre, con_notas in (("defensa_formal.html", True), ("defensa_formal_entrega.html", False)):
        doc, n, k = construir(con_notas)
        (HERE / nombre).write_text(doc, encoding="utf-8")
        print(f"{nombre}: {n} diapositivas, {k} imágenes embebidas, {len(doc) / 1024:.0f} KB")
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if chrome and "--sin-pdf" not in sys.argv:
        pdf = HERE / "defensa_formal.pdf"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", (HERE / "defensa_formal_entrega.html").as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{pdf.name}: {pdf.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
