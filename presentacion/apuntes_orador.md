# Apuntes de orador

Una entrada por diapositiva. El número es el del pie de la diapositiva proyectada.

Los bloques en cita son observaciones del jurado, con el autor y la letra que tiene la respuesta larga en `Respuesta_observaciones_jurado.md`, seguidas de la respuesta en versión compacta. Van en la diapositiva donde conviene tenerlas a mano.

-------------------------------------------

## 0 · Portada

- Saludo. Agradecer al jurado la lectura y las observaciones; al director y codirector.
- Desafio: problema dificil y cross-industria 
- Solución via 2 arquitecturas: AV + AG

> Cuando tengo muchas variables es dificil predecir bien (modelar), pero cuando además de muchas variables tengo pocas observaciones el desafío es doble. 

> La selección de características ayuda a resolver el problema, pero necesita necesita que la ayudemos con el segundo: ¿como multiplicamos información escaza?

> La solución es: 
>    1) resolver la escasez = generando más información
>    2) resolver la dimensionalidad = seleccionando lo importante

-------------------------------------------

## 1 · Organización

- La mayor parte del tiempo va a resultados.
- Conclusiones cortas, como guía para la discusión.

-------------------------------------------

## 2 · Datos y Selección de características

- Alta dimensionalidad implica espacios de variables intratables en la práctica.
- Seleccion de características: proceso de detectar las ca-
racterísticas relevantes y descartar aquellas irrelevantes o redundantes, con el objetivo de obtener un subconjunto que describa adecuadamente un problema dado con una degradación mínima del rendimiento. 

-------------------------------------------

## 3 · Alta dimensionalidad y escasez muestral 

- De los tres aspectos de complejidad, solo la escasez muestral se ataca con aumentación.
- Sobreajuste model -> baja generalización 
- Sub-ajustado model -> baja precisión
- Desbalance: muestreo y modificación del algoritmo, los dos dentro del autocodificador.

-------------------------------------------

## 4 Formas de Resolver la alta Dimensionalidad

- Capturan interacciones, pero 2ⁿ subconjuntos: con 16.063 genes, intratable.
- Heurística elegida: algoritmos genéticos (Vignolo y Gerard, 2017).

-------------------------------------------

## 5 · Aptitud acotada por los datos

- Punto de partida del aporte.
- Con pocos datos la aptitud es ruidosa: convergencia prematura o sobreajuste.
- El problema no es el algoritmo, es la calidad de la evaluación.
- Lectura del gráfico: puntos vacíos, población inicial al azar; puntos llenos, población final. Con datos suficientes la aptitud estimada coincide con la real y la población final se concentra en la zona alta. Con pocos datos la estimación es irregular y la población final se concentra en un máximo espurio: una solución que solo parece satisfactoria.
- No es una trayectoria: el AG mueve una población, la selección la concentra. Paisaje de aptitud = metáfora clásica (Wright 1932, Goldberg); la recta es una proyección de un espacio de 2ⁿ cadenas con distancia de Hamming.
- No decir "óptimo": el AG es una heurística; busca soluciones satisfactorias. Por eso el resultado es una distribución de corridas y una frecuencia de activación, no un subconjunto único.

-------------------------------------------

## 6 · Formas de Resolver la escacez muestral 

- Por qué AV y no SMOTE: Blagus y Lusa (no aporta en alta dimensión), Fajardo (AVC mejor generador), Ai.
- SMOTE solo rebalancea; acá también se aumentan problemas balanceados.
- Qué significa «todas las distancias resultan casi iguales» (concentración de distancias): con pocas observaciones en miles de dimensiones, la distancia de una observación a su vecino más cercano y a su vecino más lejano casi no difieren; entonces «el más cercano» es casi arbitrario. Y como casi todas las variables son ruido, el vecino lo deciden las variables ruidosas, no las pocas discriminantes. SMOTE interpola entre dos puntos elegidos así: el sintético no aporta información nueva sobre la clase.
- Decir: «SMOTE elige al vecino por distancia; con miles de variables y decenas de observaciones esa distancia ya no distingue vecinos cercanos de lejanos».
- Respaldo R2 si preguntan.

