# Apuntes de orador

Una entrada por diapositiva. El número es el del pie de la diapositiva proyectada.

Los bloques en cita son observaciones del jurado, con el autor y la letra que tiene la respuesta larga en `Respuesta_observaciones_jurado.md`, seguidas de la respuesta en versión compacta. Van en la diapositiva donde conviene tenerlas a mano.

------------------------------------------------------------------------

## 0 · Portada

- Saludo. Agradecer al jurado la lectura y las observaciones; al director y codirector.
- Desafio: problema dificil y cross-industria +
solución via 2 arquitecturas

------------------------------------------------------------------------

## 1 · Organización

- La mayor parte del tiempo va a resultados.
- Conclusiones cortas, como guía para la discusión.

------------------------------------------------------------------------

## 2 · Maldición de la dimensionalidad

- Alta dimensionalidad implica espacios de variables intratables en la práctica.
- Fisher: interacciones, no variables aisladas. Hughes: más variables no es más exactitud.
- Seleccion de características: proceso de detectar las ca-
racterísticas relevantes y descartar aquellas irrelevantes o redundantes, con el objetivo de obtener un subconjunto que describa adecuadamente un problema dado con una
degradación mínima del rendimiento. 

------------------------------------------------------------------------

## 3 · Cuatro propiedades

- De los tres aspectos de complejidad, solo la escasez muestral se ataca con aumentación.
- Sobreajuste model -> baja generalización 
- Sub-ajustado model -> baja precisión
- Desbalance: muestreo y modificación del algoritmo, los dos dentro del autocodificador.

------------------------------------------------------------------------

## 4 · Métodos envolventes

- Capturan interacciones, pero 2ⁿ subconjuntos: con 16.063 genes, intratable.
- Heurística elegida: algoritmos genéticos (Vignolo y Gerard, 2017).

------------------------------------------------------------------------

## 5 · Aptitud acotada por los datos

- Punto de partida del aporte.
- Con pocos datos la aptitud es ruidosa: convergencia prematura o sobreajuste.
- El problema no es el algoritmo, es la calidad de la evaluación.

------------------------------------------------------------------------

## 6 · Aumentación generativa

- Por qué AV y no SMOTE: Blagus y Lusa (no aporta en alta dimensión), Fajardo (AVC mejor generador), Ai.
- SMOTE solo rebalancea; acá también se aumentan problemas balanceados.
- Respaldo R2 si preguntan.

> **Dr. Quiroga (b): comparar con SMOTE y otros métodos de aumentación.**
> La tesis no corrió SMOTE; se reconoce como limitación. La elección se apoyó en tres resultados: Blagus y Lusa (SMOTE no aporta en alta dimensión con pocas muestras, el escenario de los tres conjuntos genómicos), Fajardo (AV condicional mejor que SMOTE y GAN) y Ai (AV guiados superan a otros sobremuestreos). SMOTE rebalancea clases; acá se aumenta también en problemas balanceados. AV contra SMOTE en el mismo flujo: trabajo futuro inmediato.

------------------------------------------------------------------------

## 7 · Propuesta

- El AV se entrena solo con la partición de entrenamiento.
- El AG recibe originales más sintéticos.
- La exactitud se mide siempre en la partición original de testeo.

------------------------------------------------------------------------

## 8 · Objetivos

- Tercer objetivo: comparar con y sin aumentación, mismo AG, mismos parámetros.
- No es una carrera contra el estado del arte.

> **Dr. Quiroga (a): comparar con el estado del arte del capítulo 2.**
> El objetivo fue medir el impacto de la aumentación sobre un mismo AG. La comparación con el capítulo 2 tiene una limitación: allí se reporta AUC y macro-F1 sobre una partición 80/20 propia; en el capítulo 4, exactitud sobre la partición original de testeo. La comparación válida es con el MLP del capítulo 3: el flujo AV+AG lo iguala o supera en los cinco conjuntos con el 0,6% a 10% de las características. Detalle en R1.

------------------------------------------------------------------------

## 9 · Organización

- "Marco teórico: el autocodificador variacional, el algoritmo genético y las métricas."

------------------------------------------------------------------------

## 10 · Autocodificador

- Codificador y decodificador entrenados juntos por distancia euclídea.
- Latente discontinuo: muestrear en regiones no usadas da salidas sin relación con los datos.
- Por eso no sirve como generador.

