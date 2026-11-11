# Guion de la defensa: estructura formal

Borrador del 4 de noviembre de 2026, para revisar antes de construir las diapositivas.

**Tesis:** Aumentación de datos mediante autoencoders variacionales y su impacto en estrategias de selección de características basadas en Algoritmos Genéticos.
**Tesista:** Claudio Sebastian Castillo. **Director:** Dr. Matías Gerard. **Codirector:** Dr. Leandro Vignolo.
**Maestría en Minería de Datos, UTN Facultad Regional Paraná.**

## Cómo leer este documento

- Cada diapositiva tiene un número, un **título que es una oración completa** (lo que el jurado lee), el **contenido visible** (figura, tabla o ítems) y las **notas de orador** (lo que vos decís, no va en la diapositiva).
- **Registro.** Títulos y texto visible en registro académico: se nombra cada fenómeno con el término técnico que usa la tesis (maldición de la dimensionalidad, colapso de la distribución posterior, escasez muestral), en oraciones completas y sin giros coloquiales. Las notas de orador son más libres porque no se proyectan.
- Tiempo previsto: 40 a 45 minutos. Son 44 diapositivas en total: 37 de contenido, portada, organización inicial, cuatro repeticiones de "Organización" que se pasan en segundos, y cierre. A razón de una por minuto da 43 minutos.
- Las figuras nombradas existen en `utnthesis/`. Las marcadas **(nuevo SVG)** se dibujan para la presentación.
- **Estado al 5 de noviembre de 2026: la presentación está construida.** Este guion es la fuente de los títulos y de las notas de orador: `build_formal.py` los toma de acá según el número de diapositiva. Los párrafos **Visible** quedan como la descripción original; el contenido visible definitivo está en `defensa_formal.src.html`. Ver la sección "Cómo quedó construida" al final.
- Los números salen de la tesis corregida y de `Respuesta_observaciones_jurado.md`. Donde la tesis y la respuesta difieren, se usa la respuesta (corridas reales como n, puntos porcentuales junto a porcentajes relativos).
- Lo que el jurado pidió está integrado sin anunciarlo: escala común en los gráficos (Quiroga c), resultados globales antes del detalle (Quiroga d), definición de "mejora" en tres criterios (Chan e), conclusiones moderadas y limitaciones explícitas (Chan f). El estado del arte (Quiroga a) y SMOTE (Quiroga b) van en respaldo.

## Reparto del tiempo

| Sección | Diapositivas | Minutos |
| --- | --- | --- |
| Portada y organización | 0 a 1 | 1 |
| 1. Introducción | 2 a 8 | 7 |
| 2. Marco teórico | 9 a 15 | 7 |
| 3. Materiales y métodos | 16 a 22 | 7 |
| 4. Resultados | 23 a 38 | 16 |
| 5. Conclusiones y trabajos futuros | 39 a 42 | 4 |
| Cierre | 43 | 1 |
| Respaldo | R1 a R7 | solo para preguntas |

---

## Portada

### 0. Portada

**Visible.** Logo UTN. "Tesis de Maestría en Minería de Datos". Título completo. Tesista. Director y codirector. Paraná, 2026.

**Notas.** Buenas tardes. Agradezco al jurado la lectura y las observaciones, que están incorporadas en lo que sigue, y al director y codirector. La exposición sigue la estructura del documento: introducción, marco teórico, materiales y métodos, resultados y conclusiones. Dura unos cuarenta minutos.

### 1. Organización

**Visible.** Lista numerada de las cinco secciones, con subtemas en una línea cada una:
1. Introducción: motivación, selección de características, estado del arte, propuesta y objetivos.
2. Marco teórico: autocodificadores variacionales, algoritmos genéticos, métricas.
3. Materiales y métodos: conjuntos de datos, línea base, modelos, diseño experimental.
4. Resultados: calidad de los datos sintéticos, resultados globales, análisis por conjunto.
5. Conclusiones y trabajos futuros.

**Notas.** Un minuto. Decir que la mayor parte del tiempo va a los resultados, y que las conclusiones son cortas porque son una guía para la discusión. Esta diapositiva se repite, con la sección activa resaltada, al entrar a cada sección.

---

## 1. Introducción

### 2. Datos y selección de características

**Visible.** Dos columnas. Izquierda: "Microarreglos de ADN: miles de genes, decenas de pacientes". Derecha: "Video, finanzas, redes sociales: grandes conjuntos de variables". En el medio, el término en una línea: *maldición de la dimensionalidad: alta demanda computacional y problemas intratables en la práctica* (Bolón-Canedo et al., 2015). Abajo, con una flecha desde el término anterior, la definición: *selección de características: determinar un subconjunto de atributos que satisfaga uno de tres criterios* (Vignolo y Gerard, 2017): el de tamaño especificado que maximice la precisión; el de menor tamaño que satisfaga una precisión mínima; el que logre el mejor compromiso entre dimensionalidad y precisión. (Construida: las tarjetas de arriba son capturas de datos reales: Leukemia, fotogramas de video y S&P 500.)

**Notas.** La motivación del capítulo 1. La tesis nombra el fenómeno como la maldición de la dimensionalidad, en el sentido de Bolón-Canedo: espacios de variables cuya optimización es intratable en la práctica. Fisher ya en los años treinta reprochaba estudiar variables aisladas en vez de sus interacciones; Hughes en los sesenta mostró que la exactitud de un clasificador no crece indefinidamente con el número de variables. Hoy el caso típico es la biomedicina: un microarreglo mide miles de genes sobre decenas de pacientes. Tres de los cinco conjuntos de la tesis son de ese tipo.

### 3. Propiedades de los datos que dificultan la selección de características

**Visible.** La caja de alta dimensionalidad y escasez muestral arriba, centrada, como punto de entrada; de ella salen tres flechas rotuladas hacia las otras tres (agrava → desbalance; genera dispersión de las muestras → complejidad; multiplica las variables irrelevantes → ruido). Cada caja tiene un rótulo, su enunciación formal (notación del capítulo 1: n características, m observaciones) y una línea:
- **Alta dimensionalidad y escasez muestral**: n ≫ m; sobreajuste a las observaciones disponibles o incapacidad de capturar la estructura de los datos.
- **Desbalance de clases**: m_mayoritaria ≫ m_minoritaria; la evaluación prioriza la clase mayoritaria y descarta características útiles para las minoritarias.
- **Complejidad**: frontera difícil de describir, por el problema o por la muestra. Tres líneas: ambigüedad (las características no distinguen las clases); fronteras intrincadas (propias del problema, no de la muestra); dispersión (pocas observaciones en muchas dimensiones).
- **Ruido**: x̃ = x + ε, en los valores: medición o transmisión. En las variables: características irrelevantes o redundantes mezcladas con las relevantes (Madelon: 480 de 500).

**Notas.** Son los cuatro problemas que organizan la tesis y la elección de los conjuntos de datos. El punto de entrada es la alta dimensionalidad con escasez muestral, que es lo que la aumentación ataca; los otros tres se encadenan con ella tal como lo dice el capítulo 1: el desbalance "puede darse en combinación con alta dimensionalidad y escasez muestral, agravando la dificultad"; la dispersión de muestras la "genera la combinación de pocas muestras y alta dimensionalidad"; y para el ruido, la reducción de dimensionalidad es el remedio contra las características irrelevantes y redundantes. Las flechas no dicen "causa": dicen agrava, genera dispersión, multiplica. Señalar que de los tres aspectos de la complejidad, solo la dispersión de muestras es atacable con aumentación; la ambigüedad y las fronteras complejas no dependen de la muestra. El desbalance tiene tres familias de remedios: muestreo, modificación del algoritmo y aprendizaje sensible al costo; la tesis usa las dos primeras dentro del autocodificador.

### 4. Enfoques para la selección de características