> **Dr. Quiroga (b): comparar con SMOTE y otros métodos de aumentación.**
> La tesis no corrió SMOTE; se reconoce como limitación. La elección se apoyó en tres resultados: Blagus y Lusa (SMOTE no aporta en alta dimensión con pocas muestras, el escenario de los tres conjuntos genómicos), Fajardo (AV condicional mejor que SMOTE y GAN) y Ai (AV guiados superan a otros sobremuestreos). SMOTE rebalancea clases; acá se aumenta también en problemas balanceados. AV contra SMOTE en el mismo flujo: trabajo futuro inmediato.

-------------------------------------------

## 7 · Propuesta

- El AV se entrena solo con la partición de entrenamiento.
- El AG recibe originales más sintéticos.
- La exactitud se mide siempre en la partición original de testeo.

-------------------------------------------

## 8 · Objetivos

- Tercer objetivo: comparar con y sin aumentación, mismo AG, mismos parámetros.
- No es una carrera contra el estado del arte.

> **Dr. Quiroga (a): comparar con el estado del arte del capítulo 2.**
> El objetivo fue medir el impacto de la aumentación sobre un mismo AG. La comparación con el capítulo 2 tiene una limitación: allí se reporta AUC y macro-F1 sobre una partición 80/20 propia; en el capítulo 4, exactitud sobre la partición original de testeo. La comparación válida es con el MLP del capítulo 3: el flujo AV+AG lo iguala o supera en los cinco conjuntos con el 0,6% a 10% de las características. Detalle en R1.


-------------------------------------------

## 9 · Organización

- "Marco teórico: el autocodificador variacional, el algoritmo genético y los criterios de evaluación."

-------------------------------------------

## 10 · Autocodificador

- Codificador y decodificador entrenados juntos minimizando el cuadrado de la distancia euclídea entre entrada y reconstrucción (suma de errores cuadráticos; no es la media, MSE, aunque PyTorch lo llame así).
- Latente discontinuo: muestrear en regiones no usadas da salidas sin relación con los datos.
- Por eso no sirve como generador.

> **Gambini (g): notación del codificador y pérdida de reconstrucción.**
> Corregido: el codificador es C_θ en todo el texto (antes alternaba con E_θ); la pérdida es el cuadrado de la distancia euclídea, no la distancia. Agradecer y decir que está incorporado, sin más.

-------------------------------------------

## 11 · Autocodificador variacional

- Cada observación se codifica como una distribución: medias y desvíos.
- Reparametrización: permite retropropagar a través del muestreo.
- Generar: z de la normal estándar, pasar por el decodificador.
- Dos términos en tensión; dejar plantado: en GCM primera etapa la KL dominó.
- KL = divergencia de Kullback-Leibler ("Kúlbac-Láibler"): ≥ 0, cero solo si las distribuciones coinciden, no simétrica (las barras ordenan: codificada respecto de N(0, I)). Para dos normales: ½ Σ (μ² + σ² − 1 − log σ²). La D de la fórmula es solo el decodificador.
- Origen de la pérdida (negativo del ELBO): no mencionar; si preguntan, R7.
- Si notan que θ y φ se intercambian respecto de la 10 (allí C_θ/D_φ; acá q_φ/D_θ): es la notación de la tesis, capítulo 3. El autocodificador clásico sigue C_θ/D_φ; el variacional adopta la de Kingma y Welling, q_φ codificador y p_θ decodificador, para coincidir con la literatura del ELBO.
- Tira de dígitos: salida real de un AV chico (latente 2-D, 256 ocultas, 60 épocas, 5.000 MNIST) entrenado para la figura; doce puntos equiespaciados sobre una recta del latente. Contraste con la mancha de la 10.

- AV = Kingma y Welling 2013

-------------------------------------------

## 12 · AV condicional

