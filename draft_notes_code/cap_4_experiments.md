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

- **Mutación:** PROB_MUT = 1/IND_SIZE (0.0001)
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

En los experimentos realizados sobre el conjunto de datos leukemia, los resultados no mostraron diferencias significativas en precisión del AG, ni tampoco en la minimización del número de características seleccionadas entre los grupos con y sin aumentación de datos. La precisión media fue de 0.99 en ambos casos, y el número promedio de características seleccionadas fue de 259 en los datos originales y 258 en los datos aumentados. La estabilidad de los resultados fue ligeramente mejor en los datos aumentados, aunque la diferencia -como puede verse en el gráfico de caja- no es estadísticamente significativa.

![Precisión en Leukemia](boxplot_leukemia_combined.png)

Entendemos posible que, en conjuntos de datos donde los modelos alcanzan una precisión alta (como es el caso que nos ocupa), la aumentación no produce mejora sustanciales en la selección de características. La estabilidad de los resultados, sin embargo, sugiere que la aumentación puede contribuir a una selección de características más robusta y consistente a lo largo de las generaciones, algo que podría ser especialmente útil en conjuntos de datos complejos.

Un aspecto que debemos resaltar sobre este dataset es la alta correlación entre las características, lo que se refleja en la cantidad significativa de características seleccionadas al menos una vez durante todas las pruebas realizadas. Tanto en los experimentos con datos aumentados como en los originales, el Algoritmo Genético (AG) seleccionó al menos una vez un número muy similar de características: 6779 y 6772. Este comportamiento sugiere que la mayoría de las características están fuertemente vinculadas, lo que permite que el AG identifique soluciones efectivas utilizando diferentes subconjuntos de características. Asimismo, se observó que un pequeño porcentaje de características (aproximadamente el 10%) es suficiente para resolver el problema de clasificación, independientemente de cuáles sean esas características, debido a la redundancia en la información aportada por las correlaciones. El análisis cuantitativo de las correlaciones muestra que, aunque solo el 0.32% de los pares de características posibles tienen una correlación absoluta mayor a 0.7, estos representan un número considerable (80742) de correlaciones significativas. Es decir: aunque el número de características altamente correlacionadas es una fracción pequeña del total, su impacto en la selección de características es notable, dado que el AG tiende a seleccionar conjuntos de características que son efectivamente intercambiables debido a su alta redundancia.

## Gisette

### Metodología

El conjunto de datos *Gisette* es un problema de clasificación binaria con alta dimensionalidad y un número equilibrado de muestras en ambas clases. Es un set de datos creado para trabajar el problema de reconocimiento de dígitos escritos a mano [@isabelleguyonGisette2004], y tiene 13500 observaciones y 5000 atributos. Este conjunto de datos fue seleccionado para evaluar cómo la aumentación de datos afecta la selección de características en un contexto donde el espacio de características es grande, pero la relación señal-ruido es moderada.

La metodología seguida en los experimentos con *gisette* fue similar a la utilizada en *leukemia*, con la diferencia de que se exploraron configuraciones más agresivas en términos de reducción del espacio de búsqueda y generación de datos sintéticos. 

La configuracion del AG fue la siguiente:

- **Mutación:** PROB_MUT = 1/IND_SIZE (0.0002)
- **Probabilidad de cruce:** PX = 0.75
- **Cromosoma activo:** p = 0.1
- **Número máximo de generaciones:** GMAX = 30

Nuevamente aquí se realizaron dos conjuntos de experimentos: uno con datos originales y otro con datos aumentados. Se prestó especial atención a la reducción del espacio de búsqueda mediante la disminución del tamaño del cromosoma activo y la observación de cómo esta reducción, combinada con la aumentación de datos, afectaba la eficiencia del AG. Se investigó también el impacto de generar un número mucho mayor de muestras sintéticas (6000), reduciendo agresivamente el tamaño del cromosoma para evaluar si el modelo podría identificar características relevantes en un espacio de búsqueda más limitado.

### Resultados

