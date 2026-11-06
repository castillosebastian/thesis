# Guion de la defensa: estructura formal

Borrador del 4 de noviembre de 2026, para revisar antes de construir las diapositivas.

**Tesis:** Aumentación de datos mediante autoencoders variacionales y su impacto en estrategias de selección de características basadas en Algoritmos Genéticos.
**Tesista:** Claudio Sebastian Castillo. **Director:** Dr. Matías Gerard. **Codirector:** Dr. Leandro Vignolo.
**Maestría en Minería de Datos, UTN Facultad Regional Paraná.**

## Cómo leer este documento

- Cada diapositiva tiene un número, un **título que es una oración completa** (lo que el jurado lee), el **contenido visible** (figura, tabla o ítems) y las **notas de orador** (lo que vos decís, no va en la diapositiva).
- **Registro.** Títulos y texto visible en registro académico: se nombra cada fenómeno con el término técnico que usa la tesis (maldición de la dimensionalidad, colapso de la distribución posterior, escasez muestral), en oraciones completas y sin giros coloquiales. Las notas de orador son más libres porque no se proyectan.
- Tiempo previsto: 40 a 45 minutos. Son 45 diapositivas en total: 38 de contenido, portada, organización inicial, cuatro repeticiones de "Organización" que se pasan en segundos, y cierre. A razón de una por minuto da 44 minutos.
- Las figuras nombradas existen en `utnthesis/`. Las marcadas **(nuevo SVG)** se dibujan para la presentación.
- **Estado al 5 de noviembre de 2026: la presentación está construida.** Este guion es la fuente de los títulos y de las notas de orador: `build_formal.py` los toma de acá según el número de diapositiva. Los párrafos **Visible** quedan como la descripción original; el contenido visible definitivo está en `defensa_formal.src.html`. Ver la sección "Cómo quedó construida" al final.
- Los números salen de la tesis corregida y de `Respuesta_observaciones_jurado.md`. Donde la tesis y la respuesta difieren, se usa la respuesta (corridas reales como n, puntos porcentuales junto a porcentajes relativos).
- Lo que el jurado pidió está integrado sin anunciarlo: escala común en los gráficos (Quiroga c), resultados globales antes del detalle (Quiroga d), definición de "mejora" en tres criterios (Chan e), conclusiones moderadas y limitaciones explícitas (Chan f). El estado del arte (Quiroga a) y SMOTE (Quiroga b) van en respaldo.

## Reparto del tiempo

| Sección | Diapositivas | Minutos |
| --- | --- | --- |
| Portada y organización | 0 a 1 | 1 |
| 1. Introducción | 2 a 8 | 7 |
| 2. Marco teórico | 9 a 16 | 8 |
| 3. Materiales y métodos | 17 a 23 | 7 |
| 4. Resultados | 24 a 39 | 16 |
| 5. Conclusiones y trabajos futuros | 40 a 43 | 4 |
| Cierre | 44 | 1 |
| Respaldo | R1 a R5 | solo para preguntas |

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

### 2. La maldición de la dimensionalidad: conjuntos con miles de variables y decenas de observaciones

**Visible.** Dos columnas. Izquierda: "Microarreglos de ADN: miles de genes, decenas de pacientes". Derecha: "Video, finanzas, redes sociales: grandes conjuntos de variables". En el medio, el término en una línea: *maldición de la dimensionalidad: alta demanda computacional y problemas intratables en la práctica* (Bolón-Canedo et al., 2015). Abajo, la definición: *selección de características: detectar las variables relevantes y descartar las irrelevantes o redundantes con mínima pérdida de rendimiento*.

**Notas.** La motivación del capítulo 1. La tesis nombra el fenómeno como la maldición de la dimensionalidad, en el sentido de Bolón-Canedo: espacios de variables cuya optimización es intratable en la práctica. Fisher ya en los años treinta reprochaba estudiar variables aisladas en vez de sus interacciones; Hughes en los sesenta mostró que la exactitud de un clasificador no crece indefinidamente con el número de variables. Hoy el caso típico es la biomedicina: un microarreglo mide miles de genes sobre decenas de pacientes. Tres de los cinco conjuntos de la tesis son de ese tipo.

### 3. Cuatro propiedades de los datos dificultan la selección de características

**Visible.** Cuatro cajas en fila, cada una con un rótulo y una línea:
- **Alta dimensionalidad y escasez muestral**: n ≫ m; sobreajuste o modelos que no capturan la estructura.
- **Desbalance de clases**: la evaluación prioriza la clase mayoritaria y descarta variables útiles para las minoritarias.
- **Complejidad**: ambigüedad de clases, fronteras complejas, dispersión de muestras.
- **Ruido**: variables sin poder predictivo mezcladas con las relevantes.

**Notas.** Son los cuatro problemas que organizan la tesis y la elección de los conjuntos de datos. Señalar que de los tres aspectos de la complejidad, solo la dispersión de muestras es atacable con aumentación; la ambigüedad y las fronteras complejas no dependen de la muestra. El desbalance tiene tres familias de remedios: muestreo, modificación del algoritmo y aprendizaje sensible al costo; la tesis usa las dos primeras dentro del autocodificador.

### 4. Los métodos envolventes capturan las interacciones entre variables, pero el espacio de 2ⁿ subconjuntos es computacionalmente intratable

**Visible.** Figura `diagrama_seleccion_características.png` (Figura 1.1) o una versión simplificada en tres columnas: Filtro (rápido, independiente del modelo, no ve interacciones), Envolvente (usa el clasificador como caja negra, captura dependencias, costo exponencial), Embebido (selección durante el entrenamiento, específico del modelo). Debajo: "Envolvente + heurística de búsqueda = algoritmo genético".