- Para GCM (14 clases) y ALL Leukemia (7), desbalanceados.
- Muestreo ponderado: cada lote se arma con probabilidad ∝ 1/n_c; las clases chicas entran más veces y su error pesa más. Es el que balancea la pérdida.
- Pesos de clase (en la tesis, no en la filmina), w_c ∝ 1/n_c: factor sobre el término de reconstrucción. No decir "cada observación se pondera dentro del MSE". Se validaron junto con el muestreo; combinados dieron el mejor resultado.
- ¿Fijos o por lote? Fijos: w_c = 1/n_c calculado una vez sobre la partición de entrenamiento, antes de entrenar (`cvae_ga_template.py:89-95`). El muestreador los usa para armar cada mini-lote (1.024, con reposición) con las clases equilibradas; la pérdida los aplica como factor sobre el término de reconstrucción. En la implementación ese factor es el promedio de los pesos del lote, casi constante porque el lote ya viene balanceado: `mean(SSE_lote × w)` con SSE ya sumada, no `Σ SSE_i × w_i`. Consecuencias: (a) la ponderación por observación no existe; el balance lo da el muestreador; (b) el factor ≈ media de 1/n_c (GCM: 14 clases, n_c de 8 a 24, ≈ 0,11–0,14) escala la reconstrucción hacia abajo: equivale a un β-VAE con β ≈ 7–9, es decir, la KL pesa 7 a 9 veces más que en la formulación estándar. Respuesta si preguntan cómo entran los pesos: "como factor sobre el término de reconstrucción del lote; el equilibrio entre clases lo garantiza el muestreador ponderado". No afirmar que cada observación se pondera individualmente.
- Salvedad (no decir, saber): este código es el de la segunda etapa (subespacio GCM y ALL). El AVC de la primera etapa sobre el espacio completo (`exp_42`) se entrenó sin pesos ni muestreador.

-------------------------------------------

## 13 · Algoritmo genético

- Individuo = solución candidata (subconjunto de variables en bits), no una observación.
- Aptitud del individuo = > probabilidad de supervivencia y reproducción.
- Población, aptitud, selección, cruce, mutación, hasta terminar.
- Sirve en espacios discretos, no diferenciables, multimodales.
- La diversidad evita la convergencia prematura.


> Los AG son una clase de algoritmo inspirado en la evolución biológica y en la teoría de la selección natural. 

> evolución de una población de soluciones potenciales a lo largo de múltiples generaciones. 

> Utilizando operadores genéticos como la selección, el cruce y la mutación los AG generan nuevas soluciones a partir de las disponibles.

> formulados por Holland, Universidad de Michigan, 1975, y difundidos por su discípulo Goldberg. Es una familia de algoritmos (ej.colonias de hormigas, abejas, etc.)

-------------------------------------------

## 14 · Cromosoma binario y operadores

- 7.129 bits en Leukemia, 16.063 en GCM.
- Selección por torneo (de 5): k al azar, pasa el mejor; equilibra explotación y exploración. Ruleta: proporcional a la aptitud, pierde diversidad. Ventana: el mejor de cada grupo, explora más.
- Cruce de dos puntos, mutación por inversión de bits.
- Proporción de bits activos al inicio: parámetro crítico en todos los experimentos.

> **Gambini (j): inconsistencia en la Figura 4.2.**
> La figura mostraba cinco variables y un cromosoma de siete bits. Corregida: siete variables, y 1100101 decodifica en X1, X2, X5 y X7, como en el ejemplo del texto. La presentación no usa esa figura.

-------------------------------------------

## 15 · Tres criterios de mejora

- Definición operativa, no respuesta: desempeño, reducción, estabilidad.
- Antes del AG, prueba de Fajardo: MLP con sintéticos contra MLP con reales.

> **Dra. Chan (e): qué significa "mejora en la selección de características".**
> Tres criterios operativos, enunciados en la metodología del capítulo 4, que no se mueven juntos: desempeño predictivo (exactitud en testeo original), reducción de variables (características medias de la población final, penalizadas en la aptitud con igual peso) y estabilidad (dispersión de exactitud y de variables entre corridas). El balance por conjunto está en la diapositiva 38.

-------------------------------------------

## 16 · Organización

- "Materiales y métodos: datos, línea base, modelos y diseño experimental."

-------------------------------------------

## 17 · Cinco conjuntos

- Leukemia (Golub), GCM (Ramaswamy, 14 tumores), ALL Leukemia (Yeoh, entró al final).
- Madelon: 5 relevantes, 15 combinaciones, 480 aleatorias. Gisette: dígitos 4 y 9.
- Particiones originales respetadas en todos los experimentos.

**Clases por conjunto (contadas en los ARFF de `ealab/data`)**