Los resultados en Gisette fueron similares a los observados en leukemia. La precisión media fue ligeramente superior en los experimentos con datos aumentados (0.960) en comparación con los datos originales (0.959), pero nuevamente, sin diferencia estadística significativa.

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

El conjunto de datos *Madelon* es un caso especial donde solo cinco características son relevantes, mientras que otras quince son combinaciones lineales de estas, y el resto son datos aleatorios. Así, este conjunto representa un desafío único para evaluar la capacidad de los AGs para identificar características útiles en un entorno donde la señal está oculta entre una gran cantidad de ruido.

La metodología seguida en los experimentos con *madelon* fue similar a la utilizada en *leukemia* y *gisette*. La configuración del AG fue la siguiente:

- **Mutación:** PROB_MUT = 1/IND_SIZE (0.002)
- **Probabilidad de cruce:** PX = 0.75
- **Cromosoma activo:** p = 0.1
- **Número máximo de generaciones:** GMAX = 30

Se generaron 2000 muestras sintéticas para incrementar el número de observaciones disponibles y evaluar si esto mejoraba la capacidad del AG para encontrar las características relevantes. Como en los experimentos precedentes, se exploraron diferentes configuraciones del cromosoma activo y se investigó cómo la aumentación de datos, en el contexto de un espacio de búsqueda complejo y ruidoso, afectaba la eficiencia de la selección de características.

### Resultados

El conjunto de datos madelon mostró resultados significativamente diferentes a Leukemia y Gisette. La precisión media en los experimentos con datos aumentados fue de 0.83, lo que representa un aumento del 10.4% en comparación con la precisión de los datos originales de 0.75. Esta diferencia es estadísticamente significativa, lo que indica que la aumentación de datos tuvo un impacto positivo en el desempeño del AG.

![Precisión en Madelon](boxplot_madelon_combined.png)

Estos resultados sugieren que la aumentación de datos puede ser especialmente efectiva en conjuntos de datos con características complejas y un alto nivel de ruido, como es el caso de Madelon. La generación de muestras sintéticas permitió al AG identificar mejor las características relevantes, lo que se tradujo en una mejora significativa en la precisión del modelo.

Por otro lado, el análisis de selección de características reveló que, en promedio, el número de características seleccionadas fue menor en los experimentos con datos aumentados (29) en comparación con los datos originales (35). Este también resalta una mayor eficiencia en la selección de características cuando se utiliza aumentación de datos.

Podemos destacar también que de los algoritmos clásicos evaluados (a cuyo reporte remitimos en el capítulo 1) solo 2 de los 18 logra superan los valores de precisión obtenidos con el AG en los datos aumentados. Ambos modelos, AdaBoost y Baggind, pasaron por un proceso de optimización de hiperparámetros. El resto de los modelos clásicos oscila entre 0.5 y 0.7 de precisión, lo que refuerza la idea de que la aumentación de datos puede ser una estrategia efectiva para mejorar el desempeño de los AGs en conjuntos de datos complejos.

## Experimento 4: GCM

PENDIENTE

## Resumen de los resultados

PENDIENTE

![Precisión en los 4 datasets](boxplot_resultados_precision.png)
![Número de características seleccionadas en los 4 datasets](boxplot_resultados_ngenes.png)




### Metodología 

El conjunto de datos *GCM* representa un desafío aún mayor que los anteriores no solo debido a la alta dimensionalidad y bajo número de muestras, sino también por las múltiples clases y la complejidad de las relaciones entre las características. 

El tratamiento metodológico de los experimentos con *gcm* fue similar al de los conjuntos de datos anteriores, con la diferencia de que se adoptó un doble proceso de selección de características. Así, el proceso consistió en encadenar una secuencia de AG, AVC y finalmente un AG. El primer AG se encargó de seleccionar un subconjunto inicial de características, que fue utilizado para entrenar un AVC. El AVC generó muestras sintéticas que se integraron con los datos originales para entrenar un segundo AG, que se encargó de seleccionar un subconjunto final de características.

