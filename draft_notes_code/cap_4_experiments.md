# Experimentos realizados y sus resultados {#sec-Capitulo4}

En este capítulo se presentan los experimentos realizados en el marco de la investigación, cuyo objetivo principal fue evaluar la efectividad de la técnica de aumentación de datos en la selección de características mediante Algoritmos Genéticos (AGs) en contextos de escasez muestral y alta dimensionalidad. Para ello, se diseñaron y ejecutaron experimentos utilizando cuatro conjuntos de datos distintos: *Leukemia*, *Gisette*, *Madelon* y *GCM*, cada uno representando diferentes desafíos en términos de tamaño y características de los datos.

El enfoque experimental adoptado fue comparativo, contrastando el desempeño de los AGs en la selección de características utilizando datos originales frente a la misma tarea utilizando datos aumentados con muestras sintéticas generados por AVs. Los parámetros de los AGs fueron mantenidos constantes entre los grupos de experimentos con y sin aumento, permitiendo una evaluación directa del impacto de la aumentación.

La metodología seguida para cada experimento se describe a continuación. Se presentan los resultados obtenidos, incluyendo métricas como precisión en la clasificación, número de características seleccionadas y estabilidad de la selección de características a lo largo de las generaciones. Se discuten las implicaciones de los resultados y se proponen posibles ajustes y mejoras para futuros experimentos.

## Leukemia

### Metodología

Según lo visto en el Capítulo 1, el conjunto de datos *Leukemia* de expresión génica obtenidos de micro-datos de ADN es reconocido por su alta dimensionalidad (7129 mediciones) relativa al número de muestras (38 para entrenamiento y 34 para testeo). Esto lo convierte en un candidato apropiado para evaluar la capacidad de los AVs para generar datos sintéticos, a partir de los cuales aumentar el número de muestras disponibles y mejorar el desempeño de los AGs en la selección de características. Por ello, nuestros  experimentos estuvieron orientadod a comparar el rendimiento de los AGs sobre los datos originales y sobre un conjunto de datos aumentado con muestras sintéticas. Comparación que se realizó en términos de precisión en la clasificación, número de características seleccionadas y estabilidad de la selección de características.

Se diseñaron entonces experimentos utilizando el modelo de AG presentado en el Capítulo 3, con una representación binaria de las características. Se utilizó una función de aptitud basada en un clasificador MLP, que evaluó la precisión en la clasificación, penalizando el número de características seleccionadas. El objetivo del AG era encontrar un subconjunto óptimo de características que maximizara la precisión y minimizara la dimensión del espacio de características.

Como hemos señalado, la innovación en este enforque estuvo en el uso de un AV para enriquecer el proceso de entrenamiento del AG. El AV, según vimos en el Capítulo 2, fue optimizado para generar muestras sintéticas que preservaran la estructura subyacente de los datos originales, y permitiera al AG explorar un espacio de características más amplio y diverso. La idea era que, al aumentar el número de muestras disponibles, el AG pudiera identificar un subconjunto más efectivo de características, lo que se traduciría en una mejora en la precisión y la eficiencia de la selección de características.

La configuración experimental del AG que empleamos en Leukemia fue la siguiente:

- **Mutación:** PROB_MUT = 1/IND_SIZE (~0.0001)
- **Probabilidad de cruce:** PX = 0.75
- **Cromosoma activo:** p = 0.1
- **Número máximo de generaciones:** GMAX = 20

Se realizaron dos conjuntos de experimentos:

1. **Datos originales:** Se trabajó directamente con las muestras disponibles en el conjunto *leukemia*, siguiendo la partición original en un conjunto de entrenamiento y un conjunto de prueba.
2. **Datos aumentados:** Se generaron experimientos con 100, 200 y 1000 muestras sintéticas adicionales mediante un AV entrenado específicamente para este conjunto de datos.

La primera serie de experimentos con datos originales y datos aumentados tuvo por objetivo contar con una primera aproximación al problema y establecer una línea base a partir de la cual iterar con ajustes y mejoras en la configuración del AG y el AV. Luego, se realizaron experimentos adicionales para explorar diferentes configuraciones del AG y el AV, con el objetivo de identificar las condiciones óptimas para la selección de características en este conjunto de datos. Se investigó el impacto de variar la probabilidad de mutación, la probabilidad de cruce, el tamaño del cromosoma activo y el número de muestras generadas por el AV. Particularmente se exploró el impacto de la reducción del tamaño del cromosoma activo en la eficiencia de la selección de características, pasando de p = 0.01 a p = 0.005.

