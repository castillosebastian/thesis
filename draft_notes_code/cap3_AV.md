## Presentación de nuestro modelo de AV

El desarrollo del modelo de Autoencodificador Variacional (AV) empleado en esta investigación se organizó en dos pasos. El primero giró en torno al diseño y validación de la arquitectura del modelo, mientras que el segundo estuvo enfocado en la optimización de dicha arquitectura para la generación de datos sintéticos en cada uno de los dataset bajo estudio. A continuación describiremos brevemente este proceso y la configuración final de los modelos elegidos para los experimentos de aumentación. 

### Modelo Inicial 

En la primera etapa, se centró el esfuerzo en el diseño de la arquitectura del AV. Este proceso comenzó con la creación de una versión exploratoria del modelo, cuya finalidad era establecer una base sobre la cual iterar en mejoras sucesivas. Se optó por una Perceptrón Multicapa (MLP), con 2 capas ocultas en el encoder y en el decoder, lo que permitiría al modelo aprender representaciones latentes complejas.

El encoder incluyó dos capas lineales, cada una seguida de una activación ReLU. Como vimos, el enconder genera dos vectores, uno para la media y otro para la varianza logarítmica de la distribución latente, componentes críticos para el proceso de reparametrización que permite al modelo generar nuevas muestras en el espacio latente. El decoder, encargado de reconstruir los datos originales a partir del espacio latente, fue diseñado con una estructura simétrica a la del encoder, utilizando nuevamente activaciones ReLU y finalizando con una función Sigmoidea en la capa de salida. La función Sigmoidea condiciona la salida a un rango entre 0 y 1, lo que es particularmente útil para la normalización de los datos de entrada y salida. 

La función de pérdida del modelo combinó la divergencia Kullback-Leibler (KLD) y error cuadrático medio (MSE). La KLD se utilizó para medir la diferencia entre la distribución aprendida por el modelo y una distribución normal estándar, mientras que el error cuadrático medio se empleó para evaluar el error de reconstrucción, es decir, qué tan bien el modelo era capaz de replicar los datos de entrada a partir del espacio latente. 

Este modelo se probó en la generación de datos sintéticos en un dataset de clases binarias: Madelon, y un dataset multiclases: GCM. Para evaluar los datos generados se realizaron experimentos de clasificación utilizando un MLP, comparando los resultados obtenidos en el dataset original y en el dataset con muestras sintéticas.  Inicialmente, la arquitectura empleada resultó insuficiente para capturar la complejidad de los datos, lo que llevó a un modelo incapaz de representar con precisión las características latentes, produciendo datos sintéticos de baja calidad.  

### Segundo Modelo AV para clases binarias

En respuesta a los problemas identificados previamente, se diseñó un nuevo modelo con una arquitectura de tres capas lineales en el encoder y el decoder, cada una con activaciones ReLU seguidas de normalización por lotes. La Batch Normalization fue seleccionada debido a su capacidad para estabilizar y acelerar el proceso de entrenamiento, promoviendo la rápida convergencia y mejorando la precisión de la reconstrucción. Este diseño permitiría que las activaciones intermedias sean estabilizadas y que la información relevante sea conservada a lo largo de las capas, mitigando los problemas de desplazamiento de covariables (*covariate shift*) durante el entrenamiento. Dado que el modelo fue ajustado para capturar la estructura de los datos a través de capas lineales y normalización por lotes, mantuvimos la elección de ReLU como función de activación dada su eficiencia computacional.

El modelo resultante fue entrenado con un optimizador Adam y una tasa de aprendizaje en el rango de [1e-5, 1e-3]. Se experimentó con diferentes tamaños del espacio latente, evaluando el equilibrio entre la calidad de reconstrucción y la capacidad de generalización del modelo. Se empleó un termino de paciencia para detener el entrenamiento si no se observaba mejora en los datos de test durante 10 épocas consecutivas. Este mecanismo de corte temprano mejoró la eficiencia del entrenamiento y la capacidad de generalización del modelo.