**Notas.** No hay un método superior en general. Los envolventes resuelven lo que Fisher pedía, las interacciones, pero el espacio es 2 elevado a n. Con 16.063 genes es intratable. Por eso se recurre a heurísticas, y los algoritmos genéticos son una de las más usadas para esta tarea (Vignolo et al., 2017). Esta es la línea que sigue la tesis.

### 5. En un algoritmo genético, la calidad de la estimación de aptitud está acotada por los datos disponibles

**Visible.** **(nuevo SVG)** Ciclo de tres cajas: el AG propone un subconjunto, un clasificador lo evalúa con los datos de entrenamiento, la aptitud guía la selección. La caja "datos" marcada con un acento: "pocas muestras, desbalance, ruido: aptitud ruidosa". Debajo: "La escasez de datos no limita al algoritmo de búsqueda, sino a la estimación de aptitud que lo guía."

**Notas.** Este es el punto de partida del aporte. La selección es el paso crítico del AG y depende de la aptitud que calcula un clasificador. Con datos insuficientes esa estimación es ruidosa, aumenta la incertidumbre en la selección y el algoritmo puede converger prematuramente o sobreajustarse a la muestra. El problema no está en el algoritmo sino en la calidad de la evaluación.

### 6. La aumentación de datos con modelos generativos es una respuesta reciente a la escasez muestral

**Visible.** Tabla corta de tres filas: SMOTE (interpola entre vecinos; rebalancea clases; pierde sentido en alta dimensión, Blagus y Lusa 2013), GAN (generador contra discriminador; entrenamiento inestable con pocas muestras, Fajardo et al. 2021), Autocodificador variacional (aprende una distribución latente continua; preserva la estructura estadística; mejor generador en comparaciones recientes, Fajardo 2021, Ai 2023). Debajo, una línea: aplicaciones de AV en imágenes, texto, habla, datos tabulares, longitudinales y grafos.

**Notas.** Estado del arte en una diapositiva. Tres razones para elegir AV: Blagus y Lusa mostraron que SMOTE no aporta en alta dimensión con pocas muestras, que es justamente el escenario de Leukemia, GCM y ALL Leukemia. Fajardo comparó sobremuestreo aleatorio, SMOTE, GAN y AV condicional y el AV condicional fue el mejor generador. Ai confirmó que los AV guiados superan a otros sobremuestreos. Además, SMOTE rebalancea clases, y la tesis usa la aumentación también en problemas balanceados. Si preguntan por SMOTE, hay una diapositiva de respaldo.

### 7. Propuesta: generación de muestras sintéticas mediante AV y selección de características con AG sobre los datos aumentados

**Visible.** Figura `AV-AG.png` (Figura 4.5) o versión simplificada **(nuevo SVG)**: datos originales → AV entrenado → N muestras sintéticas → datos aumentados (originales + sintéticos) → AG con clasificador MLP → subconjunto de características → evaluación en la partición original de testeo.

**Notas.** El flujo completo en una imagen. Tres cosas a decir: el AV se entrena solo con la partición de entrenamiento; el AG recibe originales más sintéticos; la exactitud se mide siempre en la partición original de testeo, sin datos sintéticos. Los tres beneficios esperados: más muestras, rebalanceo de clases minoritarias y atenuación del ruido por el paso codificar-decodificar.

### 8. Objetivo general y objetivos específicos

**Visible.** Objetivo general: *evaluar el impacto de la aumentación de datos mediante AV sobre el desempeño de estrategias de selección de características basadas en AG.* Objetivos específicos:
1. Integrar estrategias de aumentación basadas en AV en los AG.
2. Evaluar el desempeño de las estrategias propuestas en conjuntos de datos de diferente complejidad.
3. Comparar el AG con datos aumentados frente al mismo AG sin aumentación.

Debajo, la hipótesis en una línea: *aumentar sintéticamente las muestras permite al AG identificar subconjuntos más relevantes, con mejor exactitud y eficiencia de selección.*

**Notas.** Tal como figuran en el capítulo 1. Subrayar el tercer objetivo: la comparación central es con y sin aumentación, con el mismo algoritmo y los mismos parámetros. No es una carrera contra el estado del arte. Decirlo acá evita malentendidos en resultados.

---

## 2. Marco teórico

### 9. Organización (sección 2 resaltada)

**Notas.** Pasar en segundos: "Marco teórico: el autocodificador variacional, el algoritmo genético y las métricas."

### 10. El autocodificador proyecta los datos a un espacio latente y los reconstruye, pero ese espacio latente es discontinuo

**Visible.** Figura `autocodificadores.png` (Figura 3.1) a la izquierda y `espacio_latente_discontinuo.png` (Figura 3.2) a la derecha. Debajo, la pérdida en una línea: L(θ, φ) = Σ ‖xᵢ − D_φ(C_θ(xᵢ))‖².

**Notas.** Codificador C_θ y decodificador D_φ, entrenados juntos minimizando el cuadrado de la distancia euclídea. No hay nada que obligue a que puntos cercanos en la entrada queden cercanos en el latente. Quedan regiones del espacio latente que nunca se usaron en el entrenamiento, y muestrear ahí produce salidas sin relación con los datos. Por eso un autocodificador clásico no sirve como generador.

### 11. El autocodificador variacional codifica cada observación como una distribución, no como un punto

**Visible.** Figura `autocodificadores_variacionales.png` (Figura 3.3). Tres líneas: el codificador produce μ y σ; z = μ + σ·ε con ε ~ N(0, I) (reparametrización); el decodificador reconstruye x̂ a partir de z. Para generar: muestrear z de N(0, I) y decodificar.