En el primer conjunto de experimentos, se estableció una configuración base utilizando una probabilidad de mutación de 0.01%, una probabilidad de cruce del 75%, y un cromosoma activo con un tamaño del 10% del total de características, limitado a un máximo de 20 generaciones. Esta configuración fue seleccionada para equilibrar la exploración y explotación del espacio de búsqueda, asegurando que el Algoritmo Genético (AG) pudiera explorar adecuadamente las posibles combinaciones de características sin prologar el procesamiento en exceso. Para los experimentos con aumentación de datos, se generaron 100 muestras sintéticas adicionales mediante un AV. En estas primeras pruebas los resultados mostraron que tanto la precisión como el número de genes seleccionados fueron similares entre los grupos con y sin aumentación de datos. Sin embargo, se destacó una menor dispersión en los resultados del grupo con aumentación, lo que sugirió que la generación de datos sintéticos contribuyó a una mayor estabilidad del modelo.

En un segundo grupo de experimentos exploratorios, se investigaron variaciones en la configuración del cromosoma activo y el tamaño del conjunto de datos para examinar en profundidad los efectos de la aumentación. Específicamente, se realizaron pruebas con conjuntos de datos aumentados que incluían 200 y 1000 muestras sintéticas adicionales, y se redujo agresivamente el tamaño del cromosoma activo, en algunos casos hasta un 0.5% de las características totales. Estas configuraciones más extremas fueron seleccionadas para evaluar la robustez del AG frente a diferentes tamaños del espacio de búsqueda, especialmente en escenarios donde se esperaba que la reducción dimensional comprometiera la capacidad del AG para encontrar soluciones óptimas. 

### Resultados

En los experimentos realizados sobre el conjunto de datos leukemia, los resultados mostraron leves diferencia en favor de la aumentación, tanto en lo que respecta a precisión, como al número de características seleccionadas y la estabilidad de los resultados. Aunque la diferencia en términos de precisión no es estadísticamente significativa -como puede verse en el gráfico de caja-, si se observa una mayor estabilidad.

![Precisión en Leukemia](boxplot_leukemia_combined.png)

Sin perjuicio de lo señalado, entendemos posible que, en conjuntos de datos donde los modelos alcanzan una precisión alta (como es el caso que nos ocupa), la aumentación no produce diferencias sustanciales en la performance del AG. La estabilidad, por otro lado, podría ser un factor importante a considerar, ya que sugiere que la aumentación puede contribuir a una selección de características más robusta y consistente a lo largo de las generaciones. Aspecto, este último, que podría ser especialmente útil en conjuntos de datos complejos.

Un punto a resaltar sobre este dataset es la alta correlación entre las características, lo que se refleja en la cantidad significativa de características seleccionadas al menos una vez durante todas las pruebas realizadas. Tanto en los experimentos con datos aumentados como en los originales, el AG seleccionó al menos una vez un número muy similar de características: 6779 y 6772. Este comportamiento sugiere que la mayoría de las características están fuertemente vinculadas, lo que permite que el AG identifique soluciones efectivas utilizando diferentes subconjuntos de características. Asimismo, se observó que un pequeño porcentaje de características (aproximadamente el 10%) es suficiente para resolver el problema de clasificación, independientemente de cuáles sean esas características, debido a la redundancia en la información aportada por las correlaciones. El análisis cuantitativo de las correlaciones muestra que, aunque solo el 0.32% de los pares de características posibles tienen una correlación absoluta mayor a 0.7, estos representan un número considerable (80742) de correlaciones significativas. Es decir: aunque el número de características altamente correlacionadas es una fracción pequeña del total, su impacto en la selección de características es notable, dado que el AG tiende a seleccionar conjuntos de características que son efectivamente intercambiables debido a su alta redundancia.

## Gisette

### Metodología

El conjunto de datos *Gisette* es un problema de clasificación binaria con alta dimensionalidad y un número equilibrado de muestras en ambas clases. Es un set de datos creado para trabajar el problema de reconocimiento de dígitos escritos a mano [@isabelleguyonGisette2004], y tiene 13500 observaciones y 5000 atributos. Este conjunto de datos fue seleccionado para evaluar cómo la aumentación de datos afecta la selección de características en un contexto donde el espacio de características es grande, pero la relación señal-ruido es moderada.