**Visible.** Tres tarjetas, cada una con un esquema de igual esqueleto, Datos → … → Modelo, donde solo cambia la posición de la caja "Selección" respecto de "Entrenamiento": Filtro, antes y separada (paso previo e independiente del modelo); Envolvente, en un ciclo con el entrenamiento, que devuelve la aptitud del subconjunto (el clasificador evalúa cada subconjunto); Embebido, dentro de la misma caja (simultáneos, una sola optimización). Debajo de cada esquema, dos viñetas: Filtro (rápido y escalable, no usa el clasificador; los univariados ignoran las dependencias entre variables, los multivariados las miden con un criterio estadístico y no con el desempeño del modelo), Envolvente (captura dependencias; costo exponencial 2ⁿ subconjuntos posibles, "con n = 16.063 genes, la búsqueda exhaustiva es intratable" entre paréntesis), Embebido (menor costo que el envolvente; específico del modelo). Debajo de las tarjetas, una flecha corta sale de la tarjeta Envolvente hacia un nodo en forma de píldora: "Heurística de búsqueda: **algoritmo genético**" (Vignolo y Gerard, 2017). Sin línea de cierre.

**Notas.** No hay un método superior en general. Los envolventes resuelven lo que Fisher pedía, las interacciones, pero el espacio es 2 elevado a n; con 16.063 genes es intratable, y eso está en la tarjeta. La flecha de abajo es la decisión de la tesis: se recurre a una heurística de búsqueda, y los algoritmos genéticos son una de las más usadas para esta tarea (Vignolo y Gerard, 2017).

### 5. Algoritmos genéticos y escasez muestral

**Visible.** **(nuevo SVG)** Dos paisajes de aptitud, uno al lado del otro; eje horizontal "subconjuntos de características", eje vertical "aptitud". En cada panel, dos poblaciones del AG: la inicial, puntos vacíos repartidos al azar por toda la curva, y la final, puntos llenos agrupados (leyenda: "población inicial · población final"). Izquierda, "Datos suficientes": una curva suave con la zona alta marcada con un círculo ("solución satisfactoria"); la población final se concentra ahí ("la búsqueda alcanza una solución satisfactoria"). Derecha, "Datos escasos": la misma curva real en gris punteado y, encima, la aptitud estimada, irregular, con máximos espurios; la población final se concentra sobre uno de ellos ("se detiene en una solución que solo parece satisfactoria"), lejos de la solución satisfactoria real, marcada con el círculo. Debajo: "La escasez de datos no limita al algoritmo de búsqueda, sino a la estimación de aptitud que lo guía."

**Notas.** Este es el punto de partida del aporte. La selección es el paso crítico del AG y depende de la aptitud que calcula un clasificador. Con datos insuficientes esa estimación es ruidosa, aumenta la incertidumbre en la selección y el algoritmo puede converger prematuramente o sobreajustarse a la muestra. El problema no está en el algoritmo sino en la calidad de la evaluación. Cuidado con el lenguaje: el AG es una heurística, no busca el óptimo sino soluciones satisfactorias (capítulo 1); el eje horizontal es una abstracción del espacio de 2ⁿ subconjuntos. Lo que el gráfico muestra es la relación entre aptitud estimada y real, no la geometría del espacio. El paisaje de aptitud es la metáfora clásica del campo (Wright 1932; Goldberg la usa). No hay una trayectoria: el AG mantiene una población, y la selección la concentra generación a generación en las zonas de aptitud alta; por eso se dibujan dos poblaciones, no un camino.

### 6. Técnicas de aumentación de datos

**Visible.** Izquierda, árbol con la taxonomía del capítulo 1: Aumentación de datos → Muestreo (sobremuestreo aleatorio, que replica observaciones; SMOTE, que interpola entre vecinos cercanos) y Modelos generativos (GAN, autocodificador variacional, modelos de difusión marcados como no abordados). Derecha, tabla de tres filas, SMOTE / GAN / AV, con dos columnas: mecanismo en una frase y comportamiento con n ≫ m, con la cita que respalda cada celda (Blagus y Lusa 2013; Fajardo et al. 2021; Ai et al. 2023). Cierre: en las comparaciones directas el AV condicional fue el mejor generador frente a SMOTE y GAN; antecedentes en respaldo (R6).

**Notas.** Tres técnicas, tres mecanismos. El submuestreo del capítulo 1 no está en el árbol porque elimina instancias de la clase mayoritaria: es un remedio para el desbalance, no una técnica de aumentación. SMOTE no es un modelo: crea un punto sobre el segmento entre una observación minoritaria y uno de sus vecinos; solo rebalancea, y en alta dimensión con pocas muestras las distancias se concentran y el vecino más cercano deja de significar algo (Blagus y Lusa: sin beneficio salvo selección previa; es el escenario de Leukemia, GCM y ALL). La GAN es un juego entre generador y discriminador: muestras nítidas, pero entrenamiento inestable, colapso de modos (fatal con 14 clases) y sin codificador, así que no hay paso codificar-decodificar. El AV es un modelo probabilístico explícito, estable, con latente continuo y codificador. Fajardo comparó los cuatro y el AV condicional ganó; Ai confirmó que los AV guiados superan a otros sobremuestreos. Si preguntan por modelos de difusión: son el estándar actual en imágenes, costosos, y sin antecedentes en datos tabulares con n ≫ m cuando se diseñó la tesis; quedan como trabajo futuro. Los AV se han aplicado a imágenes, texto, habla, música, datos tabulares, longitudinales y grafos (capítulo 1). Antecedentes detallados en R6; SMOTE en R2.

### 7. Propuesta: generación de muestras sintéticas mediante AV y selección de características con AG sobre los datos aumentados

**Visible.** Figura `AV-AG.png` (Figura 4.5) o versión simplificada **(nuevo SVG)**: datos originales → AV entrenado → N muestras sintéticas → datos aumentados (originales + sintéticos) → AG con clasificador MLP → subconjunto de características → evaluación en la partición original de testeo.

**Notas.** El flujo completo en una imagen. Tres cosas a decir: el AV se entrena solo con la partición de entrenamiento; el AG recibe originales más sintéticos; la exactitud se mide siempre en la partición original de testeo, sin datos sintéticos. Los tres beneficios esperados: más muestras, rebalanceo de clases minoritarias y atenuación del ruido por el paso codificar-decodificar.

### 8. Objetivo general y objetivos específicos

**Visible.** Objetivo general: *evaluar el impacto de la aumentación de datos mediante AV sobre el desempeño de estrategias de selección de características basadas en AG.* Objetivos específicos:
1. Integrar estrategias de aumentación basadas en AV en los AG.
2. Evaluar el desempeño de las estrategias propuestas en conjuntos de datos de diferente complejidad.
3. Comparar el AG con datos aumentados frente al mismo AG sin aumentación.

Tercer bloque, con el mismo formato que los dos anteriores, "Hipótesis": *aumentar sintéticamente las muestras permite al AG identificar subconjuntos más relevantes, con mejor exactitud y eficiencia de selección.* Sin línea de cierre.

**Notas.** Tal como figuran en el capítulo 1. Subrayar el tercer objetivo: la comparación central es con y sin aumentación, con el mismo algoritmo y los mismos parámetros. No es una carrera contra el estado del arte. Decirlo acá evita malentendidos en resultados.

---

## 2. Marco teórico

### 9. Organización (sección 2 resaltada)

**Notas.** Pasar en segundos: "Marco teórico: el autocodificador variacional, el algoritmo genético y las métricas."

### 10. Autocodificadores y el problema de la generación de datos

**Visible.** Izquierda, esquema del autocodificador: x → Codificador C_θ → z (espacio latente) → Decodificador D_φ → x̂. Derecha, el espacio latente como una recta con dos grupos de puntos codificados y, entre ellos, una región sin datos de entrenamiento marcada con línea punteada. Ejemplo con dígitos (MNIST): sobre cada grupo, el dígito que decodifica ese punto, un 7 y un 3 legibles; desde el punto vacío del medio, una flecha hacia una mancha sin forma, con el rótulo "la salida no guarda relación con los datos". Debajo, la pérdida en una línea: L(θ, φ) = Σ ‖xᵢ − D_φ(C_θ(xᵢ))‖².