**Notas.** La codificación deja de ser determinística. El vector de medias fija el centro y el de desvíos el área alrededor. La reparametrización es lo que permite retropropagar a través del muestreo. Para generar muestras nuevas basta tomar z de la normal estándar y pasar por el decodificador. Esa es la propiedad que la tesis explota.

### 12. La pérdida del AV equilibra reconstrucción y regularización del espacio latente

**Visible.** La cota inferior de la evidencia en una línea:
log p_θ(x) ≥ E_{z∼q_φ(z|x)}[log p_θ(x|z)] − D_KL(q_φ(z|x) ‖ p_θ(z)).
Dos rótulos debajo de cada término: "reconstrucción (en la práctica, MSE)" y "regularización (KL contra N(0, I))". Una línea al pie: *si la KL domina, el espacio latente queda bien regularizado pero reconstruye mal.*

**Notas.** La verosimilitud marginal es intratable porque la posterior lo es; la inferencia variacional la aproxima con q_φ y se maximiza la cota inferior. Dos términos en tensión: reconstruir fielmente y mantener el latente cerca de la normal estándar. Este compromiso importa en resultados: en la primera etapa de GCM la KL dominó y la reconstrucción fue insuficiente. Dejar plantado ese concepto ahora.

### 13. El autocodificador variacional condicional incorpora la etiqueta de clase y permite generar muestras por clase en problemas desbalanceados

**Visible.** **(nuevo SVG)** Esquema del AVC: [x, y] entra al codificador; [z, y] entra al decodificador. Tres ítems: etiqueta concatenada en ambas redes; pesos de clase inversos a la frecuencia en la pérdida de reconstrucción; muestreo ponderado en cada mini-lote.

**Notas.** Para GCM y ALL Leukemia, con 14 clases desbalanceadas. Sin condicionamiento, el generador favorece las clases mayoritarias. Los pesos de clase y el muestreo ponderado se validaron juntos: separados o solos no dieron el mejor resultado, combinados sí. Esto permite generar cantidades iguales por clase, que es lo que se hace en la segunda etapa de GCM.

### 14. El algoritmo genético evoluciona una población de soluciones codificadas mediante selección, cruce y mutación

**Visible.** Figura `diagrama_ag.png` (Figura 4.1). Cuatro propiedades de Goldberg en una columna: opera sobre una codificación, evalúa una población, usa una función de aptitud sin derivadas, transiciones probabilísticas.

**Notas.** Población inicial aleatoria, evaluación por aptitud, selección, cruce, mutación, hasta un criterio de terminación. Las cuatro propiedades explican por qué sirven donde otros métodos no: espacios discretos, no diferenciables, multimodales. La diversidad de la población es lo que evita la convergencia prematura.

### 15. En la selección de características, cada cromosoma es una cadena binaria que indica qué variables se incluyen

**Visible.** Figura `codificacion-decodificacion.png` (Figura 4.2, corregida): genotipo 1100101 → fenotipo [X1, X2, X5, X7]. Al lado, pequeños esquemas de cruce (`ag_cruce.png`) y mutación (`ag_mutacion.png`).

**Notas.** Codificación binaria de largo igual al número de variables: 7.129 bits en Leukemia, 16.063 en GCM. El fenotipo es el subconjunto que entrena al clasificador. Cruce de dos puntos y mutación por inversión de bits. La proporción de bits activos en la inicialización define el tamaño del subconjunto que explora el AG, y es un parámetro crítico que aparece en todos los experimentos.

### 16. Tres criterios definen la mejora en la selección de características: desempeño predictivo, reducción de variables y estabilidad

**Visible.** Tres filas con rótulo y definición:
- **Desempeño predictivo**: exactitud en la partición original de testeo del subconjunto encontrado (exactitud balanceada en multiclase dentro de la aptitud).
- **Reducción de variables**: número medio de características seleccionadas en la población final.
- **Estabilidad**: dispersión de la exactitud y del número de variables entre corridas independientes (desviación estándar y rango intercuartílico).
Una línea al pie: *los tres criterios no varían conjuntamente; se reportan por separado.*

**Notas.** Responde a la observación de la Dra. Chan sobre qué se entiende por mejora. Decirlo como definición operativa del capítulo 4, no como respuesta. Para validar el generador en sí, antes del AG, se usa además la prueba de Fajardo: un MLP entrenado solo con sintéticos y evaluado en reales, contra un MLP entrenado con reales. En el capítulo 2 las métricas de línea base son AUC y macro-F1, que no se comparan directamente con la exactitud del AG.

---

## 3. Materiales y métodos

### 17. Organización (sección 3 resaltada)

**Notas.** "Materiales y métodos: los datos, la línea base, los modelos y el diseño experimental."

### 18. Cinco conjuntos de datos cubren los cuatro problemas: tres de expresión génica y dos del desafío NIPS 2003

**Visible.** Tabla:

| Conjunto | Observaciones × características | Clases | Desafío principal |
| --- | --- | --- | --- |
| Leukemia | 72 × 7.129 | 2, desbalanceado | n ≫ m, correlación entre genes |
| Gisette | 13.500 × 5.000 | 2, balanceado | ruido y redundancia, espacio grande |
| Madelon | 2.000 × 500 | 2, balanceado | 20 variables con señal, 480 de ruido |
| GCM | 190 × 16.063 | 14, desbalanceado | n ≫ m, multiclase, desbalance |
| ALL Leukemia | 327 × 12.600 | 14, desbalanceado | n ≫ m, multiclase; validación |