La metodología seguida en los experimentos con *gisette* fue similar a la utilizada en *leukemia*, con la diferencia de que se exploraron configuraciones más agresivas en términos de reducción del espacio de búsqueda y generación de datos sintéticos. 

La configuracion del AG fue la siguiente:

- **Mutación:** PROB_MUT = 1/IND_SIZE (~0.0002)
- **Probabilidad de cruce:** PX = 0.75
- **Cromosoma activo:** p = 0.1
- **Número máximo de generaciones:** GMAX = 30

Nuevamente aquí se realizaron dos conjuntos de experimentos: uno con datos originales y otro con datos aumentados. Se prestó especial atención a la reducción del espacio de búsqueda mediante un tamaño del cromosoma activo equivalente a 500 características. Se investigó también el impacto de generar un número mucho mayor de muestras sintéticas (6000).

### Resultados

Los resultados en Gisette fueron similares a los observados en leukemia. La precisión media fue ligeramente superior en los experimentos con datos aumentados (0.960) en comparación con los datos originales (0.959), pero sin diferencia estadística significativa.

![Precisión en Gisette](boxplot_gisette_combined.png)

Este nuevo hallazgo refuerza la hipótesis de que la aumentación de datos tiene un impacto limitado en conjuntos de datos donde los modelos ya alcanzan una alta precisión. Sin embargo, al igual que en leukemia, la estabilidad de la selección de características mejoró con la aumentación, como se refleja en la menor desviación estándar y el rango intercuartílico (IQR):

|                    | Datos aumentados    | Datos originales    |
|--------------------|---------------------|---------------------|
|**Características seleccionadas (media)** | 424.231             | 436.667             |
|**Desviación Estándar**                  | 17.796              | 14.355              |
|**Rango Intercuartil (IQR)**             | 8.000               | 21.500              |


En efecto, en Gisette se observa una diferencia más importante en la eficiencia de la selección de características. En los experimentos con datos aumentados, el número promedio de características seleccionadas fue menor (424) en comparación con los datos originales (436), señalando que el AG fue más efectivo en el reconocimiento de un subconjunto relevantes. 

## Madelon

### Metodología

El conjunto de datos *Madelon* es un caso especial donde solo cinco características son relevantes, mientras que otras quince son combinaciones lineales de estas, y el resto son datos aleatorios. Así, este conjunto representa un desafío interesante para evaluar la capacidad de los AGs para identificar características útiles en un entorno donde la señal está oculta entre una gran cantidad de ruido.

La metodología seguida en los experimentos con *Madelon* fue similar a la utilizada en *Leukemia* y *Gisette*. La configuración del AG fue la siguiente:

- **Mutación:** PROB_MUT = 1/IND_SIZE (~0.002)
- **Probabilidad de cruce:** PX = 0.75
- **Cromosoma activo:** p = 0.1
- **Número máximo de generaciones:** GMAX = 30

Se generaron 2000 muestras sintéticas para incrementar el número de observaciones disponibles y evaluar si esto mejoraba la capacidad del AG para encontrar las características relevantes. Como en los experimentos precedentes, se exploraron diferentes configuraciones del cromosoma activo y se investigó cómo la aumentación de datos, en el contexto de un espacio de búsqueda complejo y ruidoso, afectaba la eficiencia de la selección de características.

### Resultados

Los experimentos en Madelon mostraron resultados significativamente diferentes a Leukemia y Gisette. La precisión media en los experimentos con datos aumentados fue de 0.83, lo que representa un aumento del 10.4% en comparación con la precisión de los datos originales de 0.75. Esta diferencia es estadísticamente significativa, lo que indica que la aumentación de datos tuvo un impacto positivo en el desempeño del AG.

![Precisión en Madelon](boxplot_madelon_combined.png)

Estos resultados sugieren que la aumentación de datos puede ser especialmente efectiva en conjuntos de datos con características complejas y un alto nivel de ruido, como es el caso de Madelon. La generación de muestras sintéticas permitió al AG identificar mejor las características relevantes, lo que se tradujo en una mejora significativa en la precisión del modelo.