**Notas.** Codificador C_θ y decodificador D_φ, entrenados juntos minimizando el cuadrado de la distancia euclídea. No hay nada que obligue a que puntos cercanos en la entrada queden cercanos en el latente. Quedan regiones del espacio latente que nunca se usaron en el entrenamiento, y muestrear ahí produce salidas sin relación con los datos. Por eso un autocodificador clásico no sirve como generador. Sobre el ejemplo: los dos dígitos son imágenes reales de MNIST; la mancha del medio es una ilustración de lo que devuelve un decodificador en una región que nunca vio, no la salida de un modelo entrenado. Decirlo así si preguntan.

### 11. Autocodificadores variacionales

**Visible.** Figura 3.3 redibujada: codificador → μ y σ → z = μ + σ·ε → decodificador → x̂; junto a la flecha de ε, "ruido gaussiano estándar"; bajo la caja, "reparametrización" y "μ y σ definen la distribución; ε elige el punto". Debajo del esquema, en el cuerpo, la función de pérdida con sus dos términos rotulados: L(θ, φ) = Σᵢ ‖xᵢ − D_θ(zᵢ)‖² (reconstrucción) + KL(q_φ(z|xᵢ) ‖ N(0, I)) (regularización). Bajo la fórmula, una fila: "Espacio latente continuo: los puntos intermedios entre dos codificaciones decodifican dígitos válidos (AV de latente 2-D entrenado sobre MNIST)" y, a la derecha, una tira de doce dígitos decodificados a lo largo de una recta del espacio latente, donde el 1 se transforma gradualmente en 7 y después en 9. Es el contrapunto de la mancha de la filmina 10. "KL: divergencia de Kullback-Leibler" va en el rótulo del término de regularización. Sin línea de cierre: la codificación como distribución y la generación (z ∼ N(0, I) y decodificar) se dicen, no se escriben.

**Notas.** La codificación deja de ser determinística. El vector de medias fija el centro y el de desvíos el área alrededor. La reparametrización es lo que permite retropropagar a través del muestreo. Para generar muestras nuevas basta tomar z de la normal estándar y pasar por el decodificador. Esa es la propiedad que la tesis explota. La función de pérdida va en esta misma diapositiva, como en la del autocodificador: el error de reconstrucción más la divergencia KL entre la distribución codificada y la normal estándar; el segundo término es el que ordena el espacio latente. KL es la divergencia de Kullback-Leibler ("Kúlbac-Láibler"): un número mayor o igual que cero que mide cuánto se aparta una distribución de otra; vale cero solo si son iguales. No es simétrica, por eso las dos barras separan los argumentos en orden: la distribución codificada q_φ(z|x) respecto de la normal estándar. Para dos normales tiene forma cerrada, ½ Σⱼ (μⱼ² + σⱼ² − 1 − log σⱼ²): penaliza que el centro se aleje de cero y que la dispersión se aparte de uno. La D de D_θ es el decodificador; la KL no lleva D para no confundir. El origen de la pérdida (el negativo del límite inferior de evidencia, ELBO) no se menciona; está en el respaldo R7, solo si preguntan. Sobre la tira de dígitos: es la salida real de un AV pequeño (latente de 2 dimensiones, una capa oculta de 256, 60 épocas sobre 5.000 imágenes de MNIST) entrenado para esta figura; las doce imágenes son decodificaciones de puntos equiespaciados sobre una recta del latente. Por eso se ven borrosas: con dos dimensiones latentes el modelo no puede más. Señalar el contraste con la 10: ahí un punto fuera de los datos daba una mancha; acá cualquier punto intermedio da un dígito.

### 12. Autocodificador variacional condicional

**Visible.** **(nuevo SVG)** Esquema del AVC: [x, y] entra al codificador; [z, y] entra al decodificador. Tres ítems: etiqueta concatenada en ambas redes; pesos de clase inversos a la frecuencia en la reconstrucción (los errores en las clases minoritarias pesan más); muestreo ponderado en cada mini-lote (las clases minoritarias entran con mayor probabilidad).

**Notas.** Para GCM, con 14 clases desbalanceadas, y ALL Leukemia, con 7 (la tesis dice 14 por una errata; el archivo y el experimento usan 7). Sin condicionamiento, el generador favorece las clases mayoritarias: la pérdida la dominan las clases numerosas y el AVC reconstruye mal justo las que después hay que generar. Dos mecanismos contra el desbalance. El muestreo ponderado arma cada lote con probabilidad proporcional a 1/n_c, así las observaciones de las clases chicas entran más veces y su error pesa más en la suma; es el que efectivamente balancea la contribución de cada clase a la pérdida. Los pesos de clase, w_c proporcional a 1/n_c, entran como factor sobre el término de reconstrucción. Se validaron juntos: separados o solos no dieron el mejor resultado, combinados sí. No decir "cada observación se pondera por su clase dentro del MSE": el código no lo hace así (ver apuntes 19). Esto permite generar cantidades iguales por clase, que es lo que se hace en la segunda etapa de GCM.

### 13. Algoritmos genéticos

**Visible.** Sobre el ciclo, una tira de bits rotulada "Individuo · solución candidata: un subconjunto de variables codificado como una cadena de bits": celdas x₁ … xₙ con los 1 resaltados en azul; leyenda "1: la variable forma parte del subconjunto · 0: queda fuera · n bits, uno por variable (7.129 en Leukemia)"; una flecha baja desde la tira al cuadro "Población inicial aleatoria" con el rótulo "× 100, generados al azar". Debajo, el ciclo de la Figura 4.1. Cuatro propiedades de Goldberg en una columna: opera sobre una codificación, evalúa una población, usa una función de aptitud sin derivadas, transiciones probabilísticas.

**Notas.** Un individuo es una solución candidata al problema de selección, un subconjunto de variables; no es una observación. Las observaciones intervienen solo al evaluar la aptitud. Población inicial aleatoria, evaluación por aptitud, selección, cruce, mutación, hasta un criterio de terminación. Las cuatro propiedades explican por qué sirven donde otros métodos no: espacios discretos, no diferenciables, multimodales. La diversidad de la población es lo que evita la convergencia prematura.

### 14. Codificación del cromosoma y operadores genéticos

**Visible.** Figura `codificacion-decodificacion.png` (Figura 4.2, corregida): genotipo 1100101 → fenotipo [X1, X2, X5, X7]. Al lado, pequeños esquemas de cruce (`ag_cruce.png`) y mutación (`ag_mutacion.png`). Debajo, una franja "Selección: quién se reproduce" con las tres estrategias del capítulo 4 en columnas: ruleta (probabilidad proporcional a la aptitud; favorece a los más aptos y reduce la diversidad), torneo, marcada como la empleada en la tesis (se sortean k individuos y pasa el mejor; el tamaño del torneo regula la presión de selección) y ventana (grupos; el mejor de cada uno; preserva la diversidad).

**Notas.** Codificación binaria de largo igual al número de variables: 7.129 bits en Leukemia, 16.063 en GCM. El fenotipo es el subconjunto que entrena al clasificador. Selección por torneo (torneos de 5 individuos en la implementación): equilibra explotación y exploración, porque el más apto gana su torneo pero cualquier individuo puede caer en un torneo flojo y pasar; la ruleta explota más rápido y pierde diversidad; la ventana explora más. Cruce de dos puntos y mutación por inversión de bits. La proporción de bits activos en la inicialización define el tamaño del subconjunto que explora el AG, y es un parámetro crítico que aparece en todos los experimentos.

### 15. Criterios de evaluación de la selección de características

**Visible.** Tres filas con rótulo y definición:
- **Desempeño predictivo**: exactitud en la partición original de testeo del subconjunto encontrado (exactitud balanceada en multiclase dentro de la aptitud).
- **Reducción de variables**: número medio de características seleccionadas en la población final.
- **Estabilidad**: dispersión de la exactitud y del número de variables entre corridas independientes (desviación estándar y rango intercuartílico).
Una línea al pie: *los tres criterios no varían conjuntamente; se reportan por separado.*

