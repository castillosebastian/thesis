# Presentación para la defensa de tesis: diseño

Fecha: 10 de octubre de 2026. Estado: aprobado en conversación, pendiente de revisión escrita.

## Propósito

Una presentación de 20 a 25 minutos para la defensa oral de la tesis "Aumentación de datos mediante autoencoders variacionales y su impacto en estrategias de selección de características basadas en Algoritmos Genéticos" (UTN Paraná, Maestría en Minería de Datos). El autor habla; las diapositivas sostienen la explicación con una idea por diapositiva, figuras grandes y poco texto. El jurado ya leyó la tesis y envió observaciones; el relato las integra sin anunciarlas como respuestas.

Criterio de éxito: el autor puede dar la charla completa en 22 minutos siguiendo solo las diapositivas y sus notas, y el archivo se proyecta desde cualquier navegador sin internet.

## Entregables

Carpeta `presentacion/` en la raíz del repo:

| Archivo | Qué es |
| --- | --- |
| `defensa.src.html` | Fuente editable. Figuras referenciadas como `../utnthesis/<nombre>.png`. |
| `build.py` | Lee el fuente, reemplaza cada `src="../utnthesis/x.png"` por su data URI base64 y escribe `defensa.html`. Sin dependencias fuera de la biblioteca estándar. |
| `defensa.html` | Archivo final, único y portable. Es el que se proyecta. |

Fuera de alcance: exportación a PowerPoint, vista de orador en ventana separada, transiciones animadas, temas claro/oscuro.

## Aspecto

- Fondo `#FAFAF8`, texto `#1A1A1A`, gris secundario `#6B6B6B`, acento azul UTN `#1F4E79` (rótulo de sección, números clave, líneas finas, barra de progreso). Las figuras conservan el rosado y gris de la tesis.
- Títulos en serif del sistema: `Georgia, "Times New Roman", "Liberation Serif", serif`. Cuerpo en sans del sistema: `system-ui, "Segoe UI", Roboto, "Liberation Sans", sans-serif`. Sin fuentes externas.
- Cada diapositiva es una caja de 1600 x 900 unidades escalada con `transform: scale()` para caber en la ventana, centrada, manteniendo 16:9. Texto base 36 px en esa caja; títulos 64 px; número grande 180 px.
- Elementos fijos por diapositiva: rótulo de bloque arriba a la izquierda (por ejemplo "Método"), número de diapositiva abajo a la derecha, barra de progreso de 2 px al pie. La portada y la diapositiva final no llevan rótulo ni número.
- Figuras: hasta 62% de la altura, centradas, con una línea en gris debajo que indica cómo leerlas.
- Tablas: sin bordes verticales, cabecera en gris, filas con línea fina, números alineados a la derecha.
- Diapositivas de un solo número grande: como máximo cuatro en toda la presentación.
- Fundido de 150 ms al cambiar de diapositiva. Ningún otro movimiento.

## Comportamiento

- Avanzar: flecha derecha, espacio, Av Pág, clic en la mitad derecha. Retroceder: flecha izquierda, Re Pág, clic en la mitad izquierda. Inicio y Fin saltan a la primera y última.
- La diapositiva actual se refleja en la URL como `#12`; al abrir con hash se muestra esa diapositiva.
- Tecla N: muestra u oculta la franja de notas de orador al pie (fondo oscuro, texto claro, 28 px). Tecla F: pantalla completa. Tecla Escape: cierra notas.
- Impresión: `@media print` muestra todas las diapositivas, una por página apaisada A4, sin barra ni notas. Eso produce el PDF desde el navegador.
- Las diapositivas de respaldo van después de un separador titulado "Respaldo" y no cuentan en la barra de progreso ni en el total mostrado.
- Todo el JavaScript en el mismo archivo, sin bibliotecas, menos de 120 líneas.

## Contenido, diapositiva por diapositiva

Cada diapositiva lleva un `<aside class="notes">` con 3 a 6 líneas para el orador, tomadas de la tesis y de `Respuesta_observaciones_jurado.md`.

### Bloque 1: Problema e hipótesis

1. **Portada.** Logo UTN, "Tesis de Maestría", título completo, autor, directores (Dr. Matías Gerard, Dr. Leandro Vignolo), Paraná, 2025.
2. **El problema en una frase.** Texto grande: "Seleccionar características con un algoritmo genético exige evaluar miles de subconjuntos, y cada evaluación vale lo que valen los datos." Debajo, cuatro palabras en fila: alta dimensionalidad, escasez muestral, desbalance, ruido.
3. **Dónde duele.** Diagrama SVG mínimo: AG propone subconjunto, clasificador lo evalúa con los datos, aptitud guía la selección. Flecha marcada en rojo discreto sobre "los datos": con pocas muestras la aptitud es ruidosa y la búsqueda se desorienta.
4. **Hipótesis y objetivos.** Hipótesis: aumentar sintéticamente las muestras con un autocodificador variacional mejora la selección con AG. Tres objetivos específicos tal como figuran en el capítulo 1.

### Bloque 2: Datos y línea base

5. **Cinco conjuntos de datos.** Tabla: nombre, observaciones x características, clases, desafío principal (Leukemia 72x7.129 binario desbalanceado; Gisette 13.500x5.000 binario con ruido; Madelon 2.000x500 binario con 480 variables de ruido; GCM 190x16.063, 14 clases desbalanceadas; ALL Leukemia 327x12.600, 14 clases desbalanceadas).
6. **Línea base con modelos clásicos.** Tabla reducida de la Tabla 2.1: mejor y mediana por conjunto. Mensaje: Leukemia y Gisette están cerca de saturar; Madelon y GCM tienen margen.