Estos experimentos fueron clave para ajustar el AV a las necesidades específicas de los conjuntos de datos utilizados en la investigación, permitiendo una generación de datos sintéticos que no solo replicara los patrones de los datos originales, sino que también capturara la variabilidad inherente a estos.

--- 
**Arquitectura del Autocodificador Variacional**

La arquitectura del Autocodificador Variacional está compuesta por tres capas lineales (una capa de entrada y dos capas ocultas), cada una seguida de una normalización por lotes (Batch Normalization) y una activación ReLU. El proceso de codificación se realiza de la siguiente manera:

$h_1 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_1}x + b_1))$
$h_2 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_2}h_1 + b_2))$
$h_3 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_3}h_2 + b_3))$

Donde:

-$\mathbf{W_1}$es una matriz de pesos que transforma el vector de entrada $x$ al espacio de características de dimensión $H$.   
-$\mathbf{W_2}$transforma $h_1$ a un espacio de características de dimensión$H2$.   
-$\mathbf{W_3}$ mantiene la dimensión $H2$ mientras transforma$h_2$.      
-$b_1$,$b_2$, y$b_3$son los sesgos correspondientes a cada capa.

Después de las tres capas, se generan los vectores latentes $\mu$ y $\log(\sigma^2)$ mediante dos capas lineales independientes que también aplican normalización por lotes.

**2.2. Reparametrización**

El vector latente $z$ se obtiene mediante la técnica de reparametrización, donde se introduce ruido gaussiano para permitir la retropropagación del gradiente:

$z = \mu + \sigma \times \epsilon$

Donde $\epsilon$ es una variable aleatoria con distribución normal estándar, y $\sigma$ se calcula a partir de $\log(\sigma^2)$.

**2.3. Decodificador**

El decodificador reconstruye el vector de entrada a partir del vector latente$z$utilizando una arquitectura de tres capas lineales, cada una seguida por una normalización por lotes y una activación ReLU:

$h_4 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_4}z + b_4))$
$h_5 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_5}h_4 + b_5))$
$\hat{x} = \text{BatchNorm}(\mathbf{W_6}h_5 + b_6)$

Donde:

-$\mathbf{W_4}$ transforma el vector latente $z$ al espacio de características de dimensión $H2$.     
-$\mathbf{W_5}$ transforma $h_4$ al espacio de características de dimensión $H$.   
-$\mathbf{W_6}$ transforma $h_5$ de regreso al espacio de la dimensión original de la entrada $D_{in}$.   
-$b_4$,$b_5$, y$b_6$son los sesgos correspondientes a cada capa.

Finalmente, la salida $\hat{x}$ es una aproximación reconstruida de la entrada original$x$.

---

### Modelo CVAE para datos multiclase

Para abordar el dataset GCM, que contiene 14 clases con distribuciones desiguales, se creo un Autocodificador Variacional Condicional (CVAE) que combina la capacidad de generación de un VAE tradicional con el condicionamiento explícito en las etiquetas de clase. El CVAE propuesto permitió una modelización más precisa de los datos, al incorporar información de clase en el proceso de codificación y decodificación.

En escenarios donde los datasets están desbalanceados, los modelos generativos pueden tender a favorecer las clases mayoritarias, ignorando las minoritarias. Para abordar el desbalance de clases que presenta GCM, se implementó una estrategia de ponderación de clases dentro de la función de pérdida, penalizando de manera diferenciada los errores de reconstrucción en función de la clase, mejorando así la capacidad del modelo para representar adecuadamente las clases minoritarias.

---
**Arquitectura del Autocodificador Variacional Condicional (CVAE)**

La arquitectura del Autocodificador Variacional Condicional (CVAE) se basa en una modificación del Autocodificador Variacional tradicional para incorporar información adicional en forma de etiquetas. Esta información se concatena tanto en la fase de codificación como en la de decodificación, permitiendo que el modelo aprenda distribuciones condicionales.

**2.1. Codificador**