Por otro lado, el análisis de selección de características reveló que, en promedio, el número de características seleccionadas fue menor en los experimentos con datos aumentados (29) en comparación con los datos originales (35). Este hallazgo, también resalta la eficiencia de la aumentación de datos en la selección de características.

Finalmente, podemos destacar también que de los algoritmos clásicos evaluados (cuyo reporte hicimos en el Capítulo 1) solo 2 de los 18 logra superan los valores de precisión obtenidos con el AG en los datos aumentados. Ambos modelos, AdaBoost y Baggind, lograron esos resultados luego de un proceso de optimización de hiperparámetros. El resto de los modelos clásicos oscila entre 0.5 y 0.7 de precisión, lo que refuerza la idea de que la aumentación de datos puede ser una estrategia efectiva para mejorar el desempeño de los AGs en conjuntos de datos complejos.

## Experimento 4: GCM

### Metodología parte 1

El conjunto de datos *GCM* representa un desafío aún mayor que los anteriores no solo debido a la alta dimensionalidad y bajo número de muestras, sino también por las múltiples clases y el desbalance entre ellas.  El dataset consiste en 16063 atributos (biomarcadores), sobre 190 muestras de tumores que refieren a 14 clases de cáncer humano.

El proceso de experimentación en GCM estuvo dividido en dos partes. En la primera parte, se realizaron experimentos exploratorios con diferentes configuraciones del AVC y el AG. El objetivo de esta etapa fue establecer una línea base para evaluar la efectividad de la aumentación de datos. En la segunda parte, se realizaron ajustes en la metodología, el modelo de AVC y el diseño de la integración AVC-AG. Esta vez, el objetivo era mejorar la calidad de los datos sintéticos y la eficiencia de la selección de características.

Aunque se realizaron una gran cantidad de experimentos (algunos exploratorios y otros más específicos), nos centraremos en los resultados de la primera y segunda parte, que nos permitieron identificar los desafíos y oportunidades en la utilización de AVs en conjuntos de datos complejos como GCM.

La cantidad de muestras sintéticas generadas en los experimentos fue ajustada a lo largo de las pruebas, conforme se exploraban opciones de mejora. Ello dio lugar a la siguiente tabla de experimentos por cantidad de muestras analizadas, donde la primera fila representa la cantidad experimentos con las muestras originales (sin aumentación):

| n_muestras        | cantidad_experimentos |
|-------------------|-----------------------|
| 133               | 20                    |
| 3129              | 15                    |
| 1322              | 4                     |
| 1323              | 4                     |
| 1304              | 2                     |
| 254               | 2                     |
| 6106              | 1                     |

Al enfrentarnos a GCM asumíamos que la generación sintética de muestras y ulterior proceso de selección de características plantearía un desafío significativo al AG debido a la complejidad del dataset. La calidad de reconstrucción lograda en los datos  sintéticos generados por el AVC presentado en el Capítulo 2, aunque capaz de preservar la estructura subyacente del conjuntos de datos de GCM, no permitía suponer una mejora significativa en la precisión de la clasificación con un AG. Por otro lado, el desbalance que tienen las clases en GCM, determinaba que la calidad de reconstrucción de las clases minoritarias fuera menor, lo que podría afectar la capacidad del AG para identificar un subconjunto relevante de características. Por todo ello, esperabamos que los experimentos con datos aumentados presentaran resultados mixtos, con posibles mejoras en la estabilidad de la selección de características, pero sin mejoras significativa en la precisión. 

Respecto de los recursos de hardware utilizados, dado que la aumentación de datos requeriría un poder de cómputo proporcional a al tamaño del dataset por la cantidad de muestras sintéticas generadas, se optó por utilizar un entorno en la nube para ejecutar los experimentos de manera eficiente. Para este propósito, se trabajó con una máquina virtual en Google Cloud Platform con 8 vCPUs y 30 GB de RAM.

La configuración inicial del AG fue la siguiente:

- **Mutación:** PROB_MUT = 1,16,160/IND_SIZE ~(0.0006, 0.01, 0.1)
- **Probabilidad de cruce:** PX = 0.75 
- **Cromosoma activo:** p = 0.1
- **Número máximo de generaciones:** GMAX = 20