**Notas.** Leukemia es Golub 1999, ALL y AML. GCM es Ramaswamy 2001, 14 tipos de tumor. ALL Leukemia es Yeoh 2002 y entró al final para validar el flujo de GCM; por eso no está en la línea base. Madelon es artificial: 5 relevantes, 15 combinaciones lineales y 480 aleatorias, un XOR multidimensional. Gisette distingue los dígitos 4 y 9 con sondas sin poder predictivo. Las particiones originales de entrenamiento y testeo se respetan en todos los experimentos con AV y AG.

### 19. Los modelos clásicos sobre el conjunto completo de variables establecen la línea base y caracterizan la dificultad de cada problema

**Visible.** Tabla reducida de la Tabla 2.1: por conjunto, métrica, mejor modelo y el rango donde cae la mayoría de los 18 modelos.

| Conjunto | Métrica | Mejor | Rango de la mayoría | Lectura |
| --- | --- | --- | --- | --- |
| Leukemia | AUC | 1,00 (Bagging, RF, SVC) | 0,85 a 1,00 | cerca de saturar |
| Gisette | AUC | 1,00 (Gradient Boosting) | 0,92 a 0,99 | cerca de saturar |
| Madelon | AUC | 0,91 (Bagging) | 0,57 a 0,70 | margen amplio |
| GCM | macro-F1 | 0,71 (SGD), 0,68 (MLP) | 0,48 a 0,62 | margen amplio; clases con F1 nulo |

**Notas.** Dieciocho modelos de scikit-learn con búsqueda en grilla, sobre una partición 80/20 propia. Dos lecturas: Leukemia y Gisette casi no tienen margen; Madelon y GCM sí. En GCM, clases como Breast o Prostate tienen F1 cero: el modelo nunca las predice. Esa es la asimetría que la aumentación por clase intenta corregir. Aclarar si preguntan: estas métricas son AUC y F1 sobre otra partición, así que no se comparan directamente con la exactitud del AG; la comparación válida está en respaldo.

### 20. Arquitectura final de AV y AVC: tres capas con normalización por lotes e hiperparámetros ajustados por conjunto

**Visible.** Izquierda: arquitectura en tres líneas (codificador: 3 capas lineales + BatchNorm + ReLU; μ y log σ² por capas lineales independientes; decodificador simétrico). Derecha: Tabla 4.1 compactada:

| Conjunto | Modelo | Capas 2 y 3 | Latente | Tasa de aprendizaje | Épocas |
| --- | --- | --- | --- | --- | --- |
| Leukemia | AV | 346, 178 | 108 | 2,7·10⁻⁴ | 2.889 |
| Madelon | AV | 835, 308 | 25 | 1,6·10⁻⁴ | 1.364 |
| Gisette | AV | 3.870, 2.987 | 18 | 9,5·10⁻⁴ | 2.739 |
| GCM | AVC | 358, 189 | 35 | 6,9·10⁻⁴ | 3.613 |
| ALL Leukemia | AVC | 434, 176 | 35 | 4,0·10⁻⁴ | 949 |

**Notas.** Se partió de dos capas, se vio baja calidad de reconstrucción y se pasó a tres con normalización por lotes. Pérdida: MSE más KL; MSE balanceado por clase en multiclase. Optimizador Adam, parada temprana con paciencia de 10 épocas. Hiperparámetros por búsqueda en grilla y optimización bayesiana: capas 2 y 3 entre 50 y 5.000 neuronas, latente entre 10 y 300 (hasta 1.000 en AVC), tasa entre 10⁻⁵ y 10⁻². Normalización estándar de entrada. Dropout y pérdida L1 se probaron y no aportaron.

### 21. La función de aptitud del AG pondera con igual peso la exactitud y la reducción del número de variables

**Visible.** Fórmula grande: f = α · acc + (1 − α) · (1 − k/n), con α = 0,5, k variables seleccionadas, n totales. Debajo, la configuración común en ítems: población de individuos binarios; selección por torneo; cruce de dos puntos (p = 0,75); mutación por inversión de bits (probabilidad por conjunto, entre 0,0002 y 0,1); 15 a 30 generaciones; evaluador MLP; biblioteca DEAP.

**Notas.** Por diseño el AG sacrifica algo de exactitud a cambio de dimensionalidad. Ejemplo: 100% de exactitud con todas las variables da f = 0,5; 80% con el 20% de las variables da f = 0,8. Esto hay que tenerlo presente cuando se compara con trabajos que usan todos los genes. La proporción de genes activos al inicio se ajustó por conjunto: 10% en la mayoría, hasta 0,3% en los experimentos de reducción agresiva de GCM y ALL.

### 22. El diseño experimental compara el mismo AG con y sin aumentación, evaluado siempre en la partición original de testeo

**Visible.** Figura `diseño_experimentos.png` (Figura 4.6). Tres líneas: mismos parámetros del AG en ambos grupos; cada corrida completa del AG es una observación; comparación de distribuciones entre grupos con gráficos de cajas, test t de Welch y Mann-Whitney.

**Notas.** Cada punto en los gráficos que siguen es una corrida completa del AG, y el valor es la exactitud media de la población final en la partición original de testeo. Se comparan distribuciones de corridas con aumentación contra corridas sin aumentación. Los valores p se calculan con las corridas como n. Esto corrige un test de la tesis que había usado la cantidad de observaciones del conjunto; con el n correcto la conclusión no cambia. Decirlo acá, antes de que lo pregunten.

### 23. Para los problemas multiclase se diseñó un flujo en tres etapas: selección, generación y selección

**Visible.** **(nuevo SVG)** Tres cajas en fila: (1) AG sobre el espacio completo produce las características más frecuentes en los cromosomas finales; (2) AVC entrenado en ese subespacio genera muestras balanceadas por clase; (3) AG final sobre originales más sintéticos. Debajo: en GCM, 1.600 características de 590 cromosomas y 3.000 muestras; en ALL Leukemia, subespacio de 3 corridas y 1.000 muestras. Ejecución en la nube: 8 vCPU, 30 GB de RAM.