El codificador del CVAE combina la entrada original con las etiquetas antes de ser procesada por una secuencia de capas lineales (una capa de entrada y dos capas ocultas), cada una seguida por una normalización por lotes (Batch Normalization) y una activación ReLU. El proceso de codificación se realiza de la siguiente manera:

$h_1 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_1}[x, y] + b_1))$
$h_2 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_2}h_1 + b_2))$
$h_3 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_3}h_2 + b_3))$

Donde:

- $[x, y]$ es la concatenación del vector de entrada $x$ con las etiquetas $y$.
- $\mathbf{W_1}$ es una matriz de pesos que transforma el vector combinado $ [x, y]$ al espacio de características de dimensión $ H$.
- $\mathbf{W_2}$ transforma $ h_1$ a un espacio de características de dimensión $ H2$.
- $\mathbf{W_3}$ mantiene la dimensión $ H2$ mientras transforma $ h_2$.
- $ b_1$, $ b_2$, y $ b_3$ son los sesgos correspondientes a cada capa.

Al igual que en el Autocodificador Variacional tradicional, se generan los vectores latentes $\mu$ y $\log(\sigma^2)$ mediante dos capas lineales independientes.

**2.2. Reparametrización**

El vector latente $z$ se obtiene mediante la técnica de reparametrización, similar al Autocodificador Variacional tradicional:

$z = \mu + \sigma \times \epsilon$

Donde $\epsilon$ es una variable aleatoria con distribución normal estándar, y $\sigma$ se calcula a partir de $\log(\sigma^2)$.

**2.3. Decodificador**

El decodificador del CVAE reconstruye el vector de entrada a partir del vector latente $ z$ y las etiquetas $ y$, utilizando una arquitectura de tres capas lineales, cada una seguida por una normalización por lotes y una activación ReLU:

$h_4 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_4}[z, y] + b_4))$
$h_5 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_5}h_4 + b_5))$
$\hat{x} = \text{sigmoid}(\mathbf{W_6}h_5 + b_6)$

Donde:

- $[z, y]$ es la concatenación del vector latente $ z$ con las etiquetas $ y$.
- $\mathbf{W_4}$ transforma el vector combinado $ [z, y]$ al espacio de características de dimensión $ H2 + \text{labels\_length}$.
- $\mathbf{W_5}$ transforma $ h_4$ al espacio de características de dimensión $ H$.
- $\mathbf{W_6}$ transforma $ h_5$ de regreso al espacio de la dimensión original de la entrada $ D_{in}$.
- $ b_4$, $ b_5$, y $ b_6$ son los sesgos correspondientes a cada capa.

Finalmente, la salida $\hat{x}$ es una aproximación reconstruida de la entrada original $x$, condicionada por las etiquetas $y$.

**Elementos distintivos respecto a la arquitectura anterior**:

- **Incorporación de etiquetas**: Tanto en el codificador como en el decodificador, se concatenan las etiquetas $ y$ con las entradas y el vector latente, respectivamente.
- **Dimensiones ajustadas**: Se han ajustado las dimensiones de las capas para acomodar las etiquetas, reflejadas en las matrices de pesos y las normalizaciones por lotes.
- **Capas adicionales en la fase de decodificación**: Se añaden capas y ajustes para manejar las etiquetas adicionales en el proceso de decodificación.

Esta arquitectura permite que el CVAE capture relaciones condicionales más complejas entre las entradas y sus correspondientes etiquetas.
---

### Optimización de Hiperparámetros

La búsqueda y ajuste de hiperparámetros para los modelos de AV y AVC ha sido un proceso crucial para optimizar la generación de datos sintéticos y, en última instancia, mejorar el rendimiento de nuestro Algoritmo Genético. A lo largo de esta etapa de investigación, se implementaron diversas estrategias para identificar las configuraciones óptimas de los modelos, así como para evitar el sobreajuste y garantizar la robustez de los resultados.