- Leukemia: leucemia aguda: linfoblástica vs mieloide . 
- ALL Leukemia: 7 subtipos de leucemia. 
- GCM: 14 tipos de tumor: leucemia 24, linfoma 16, sistema nervioso central 16, los otros 11 con 8 cada uno (mama, próstata, pulmón, colorrectal, vejiga, melanoma, útero, riñón, páncreas, ovario, mesotelioma). Testeo 46: entre 2 y 6 por clase.
- Gisette: dígitos 4 y 9.

-------------------------------------------

## 18 · Línea base

- Dieciocho modelos, grilla, partición 80/20 propia.
- Leukemia y Gisette sin margen; Madelon y GCM con margen.
- En GCM hay clases con F1 cero: nunca se predicen.

**Cómo nombrar la métrica**

- Primera vez: "área bajo la curva ROC"; después, "AUC". Es un área entre 0 y 1, no un porcentaje: decir "entre 0,85 y 1,00", nunca "85 de precisión".
- Frase: "La métrica es el área bajo la curva ROC, AUC. En Leukemia la mayoría de los modelos clásicos obtiene valores entre 0,85 y 1, y tres de ellos llegan a 1: el problema está cerca de saturar."
- Lectura intuitiva, si la piden: probabilidad de que el modelo asigne una puntuación mayor a una observación positiva que a una negativa; 1 es separación perfecta, 0,5 es azar. Palabra genérica: "desempeño" o "capacidad de discriminación".
- No decir "precisión" ni "exactitud": son métricas con definición propia (precisión = positivos predichos que son correctos; exactitud = proporción de aciertos, la que usa el AG como aptitud). Los porcentajes quedan para la exactitud del AG en el capítulo 4.
- GCM: "macro-F1", media del F1 por clase, mismo peso para cada clase sin importar su tamaño; por eso se ve que Breast o Prostate tienen F1 cero.

> **Gambini (h): el SGD no es un clasificador.**
> Tiene razón: es un método de optimización. Lo usado es el `SGDClassifier` de scikit-learn, un clasificador lineal entrenado con descenso de gradiente estocástico. El texto corregido lo presenta así.

> **Gambini (i): descripción superficial de los métodos clásicos.**
> Es cierto; su función es dar la línea de base sobre el espacio completo y dimensionar la dificultad de cada conjunto. El aporte está en la integración AV+AG de los capítulos 3 y 4. Reconocerlo sin justificarse de más.

-------------------------------------------

## 19 · Arquitectura

- De dos capas a tres con normalización por lotes.
- Columna "Entrada (capa 1)": es la dimensión de las características, no una capa con pesos; sirve para leer la compresión hasta el latente (Leukemia 7.129 → 108, unas 66 veces; GCM 16.063 → 35, unas 460 veces; Gisette 5.000 → 18, unas 280 veces). "Tres capas" = capas ocultas, sin contar la entrada ni las cabezas de μ y log σ². En las ecuaciones del capítulo 3 la entrada es x y h₁ es la capa 2 de la tabla.
- Error cuadrático (suma, no media) más KL; Adam; parada temprana con paciencia 10. En la filmina dice "error cuadrático" a secas, a propósito.
- Dropout y L1 se probaron y no aportaron.
- Puente con la 11 (σ allá, log σ² acá): "El codificador "la media y el logaritmo de la varianza"

**Si preguntan por qué MSE**

- Qué mide: la diferencia entre cada observación y su reconstrucción, elevada al cuadrado y sumada sobre todas las variables y todas las observaciones. Es la distancia entre la entrada y la salida.
- Por qué cuadrático y no otra cosa: la pérdida del AV tiene dos términos, reconstrucción y KL. El error cuadrático es el término de reconstrucción que corresponde a datos continuos (se asume que cada observación se distribuye normal alrededor de su reconstrucción). Si los datos fueran binarios, 0 o 1, el término sería entropía cruzada. Nuestros datos son continuos y estandarizados, por eso error cuadrático.
- Por qué suma y no promedio: para que quede en la misma escala que la KL, que también es una suma; no hay un peso β entre ambos términos. "MSE" es el nombre que usa la tesis (y la función de PyTorch, `MSELoss`), configurada con `reduction="sum"`: error cuadrático sumado sobre variables y lote, que es el cuadrado de la distancia euclídea de la filmina 10. Con el promedio la reconstrucción pesaría miles de veces menos y la KL dominaría.
- Desbalance, dos mecanismos: muestreo ponderado por clase en cada lote (es el que efectivamente balancea la contribución de cada clase a la pérdida) y un factor de peso de clase sobre el término de reconstrucción. Validados juntos; la combinación dio la mejor reconstrucción de las clases minoritarias.
- L1 se probó sin beneficio claro.