### Bloque 3: Método

7. **El autocodificador variacional.** Diagrama SVG: x, codificador, mu y sigma, z, decodificador, x reconstruido. Fórmula de la pérdida en una línea: reconstrucción (MSE) más divergencia KL. Nota: versión condicional por clase para los multiclase, con pesos de clase y muestreo ponderado.
8. **Los datos sintéticos sirven para entrenar.** Figura `grafico_MLP-reales-vs-sintenticos.png`. Mensaje: un MLP entrenado solo con sintéticos iguala al entrenado con reales en Leukemia, Madelon y GCM.
9. **Más muestras no siempre es mejor.** Figura `n_samples_accuracy_comparison.png`. Mensaje: en GCM, 3.000 muestras balanceadas mejoran; 6.000 degradan. Espacio latente de 35 supera a 50.
10. **El algoritmo genético.** Cromosoma binario de largo igual al número de características; aptitud = 0,5 x exactitud + 0,5 x (1 menos la fracción de características activas); evaluador MLP; cruce, mutación, 15 a 30 generaciones, población 100. Un pequeño SVG del cromosoma.
11. **Diseño experimental.** Figura `diseño_experimentos.png`. Mismo AG con y sin aumentación, mismos parámetros. Evaluación siempre en la partición original de testeo. Tres criterios: exactitud, número de características, estabilidad entre corridas.

### Bloque 4: Resultados

12. **Resultados globales.** Tabla de cinco filas: corridas, exactitud original, exactitud aumentada, diferencia en puntos, p, lectura. Valores de `Respuesta_observaciones_jurado.md`.
13. **Dónde existe el efecto.** Figura `diferencia_exactitud_ic95.png`. Línea de lectura: "donde la barra cruza el cero no hay evidencia".
14. **La regla.** Figura `boxplot_resultados_precision_escala_unificada.png`. Texto: "Saturado: no cambia. Con margen y buena reconstrucción: mejora."
15. **Madelon.** Número grande "+7,8 puntos" (0,750 a 0,828, p < 0,001) y "29 variables en lugar de 36". Figura `boxplot_madelon_combined.png` reducida. Por qué: el AV realza las 20 variables con señal entre 480 de ruido.
16. **GCM, primera etapa: falló.** 0,512 contra 0,538 con el AVC sobre 16.063 variables. Diagnóstico: MLP 100% en sintéticos, 50% en reales: colapso de la posterior. Figura `boxplot_gcm_combined_part1.png` pequeña.
17. **Selección, generación, selección.** Diagrama SVG de tres cajas en fila: AG sobre 16.063 produce 1.600 características más frecuentes; AVC genera 3.000 muestras en ese subespacio; AG final sobre datos aumentados. Resultado: 0,497 a 0,541, +4,4 puntos, p = 0,005. Figura `boxplot_gcm_combined.png` pequeña.
18. **ALL Leukemia: validación.** Mismo flujo. Tendencia favorable con 35 y 180 genes, sin significación; con 300 genes no hay diferencia. Figura `boxplot_all_leukemia_ngenes_accuracy.png`.
19. **Qué significa "mejora".** Tabla de tres criterios por conjunto (desempeño, reducción de variables, estabilidad) tomada de la respuesta (e).

### Bloque 5: Cierre

20. **Limitaciones.** Cinco líneas: pocos conjuntos y dos artificiales; pocas corridas en multiclase y tests chicos; depende de la calidad del AV; umbral de muestras sintéticas; un solo clasificador y parámetros por conjunto.
21. **Conclusiones y trabajos futuros.** Tres conclusiones en una línea cada una. Tres líneas de futuro: pérdida con KL recocida y AV jerárquicos; optimización conjunta AV-AG; ensambles y encadenamientos.
22. **Gracias.** Título, autor, repositorio del código.

### Respaldo

- B1. **Leukemia y Gisette.** Figuras `boxplot_leukemia_combined.png` y `boxplot_gisette_combined.png` lado a lado; sin diferencia significativa, menor dispersión.
- B2. **Comparación con el estado del arte.** Tabla de la respuesta (a): MLP con todas las variables, AG sin y con aumentación, variables usadas; más Ramaswamy 78%, NIPS 2003 error 0,07.
- B3. **Por qué no SMOTE.** Tres referencias: Blagus y Lusa 2013, Fajardo 2021, Ai 2023. SMOTE rebalancea, no aumenta.
- B4. **Test de significación en GCM.** Corridas reales 9 contra 10, Welch p = 0,005, Mann-Whitney p = 0,006; toda la etapa 18 contra 25, p = 0,008.

## Verificación

1. `python3 presentacion/build.py` termina sin error y `defensa.html` no contiene `../utnthesis/`.
2. Capturas con Chrome sin cabeza de cada diapositiva a 1920x1080 y de cinco diapositivas representativas a 1366x768; revisión visual de recorte, superposición y legibilidad.
3. Navegación: hash en URL, teclas, clic, notas, pantalla completa, probadas en el navegador.
4. Impresión a PDF desde Chrome sin cabeza: 26 páginas apaisadas.
5. Lectura en voz alta del guion de notas para estimar el tiempo: objetivo 22 minutos.