> **Gambini (g): notación del codificador y pérdida de reconstrucción.**
> Corregido: el codificador es C_θ en todo el texto (antes alternaba con E_θ); la pérdida es el cuadrado de la distancia euclídea, no la distancia. Agradecer y decir que está incorporado, sin más.

------------------------------------------------------------------------

## 11 · Autocodificador variacional

- Cada observación se codifica como una distribución: medias y desvíos.
- Reparametrización: permite retropropagar a través del muestreo.
- Generar: z de la normal estándar, pasar por el decodificador.
- Dos términos en tensión; dejar plantado: en GCM primera etapa la KL dominó.
- KL = divergencia de Kullback-Leibler ("Kúlbac-Láibler"): ≥ 0, cero solo si las distribuciones coinciden, no simétrica (las barras ordenan: codificada respecto de N(0, I)). Para dos normales: ½ Σ (μ² + σ² − 1 − log σ²). La D de la fórmula es solo el decodificador.
- Origen de la pérdida (negativo del ELBO): no mencionar; si preguntan, R7.

------------------------------------------------------------------------

## 12 · AV condicional

- Para GCM y ALL Leukemia: 14 clases desbalanceadas.
- Pesos de clase: el error de reconstrucción de cada observación se multiplica por w_c ∝ 1/n_c (30 vs 10 observaciones: la chica pesa el triple). Evita que las clases numerosas dominen la pérdida.
- Pesos de clase y muestreo ponderado: solo funcionan combinados.
- Permite generar cantidades iguales por clase.

------------------------------------------------------------------------

## 13 · Algoritmo genético

- Individuo = solución candidata (subconjunto de variables en bits), no una observación.
- Población, aptitud, selección, cruce, mutación, hasta terminar.
- Sirve en espacios discretos, no diferenciables, multimodales.
- La diversidad evita la convergencia prematura.


Los AG son una clase de algoritmo inspirado en la evolución biológica y en la teoría de la selección natural. Los mismos se basan en el concepto de evolución de una población de soluciones potenciales a lo largo de múltiples generaciones. Utilizando operadores genéticos como la selección, el cruce y la mutación los AG generan nuevas soluciones a partir de las disponibles, mejorando su calidad y favoreciendo la preeminencia de ciertas características.

------------------------------------------------------------------------

## 14 · Cromosoma binario y operadores

- 7.129 bits en Leukemia, 16.063 en GCM.
- Selección por torneo (de 5): k al azar, pasa el mejor; equilibra explotación y exploración. Ruleta: proporcional a la aptitud, pierde diversidad. Ventana: el mejor de cada grupo, explora más.
- Cruce de dos puntos, mutación por inversión de bits.
- Proporción de bits activos al inicio: parámetro crítico en todos los experimentos.

> **Gambini (j): inconsistencia en la Figura 4.2.**
> La figura mostraba cinco variables y un cromosoma de siete bits. Corregida: siete variables, y 1100101 decodifica en X1, X2, X5 y X7, como en el ejemplo del texto. La presentación no usa esa figura.

------------------------------------------------------------------------

## 15 · Tres criterios de mejora

- Definición operativa, no respuesta: desempeño, reducción, estabilidad.
- Antes del AG, prueba de Fajardo: MLP con sintéticos contra MLP con reales.

> **Dra. Chan (e): qué significa "mejora en la selección de características".**
> Tres criterios operativos, enunciados en la metodología del capítulo 4, que no se mueven juntos: desempeño predictivo (exactitud en testeo original), reducción de variables (características medias de la población final, penalizadas en la aptitud con igual peso) y estabilidad (dispersión de exactitud y de variables entre corridas). El balance por conjunto está en la diapositiva 38.

------------------------------------------------------------------------

## 16 · Organización

- "Materiales y métodos: datos, línea base, modelos y diseño experimental."

------------------------------------------------------------------------

## 17 · Cinco conjuntos

- Leukemia (Golub), GCM (Ramaswamy, 14 tumores), ALL Leukemia (Yeoh, entró al final).
- Madelon: 5 relevantes, 15 combinaciones, 480 aleatorias. Gisette: dígitos 4 y 9.
- Particiones originales respetadas en todos los experimentos.

------------------------------------------------------------------------

## 18 · Línea base