**Notas.** Responde a la observación de la Dra. Chan sobre qué se entiende por mejora. Decirlo como definición operativa del capítulo 4, no como respuesta. Para validar el generador en sí, antes del AG, se usa además la prueba de Fajardo: un MLP entrenado solo con sintéticos y evaluado en reales, contra un MLP entrenado con reales. En el capítulo 2 las métricas de línea base son AUC y macro-F1, que no se comparan directamente con la exactitud del AG.

---

## 3. Materiales y métodos

### 16. Organización (sección 3 resaltada)

**Notas.** "Materiales y métodos: los datos, la línea base, los modelos y el diseño experimental."

### 17. Conjuntos de datos

**Visible.** Tabla:

| Conjunto | Tema | Observaciones × características | Clases | Desafío principal |
| --- | --- | --- | --- | --- |
| Leukemia | Expresión génica; ALL frente a AML | 72 × 7.129 | 2, desbalanceado | n ≫ m, correlación entre genes |
| Gisette | Dígitos manuscritos; 4 frente a 9 | 13.500 × 5.000 | 2, balanceado | ruido y redundancia, espacio grande |
| Madelon | Artificial; XOR en 5 dimensiones | 2.000 × 500 | 2, balanceado | 20 variables con señal, 480 de ruido |
| GCM | Expresión génica; 14 tipos de tumor | 190 × 16.063 | 14, desbalanceado | n ≫ m, multiclase, desbalance |
| ALL Leukemia | Expresión génica; LLA pediátrica | 327 × 12.600 | 7, desbalanceado | n ≫ m, multiclase; validación |

Pie en una sola línea: referencias (Golub 1999, Ramaswamy 2001, Yeoh 2002; Gisette y Madelon, NIPS 2003) y, en negrita, "En todos los experimentos se respetan las particiones originales de entrenamiento y testeo".

**Notas.** Leukemia es Golub 1999, ALL y AML. GCM es Ramaswamy 2001, 14 tipos de tumor. ALL Leukemia es Yeoh 2002 y entró al final para validar el flujo de GCM; por eso no está en la línea base. Madelon es artificial: 5 relevantes, 15 combinaciones lineales y 480 aleatorias, un XOR multidimensional. Gisette distingue los dígitos 4 y 9 con sondas sin poder predictivo. Las particiones originales de entrenamiento y testeo se respetan en todos los experimentos con AV y AG.

### 18. Línea base: modelos clásicos sobre el espacio completo de características

**Visible.** Tabla reducida de la Tabla 2.1: por conjunto, métrica, mejor modelo y el rango donde cae la mayoría de los 18 modelos.

| Conjunto | Métrica | Mejor | Rango de la mayoría | Lectura |
| --- | --- | --- | --- | --- |
| Leukemia | AUC | 1,00 (Bagging, RF, SVC) | 0,85 a 1,00 | cerca de saturar |
| Gisette | AUC | 1,00 (Gradient Boosting) | 0,92 a 0,99 | cerca de saturar |
| Madelon | AUC | 0,91 (Bagging) | 0,57 a 0,70 | margen amplio |
| GCM | macro-F1 | 0,71 (SGD), 0,68 (MLP) | 0,48 a 0,62 | margen amplio; clases con F1 nulo |

**Notas.** Dieciocho modelos de scikit-learn con búsqueda en grilla, sobre una partición 80/20 propia. Dos lecturas: Leukemia y Gisette casi no tienen margen; Madelon y GCM sí. En GCM, clases como Breast o Prostate tienen F1 cero: el modelo nunca las predice. Esa es la asimetría que la aumentación por clase intenta corregir. Aclarar si preguntan: estas métricas son AUC y F1 sobre otra partición, así que no se comparan directamente con la exactitud del AG; la comparación válida está en respaldo.

### 19. Arquitectura e hiperparámetros de AV y AVC

**Visible.** Izquierda: arquitectura en tres líneas (codificador: 3 capas lineales + BatchNorm + ReLU; μ y log σ² por capas lineales independientes; decodificador simétrico). Derecha: Tabla 4.1 compactada:

| Conjunto | Modelo | Entrada (capa 1) | Capas 2 y 3 | Latente | Tasa de aprendizaje | Épocas |
| --- | --- | --- | --- | --- | --- | --- |
| Leukemia | AV | 7.129 | 346, 178 | 108 | 2,7·10⁻⁴ | 2.889 |
| Madelon | AV | 500 | 835, 308 | 25 | 1,6·10⁻⁴ | 1.364 |
| Gisette | AV | 5.000 | 3.870, 2.987 | 18 | 9,5·10⁻⁴ | 2.739 |
| GCM | AVC | 16.063 | 358, 189 | 35 | 6,9·10⁻⁴ | 3.613 |
| ALL Leukemia | AVC | 12.600 | 434, 176 | 35 | 4,0·10⁻⁴ | 949 |

La columna de entrada da la dimensión de partida y permite leer la compresión hasta el latente (Leukemia: 7.129 a 108, unas 66 veces; GCM: 16.063 a 35, unas 460 veces).

**Notas.** Se partió de dos capas, se vio baja calidad de reconstrucción y se pasó a tres con normalización por lotes. Pérdida: MSE más KL; MSE balanceado por clase en multiclase. Optimizador Adam, parada temprana con paciencia de 10 épocas. Hiperparámetros por búsqueda en grilla y optimización bayesiana: capas 2 y 3 entre 50 y 5.000 neuronas, latente entre 10 y 300 (hasta 1.000 en AVC), tasa entre 10⁻⁵ y 10⁻². Normalización estándar de entrada. Dropout y pérdida L1 se probaron y no aportaron.

### 20. Función de aptitud del algoritmo genético

**Visible.** Fórmula grande: f = α · acc + (1 − α) · (1 − k/n), con α = 0,5, k variables seleccionadas, n totales. Debajo, la configuración común en ítems: población de individuos binarios; selección por torneo; cruce de dos puntos (p = 0,75); mutación por inversión de bits (probabilidad por conjunto, entre 0,0002 y 0,1); 15 a 30 generaciones; evaluador MLP; biblioteca DEAP.

**Notas.** Por diseño el AG sacrifica algo de exactitud a cambio de dimensionalidad. Ejemplo: 100% de exactitud con todas las variables da f = 0,5; 80% con el 20% de las variables da f = 0,8. Esto hay que tenerlo presente cuando se compara con trabajos que usan todos los genes. La proporción de genes activos al inicio se ajustó por conjunto: 10% en la mayoría, hasta 0,3% en los experimentos de reducción agresiva de GCM y ALL.

### 21. Diseño experimental

**Visible.** Figura `diseño_experimentos.png` (Figura 4.6). Tres líneas: mismos parámetros del AG en ambos grupos; cada corrida completa del AG es una observación; comparación de distribuciones entre grupos con gráficos de cajas, test t de Welch y Mann-Whitney.

**Notas.** Cada punto en los gráficos que siguen es una corrida completa del AG, y el valor es la exactitud media de la población final en la partición original de testeo. Se comparan distribuciones de corridas con aumentación contra corridas sin aumentación. Los valores p se calculan con las corridas como n. Esto corrige un test de la tesis que había usado la cantidad de observaciones del conjunto; con el n correcto la conclusión no cambia. Decirlo acá, antes de que lo pregunten.

### 22. Flujo en tres etapas para problemas multiclase

**Visible.** El mismo diagrama del diseño experimental de la 21 (dos filas, sin y con aumentación, evaluación en la partición original de testeo), más un elemento nuevo en verde debajo de la fila con aumentación: "Selección previa sobre el espacio completo / subespacio: características más frecuentes en experimentos previos", con una flecha hacia arriba que toca la flecha entre "Datos originales" y "AV / AVC". Lectura: entre el paso 1 y el 2 intervino una selección; no es una corrida nueva del AG sino la consolidación de los cromosomas de experimentos previos (en GCM, 590 cromosomas), de los que se toman las características más frecuentes. Las tres etapas son selección previa (verde), generación (AVC) y selección final (AG). Debajo, tabla: en GCM, 1.600 características de 590 cromosomas y 3.000 muestras balanceadas por clase; en ALL Leukemia, subespacio de 3 corridas y 1.000 muestras. Línea: ejecución en la nube, 8 vCPU y 30 GB.