**Notas.** Presentarlo como parte del método, aunque nació de un resultado: la primera etapa de GCM falló y el diagnóstico llevó a este flujo. La hipótesis de trabajo: si el AVC no puede aprender la distribución de 16.063 variables con 133 muestras, que aprenda la de 1.600. Los detalles del fracaso y del diagnóstico se cuentan en resultados.

---

## 4. Resultados

### 24. Organización (sección 4 resaltada)

**Notas.** "Resultados en tres partes: primero la calidad de los datos sintéticos, después los resultados globales de la integración, y recién después cada conjunto."

### 25. Un MLP entrenado únicamente con datos sintéticos alcanza la exactitud del entrenado con datos reales en tres de los cuatro conjuntos

**Visible.** Figura 3.4 redibujada con los mismos valores. Línea de lectura: exactitud en la partición original de testeo; gris entrenado con reales, azul entrenado con sintéticos.

**Notas.** La prueba de Fajardo. Leukemia: 0,95 con sintéticos contra 0,81 con reales; el recall de la clase minoritaria sube de 0,56 a 0,89. Madelon: 0,57 contra 0,55. GCM: 0,54 en ambos, con patrones distintos por clase. Gisette: 0,95 contra 0,97, dos puntos abajo. Conclusión del capítulo 3: el AV captura la estructura de los datos lo suficiente como para que valga la pena aumentar. No es todavía el resultado de la tesis; es la condición previa.

### 26. La cantidad de muestras sintéticas presenta un umbral: en GCM, superarlo degrada la exactitud

**Visible.** Figura `n_samples_accuracy_comparison.png` (Figura 3.5): exactitud del MLP con 190, 400, 3.000 y 6.000 muestras sintéticas. Dos líneas al pie: con 3.000 muestras balanceadas (214 por clase) se iguala al MLP con reales; con 6.000 se degrada. Un espacio latente de 35 superó a configuraciones de más de 50.

**Notas.** Dos hallazgos del capítulo 3 que condicionan todo. Primero, el umbral: pasado cierto punto los sintéticos sobreajustan al generador. Segundo, contra la intuición de "más dimensión latente es mejor" (Boom 2021), un latente compacto generalizó mejor, en línea con Ai 2023. Las arquitecturas simples, de tres capas, rindieron igual o mejor que las de cuatro. Estas dos cosas se calibran por problema; es una limitación.

### 27. Resultados globales: la aumentación mejoró significativamente la exactitud en dos de los cinco conjuntos y no la modificó en los otros tres

**Visible.** Tabla global:

| Conjunto | Corridas (aum. / orig.) | Exactitud orig. | Exactitud aum. | Diferencia (pp) | p | Lectura |
| --- | --- | --- | --- | --- | --- | --- |
| Leukemia | 90 / 90 | 0,989 | 0,992 | +0,3 | 0,09 | saturado, sin cambio |
| Gisette | 13 / 12 | 0,959 | 0,960 | +0,1 | 0,63 | saturado, sin cambio |
| Madelon | 30 / 49 | 0,750 | 0,828 | +7,8 | < 0,001 | mejora significativa |
| GCM, 2.ª etapa | 9 / 10 | 0,497 | 0,541 | +4,4 | 0,005 | mejora significativa |
| ALL Leukemia | 18 / 18 | 0,669 | 0,672 | +0,3 | 0,87 | sin cambio |

**Notas.** La vista global primero, como pidió el Dr. Quiroga. Dos resultados significativos: Madelon y la segunda etapa de GCM. En los otros tres la exactitud no cambia de forma significativa, y lo digo de entrada para no sobrevender. Los porcentajes relativos de la tesis, 10,4% en Madelon y 8,85% en GCM, son 7,8 y 4,4 puntos porcentuales. Test de Welch con las corridas como n; Mann-Whitney da la misma conclusión en todos los casos.

### 28. Los intervalos de confianza del 95% excluyen el cero únicamente en Madelon y GCM

**Visible.** Figura `diferencia_exactitud_ic95.png`. Línea de lectura: diferencia aumentados menos originales en puntos porcentuales, con intervalo de confianza del 95%; donde la barra cruza el cero no hay evidencia de efecto.

**Notas.** Este gráfico resume la tesis. La versión actual del PNG calcula GCM con toda la segunda etapa (18 contra 25 corridas, +4,0 puntos); para que coincida con la tabla anterior se regenera con las 9 contra 10 corridas de ~450 y ~750 genes (+4,4, IC 1,6 a 7,3). Madelon y GCM claramente por encima de cero. Leukemia y Gisette tocan el cero con intervalos cortísimos: no hay nada que mejorar. ALL Leukemia tiene un intervalo ancho: pocas corridas y mucha variabilidad. El de GCM también es ancho: 9 y 10 corridas con un test de 57 muestras, donde cada muestra mal clasificada mueve la exactitud 1,75 puntos.

### 29. Con escala común, la diferencia solo es apreciable en los conjuntos con margen de mejora

**Visible.** Figura `boxplot_resultados_precision_escala_unificada.png`, eje común de 0,4 a 1,0. Dos frases debajo: "Problema saturado: sin cambio." "Margen de mejora y reconstrucción adecuada: mejora."

**Notas.** La escala común que pidió el jurado. Los paneles separados de la tesis agrandaban diferencias de milésimas en Leukemia y Gisette; acá las cajas se superponen por completo. La regla tiene dos condiciones, y la segunda, que el AV reconstruya bien, es la que falló en la primera etapa de GCM. Lo que sigue son los dos casos que explican la regla, y después la validación.