- Dieciocho modelos, grilla, partición 80/20 propia.
- Leukemia y Gisette sin margen; Madelon y GCM con margen.
- En GCM hay clases con F1 cero: nunca se predicen.

> **Gambini (h): el SGD no es un clasificador.**
> Tiene razón: es un método de optimización. Lo usado es el `SGDClassifier` de scikit-learn, un clasificador lineal entrenado con descenso de gradiente estocástico. El texto corregido lo presenta así.

> **Gambini (i): descripción superficial de los métodos clásicos.**
> Es cierto; su función es dar la línea de base sobre el espacio completo y dimensionar la dificultad de cada conjunto. El aporte está en la integración AV+AG de los capítulos 3 y 4. Reconocerlo sin justificarse de más.

------------------------------------------------------------------------

## 19 · Arquitectura

- De dos capas a tres con normalización por lotes.
- MSE más KL; Adam; parada temprana con paciencia 10.
- Dropout y L1 se probaron y no aportaron.

------------------------------------------------------------------------

## 20 · Función de aptitud

- Mitad exactitud, mitad reducción: sacrifica exactitud por diseño.
- Ejemplo: 100% con todas las variables da 0,5; 80% con el 20% da 0,8.
- Genes activos al inicio: 10% en general, hasta 0,3% en GCM y ALL.

------------------------------------------------------------------------

## 21 · Diseño experimental

- Cada punto es una corrida completa del AG; exactitud en testeo original.
- Valores p con las corridas como n: corrige un test de la tesis, la conclusión no cambia.
- Decirlo antes de que lo pregunten.

------------------------------------------------------------------------

## 22 · Flujo en tres etapas

- Nació del fracaso de la primera etapa de GCM.
- Si no aprende 16.063 variables con 133 muestras, que aprenda 1.600.

------------------------------------------------------------------------

## 23 · Organización

- "Resultados: calidad de los sintéticos, resultados globales, después cada conjunto."

------------------------------------------------------------------------

## 24 · MLP con sintéticos

- Leukemia 0,95 contra 0,81. Madelon 0,57 contra 0,55. GCM 0,54 en ambos. Gisette 0,95 contra 0,97.
- Es la condición previa, no el resultado de la tesis.

------------------------------------------------------------------------

## 25 · Umbral de muestras

- Pasado el umbral, los sintéticos sobreajustan al generador.
- Latente compacto generalizó mejor (Ai 2023, contra Boom 2021).
- Se calibra por problema: limitación.

------------------------------------------------------------------------

## 26 · Resultados globales

- Significativo en Madelon (+7,8 pp) y en GCM segunda etapa (+4,4 pp).
- En los otros tres, sin cambio. Decirlo de entrada.
- Welch con corridas como n; Mann-Whitney coincide.

> **Dr. Quiroga (d): analizar primero los resultados de forma global.**
> Incorporado en el orden de la exposición: una tabla con los cinco conjuntos, después el gráfico de diferencias con intervalos de confianza, después la regla que resume todo, y recién entonces los dos casos que la explican, Madelon y GCM.

------------------------------------------------------------------------

## 27 · Intervalos de confianza

- Madelon y GCM excluyen el cero.
- Leukemia y Gisette: intervalos mínimos, nada que mejorar.
- ALL y GCM anchos: pocas corridas; test de 57 muestras, 1,75 pp por muestra.

------------------------------------------------------------------------

## 28 · Escala común

- Pedida por el jurado: Leukemia y Gisette se superponen por completo.
- Regla con dos condiciones: margen de mejora y reconstrucción adecuada.

> **Dr. Quiroga (c): unificar las escalas de los gráficos de exactitud.**
> Tiene razón: la Figura 4.16 usaba un eje distinto por panel y agrandaba diferencias no significativas. Para la defensa, dos gráficos: eje común de 0,4 a 1,0 (esta diapositiva) y diferencia en puntos porcentuales con IC 95% (la anterior). Si señalan "Precisión" en los ejes de la tesis: error de rótulo, la métrica es exactitud.

------------------------------------------------------------------------

## 29 · Madelon

- 0,750 a 0,828; desvío 0,038 a 0,023; menos variables.
- 2.000 sintéticos, 30 generaciones.
- Capítulo 2 reporta AUC en otra partición: referencia de orden, no comparación directa.