-------------------------------------------

## 20 · Función de aptitud

- Mitad exactitud, mitad reducción: sacrifica exactitud por diseño.
- Ejemplo: 100% con todas las variables da 0,5; 80% con el 20% da 0,8.
- Genes activos al inicio: 10% en general, hasta 0,3% en GCM y ALL.

**Si preguntan por qué no colapsa a cero variables**

- Descartar sube f solo mientras la exactitud no caiga. Sin genes informativos, la exactitud baja al azar (≈0,55 en Leukemia) y f ≈ 0,78; con 5 genes con señal y 0,95 de exactitud, f ≈ 0,97.
- Con α = 0,5 el óptimo es "lo mínimo que todavía clasifica bien". Con α mucho menor colapsaría a cero; con α mucho mayor no reduciría.

-------------------------------------------

## 21 · Diseño experimental

- Cada punto es una corrida completa del AG; exactitud en testeo original.
- Valores p con las corridas como n: corrige un test de la tesis, la conclusión no cambia.
- Decirlo antes de que lo pregunten.

**Qué se mide exactamente**

- Por individuo: MLP pequeño (5 y 3 neuronas, tanh) entrenado con las variables activas sobre la partición de entrenamiento (originales, o originales + sintéticas); exactitud sobre la partición original de testeo; f = 0,5 · exactitud + 0,5 · (1 − k/n).
- La unidad de análisis es la corrida completa del AG; su valor es la exactitud media de la población final, medida en la partición original de testeo. Se comparan las distribuciones de esas corridas entre los dos grupos.

-------------------------------------------

## 22 · Flujo en tres etapas

- Nació del fracaso de la primera etapa de GCM.
- Si no aprende 16.063 variables con 133 muestras, que aprenda 1.600.
- Lectura del diagrama: es el de la 21; lo nuevo es el recuadro verde, que entra entre los datos originales y el AVC. Señalarlo: "entre el paso 1 y el 2 intervino una selección". No es una corrida nueva del AG: se consolidaron los experimentos previos (590 cromosomas en GCM) y se tomaron las características más frecuentes. Etapas: selección previa (verde), generación (AVC), selección final (AG).
- línea de investigación malograda por 'filtracion de datos'.



-------------------------------------------

## 23 · Organización

- "Resultados: calidad de los sintéticos, resultados globales, después cada conjunto."

-------------------------------------------

## 24 · MLP con sintéticos

- Leukemia 0,95 contra 0,81. Madelon 0,57 contra 0,55. GCM 0,54 en ambos. Gisette 0,95 contra 0,97.
- Es la condición previa, no el resultado de la tesis.
- Protocolo de Fajardo et al. 2021 (tesis, cap. 3): un MLP entrenado solo con sintéticos y otro solo con reales, ambos evaluados en la misma partición original de testeo. Si rinden parecido, el generador capturó la estructura de los datos. Fajardo lo usó para AV condicionales sobre MNIST desbalanceado.
- Leukemia 0,95 contra 0,81 no es "lo sintético es mejor": el MLP con reales tiene 11 AML; con sintéticos ve cientos y el recall de AML sube de 0,56 a 0,89. Efecto de cantidad y balance; el testeo (34 originales) nunca lo vio el AV.

-------------------------------------------

## 25 · Umbral de muestras

- Pasado el umbral, los sintéticos sobreajustan al generador.
- Latente compacto generalizó mejor (Ai 2023, contra Boom 2021).
- Cantidad de sintéticos: barrido por conjunto (`ealab/exp`). Leukemia 100–300 (sobre 38 de entrenamiento); Madelon 2.000 y Gisette 6.000 (igual al entrenamiento); GCM 190, 200, 400, 1.400, 3.000, 6.000 (el más sistemático); ALL Leukemia 3.000.
- Criterio: igualar las clases, como Fajardo; en multiclase ~200 por clase (GCM 3.000/14 = 214). Pasado el umbral (6.000 en GCM) la exactitud cae.
- Respuesta a "¿cómo eligieron la cantidad?": barrido por conjunto, criterio de balance, umbral medido. No hay regla general entre conjuntos: eso sí es limitación.
- Pendiente: la tesis dice 1.000 sintéticos en ALL Leukemia; `exp_53` tiene 3.000. Confirmar cuál se usó en el AG.