### 30. Madelon: la aumentación incrementa la exactitud en 7,8 puntos porcentuales y reduce el número de variables seleccionadas

**Visible.** Figura `boxplot_madelon_combined.png` (exactitud y número de variables). Dos números grandes: "+7,8 puntos (0,750 → 0,828, p < 0,001)" y "29 variables en lugar de 36".

**Notas.** El resultado más limpio. Configuración: 2.000 muestras sintéticas, mutación 0,002, cruce 0,75, 30 generaciones. La exactitud sube de 0,750 a 0,828 y la dispersión baja (desviación 0,023 contra 0,038). Además el subconjunto es más chico. La tesis señala que solo 2 de los 18 clásicos del capítulo 2, AdaBoost y Bagging, superan este nivel, y con las 500 variables; decirlo con la salvedad de que el capítulo 2 reporta AUC sobre otra partición, así que es una referencia de orden de magnitud, no una comparación directa.

### 31. Interpretación del caso Madelon: un espacio latente compacto preserva las 20 variables informativas y atenúa las 480 de ruido

**Visible.** **(nuevo SVG)** Esquema: 500 variables (20 con señal, 480 ruido) → latente de 25 dimensiones → 500 variables reconstruidas, con el ruido atenuado. Una línea: *los sintéticos realzan la señal que el AG necesita encontrar.*

**Notas.** La interpretación de la tesis. El AV reconstruye desde un latente de 25 dimensiones: no puede memorizar 480 variables aleatorias, así que las reconstruye cerca de su media, y conserva la estructura de las 20 informativas. Al AG le llega un conjunto donde la señal pesa más. Es consistente con la dificultad vista en la línea base, donde la mayoría de los clásicos sin selección quedaba lejos de saturar.

### 32. GCM, primera etapa: con el AVC entrenado sobre las 16.063 variables, la aumentación no mejoró la exactitud

**Visible.** Figura `boxplot_gcm_combined_part1.png` (Figura 4.10). Número: "0,512 con aumentación contra 0,538 sin aumentación". Configuración en una línea: 1.400 sintéticas (100 por clase) más 133 originales; cromosomas de ~1.600 genes; 20 generaciones.

**Notas.** Cuento el fracaso porque explica el aporte. Se esperaba resultado mixto por la calidad de reconstrucción vista en el capítulo 3 y el desbalance. La exactitud bajó levemente y la dispersión fue similar. Antes se habían probado cromosomas del 20% y 30% de las variables con exactitud entre 0,2 y 0,35, por eso se fijó el 10%.

### 33. Diagnóstico: el clasificador ajusta por completo la distribución sintética, pero no generaliza a la distribución real

**Visible.** Dos números grandes: "100% de exactitud en la partición sintética de testeo" y "50% en la partición real de testeo" (Tabla 4.4, MLP entrenado con 3.000 sintéticos). Debajo: *la distribución sintética es internamente consistente y de menor complejidad que la real: permite igualar al MLP entrenado con datos reales, no superarlo ni guiar mejor al AG.* Una línea más: *explicación plausible, colapso de la distribución posterior: la divergencia KL domina la pérdida y la reconstrucción deja de representar los datos reales.*

**Notas.** Conectar con la diapositiva 25: allí el MLP con sintéticos igualaba al MLP con reales en GCM (0,54 contra 0,54), y acá se ve por qué no lo supera. El modelo aprende los sintéticos a la perfección, pero en los reales queda en el mismo nivel que sin aumentación. La primera etapa del AG había usado 1.400 sintéticos; el diagnóstico se hizo con 3.000 y da el mismo cuadro. La explicación plausible es el colapso de la posterior, que en el marco teórico quedó plantado: la KL domina en un problema con relaciones complejas. Dos salidas: reponderar la KL contra la reconstrucción, o reducir el problema antes de generar. Se tomó la segunda; la primera queda como trabajo futuro.

### 34. GCM, segunda etapa: con el flujo selección-generación-selección, la aumentación incrementa la exactitud en 4,4 puntos porcentuales

**Visible.** Solo el panel izquierdo (exactitud) de `boxplot_gcm_combined.png` (Figura 4.11). Números: "+4,4 puntos (0,497 → 0,541, p = 0,005; 9 y 10 corridas)". Línea: número de variables sin cambio dentro de cada tamaño de cromosoma (454 contra 462; 785 contra 781).

**Notas.** El panel derecho de la figura de la tesis no se proyecta: mezcla corridas de ~450 y ~750 genes en proporciones distintas por grupo y sugiere una reducción de variables que no existe; por eso el número de variables va como texto, comparado dentro de cada tamaño. Con el AVC entrenado en las 1.600 características más frecuentes, pesos de clase y muestreo ponderado, 3.000 muestras balanceadas, cromosomas de ~450 y ~750, 15 generaciones. La mejora es de exactitud, no de reducción de variables. La dispersión aumenta (desviación 0,033 contra 0,022 en estas 9 y 10 corridas), y lo digo antes de que lo pregunten: pocas corridas y un test de 57 muestras. Tomando toda la etapa, 18 contra 25 corridas, p = 0,008 y desviación 0,052 contra 0,036. Con 6.000 muestras el resultado se degradó, coherente con el umbral del capítulo 3.

### 35. GCM con reducción progresiva del cromosoma: la exactitud se mantiene hasta ~45 genes y la media con aumentación es superior en los cuatro tamaños

**Visible.** Figura `boxplot_gcm_ngenes_accuracy.png` (Figura 4.12), redibujada con los mismos datos y rótulos limpios. Tabla mínima, medias de corridas (aum. / orig.):