------------------------------------------------------------------------

## 30 · Interpretación de Madelon

- Latente de 25: no puede memorizar 480 variables de ruido, las deja cerca de la media.
- Conserva las 20 informativas: al AG le llega más señal.

------------------------------------------------------------------------

## 31 · GCM primera etapa

- No mejoró: 0,538 a 0,512, dispersión similar.
- Cromosomas de 20% y 30% daban 0,2 a 0,35; por eso 10%.

------------------------------------------------------------------------

## 32 · Diagnóstico

- Ajusta los sintéticos a la perfección; en reales queda igual que sin aumentación.
- Colapso de la posterior: la KL domina.
- Dos salidas: reponderar la KL (futuro) o reducir antes de generar (elegida).

------------------------------------------------------------------------

## 33 · GCM segunda etapa

- AVC sobre las 1.600 más frecuentes, 3.000 muestras balanceadas, cromosomas ~450 y ~750.
- 0,497 a 0,541, p = 0,005. Mejora de exactitud, no de reducción.
- Dispersión sube (0,033 contra 0,022): pocas corridas, test de 57. Con 6.000 muestras se degradó.

------------------------------------------------------------------------

## 34 · Reducción del cromosoma

- De 16.063 a 45 genes, exactitud aceptable.
- Media con aumentación arriba en los cuatro tamaños; solo ~450 significativo, 5 contra 5.
- Tendencia, no confirmación.

------------------------------------------------------------------------

## 35 · ALL Leukemia

- Con 35 y 180 genes arriba, con 300 abajo; nada significativo, 5 a 8 corridas.
- Flujo viable en un segundo problema; menor dispersión (0,056 contra 0,065).
- Moderado, como pide la Dra. Chan.

> **Dra. Chan (f), aplicada a ALL Leukemia.**
> La tesis dice que la combinación "incrementa la precisión de manera consistente"; los datos dan +1,7 y +0,9 puntos con p mayor a 0,4, y con 300 genes los originales fueron mejores. Decir: "no se observaron diferencias significativas; la tendencia favorable en 35 y 180 genes no alcanza significación".

------------------------------------------------------------------------

## 36 · Conjuntos saturados

- Leukemia: 80.742 pares de genes con correlación mayor a 0,7; cualquier 10% clasifica.
- Gisette: subconjunto algo más chico y más estable.

------------------------------------------------------------------------

## 37 · Evaluación por criterio

- Saturados: solo estabilidad. Gisette y Madelon: además menos variables.
- GCM: gana exactitud, pierde estabilidad. Reconocerlo.

> **Dra. Chan (e), balance por conjunto.**
> Leukemia: sin diferencia, igual reducción, mejora estabilidad. Gisette: sin diferencia, menos variables, estabilidad leve. Madelon: mejora en los tres. GCM: mejora exactitud, igual reducción, empeora estabilidad. ALL Leukemia: sin diferencia, igual reducción, estabilidad leve. La distinción favorece: permite decir qué mejoró en cada caso en vez de un "mejora" genérico.

------------------------------------------------------------------------

## 38 · Síntesis

- La regla en tres líneas es lo que el jurado va a recordar.
- La tercera, el flujo en tres etapas, es el aporte propio.

------------------------------------------------------------------------

## 39 · Organización

- "Conclusiones, limitaciones y trabajos futuros."

------------------------------------------------------------------------

## 40 · Conclusiones

- En orden de solidez; la cuarta es el aporte metodológico.
- De palabra: existe un umbral de sintéticos; arquitecturas simples rinden igual o mejor.

------------------------------------------------------------------------

## 41 · Limitaciones

- No es una receta universal.
- Pocas corridas explican ALL y el intervalo ancho de GCM.
- De palabra: SMOTE no se corrió en el mismo flujo; es trabajo futuro inmediato.

> **Dra. Chan (f): limitaciones de generalización y conclusiones moderadas.**
> Con evidencia significativa se sostienen dos conclusiones: Madelon y GCM segunda etapa. En los otros tres solo menor dispersión y, en Gisette y Madelon, subconjuntos más compactos. Cinco limitaciones: cinco conjuntos, dos artificiales; pocas corridas y testeos chicos en GCM y ALL; el efecto depende de la calidad del AV (GCM primera etapa empeoró); umbral de muestras sintéticas (6.000 en GCM degradó); un solo clasificador en la aptitud e hiperparámetros ajustados por conjunto. Los porcentajes relativos de la tesis (10,4% y 8,85%) se dan junto a los puntos porcentuales (7,8 y 4,4).