-------------------------------------------

## 26 · Resultados globales

- Significativo en Madelon (+7,8 pp) y en GCM segunda etapa (+4,4 pp).
- En los otros tres, sin cambio. Decirlo de entrada.
- Welch con corridas como n; Mann-Whitney coincide.

> **Dr. Quiroga (d): analizar primero los resultados de forma global.**
> Incorporado en el orden de la exposición: una tabla con los cinco conjuntos, después el gráfico de diferencias con intervalos de confianza, después la regla que resume todo, y recién entonces los dos casos que la explican, Madelon y GCM.

-------------------------------------------

## 27 · Intervalos de confianza

- Madelon y GCM excluyen el cero.
- Leukemia y Gisette: intervalos mínimos, nada que mejorar.
- ALL y GCM anchos: pocas corridas; test de 57 muestras, 1,75 pp por muestra.

>"El intervalo del 95 % es el rango de valores que la diferencia verdadera podría tener según estas corridas; si incluye el cero, no hay evidencia de efecto."

-------------------------------------------

## 28 · Escala común

- Pedida por el jurado: Leukemia y Gisette se superponen por completo.
- Regla con dos condiciones: margen de mejora y reconstrucción adecuada.

**Qué es "exactitud" en el eje**

- Cada punto es una corrida completa del AG; su valor es `pob_accuracy_avg`: la exactitud media de la población final, medida en la partición original de testeo. 
- Es la media de la población final, no la del mejor individuo. 
- En GCM y ALL Leukemia es exactitud balanceada (media de la sensibilidad por clase); en los binarios, exactitud simple. 

> **Dr. Quiroga (c): unificar las escalas de los gráficos de exactitud.**
> Tiene razón: la Figura 4.16 usaba un eje distinto por panel y agrandaba diferencias no significativas. Para la defensa, dos gráficos: eje común de 0,4 a 1,0 (esta diapositiva) y diferencia en puntos porcentuales con IC 95% (la anterior). Si señalan "Precisión" en los ejes de la tesis: error de rótulo, la métrica es exactitud.

-------------------------------------------

## 29 · Madelon

- 0,750 a 0,828; desvío 0,038 a 0,023; menos variables.
- 2.000 sintéticos, 30 generaciones.
- Capítulo 2 reporta AUC en otra partición: referencia de orden, no comparación directa.

-------------------------------------------

## 30 · Interpretación de Madelon

- Latente de 25: no puede memorizar 480 variables de ruido, las deja cerca de la media.
- Conserva las 20 informativas: al AG le llega más señal.

-------------------------------------------

## 31 · GCM primera etapa

- No mejoró: 0,538 a 0,512, dispersión similar.
- Cromosomas de 20% y 30% daban 0,2 a 0,35; por eso 10%.

-------------------------------------------

## 32 · Diagnóstico

- Ajusta los sintéticos a la perfección; en reales queda igual que sin aumentación.
- Hipótesis principal, sobreajuste: 133 observaciones en 16.063 dimensiones; la reconstrucción es una suma sobre 16.063 variables y la KL sobre 35, así que en magnitud domina la reconstrucción y lo natural es que el AVC memorice el entrenamiento. 
- Hipótesis de la tesis, colapso de la distribución posterior (la distribución del latente z que produce el codificador, q(z|x)). En términos simples: el codificador produce la misma distribución para todas las observaciones, exactamente la normal estándar; entonces la KL vale cero, la mejor nota posible en ese término, pero z deja de llevar información sobre x y el decodificador, que recibe siempre lo mismo, devuelve siempre lo mismo: algo parecido al promedio. 

-------------------------------------------

## 33 · GCM segunda etapa

- AVC sobre las 1.600 más frecuentes, 3.000 muestras balanceadas, cromosomas ~450 y ~750.
- 0,497 a 0,541, p = 0,005. Mejora de exactitud, no de reducción.
- Dispersión sube (0,033 contra 0,022): pocas corridas, test de 57. Con 6.000 muestras se degradó.