En la primera etapa se experimentó con un cromosoma activo que representaba el 10% de las características totales, al rededor de 1600 genes por cromosoma, tanto para el grupo de experimentos con datos originales como al grupo de experimentos con datos aumentados. Esta medida se adoptó luego de realizados dos experimentos exploratorios con cromosomas activos en valores del 20% y 30% de las características totales, donde se observó una acentuada degradación en la precisión (en el rango de 0.2 y 0.35). 

Asimismo se varió la probabilidad de mutación en tres valores: 0.0006, 0.01 y 0.1, para instar una exploración más amplia del espacio de búsqueda. La probabilidad de cruce se mantuvo constante en 0.75, y el número máximo de generaciones fue de 20.

Respecto del grupo de experimentos con datos aumentados, el dataset mixto de entrenamiento incluía 1400 muestras sintéticas (100 instancias por clase) y la partición original de entrenamiento (con 133 observaciones). La evaluación se realizó sobre los datos originales de testeo (57 observaciones). 

### Resultados parte 1

Los resultados, como anticipabamos, nos fueron favorables. La precisión media fue ligeramente superior en los experimentos con datos originales (0.538) en comparación con los datos aumentados (0.512). La estabilidad de la selección de características fue similar en ambos grupos, con una dispersión similar en la cantidad de características seleccionadas, como se puede observar en el siguiente gráfico.

![GCM Resultados exploratorios](boxplot_gcm_combined_part1.png)

Como resultado de esta primera etapa de experimentos se identificó una dificultad importante en la metodología utilizada. La calidad de los datos sintéticos generados por el AVC no contribuyó a mejorar la precisión de la clasificación, lo que sugiere que el AG no fue capaz de identificar un subconjunto relevante de características en los datos aumentados. Ante esta circunstancia se procedió a realizar un test de diagnóstico para evaluar la calidad de los datos sintéticos. Se generaron 3000 muestras, se entrenó y evaluó un MLP con estos datos. Los resultados en la partición sintética de testeo fueron los siguientes:


| Clase | Precisión | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0     | 1.00      | 1.00   | 1.00     | 23      |
| 1     | 1.00      | 1.00   | 1.00     | 28      |
| 2     | 1.00      | 1.00   | 1.00     | 31      |
| 3     | 1.00      | 1.00   | 1.00     | 31      |
| 4     | 0.97      | 1.00   | 0.98     | 32      |
| 5     | 1.00      | 0.97   | 0.99     | 34      |
| 6     | 0.96      | 1.00   | 0.98     | 26      |
| 7     | 1.00      | 0.97   | 0.98     | 31      |
| 8     | 1.00      | 1.00   | 1.00     | 30      |
| 9     | 1.00      | 1.00   | 1.00     | 38      |
| 10    | 1.00      | 1.00   | 1.00     | 30      |
| 11    | 1.00      | 1.00   | 1.00     | 31      |
| 12    | 1.00      | 1.00   | 1.00     | 26      |
| 13    | 1.00      | 1.00   | 1.00     | 29      |
| **Exactitud**  | \multicolumn{4}{c|}{1.00 (420)} |
| **Macro avg**  | 1.00      | 1.00   | 1.00     | 420     |
| **Weighted avg** | 1.00      | 1.00   | 1.00     | 420     |

Estos resultados sugieren que el MLP fue capaz de aprender correctamente la estructura de los datos sintéticos, lo que se tradujo en una precisión del 100% en la clasificación, sin embargo, el mismo modelo evaluado en los datos de test originales arrojó una precisión de 0.5. Esta discrepancia sugiere que la distribución de probabilidad de los datos sintéticos no es representativa de la que caracteriza a los datos reales, circuanstancia que estaría limitando la capacidad del AG para identificar un subconjunto relevante de características. Esto explicaría las motivos por los cuales los experimentos con datos aumentados no lograron mejorar la precisión de la clasificación.