**Notas.** Presentarlo como parte del método, aunque nació de un resultado: la primera etapa de GCM falló y el diagnóstico llevó a este flujo. La hipótesis de trabajo: si el AVC no puede aprender la distribución de 16.063 variables con 133 muestras, que aprenda la de 1.600. Los detalles del fracaso y del diagnóstico se cuentan en resultados.

---

## 4. Resultados

### 23. Organización (sección 4 resaltada)

**Notas.** "Resultados en tres partes: primero la calidad de los datos sintéticos, después los resultados globales de la integración, y recién después cada conjunto."

### 24. Un MLP entrenado únicamente con datos sintéticos alcanza la exactitud del entrenado con datos reales en tres de los cuatro conjuntos

**Visible.** Figura 3.4 redibujada con los mismos valores. Línea de lectura: exactitud en la partición original de testeo; gris entrenado con reales, azul entrenado con sintéticos.

**Notas.** La prueba de Fajardo. Leukemia: 0,95 con sintéticos contra 0,81 con reales; el recall de la clase minoritaria sube de 0,56 a 0,89. Madelon: 0,57 contra 0,55. GCM: 0,54 en ambos, con patrones distintos por clase. Gisette: 0,95 contra 0,97, dos puntos abajo. Conclusión del capítulo 3: el AV captura la estructura de los datos lo suficiente como para que valga la pena aumentar. No es todavía el resultado de la tesis; es la condición previa.

### 25. La cantidad de muestras sintéticas presenta un umbral: en GCM, superarlo degrada la exactitud

**Visible.** Figura `n_samples_accuracy_comparison.png` (Figura 3.5): exactitud del MLP con 190, 400, 3.000 y 6.000 muestras sintéticas. Dos líneas al pie: con 3.000 muestras balanceadas (214 por clase) se iguala al MLP con reales; con 6.000 se degrada. Un espacio latente de 35 superó a configuraciones de más de 50.

**Notas.** Dos hallazgos del capítulo 3 que condicionan todo. Primero, el umbral: pasado cierto punto los sintéticos sobreajustan al generador. Segundo, contra la intuición de "más dimensión latente es mejor" (Boom 2021), un latente compacto generalizó mejor, en línea con Ai 2023. Las arquitecturas simples, de tres capas, rindieron igual o mejor que las de cuatro. Estas dos cosas se calibran por problema; es una limitación.

### 26. Resultados globales: la aumentación mejoró significativamente la exactitud en dos de los cinco conjuntos y no la modificó en los otros tres

**Visible.** Tabla global:

| Conjunto | Corridas (aum. / orig.) | Exactitud orig. | Exactitud aum. | Diferencia (pp) | p | Lectura |
| --- | --- | --- | --- | --- | --- | --- |
| Leukemia | 90 / 90 | 0,989 | 0,992 | +0,3 | 0,09 | saturado, sin cambio |
| Gisette | 13 / 12 | 0,959 | 0,960 | +0,1 | 0,63 | saturado, sin cambio |
| Madelon | 30 / 49 | 0,750 | 0,828 | +7,8 | < 0,001 | mejora significativa |
| GCM, 2.ª etapa | 9 / 10 | 0,497 | 0,541 | +4,4 | 0,005 | mejora significativa |
| ALL Leukemia | 18 / 18 | 0,669 | 0,672 | +0,3 | 0,87 | sin cambio |

**Notas.** La vista global primero, como pidió el Dr. Quiroga. Dos resultados significativos: Madelon y la segunda etapa de GCM. En los otros tres la exactitud no cambia de forma significativa, y lo digo de entrada para no sobrevender. Los porcentajes relativos de la tesis, 10,4% en Madelon y 8,85% en GCM, son 7,8 y 4,4 puntos porcentuales. Test de Welch con las corridas como n; Mann-Whitney da la misma conclusión en todos los casos.

### 27. Los intervalos de confianza del 95% excluyen el cero únicamente en Madelon y GCM

**Visible.** Figura `diferencia_exactitud_ic95.png`. Línea de lectura: diferencia aumentados menos originales en puntos porcentuales, con intervalo de confianza del 95%; donde la barra cruza el cero no hay evidencia de efecto.

**Notas.** Este gráfico resume la tesis. La versión actual del PNG calcula GCM con toda la segunda etapa (18 contra 25 corridas, +4,0 puntos); para que coincida con la tabla anterior se regenera con las 9 contra 10 corridas de ~450 y ~750 genes (+4,4, IC 1,6 a 7,3). Madelon y GCM claramente por encima de cero. Leukemia y Gisette tocan el cero con intervalos cortísimos: no hay nada que mejorar. ALL Leukemia tiene un intervalo ancho: pocas corridas y mucha variabilidad. El de GCM también es ancho: 9 y 10 corridas con un test de 57 muestras, donde cada muestra mal clasificada mueve la exactitud 1,75 puntos.

### 28. Con escala común, la diferencia solo es apreciable en los conjuntos con margen de mejora

**Visible.** Figura `boxplot_resultados_precision_escala_unificada.png`, eje común de 0,4 a 1,0. Dos frases debajo: "Problema saturado: sin cambio." "Margen de mejora y reconstrucción adecuada: mejora."

**Notas.** La escala común que pidió el jurado. Los paneles separados de la tesis agrandaban diferencias de milésimas en Leukemia y Gisette; acá las cajas se superponen por completo. La regla tiene dos condiciones, y la segunda, que el AV reconstruya bien, es la que falló en la primera etapa de GCM. Lo que sigue son los dos casos que explican la regla, y después la validación.

### 29. Madelon: la aumentación incrementa la exactitud en 7,8 puntos porcentuales y reduce el número de variables seleccionadas

**Visible.** Figura `boxplot_madelon_combined.png` (exactitud y número de variables). Dos números grandes: "+7,8 puntos (0,750 → 0,828, p < 0,001)" y "29 variables en lugar de 36".

**Notas.** El resultado más limpio. Configuración: 2.000 muestras sintéticas, mutación 0,002, cruce 0,75, 30 generaciones. La exactitud sube de 0,750 a 0,828 y la dispersión baja (desviación 0,023 contra 0,038). Además el subconjunto es más chico. La tesis señala que solo 2 de los 18 clásicos del capítulo 2, AdaBoost y Bagging, superan este nivel, y con las 500 variables; decirlo con la salvedad de que el capítulo 2 reporta AUC sobre otra partición, así que es una referencia de orden de magnitud, no una comparación directa.

### 30. Interpretación del caso Madelon: un espacio latente compacto preserva las 20 variables informativas y atenúa las 480 de ruido

**Visible.** **(nuevo SVG)** Esquema: 500 variables (20 con señal, 480 ruido) → latente de 25 dimensiones → 500 variables reconstruidas, con el ruido atenuado. Una línea: *los sintéticos realzan la señal que el AG necesita encontrar.*

**Notas.** La interpretación de la tesis. El AV reconstruye desde un latente de 25 dimensiones: no puede memorizar 480 variables aleatorias, así que las reconstruye cerca de su media, y conserva la estructura de las 20 informativas. Al AG le llega un conjunto donde la señal pesa más. Es consistente con la dificultad vista en la línea base, donde la mayoría de los clásicos sin selección quedaba lejos de saturar.

### 31. GCM, primera etapa: con el AVC entrenado sobre las 16.063 variables, la aumentación no mejoró la exactitud

**Visible.** Figura `boxplot_gcm_combined_part1.png` (Figura 4.10). Número: "0,512 con aumentación contra 0,538 sin aumentación". Configuración en una línea: 1.400 sintéticas (100 por clase) más 133 originales; cromosomas de ~1.600 genes; 20 generaciones.

**Notas.** Cuento el fracaso porque explica el aporte. Se esperaba resultado mixto por la calidad de reconstrucción vista en el capítulo 3 y el desbalance. La exactitud bajó levemente y la dispersión fue similar. Antes se habían probado cromosomas del 20% y 30% de las variables con exactitud entre 0,2 y 0,35, por eso se fijó el 10%.