-------------------------------------------

## 34 · Reducción del cromosoma

- De 16.063 a 45 genes, exactitud aceptable.
- Media con aumentación (rombos) arriba en los cuatro tamaños; solo ~450 significativo, 5 contra 5.
- En ~200 la mediana con aumentación queda por debajo (0,479 contra 0,486): una corrida de 0,571 levanta la media, tres de cinco quedan bajo la mediana del otro grupo. La tesis lo dice ("a excepción del grupo de ~200"). Si preguntan: "con cinco corridas por grupo, una sola decide el signo; p = 0,38; en ese tamaño no hay diferencia defendible".
- Tendencia, no confirmación.

-------------------------------------------

## 35 · ALL Leukemia

- Con 35 y 180 genes arriba, con 300 abajo; nada significativo, 5 a 8 corridas.
- Flujo viable en un segundo problema; menor dispersión (0,056 contra 0,065).
- Moderado, como pide la Dra. Chan.

> **Dra. Chan (f), aplicada a ALL Leukemia.**
> La tesis dice que la combinación "incrementa la precisión de manera consistente"; los datos dan +1,7 y +0,9 puntos con p mayor a 0,4, y con 300 genes los originales fueron mejores. Decir: "no se observaron diferencias significativas; la tendencia favorable en 35 y 180 genes no alcanza significación".

-------------------------------------------

## 36 · Conjuntos saturados

- Leukemia: 80.742 pares de genes con correlación mayor a 0,7; cualquier 10% clasifica.
- Gisette: subconjunto algo más chico y más estable.

-------------------------------------------

## 37 · Evaluación por criterio

- Saturados: solo estabilidad. Gisette y Madelon: además menos variables.
- GCM: gana exactitud, pierde estabilidad. Reconocerlo.

> **Dra. Chan (e), balance por conjunto.**
> Leukemia: sin diferencia, igual reducción, mejora estabilidad. Gisette: sin diferencia, menos variables, estabilidad leve. Madelon: mejora en los tres. GCM: mejora exactitud, igual reducción, empeora estabilidad. ALL Leukemia: sin diferencia, igual reducción, estabilidad leve. La distinción favorece: permite decir qué mejoró en cada caso en vez de un "mejora" genérico.

-------------------------------------------

## 38 · Síntesis

- La regla en tres líneas es lo que el jurado va a recordar.
- La tercera, el flujo en tres etapas, es el aporte propio.

-------------------------------------------

## 39 · Organización

- "Conclusiones, limitaciones y trabajos futuros."

-------------------------------------------

## 40 · Conclusiones

- En orden de solidez; la cuarta es el aporte metodológico.
- De palabra: existe un umbral de sintéticos; arquitecturas simples rinden igual o mejor.

-------------------------------------------

## 41 · Limitaciones

- No es una receta universal.
- Pocas corridas explican ALL y el intervalo ancho de GCM.
- De palabra: SMOTE no se corrió en el mismo flujo; es trabajo futuro inmediato.

> **Dra. Chan (f): limitaciones de generalización y conclusiones moderadas.**
> Con evidencia significativa se sostienen dos conclusiones: Madelon y GCM segunda etapa. En los otros tres solo menor dispersión y, en Gisette y Madelon, subconjuntos más compactos. Cinco limitaciones: cinco conjuntos, dos artificiales; pocas corridas y testeos chicos en GCM y ALL; el efecto depende de la calidad del AV (GCM primera etapa empeoró); umbral de muestras sintéticas (6.000 en GCM degradó); un solo clasificador en la aptitud e hiperparámetros ajustados por conjunto. Los porcentajes relativos de la tesis (10,4% y 8,85%) se dan junto a los puntos porcentuales (7,8 y 4,4).

-------------------------------------------

## 42 · Trabajos futuros

- Si hay que elegir uno: KL con peso creciente durante el entrenamiento (KL annealing) contra el colapso de la posterior; podría evitar las tres etapas. No decir "recocida".
- El cuarto viene de la sugerencia del Dr. Quiroga.

-------------------------------------------

## 43 · Cierre

- Agradecer.
- Respaldo disponible: estado del arte, SMOTE, test de GCM, línea base, por clase.

-------------------------------------------

## R1 · Estado del arte