En este punto, asumimos que un problema importante que tenía nuestro modelo de AVC se explicaba por la función de pérdida. En efecto,como vimos en el capítulo 2, dicha función resulta de la combinación de dos términos: la pérdida de reconstrucción y la divergencia KL. La divergencia KL es una medida de la diferencia entre dos distribuciones de probabilidad, y se utiliza para regularizar el espacio latente, mantenerlo distribuido y compacto; mientras que la pérdida de reconstrucción mide la diferencia entre los datos originales y los datos reconstruidos. En el caso de GCM, la divergencia KL podría estar dominando la función de pérdida, lo que resultaría en una distribución latente regularizada, pero no necesariamente representativa de los datos reales. Esto significa que el modelo está produciendo una distribución convenientemente discriminada, a expensas de la precisión en la reconstrucción de los datos originales. Situación particularmente problemática cuando los datos presentan relaciones complejas como en GCM. Ante esta problemática, entendimos que se abrían distintos caminos: podíamos ajustar los pesos de la divergencia KL y la reconstrucción para que el AVC sea capaz de generar datos que sean representativos de los datos reales, o bien, explorar la aplicación del AVC a un subespacio de características seleccionadas por un AG, lo que podría reducir la complejidad del problema y mejorar la calidad de los datos sintéticos. En la próxima parte de los experimentos, exploramos esta segunda opción. 

### Metodología Parte 2

Para abordar las limitaciones observadas, se realizaron ajustes en distintas configuraciones. En primer lugar, se adaptó la función de pérdida para incluir un factor de peso por clase que permitiera rebalancear el desequilibrio entre las clases. Ello con el fin de penalizar con mayor severidad los errores en las clases minoritarias, y así procurar una representación más fiel de la distribución real de los datos. En segundo lugar, se integró un muestreador aleatorio ponderado en la etapa de entrenamiento del AVC, que permitiría ajustar los lotes de entrenamiento con igual objetivo de mejorar la representación de las clases. Finalmente, se ajustó la etapa de inicio del proceso generativo, aplicando el AVC ya no al conjunto de datos completo, sino a un subconjunto de características seleccionadas por un AG. La idea era reducir la complejidad del problema y mejorar la calidad de los datos sintéticos, permitiendo al AVC enfocarse en un espacio de características reducido y relevante. Veamos esto último en detalle.

Como vimos, una de las limitaciones observadas en los experimentos iniciales fue la dificultad del AVC para generar datos sintéticos representativos de la distribución de los datos reales. Asumimos entonces, que aplicar el AVC a un subconjunto de características seleccionadas tendría como resultado una simplificación de la distribución de probabilidad original, y por lo tanto una mejora en la calidad de los datos sintéticos. Para ello, se diseñó un flujo de procesamiento que partía de un subespacio de características relavantes, y luego procedía a la generación de datos sintéticos con un AVC y la selección de características mediante un AG, tal cual el flujo de trabajo presentado en el Capítulo 3. 

La definición del subespacio de entrada partió de las características más frecuentes encontradas en los experimentos iniciales, donde se trabajó con un cromosoma activo que representaba el 10% de las características totales, al rededor de 1600 genes por cromosoma. Este subconjunto de características, que ya habían sido preseleccionadas por un AG, se utilizó como entrada para el AVC. A partir de este subconjunto, se aplicó el modelo generativo a la creación datos sintéticos, y luego se procedió a la selección de características mediante un AG. Este flujo de trabajo, consistente en el encademiento de tres procesos: *selección-generación-selección*, permitió concentrar el aprendizaje de los modelos en un subespacio de características.

Respecto de la configuración de los experimentos se implementaron las siguientes modificaciones: se ajustó el total de muestras sintéticas generadas por el AVC a 3000.Se redujo el tamaño del cromosoma activo a 0.05 y 0.025 respecto del espacio original de características (~750 y ~450 atributos respectivamente). Se mantuvo constante la probabilidad de cruce en 0.75, como también la probabilidad de mutación en 0.1 (~0.0006). El número máximo de generaciones se redujo a 15, considerando la reducción en la complejidad del problema.

Como resultado de todas estas modificaciones, se esperaba que la calidad de los datos sintéticos mejorara, lo que se traduciría en una mejora en la precisión de la clasificación, y en la eficiencia de la selección de características.

### Resultados Parte 2

Efectivamente, los experimentos realizados en la segunda parte de la investigación mostraron una mejora significativa en la precisión de la clasificación. 

La precisión media en los experimentos con datos aumentados fue de 0.541, lo que representa un aumento de 8.85% en comparación con la precisión de los datos originales de 0.497. Esta diferencia es estadísticamente significativa, lo que indica que la aumentación de datos tuvo un impacto positivo en el desempeño del AG. 

![GCM Resultados parte 2](boxplot_gcm_combined.png)