### 32. Diagnóstico: el clasificador ajusta por completo la distribución sintética, pero no generaliza a la distribución real

**Visible.** Dos números grandes: "100% de exactitud en la partición sintética de testeo" y "50% en la partición real de testeo" (Tabla 4.4, MLP entrenado con 3.000 sintéticos). Debajo: *la distribución sintética es internamente consistente y de menor complejidad que la real: permite igualar al MLP entrenado con datos reales, no superarlo ni guiar mejor al AG.* Una línea más: *explicación plausible, colapso de la distribución posterior: la divergencia KL domina la pérdida y la reconstrucción deja de representar los datos reales.*

**Notas.** Conectar con la diapositiva 24: allí el MLP con sintéticos igualaba al MLP con reales en GCM (0,54 contra 0,54), y acá se ve por qué no lo supera. El modelo aprende los sintéticos a la perfección, pero en los reales queda en el mismo nivel que sin aumentación. La primera etapa del AG había usado 1.400 sintéticos; el diagnóstico se hizo con 3.000 y da el mismo cuadro. La explicación plausible es el colapso de la posterior, que en el marco teórico quedó plantado: la KL domina en un problema con relaciones complejas. Dos salidas: reponderar la KL contra la reconstrucción, o reducir el problema antes de generar. Se tomó la segunda; la primera queda como trabajo futuro.

### 33. GCM, segunda etapa: con el flujo selección-generación-selección, la aumentación incrementa la exactitud en 4,4 puntos porcentuales

**Visible.** Solo el panel izquierdo (exactitud) de `boxplot_gcm_combined.png` (Figura 4.11). Números: "+4,4 puntos (0,497 → 0,541, p = 0,005; 9 y 10 corridas)". Línea: número de variables sin cambio dentro de cada tamaño de cromosoma (454 contra 462; 785 contra 781).

**Notas.** El panel derecho de la figura de la tesis no se proyecta: mezcla corridas de ~450 y ~750 genes en proporciones distintas por grupo y sugiere una reducción de variables que no existe; por eso el número de variables va como texto, comparado dentro de cada tamaño. Con el AVC entrenado en las 1.600 características más frecuentes, pesos de clase y muestreo ponderado, 3.000 muestras balanceadas, cromosomas de ~450 y ~750, 15 generaciones. La mejora es de exactitud, no de reducción de variables. La dispersión aumenta (desviación 0,033 contra 0,022 en estas 9 y 10 corridas), y lo digo antes de que lo pregunten: pocas corridas y un test de 57 muestras. Tomando toda la etapa, 18 contra 25 corridas, p = 0,008 y desviación 0,052 contra 0,036. Con 6.000 muestras el resultado se degradó, coherente con el umbral del capítulo 3.

### 34. GCM con reducción progresiva del cromosoma: la exactitud se mantiene hasta ~45 genes y la media con aumentación es superior en los cuatro tamaños

**Visible.** Figura `boxplot_gcm_ngenes_accuracy.png` (Figura 4.12), redibujada con los mismos datos y rótulos limpios. Tabla mínima, medias de corridas (aum. / orig.):

| Genes activos | Corridas | Exactitud orig. | Exactitud aum. | p |
| --- | --- | --- | --- | --- |
| ~45 | 4 / 10 | 0,432 | 0,443 | 0,43 |
| ~200 | 5 / 5 | 0,476 | 0,498 | 0,38 |
| ~450 | 5 / 5 | 0,489 | 0,538 | 0,035 |
| ~750 | 4 / 5 | 0,505 | 0,545 | 0,10 |

**Notas.** Experimentos de validación interna con reducción agresiva. Pese a pasar de 16.063 a 45 genes la exactitud queda en un nivel aceptable. En media los aumentados quedan arriba en los cuatro grupos; en ~200 la mediana queda apenas por debajo, que es lo que muestra la figura y lo que dice la tesis. Solo ~450 alcanza significación por sí solo, con 5 y 5 corridas. Decirlo como tendencia, no como confirmación.

### 35. ALL Leukemia valida el flujo en un segundo problema multiclase: tendencia favorable, sin significación estadística

**Visible.** Figura `boxplot_all_leukemia_ngenes_accuracy.png` (Figura 4.13). Tabla mínima: ~35 genes 0,608 → 0,625; ~180 0,654 → 0,663; ~300 0,754 → 0,735; ningún p menor a 0,4.

**Notas.** Mismo flujo: AVC sobre un subespacio de 3 corridas, 1.000 sintéticas, 15 generaciones. Con 35 y 180 genes la aumentación queda por encima, con 300 por debajo, y ninguna diferencia es significativa con 5 a 8 corridas por grupo. Lo digo moderado, como pide la Dra. Chan: el flujo es viable en un segundo problema y la tendencia acompaña, pero no es una confirmación estadística. Sí hay menor dispersión con aumentación: desviación 0,056 contra 0,065. En 35 genes la mutación de 0,028 explica parte de la variabilidad.

### 36. En los conjuntos saturados la aumentación no modifica la exactitud, pero reduce la dispersión entre corridas

**Visible.** Figuras `boxplot_leukemia_combined.png` y `boxplot_gisette_combined.png` lado a lado, reducidas. Dos líneas: Leukemia, desviación 0,011 contra 0,016; 6.779 y 6.772 genes seleccionados al menos una vez. Gisette, 424 contra 437 variables, rango intercuartílico 8 contra 21.

**Notas.** Rápido, porque ya se vio en la tabla global. En Leukemia el 10% de los genes alcanza para clasificar casi sin importar cuáles: 80.742 pares de genes con correlación mayor a 0,7. No hay qué mejorar. En Gisette lo que cambia es la estabilidad del número de variables y un subconjunto algo más chico.

### 37. Evaluación por criterio: desempeño predictivo, reducción de variables y estabilidad en cada conjunto

**Visible.** Tabla de la respuesta (e):

| Conjunto | Desempeño predictivo | Reducción de variables | Estabilidad de la exactitud |
| --- | --- | --- | --- |
| Leukemia | sin diferencia (p = 0,09) | igual (259 vs 259) | mejora (0,011 vs 0,016) |
| Gisette | sin diferencia (p = 0,63) | mejora (424 vs 437) | mejora leve (0,003 vs 0,004) |
| Madelon | mejora (p < 0,001) | mejora (29 vs 36) | mejora (0,023 vs 0,038) |
| GCM | mejora (p = 0,005) | igual (454 vs 462; 785 vs 781) | empeora (0,033 vs 0,022) |
| ALL Leukemia | sin diferencia (p = 0,87) | igual (174 vs 173) | mejora leve (0,056 vs 0,065) |

**Notas.** Esta tabla responde con precisión a qué llamamos mejora, con los tres criterios del marco teórico. En los saturados lo único defendible es la estabilidad. En Gisette y Madelon además el subconjunto es más chico. En GCM gano exactitud y pierdo estabilidad; lo reconozco como está.

### 38. Síntesis: el efecto de la aumentación está condicionado por el margen de mejora y la calidad de la reconstrucción

**Visible.** Tres líneas:
- Mejora la exactitud donde existe margen de mejora y el AV reconstruye adecuadamente (Madelon, GCM en segunda etapa).
- No modifica la exactitud en problemas saturados (Leukemia, Gisette); aporta estabilidad.
- En problemas multiclase desbalanceados requiere generar sobre un subespacio seleccionado y calibrar la cantidad de muestras.

**Notas.** Cerrar la sección con la regla en tres líneas, que es lo que el jurado va a recordar. La tercera es el aporte metodológico propio. De aquí a conclusiones.

---

## 5. Conclusiones y trabajos futuros

### 39. Organización (sección 5 resaltada)

**Notas.** "Conclusiones, limitaciones y trabajos futuros."

### 40. Conclusiones