- El objetivo era medir la aumentación sobre el mismo AG, no superar a Ramaswamy.
- La aptitud penaliza variables: iguala o supera al MLP con 0,6% a 10% de las características.

> **Dr. Quiroga (a), frente a la literatura externa.**
> GCM: Ramaswamy 78% con SVM sobre los 16.063 genes; nuestro 54% usa 450 a 780 genes y una aptitud que penaliza variables con peso 0,5. Madelon: los ganadores de NIPS 2003 rondan 93% de exactitud balanceada; nuestro 83% con 29 variables supera a 16 de los 18 clásicos del capítulo 2 (cifra de NIPS pendiente de verificar en Guyon 2004). Leukemia: Golub con 50 genes; nosotros 30 a 65 en el mismo rango. Si insisten en el capítulo 2: mostrar R4 y aclarar que métricas y particiones difieren; no convertir AUC en exactitud.

-------------------------------------------

## R2 · SMOTE

- No se corrió; se reconoce.
- Blagus y Lusa es justamente el escenario de los tres conjuntos genómicos.

-------------------------------------------

## R3 · Test en GCM

- El script de la tesis usó como n las observaciones.
- Con corridas: Welch 0,005 y Mann-Whitney 0,005; toda la etapa 0,008 y 0,011.

-------------------------------------------

## R4 · Línea base completa

- Solo si piden un modelo concreto.
- Algunos no se evaluaron en GCM y Gisette: dimensionalidad y multiclase.

> **Gambini (i), si piden un modelo concreto.**
> Para cada familia se citan los supuestos centrales y la referencia general (Hastie, Tibshirani y Friedman, 2009). Lo que importa poder explicar: por qué algunos modelos no se evaluaron en GCM y Gisette.

-------------------------------------------

## R5 · Por clase

- Con sintéticos varias clases llegan a precisión 1,00 pero cae el recall: modelo más conservador.
- Clases 7 y 3 empeoran; la 12 duplica su F1.

-------------------------------------------

## R6 · Antecedentes: AV para aumentación y AV con AG

- Fajardo 2021: AVC mejor generador que GAN, SMOTE y sobremuestreo; de ahí la prueba del capítulo 3.
- Ai 2023 y Khmaissia-Frigui 2023: AV guiados superan a otros sobremuestreos.
- Martins 2022: AV + AG, pero para diseño de proteínas; el más cercano.
- Ninguno combina AV y AG para selección de características: ese es el aporte.

-------------------------------------------

## R7 · Origen de la pérdida: el límite inferior de evidencia (ELBO)

- Solo si preguntan de dónde sale la pérdida de la 11. Cuatro pasos, en orden.
- 1 Objetivo: máxima verosimilitud, θ que haga probable lo observado.
- 2 Impedimento: p_θ(x) es una integral sobre z que no se puede calcular (red adentro; z de decenas de dimensiones; casi ningún z del prior produce x). No se calcula, luego no se deriva.
- 3 Sustituto: ELBO. Un z sorteado del codificador en vez de todos los z del prior; KL cerrada. Calculable y derivable.
- 4 Alcance: cota, no la verosimilitud; la brecha es el error del codificador respecto de la posterior verdadera.
- Cierre: −ELBO = error cuadrático + KL, la pérdida de la 11. Dos términos en tensión; en GCM primera etapa la KL dominó.

> **Gambini (g): la factorización p(x,z) = p(x|z) p(z) no es la regla de Bayes.**
> Corregido: ahora se presenta como regla del producto, de la que se deriva la regla de Bayes. No discutirlo.

## R8 · Espacio latente del AV: malla sobre MNIST

- Solo si preguntan por la estructura del latente o por qué el AV sí genera. Leer con la 10 (hueco) y la 11 (recorrido recto).
- Malla 15 × 15, z₁ y z₂ entre −2,5 y 2,5, mismo AV mínimo de la 11. Regiones contiguas por dígito, transiciones graduales, sin huecos.
- Por qué: la KL mantiene las codificaciones cerca de N(0, I); el decodificador se entrena sobre todo el rango que después se muestrea.
- Borrosidad: dos dimensiones latentes son pocas; se eligieron para poder dibujar. En la tesis, latentes de 18 a 108.
- Misma figura que Kingma y Welling para MNIST.

-------------------------------------------