Uno de los primeros pasos fue ampliar la búsqueda de hiperparámetros, ajustando variables clave como las dimensiones latentes, las tasas de aprendizaje, y el número de neuronas en las capas ocultas. Un cambio significativo fue la implementación de un mecanismo de paciencia, configurado para detener el entrenamiento si no se observaba mejora en los datos de test durante 10 épocas consecutivas. Esta modificación tuvo un impacto directo en la calidad del modelo, ya que en experimentos iniciales, los modelos seguían entrenándose durante todas las épocas establecidas, lo que en muchos casos resultaba en un sobreajuste. La implementación de este corte temprano no solo mejoró la eficiencia del entrenamiento, sino que también contribuyó a reducir el error y mejorar la capacidad de generalización del modelo.

El análisis de los resultados obtenidos mediante estas configuraciones reveló que un MLP entrenado con datos sintéticos generados por un AV podía igualar o incluso superar el rendimiento de un MLP entrenado con datos reales en algunos casos. Este hallazgo es particularmente relevante, ya que sugiere que, bajo ciertas configuraciones, los datos sintéticos pueden ser tan útiles como los datos reales para el entrenamiento de modelos predictivos. Este fenómeno se observó de manera consistente en varios conjuntos de datos, como Leukemia, Madelon, y Gisette, donde la precisión y la exactitud del modelo entrenado con datos sintéticos alcanzaron o superaron las métricas obtenidas con los datos originales.

Un hallazgo interesante se refiere a las dimensiones latentes del modelo. A medida que se ampliaba la búsqueda de hiperparámetros, se descubrió que las mejores configuraciones para la variable latente no eran necesariamente las más grandes. De hecho, en muchos casos, valores para la dimensión latente entre 3 y 100 ofrecieron los mejores resultados. Esto, que inicialmente puede ser contraintuitivo, ya que se podría suponer que un mayor espacio latente permitiría capturar más complejidad en los datos; sugiere que un espacio latente excesivamente grande puede introducir ruido y hacer que el modelo pierda la capacidad de generalizar correctamente.

Las pruebas con diferentes arquitecturas también proporcionaron información valiosa. En el caso de leukemia, se exploraron modelos VAE de  dos, tres y cuatro capas ocultas, así como CVAE con múltiples capas, pero no se observaron mejoras significativas al aumentar la complejidad del modelo. En particular, se encontró que las configuraciones más simples (i.e. dos capas ocultas), ofrecían resultados tan buenos o incluso mejores que sus contrapartes más complejas. Esta observación refuerza la idea de que, en algunos casos, la simplicidad puede ser preferible y que el sobredimensionamiento de la arquitectura no necesariamente se traduce en mejores resultados.

Por otro lado, los experimentos realizados en el dataset GCM presentaron un desafío diferente. A pesar de la implementación de un AVC de tres capas ocultas, los resultados no mostraron mejoras sustanciales en comparación con un más simple de dos capas. Además, se observó una disminución en la capacidad del modelo para predecir correctamente clases con menor soporte en el conjunto de datos, lo que sugiere que la complejidad del modelo no fue capaz de capturar adecuadamente la variabilidad de las clases menos representadas. Este resultado subraya la dificultad inherente al trabajo con conjuntos de datos multiclase, especialmente cuando las clases tienen distribuciones subyacentes similares, están desbalanceadas o ambos.

En cuanto a la búsqueda de hiperparámetros, se utilizaron tanto Grid Search como Optimización Bayesiana (BO). Cada una de estas técnicas tiene sus fortalezas, y la elección entre ellas depende en gran medida del objetivo de la búsqueda. Grid Search, por ejemplo, permite un control total sobre el espacio de búsqueda, lo que es útil para responder preguntas específicas, como la configuración óptima de la dimensión latente. Sin embargo, la BO demostró ser particularmente eficiente en la exploración de un espacio de hiperparámetros más amplio y menos definido, logrando un equilibrio entre la exploración y la explotación que resulta especialmente útil cuando se busca optimizar un modelo sin un conocimiento previo preciso del mejor rango de parámetros.