**Visible.** Cuatro ítems:
1. Los datos sintéticos generados por un AV/AVC adecuadamente configurado son aptos para el entrenamiento: un MLP entrenado únicamente con sintéticos alcanza la exactitud del entrenado con reales en Leukemia, Madelon y GCM.
2. La aumentación mejora la selección con AG cuando el problema tiene margen de mejora y el AV reconstruye adecuadamente: +7,8 puntos porcentuales en Madelon y +4,4 en GCM, ambos significativos.
3. En problemas saturados no modifica la exactitud; reduce la dispersión y, en algunos casos, el tamaño del subconjunto.
4. En problemas multiclase desbalanceados, el flujo selección-generación-selección es la condición para que la aumentación resulte útil; aplicar el AVC sobre el espacio completo la perjudicó.

**Notas.** En orden de solidez. La cuarta es el aporte metodológico propio. Añadir de palabra los dos hallazgos de configuración: existe un umbral de muestras sintéticas, y arquitecturas simples con latente moderado rinden igual o mejor que las grandes.

### 41. Limitaciones

**Visible.** Cinco ítems cortos:
1. Cinco conjuntos de datos, dos de ellos artificiales; el efecto depende de la dificultad del problema.
2. Número reducido de corridas en GCM y ALL Leukemia (5 a 10 por configuración) y particiones de testeo pequeñas.
3. El efecto depende de la calidad del AV: con una reconstrucción deficiente, la aumentación perjudica el resultado.
4. Existe un umbral de muestras sintéticas más allá del cual el resultado se degrada.
5. Un único clasificador en la función de aptitud (MLP) e hiperparámetros ajustados por conjunto, no transferibles sin reajuste.

**Notas.** Responde a la Dra. Chan sobre generalización. La primera y la tercera son las que acotan: la aumentación no es una receta universal. La segunda explica por qué ALL Leukemia no alcanza significación y por qué el intervalo de GCM es ancho. Agregar de palabra: no se corrió SMOTE dentro del mismo flujo, y es trabajo futuro inmediato.

### 42. Trabajos futuros

**Visible.** Cuatro ítems:
1. Función de pérdida del AV: reponderar reconstrucción y KL, inferencia variacional recocida; AV jerárquicos para datos como GCM.
2. Integración AV-AG: selección dinámica en varias etapas y optimización conjunta de ambos modelos.
3. Encadenamientos y ensambles de AV y AG para reducir varianza.
4. Comparación con SMOTE y otros generadores dentro del mismo flujo con AG.

**Notas.** Los tres primeros son los del capítulo 5. El cuarto se agrega por la sugerencia del Dr. Quiroga. Si hay que elegir uno, el primero: el colapso de la posterior en GCM sugiere que una pérdida con KL recocida podría evitar el flujo en tres etapas.

---

## Cierre

### 43. Agradecimientos y cierre

**Visible.** Título de la tesis, tesista, directores, repositorio del código. "Muchas gracias."

**Notas.** Diapositivas de respaldo a continuación: comparación con el estado del arte, por qué no SMOTE, test de significación en GCM, línea base completa, tablas por clase del capítulo 3.

---

## Respaldo

### R1. Comparación con el MLP sobre todas las variables: el flujo AV+AG iguala o supera su exactitud con entre el 0,6% y el 10% de las características

**Visible.** Tabla de la respuesta (a):

| Conjunto | MLP, todas las variables (cap. 3) | AG sin aumentación | AG con aumentación | Variables usadas |
| --- | --- | --- | --- | --- |
| Leukemia | 0,81 | 0,989 | 0,992 | 30 a 680 de 7.129 |
| Gisette | 0,97 | 0,959 | 0,960 | 437 y 424 de 5.000 |
| Madelon | 0,55 | 0,750 | 0,828 | 36 y 29 de 500 |
| GCM | 0,54 | 0,497 | 0,541 | 450 a 780 de 16.063 |
| ALL Leukemia | sin medición | 0,669 | 0,672 | 35 a 300 de 12.600 |

Debajo, referencias externas: GCM, Ramaswamy 2001, 78% con SVM uno contra todos sobre 16.063 genes. Madelon, NIPS 2003, error balanceado cercano a 0,07 de los ganadores. Leukemia, Golub 1999, 50 genes.

**Notas.** Si preguntan por el estado del arte: el objetivo era medir el impacto de la aumentación sobre el mismo algoritmo, no superar a Ramaswamy, que usa todos los genes. La aptitud penaliza el número de variables con peso 0,5, así que sacrifica exactitud por diseño. Confirmar la cifra de NIPS 2003 en Guyon et al. 2004 antes de la defensa.

### R2. Fundamento de la elección de autocodificadores variacionales frente a SMOTE

**Visible.** Tres referencias en tres líneas: Blagus y Lusa 2013 (SMOTE no beneficia en alta dimensión con pocas muestras); Fajardo et al. 2021 (AV condicional supera a SMOTE y GAN en MNIST desbalanceado); Ai et al. 2023 (AV guiados superan a otros sobremuestreos en tabulares e imágenes). Una línea: SMOTE rebalancea clases; la tesis aumenta también problemas balanceados.

**Notas.** La tesis no corrió SMOTE; se reconoce. La referencia más fuerte es Blagus y Lusa porque es justamente el escenario de los tres conjuntos genómicos.

### R3. Significación en GCM con las corridas reales como n

**Visible.** Tabla: 9 contra 10 corridas (~450 y ~750), +4,4 puntos, IC 95% de 1,6 a 7,3, Welch p = 0,005, Mann-Whitney p = 0,005; toda la segunda etapa, 18 contra 25, +4,0 puntos, IC de 1,1 a 7,0, Welch p = 0,008, Mann-Whitney p = 0,011. Desglose por tamaño de cromosoma: la tabla de la diapositiva 34.

**Notas.** Si preguntan por el test: el script de la tesis usó como n las observaciones de los conjuntos (3.133 y 133). Recalculado con las corridas, la diferencia sigue siendo significativa por dos tests.

### R4. Línea base completa: Tabla 2.1

**Visible.** Tabla 2.1 completa, 18 modelos por 4 conjuntos.

**Notas.** Solo si piden un modelo concreto. Recordar por qué algunos no se evaluaron en GCM y Gisette: dimensionalidad y multiclase.

### R5. Resultados por clase del MLP con datos reales y sintéticos

**Visible.** Tablas 3.1 (Leukemia) y 3.4 (GCM) compactadas: precisión, recall y F1 por clase.

**Notas.** Para la pregunta de qué pasa por clase en GCM: con sintéticos varias clases llegan a precisión 1,00 pero el recall cae; el modelo es más conservador. Las clases 7 y 3 se deterioran, la 12 duplica su F1.

### R6. Antecedentes: aumentación con AV y combinación de AV con AG

**Visible.** Tabla de cuatro filas (trabajo, qué hace, resultado y relación con la tesis): Fajardo et al. 2021 (AVC contra GAN, SMOTE y sobremuestreo aleatorio en MNIST desbalanceado; AVC mejor generador; origen de la prueba del capítulo 3); Ai et al. 2023 (MGVAE guiado por la clase mayoritaria; supera a otros sobremuestreos); Khmaissia y Frigui 2023 (AV entrenado con muestras de baja confianza; semisupervisado; STL10 y CIFAR-100); Martins et al. 2022 (AV y AG para diseño de proteínas luxA; el AG guiado supera al muestreo directo; el antecedente más cercano). Cierre: ningún antecedente combina AV y AG para selección de características.

**Notas.** Si preguntan por antecedentes de AV con AG: Martins 2022 es el más cercano, pero usa el AG para optimizar propiedades de proteínas generadas, no para seleccionar características, y no es aumentación de datos en sentido estricto. Los otros tres son aumentación con AV para clasificación; de Fajardo sale la prueba de validación del generador que usa el capítulo 3. Estos cuatro trabajos están resumidos en una sección del capítulo 3 que quedó comentada en el fuente de la tesis.

### R7. Origen de la función de pérdida: el límite inferior de evidencia