| Genes activos | Corridas | Exactitud orig. | Exactitud aum. | p |
| --- | --- | --- | --- | --- |
| ~45 | 4 / 10 | 0,432 | 0,443 | 0,43 |
| ~200 | 5 / 5 | 0,476 | 0,498 | 0,38 |
| ~450 | 5 / 5 | 0,489 | 0,538 | 0,035 |
| ~750 | 4 / 5 | 0,505 | 0,545 | 0,10 |

**Notas.** Experimentos de validación interna con reducción agresiva. Pese a pasar de 16.063 a 45 genes la exactitud queda en un nivel aceptable. En media los aumentados quedan arriba en los cuatro grupos; en ~200 la mediana queda apenas por debajo, que es lo que muestra la figura y lo que dice la tesis. Solo ~450 alcanza significación por sí solo, con 5 y 5 corridas. Decirlo como tendencia, no como confirmación.

### 36. ALL Leukemia valida el flujo en un segundo problema multiclase: tendencia favorable, sin significación estadística

**Visible.** Figura `boxplot_all_leukemia_ngenes_accuracy.png` (Figura 4.13). Tabla mínima: ~35 genes 0,608 → 0,625; ~180 0,654 → 0,663; ~300 0,754 → 0,735; ningún p menor a 0,4.

**Notas.** Mismo flujo: AVC sobre un subespacio de 3 corridas, 1.000 sintéticas, 15 generaciones. Con 35 y 180 genes la aumentación queda por encima, con 300 por debajo, y ninguna diferencia es significativa con 5 a 8 corridas por grupo. Lo digo moderado, como pide la Dra. Chan: el flujo es viable en un segundo problema y la tendencia acompaña, pero no es una confirmación estadística. Sí hay menor dispersión con aumentación: desviación 0,056 contra 0,065. En 35 genes la mutación de 0,028 explica parte de la variabilidad.

### 37. En los conjuntos saturados la aumentación no modifica la exactitud, pero reduce la dispersión entre corridas

**Visible.** Figuras `boxplot_leukemia_combined.png` y `boxplot_gisette_combined.png` lado a lado, reducidas. Dos líneas: Leukemia, desviación 0,011 contra 0,016; 6.779 y 6.772 genes seleccionados al menos una vez. Gisette, 424 contra 437 variables, rango intercuartílico 8 contra 21.

**Notas.** Rápido, porque ya se vio en la tabla global. En Leukemia el 10% de los genes alcanza para clasificar casi sin importar cuáles: 80.742 pares de genes con correlación mayor a 0,7. No hay qué mejorar. En Gisette lo que cambia es la estabilidad del número de variables y un subconjunto algo más chico.

### 38. Evaluación por criterio: desempeño predictivo, reducción de variables y estabilidad en cada conjunto

**Visible.** Tabla de la respuesta (e):

| Conjunto | Desempeño predictivo | Reducción de variables | Estabilidad de la exactitud |
| --- | --- | --- | --- |
| Leukemia | sin diferencia (p = 0,09) | igual (259 vs 259) | mejora (0,011 vs 0,016) |
| Gisette | sin diferencia (p = 0,63) | mejora (424 vs 437) | mejora leve (0,003 vs 0,004) |
| Madelon | mejora (p < 0,001) | mejora (29 vs 36) | mejora (0,023 vs 0,038) |
| GCM | mejora (p = 0,005) | igual (454 vs 462; 785 vs 781) | empeora (0,033 vs 0,022) |
| ALL Leukemia | sin diferencia (p = 0,87) | igual (174 vs 173) | mejora leve (0,056 vs 0,065) |

**Notas.** Esta tabla responde con precisión a qué llamamos mejora, con los tres criterios del marco teórico. En los saturados lo único defendible es la estabilidad. En Gisette y Madelon además el subconjunto es más chico. En GCM gano exactitud y pierdo estabilidad; lo reconozco como está.

### 39. Síntesis: el efecto de la aumentación está condicionado por el margen de mejora y la calidad de la reconstrucción

**Visible.** Tres líneas:
- Mejora la exactitud donde existe margen de mejora y el AV reconstruye adecuadamente (Madelon, GCM en segunda etapa).
- No modifica la exactitud en problemas saturados (Leukemia, Gisette); aporta estabilidad.
- En problemas multiclase desbalanceados requiere generar sobre un subespacio seleccionado y calibrar la cantidad de muestras.

**Notas.** Cerrar la sección con la regla en tres líneas, que es lo que el jurado va a recordar. La tercera es el aporte metodológico propio. De aquí a conclusiones.

---

## 5. Conclusiones y trabajos futuros

### 40. Organización (sección 5 resaltada)

**Notas.** "Conclusiones, limitaciones y trabajos futuros."

### 41. Conclusiones

**Visible.** Cuatro ítems:
1. Los datos sintéticos generados por un AV/AVC adecuadamente configurado son aptos para el entrenamiento: un MLP entrenado únicamente con sintéticos alcanza la exactitud del entrenado con reales en Leukemia, Madelon y GCM.
2. La aumentación mejora la selección con AG cuando el problema tiene margen de mejora y el AV reconstruye adecuadamente: +7,8 puntos porcentuales en Madelon y +4,4 en GCM, ambos significativos.
3. En problemas saturados no modifica la exactitud; reduce la dispersión y, en algunos casos, el tamaño del subconjunto.
4. En problemas multiclase desbalanceados, el flujo selección-generación-selección es la condición para que la aumentación resulte útil; aplicar el AVC sobre el espacio completo la perjudicó.

**Notas.** En orden de solidez. La cuarta es el aporte metodológico propio. Añadir de palabra los dos hallazgos de configuración: existe un umbral de muestras sintéticas, y arquitecturas simples con latente moderado rinden igual o mejor que las grandes.

### 42. Limitaciones