------------------------------------------------------------------------

## 42 · Trabajos futuros

- Si hay que elegir uno: KL recocida contra el colapso de la posterior, podría evitar las tres etapas.
- El cuarto viene de la sugerencia del Dr. Quiroga.

------------------------------------------------------------------------

## 43 · Cierre

- Agradecer.
- Respaldo disponible: estado del arte, SMOTE, test de GCM, línea base, por clase.

------------------------------------------------------------------------

## R1 · Estado del arte

- El objetivo era medir la aumentación sobre el mismo AG, no superar a Ramaswamy.
- La aptitud penaliza variables: iguala o supera al MLP con 0,6% a 10% de las características.

> **Dr. Quiroga (a), frente a la literatura externa.**
> GCM: Ramaswamy 78% con SVM sobre los 16.063 genes; nuestro 54% usa 450 a 780 genes y una aptitud que penaliza variables con peso 0,5. Madelon: los ganadores de NIPS 2003 rondan 93% de exactitud balanceada; nuestro 83% con 29 variables supera a 16 de los 18 clásicos del capítulo 2 (cifra de NIPS pendiente de verificar en Guyon 2004). Leukemia: Golub con 50 genes; nosotros 30 a 65 en el mismo rango. Si insisten en el capítulo 2: mostrar R4 y aclarar que métricas y particiones difieren; no convertir AUC en exactitud.

------------------------------------------------------------------------

## R2 · SMOTE

- No se corrió; se reconoce.
- Blagus y Lusa es justamente el escenario de los tres conjuntos genómicos.

------------------------------------------------------------------------

## R3 · Test en GCM

- El script de la tesis usó como n las observaciones.
- Con corridas: Welch 0,005 y Mann-Whitney 0,005; toda la etapa 0,008 y 0,011.

------------------------------------------------------------------------

## R4 · Línea base completa

- Solo si piden un modelo concreto.
- Algunos no se evaluaron en GCM y Gisette: dimensionalidad y multiclase.

> **Gambini (i), si piden un modelo concreto.**
> Para cada familia se citan los supuestos centrales y la referencia general (Hastie, Tibshirani y Friedman, 2009). Lo que importa poder explicar: por qué algunos modelos no se evaluaron en GCM y Gisette.

------------------------------------------------------------------------

## R5 · Por clase

- Con sintéticos varias clases llegan a precisión 1,00 pero cae el recall: modelo más conservador.
- Clases 7 y 3 empeoran; la 12 duplica su F1.

------------------------------------------------------------------------

## R6 · Antecedentes: AV para aumentación y AV con AG

- Fajardo 2021: AVC mejor generador que GAN, SMOTE y sobremuestreo; de ahí la prueba del capítulo 3.
- Ai 2023 y Khmaissia-Frigui 2023: AV guiados superan a otros sobremuestreos.
- Martins 2022: AV + AG, pero para diseño de proteínas; el más cercano.
- Ninguno combina AV y AG para selección de características: ese es el aporte.

------------------------------------------------------------------------

## R7 · Origen de la pérdida: el límite inferior de evidencia (ELBO)

- Solo si preguntan de dónde sale la pérdida de la 11. Cuatro pasos, en orden.
- 1 Objetivo: máxima verosimilitud, θ que haga probable lo observado.
- 2 Impedimento: p_θ(x) es una integral sobre z que no se puede calcular (red adentro; z de decenas de dimensiones; casi ningún z del prior produce x). No se calcula, luego no se deriva.
- 3 Sustituto: ELBO. Un z sorteado del codificador en vez de todos los z del prior; KL cerrada. Calculable y derivable.
- 4 Alcance: cota, no la verosimilitud; la brecha es el error del codificador respecto de la posterior verdadera.
- Cierre: −ELBO = error cuadrático + KL, la pérdida de la 11. Dos términos en tensión; en GCM primera etapa la KL dominó.

> **Gambini (g): la factorización p(x,z) = p(x|z) p(z) no es la regla de Bayes.**
> Corregido: ahora se presenta como regla del producto, de la que se deriva la regla de Bayes. No discutirlo.