A pesar de los avances logrados, también se encontraron limitaciones. Por ejemplo, incrementar el tamaño de los datos sintéticos en leukemia no condujo a una mejora significativa en los resultados, lo que sugiere que, para ciertos datasets, los beneficios de aumentar los datos sintéticos son marginales una vez alcanzado un umbral de rendimiento. En el caso de GCM, los problemas de baja calidad en la reconstrucción de datos sintéticos por parte del AVC sugieren que simplemente aumentar el tamaño del dataset no compensa una arquitectura subóptima.

En efecto, uno de los experimentos más interesantes fue el relacionado con el aumento del tamaño del conjunto de datos sintéticos en el dataset GCM. Inicialmente, se logró incrementar las observaciones del conjunto de datos de entrenamiento a 3000 muestras balanceadas, con 214 observaciones por clase. Este aumento resultó en una mejora significativa en la performance del modelo, logrando igualar los resultados obtenidos con el clasificador MLP entrenado con datos reales. Sin embargo, al continuar incrementando la cantidad de datos sintéticos a 6000 muestras, se observó una degradación en el rendimiento. Esto sugiere la existencia de un umbral en la cantidad de datos sintéticos que, una vez superado, introduce ruido en el modelo en lugar de aportar valor. Este ruido puede estar relacionado con el solapamiento de las fronteras de decisión en las muestras generadas, lo que aumenta el error y disminuye la precisión del modelo.

Los resultados obtenidos en los experimentos reflejan que los beneficios de la aumentación de datos tienen un límite. Superado este umbral, la generación adicional de datos no solo deja de ser útil, sino que puede ser perjudicial, como se evidenció en nuestros experimentos. Este fenómeno destaca la importancia de una cuidadosa calibración en la cantidad de datos sintéticos generados, especialmente en conjuntos de datos con características complejas y altamente dimensionales como GCM.

Otro aspecto explorado fue la implementación de la pérdida L1 en lugar de MSE. Se realizaron pruebas para evaluar si la L1_loss podría ofrecer mejoras, pero los resultados no mostraron diferencias significativas en comparación con MSE. Este hallazgo sugiere que, al menos en este contexto específico, la L1_loss no proporciona un beneficio claro sobre el MSE para la tarea de generación de datos sintéticos.

Además, se experimentó con el uso de dropout como técnica de regularización. Se probaron tasas de dropout en un rango de 0.05 a 0.5 en distintas configuraciones de AVC, tanto con arquitecturas pequeñas (100-500 neuronas por capa) como grandes (1000-7000 neuronas por capa). Aunque algunos experimentos con una arquitectura más pequeña mostraron  resultados interesantes en el clasificador MLP, en conjunto este grupo de experimentos se mantuvieron por debajo de los mejores experimentos previos. Esto sugiere que el dropout, si bien útil en otros contextos, no aporta beneficios en configuraciones ya optimizadas del AVC para este tipo de tareas.

Estos resultados llevaron a una reflexión sobre la falta de impacto positivo de ciertos ajustes, como la introducción de L1_loss y dropout. Es probable que la estabilidad y el buen rendimiento de las configuraciones ya validadas de AV y AVC, alcanzados a través de numerosos experimentos, limiten el potencial de mejora adicional mediante estos métodos. De hecho, en lugar de mejorar el rendimiento, estos cambios podrían estar degradando los resultados debido a la interferencia con una configuración ya optimizada.

En resumen, la búsqueda de hiperparámetros y el ajuste de la arquitectura del AV y AVC revelaron la importancia de un enfoque balanceado que evite tanto la simplicidad excesiva como la complejidad innecesaria. Los resultados obtenidos muestran que, bajo ciertas configuraciones, los datos sintéticos pueden igualar o superar la utilidad de los datos reales en la formación de modelos predictivos, aunque la eficiencia y la calidad de estos resultados dependen en gran medida de la cuidadosa calibración de los hiperparámetros y de la adecuada elección de la arquitectura del modelo. 