Respecto de la selección de características, no se observa gran diferencia en el número de características seleccionadas entre los experimentos con datos originales y los datos aumentados. En efecto, el número de características promedio seleccionadas en los experimentos con aumentación y cromosomas de tamaño 0.05 y 0.025 fue de 453 y 784 respectivamente, en comparación con 461 y 781 en los experimentos con datos originales.

Para validar los resultados obtenidos, se realizó un grupo de experimentos adicionales donde se disminuyó el tamaño del cromosoma activo a 0.015 y 0.003, lo que representó una selección de atributos en torno a ~200 y ~45. Los resultados mostraron que, pese a la importante reducción en el espacio de búsqueda, la precisión se mantuvo en un nivel aceptable en ambos grupos. La mejor performance del grupo con datos aumentados tiene lugar en los experimentos con reducción más agregisiva del cromosomas, con un tamaño 0.003 (~45). 

A continuación presentamos la serie completa de experimentos realizados en GCM, donde se puede observar la evolución de la precisión en función del tamaño del cromosoma activo. 

![GCM Resultados completos](boxplot_gcm_ngenes_accuracy.png)

Finalmente, se realizó un experimento con 6000 muestras sintéticas, donse se observó una degradación de los resultados. Esto sugiere que la generación de un número excesivo de muestras sintéticas puede comprometer la calidad de los datos y afectar negativamente la precisión de la clasificación.

Todo lo anterior sugiere que, si bien la aumentación de datos mediante AVs puede enfrentar desafíos significativos en conjuntos de datos complejos como gcm, es posible mejorar la calidad de los datos sintéticos mediante ajustes en la arquitectura del AV y en la metodología de selección de características. La combinación de AVs y AGs en un flujo de trabajo encadenado demostró ser una estrategia prometedora para mejorar la precisión y la eficiencia en la selección de características.

## Resumen de los resultados

Los experimentos realizados en los cuatro conjuntos de datos (*Leukemia*, *Gisette*, *Madelon* y *GCM*) evidencian una tendencia general sobre el impacto de la aumentación de datos mediante Autocodificacadores Variacionales en la selección de características utilizando Algoritmos Genéticos. 

![Precisión en los 4 datasets](boxplot_resultados_precision.png)

![Número de características seleccionadas en los 4 datasets](boxplot_resultados_ngenes.png)

Si bien el uso de datos aumentados no siempre produjo mejoras estadísticamente significativas en la precisión de clasificación, como fue el caso de *Leukemia* y *Gisette* que representan desafíos donde los modelos ya alcanzan una alta precisión, se observó una clara tendencia hacia una mayor estabilidad en la selección de características y mejora en el poder de clasificación en los dataset más complejos, como *Madelon* y *GCM*. Este hallazgo sugiere que la aumentación de datos puede contribuir a generar modelos más consistentes a lo largo de múltiples generaciones, lo cual es particularmente relevante en escenarios de alta dimensionalidad y escasez muestral.

En el caso del conjunto de datos *Madelon*, donde el problema de selección de características presenta una clara distinción entre señales relevantes y ruido, la aumentación de datos mostró una mejora significativa en la precisión, incrementando la capacidad del AG para identificar las características correctas en un espacio de búsqueda extremadamente ruidoso. Este resultado resalta la utilidad de la aumentación en problemas donde la presencia de ruido dificulta la tarea de selección.

Por otro lado, los experimentos con *GCM* ilustran las limitaciones de la aumentación en conjuntos de datos con una distribución de clases desbalanceada y de alta complejidad. Sin embargo los ajustes en la arquitectura del AV y en la configuración experimental permitieron mejoras importantes, permitiendo una generación de datos sintéticos de mayor calidad y una selección de características más eficiente. En este sentido, la integración de estrategias más complejas, como la combinación de selección de características previa a la aumentación, demostró ser una vía prometedora para mejorar los resultados.

En conjunto, los hallazgos de este capítulo sugieren que la aumentación de datos, cuando se utiliza en combinación con AGs, puede ser una herramienta efectiva en la selección de características, especialmente en contextos donde la dimensionalidad y el ruido dificultan la tarea. Asimismo, se destaca que el éxito de esta técnica depende críticamente de la calidad de los datos sintéticos generados y de la adecuada configuración de los modelos subyacentes, lo que subraya la importancia de ajustar las metodologías de manera específica para cada tipo de conjunto de datos.