**Visible.** Cinco ítems cortos:
1. Cinco conjuntos de datos, dos de ellos artificiales; el efecto depende de la dificultad del problema.
2. Número reducido de corridas en GCM y ALL Leukemia (5 a 10 por configuración) y particiones de testeo pequeñas.
3. El efecto depende de la calidad del AV: con una reconstrucción deficiente, la aumentación perjudica el resultado.
4. Existe un umbral de muestras sintéticas más allá del cual el resultado se degrada.
5. Un único clasificador en la función de aptitud (MLP) e hiperparámetros ajustados por conjunto, no transferibles sin reajuste.

**Notas.** Responde a la Dra. Chan sobre generalización. La primera y la tercera son las que acotan: la aumentación no es una receta universal. La segunda explica por qué ALL Leukemia no alcanza significación y por qué el intervalo de GCM es ancho. Agregar de palabra: no se corrió SMOTE dentro del mismo flujo, y es trabajo futuro inmediato.

### 43. Trabajos futuros

**Visible.** Cuatro ítems:
1. Función de pérdida del AV: reponderar reconstrucción y KL, inferencia variacional recocida; AV jerárquicos para datos como GCM.
2. Integración AV-AG: selección dinámica en varias etapas y optimización conjunta de ambos modelos.
3. Encadenamientos y ensambles de AV y AG para reducir varianza.
4. Comparación con SMOTE y otros generadores dentro del mismo flujo con AG.

**Notas.** Los tres primeros son los del capítulo 5. El cuarto se agrega por la sugerencia del Dr. Quiroga. Si hay que elegir uno, el primero: el colapso de la posterior en GCM sugiere que una pérdida con KL recocida podría evitar el flujo en tres etapas.

---

## Cierre

### 44. Agradecimientos y cierre

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

**Visible.** Tabla: 9 contra 10 corridas (~450 y ~750), +4,4 puntos, IC 95% de 1,6 a 7,3, Welch p = 0,005, Mann-Whitney p = 0,005; toda la segunda etapa, 18 contra 25, +4,0 puntos, IC de 1,1 a 7,0, Welch p = 0,008, Mann-Whitney p = 0,011. Desglose por tamaño de cromosoma: la tabla de la diapositiva 35.

**Notas.** Si preguntan por el test: el script de la tesis usó como n las observaciones de los conjuntos (3.133 y 133). Recalculado con las corridas, la diferencia sigue siendo significativa por dos tests.

### R4. Línea base completa: Tabla 2.1

**Visible.** Tabla 2.1 completa, 18 modelos por 4 conjuntos.

**Notas.** Solo si piden un modelo concreto. Recordar por qué algunos no se evaluaron en GCM y Gisette: dimensionalidad y multiclase.

### R5. Resultados por clase del MLP con datos reales y sintéticos

**Visible.** Tablas 3.1 (Leukemia) y 3.4 (GCM) compactadas: precisión, recall y F1 por clase.

**Notas.** Para la pregunta de qué pasa por clase en GCM: con sintéticos varias clases llegan a precisión 1,00 pero el recall cae; el modelo es más conservador. Las clases 7 y 3 se deterioran, la 12 duplica su F1.

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
- **La diapositiva 31 se mantuvo**, rotulada como esquema ilustrativo de una interpretación y no como resultado medido.

## Decisiones de construcción tomadas por mí

Se pueden revertir; están acá para que las veas antes de que se construya nada.

- **Dos salidas del mismo fuente.** Un archivo para proyectar, con notas de orador ocultas tras la tecla N, y un archivo limpio sin notas para entregar al jurado o a los directores (HTML y PDF). Las notas contienen indicaciones tácticas que no deberían circular.
- **Figura de intervalos de confianza regenerada** desde el archivo de experimentos para que GCM use las 9 contra 10 corridas que reporta la tabla global. La versión actual usa toda la segunda etapa.
- **Figuras 4.12 y 4.13 redibujadas** con los mismos datos, eje rotulado y nombres de grupo legibles ("~45 genes, aumentados") en lugar de las etiquetas crudas de experimento. Las figuras originales llevan título de matplotlib recortado.
- **Recorte de la banda superior** en las cuatro figuras PNG que tienen el título recortado (3.4, 3.5, 4.12, 4.13).
- **Diapositiva 34 muestra solo el panel de exactitud** de la Figura 4.11; el panel de variables mezcla tamaños de cromosoma y engaña.
- **Diapositiva 7 y 23 con SVG nuevo** en lugar de `AV-AG.png`, para que el flujo se lea proyectado; `AV-AG.png` queda como alternativa si preferís la figura de la tesis.
- **Desglose de GCM por tamaño de cromosoma (diapositiva 35 y R3)** tomado del archivo `filtered_experiment_data_v2.csv`, que coincide con las medias de la tesis. La tabla equivalente de `Respuesta_observaciones_jurado.md` da otras cantidades de corridas y otras medias para ~45 y ~200; no encontré de dónde salen, así que el guion usa el archivo.

## Pendientes antes de construir

- Confirmar el año de la portada (el PDF entregado dice mayo de 2025; la defensa es en 2026).
- Confirmar si Figura 1.1 (`diagrama_seleccion_características.png`) se lee bien proyectada o conviene redibujarla.
- Decidir si la diapositiva 31 (por qué funciona en Madelon) se mantiene; es interpretación, no resultado medido.
- Verificar la cifra de NIPS 2003 en Guyon et al. 2004 para R1.
- Madelon, variables sin aumentación: el capítulo 4 dice 35 y la respuesta al jurado dice 36. El archivo de experimentos da 35,8 sobre 49 corridas, así que el guion usa 36. Si preguntan por la diferencia con la tesis, es redondeo.