La configuración del AG fue la siguiente:

- **Mutación:** PROB_MUT = 1/IND_SIZE (0.00006)
- **Probabilidad de cruce:** PX = 0.75
- **Cromosoma activo:** p = 0.1
- **Número máximo de generaciones:** GMAX = 20

La primera etapa de subselección de características se realizó con un cromosoma activo que representaba el 10% de las características totales, limitado a un máximo de 20 generaciones. El AVC se entrenó con un conjunto de datos aumentado que incluía 200 muestras sintéticas generadas por un AV específico para este conjunto de datos. El segundo AG se entrenó con un conjunto de datos que combinaba las muestras originales y las sintéticas, utilizando un cromosoma activo del 5% y un máximo de 20 generaciones.

Se realizaron múltiples experimentos exploratorios con diferentes tamaños de muestras sintéticas (desde 200 hasta 1400) y diferentes configuraciones del cromosoma activo, buscando identificar las condiciones óptimas para la selección de características en este conjunto de datos.

Se exploraron varias configuraciones, incluyendo la mezcla de datos originales y sintéticos durante el entrenamiento del AG, así como la evaluación del modelo en una partición original del conjunto de datos. Se prestó especial atención a la calidad de las muestras generadas por el AV y su impacto en la selección de características, así como a la posibilidad de que los AGs estuvieran sobreajustándose a los datos sintéticos, en detrimento de su capacidad de generalización.

### Resultados Parte 1

El primer conjunto de experimentos con el conjunto de datos gcm mostró resultados mixtos. La precisión media fue ligeramente superior en los experimentos con datos originales en comparación con los datos aumentados.
### Metodología Parte 2


Para abordar las limitaciones observadas, se realizaron ajustes en la metodología, como la integración de pesos de clase en la función de pérdida personalizada del AV y la inclusión de un muestreador aleatorio ponderado en el cargador de datos. Estos ajustes, junto con una subselección inicial de características, mejoraron significativamente los resultados en una serie posterior de experimentos, alcanzando una precisión balanceada superior al 0.65 en algunos casos.





El conjunto de datos gcm, que presenta un desafío significativo debido a su alta dimensionalidad y bajo número de muestras, mostró resultados mixtos. La precisión media fue ligeramente superior en los experimentos con datos aumentados (0.517) en comparación con los datos originales (0.467). Sin embargo, la diferencia no fue estadísticamente significativa (p-value: 0.355).

Interpretación: La falta de una mejora significativa en la precisión sugiere que, en el caso de gcm, la calidad de los datos sintéticos generados por el AV no fue suficiente para superar las limitaciones impuestas por la alta dimensionalidad y la complejidad del conjunto de datos. Es posible que el AV no haya sido capaz de capturar adecuadamente la distribución de probabilidad original, lo que limitó la capacidad del AG para generalizar a partir de los datos sintéticos.

Selección de Características
El análisis de pob_ngenes_avg mostró que el número promedio de características seleccionadas fue mayor en los datos aumentados (378.477) en comparación con los datos originales (305.160). Esto sugiere que la selección de características fue menos eficiente en los experimentos con datos aumentados.

Interpretación: La mayor cantidad de características seleccionadas en los experimentos con datos aumentados puede indicar que el AG tuvo dificultades para identificar un subconjunto relevante de características cuando se le proporcionaron datos sintéticos que no representaban adecuadamente la estructura original del conjunto de datos. Este resultado destaca la importancia de la calidad de los datos sintéticos en la eficacia de la selección de características.




Interpretación: Estos resultados sugieren que, si bien la aumentación de datos mediante AVs puede enfrentar desafíos significativos en conjuntos de datos complejos como gcm, es posible mejorar la calidad de los datos sintéticos mediante ajustes en la arquitectura del AV y en la metodología de selección de características. La combinación de AVs y AGs en un flujo de trabajo iterativo y refinado demostró ser una estrategia prometedora para mejorar la precisión y la eficiencia en la selección de características.