**Visible.** Cuatro pasos en filas, cada uno con rótulo, fórmula y explicación breve:
1. Objetivo, máxima verosimilitud: max_θ log p_θ(x). Elegir θ para que el modelo asigne la mayor probabilidad posible a las observaciones reales.
2. Impedimento, la integral sobre z: p_θ(x) = ∫ p_θ(x|z) p(z) dz. No se puede calcular: sin fórmula (el integrando contiene la red D_θ) ni aproximación numérica (z tiene decenas de dimensiones y casi ningún z del prior produce x). Lo que no se calcula no se diferencia.
3. Sustituto, límite inferior de evidencia (ELBO): log p_θ(x) ≥ E_{z∼q_φ(z|x)}[log p_θ(x|z)] − KL(q_φ(z|x) ‖ p(z)). Sí se puede calcular: un solo z sorteado del codificador q_φ(z|x), que propone z adecuados para esa x, y una KL entre normales con fórmula cerrada.
4. Alcance, una cota y no la verosimilitud: log p_θ(x) − ELBO = KL(q_φ(z|x) ‖ p_θ(z|x)). La brecha es el error del codificador respecto de la posterior verdadera; maximizar la cota eleva la verosimilitud y reduce la brecha, sin garantizar que llegue a cero.
Línea al pie: el logaritmo convierte el producto de las probabilidades de todas las observaciones en una suma, sin cambiar el máximo; la pérdida de la diapositiva 11 es el negativo de la cota, −ELBO = error cuadrático + KL.

**Notas.** Solo si preguntan de dónde sale la pérdida de la diapositiva 11. Recorrer los cuatro pasos en orden. Uno: entrenar es máxima verosimilitud. Dos: la verosimilitud exige integrar sobre todos los z y esa integral no se puede calcular; por eso tampoco se puede derivar (la intratabilidad es del cálculo, no de la derivada). Tres: el ELBO reemplaza la integral por un sorteo del codificador y una KL cerrada; eso sí se calcula y se deriva. Cuatro: es una cota; la brecha es el error del codificador, que la propia optimización reduce. Cierre: cambiar el signo para minimizar, y con decodificador gaussiano el primer término es el error cuadrático: es la pérdida de la 11. Si viene al caso, el compromiso entre los dos términos: en la primera etapa de GCM la KL dominó y la reconstrucción fue insuficiente.

### R8. Estructura del espacio latente de un autocodificador variacional: malla de decodificaciones sobre MNIST

**Visible.** Izquierda, una malla de 15 × 15 imágenes: las decodificaciones de una grilla regular del latente bidimensional (z₁ y z₂ entre −2,5 y 2,5) del mismo AV de la diapositiva 11. Derecha, tres párrafos: cómo se construye; qué muestra (regiones contiguas por dígito, transiciones graduales, ningún hueco); por qué (la KL mantiene las codificaciones cerca de N(0, I), así el decodificador se entrena sobre todo el rango que después se muestrea; garantía que el autocodificador clásico no tiene). Nota en gris: misma figura que presentan Kingma y Welling para MNIST; esta se obtuvo con un AV mínimo entrenado para la defensa.

**Notas.** Solo si preguntan por la estructura del espacio latente o por qué el AV sí sirve como generador. Leerla con la 10 y la 11: la 10 muestra el hueco del autocodificador clásico; la 11, un recorrido recto por el latente del AV; esta, el latente entero. Si preguntan por la borrosidad: dos dimensiones latentes son muy pocas para MNIST, se eligieron para poder dibujar la malla; los AV de la tesis usan latentes de 18 a 108 dimensiones.

---

## Cómo quedó construida

Archivos, todos en `presentacion/`:

- `defensa_formal.html`: para proyectar. Flechas para avanzar, N muestra las notas, F pantalla completa. La dirección `#12` abre la diapositiva 12 del guion y `#R2` el respaldo 2.
- `defensa_formal_entrega.html` y `defensa_formal.pdf`: las mismas diapositivas sin notas de orador, para entregar o como respaldo si falla el navegador.
- `defensa_formal.src.html`: el fuente editable del contenido visible. `guion_defensa.md` aporta títulos y notas.
- `figuras.py` y `figuras/`: los gráficos de datos, generados desde `utnthesis/filtered_experiment_data_v2.csv` y `utnthesis/experiments_results.csv`.
- Para reconstruir después de un cambio: `../.venv/bin/python figuras.py` (solo si cambian los gráficos) y `../.venv/bin/python build_formal.py`.

Decisiones tomadas al construir, que se pueden revertir:

- **Todos los gráficos de datos se redibujaron** desde los archivos de experimentos, con un estilo único: gris para sin aumentación o datos reales, azul para con aumentación o datos sintéticos. Las figuras de la tesis usan rosa y gris, títulos recortados y etiquetas crudas de experimento; redibujarlas las vuelve legibles proyectadas y consistentes entre sí. Los valores son los mismos.
- **Los diagramas se redibujaron** en el estilo de línea de la presentación (autocodificador, espacio latente, AV, AVC, ciclo del AG, cromosomas, diseño experimental, flujo en tres etapas). Los de la tesis tienen fondos grises o amarillos que no combinan con una estética simple.
- **La figura de escala común y la de intervalos de confianza usan en GCM las 9 y 10 corridas** de la tabla global, no toda la segunda etapa.
- **Dispersión de GCM corregida a 0,033 contra 0,022**, que es la desviación de esas 9 y 10 corridas. El valor anterior, 0,052 contra 0,036, corresponde a toda la segunda etapa (18 y 25 corridas) y mezclaba dos conjuntos de corridas en la misma fila. `Respuesta_observaciones_jurado.md` todavía usa el valor anterior.
- **Mann-Whitney en GCM: p = 0,005** para 9 contra 10 corridas y 0,011 para toda la etapa, recalculados. El guion decía 0,006.
- **Portada con el año 2026** y nombre como figura en la tesis, sin tilde en Sebastian.
- **La diapositiva 30 se mantuvo**, rotulada como esquema ilustrativo de una interpretación y no como resultado medido.

## Decisiones de construcción tomadas por mí

Se pueden revertir; están acá para que las veas antes de que se construya nada.

- **Dos salidas del mismo fuente.** Un archivo para proyectar, con notas de orador ocultas tras la tecla N, y un archivo limpio sin notas para entregar al jurado o a los directores (HTML y PDF). Las notas contienen indicaciones tácticas que no deberían circular.
- **Figura de intervalos de confianza regenerada** desde el archivo de experimentos para que GCM use las 9 contra 10 corridas que reporta la tabla global. La versión actual usa toda la segunda etapa.
- **Figuras 4.12 y 4.13 redibujadas** con los mismos datos, eje rotulado y nombres de grupo legibles ("~45 genes, aumentados") en lugar de las etiquetas crudas de experimento. Las figuras originales llevan título de matplotlib recortado.
- **Recorte de la banda superior** en las cuatro figuras PNG que tienen el título recortado (3.4, 3.5, 4.12, 4.13).
- **Diapositiva 33 muestra solo el panel de exactitud** de la Figura 4.11; el panel de variables mezcla tamaños de cromosoma y engaña.
- **Diapositiva 7 y 22 con SVG nuevo** en lugar de `AV-AG.png`, para que el flujo se lea proyectado; `AV-AG.png` queda como alternativa si preferís la figura de la tesis.
- **Desglose de GCM por tamaño de cromosoma (diapositiva 34 y R3)** tomado del archivo `filtered_experiment_data_v2.csv`, que coincide con las medias de la tesis. La tabla equivalente de `Respuesta_observaciones_jurado.md` da otras cantidades de corridas y otras medias para ~45 y ~200; no encontré de dónde salen, así que el guion usa el archivo.

## Pendientes antes de construir

- Confirmar el año de la portada (el PDF entregado dice mayo de 2025; la defensa es en 2026).
- Confirmar si Figura 1.1 (`diagrama_seleccion_características.png`) se lee bien proyectada o conviene redibujarla.
- Decidir si la diapositiva 30 (por qué funciona en Madelon) se mantiene; es interpretación, no resultado medido.
- Verificar la cifra de NIPS 2003 en Guyon et al. 2004 para R1.
- Madelon, variables sin aumentación: el capítulo 4 dice 35 y la respuesta al jurado dice 36. El archivo de experimentos da 35,8 sobre 49 corridas, así que el guion usa 36. Si preguntan por la diferencia con la tesis, es redondeo.
