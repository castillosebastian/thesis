## Presentación de nuestro modelo de AV

### AV empleado en dataset de dos clases

El modelo encoder-decoder empleado para la generación de datos sintéticos en el dataset de dos clases (leukemia, madelon y gisette) se compone de dos capas ocultas, cada una seguida de una activación ReLU, mientras que el decoder es simétrico al encoder, con activaciones ReLU y una función de salida Sigmoid. La función de pérdida utilizada combina la divergencia KL y el error cuadrático medio (MSE) para garantizar una representación latente adecuada y una reconstrucción precisa de los datos.

#### 2.1. Encoder

El encoder se encarga de mapear los datos de entrada a un espacio latente de menor dimensión. Está conformado por tres capas lineales con activación ReLU, seguidas de normalización por lotes:

$h_1 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_1}x + b_1))$\
$h_2 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_2}h_1 + b_2))$\
$h_3 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_3}h_2 + b_3))$

#### 2.2. Decoder

El decoder toma el vector latente $z$ y lo transforma de nuevo al espacio original, reconstruyendo los datos de entrada:

$h_4 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_4}z + b_4))$\
$h_5 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_5}h_4 + b_5))$\
$\hat{x} = \text{BatchNorm}(\mathbf{W_6}h_5 + b_6)$

##### Diagrama de Arquitectura del VAE

``` markdown
+------------------------------------+
|                                    |
|           Encoder                  |
|                                    |
|  Input -> [Linear -> ReLU -> BN]   |
|        -> [Linear -> ReLU -> BN]   |
|        -> [Linear -> ReLU -> BN]   |
|                                    |
|    μ  <---------+                  |
|    logσ² <------+                  |
|                                    |
+------------------------------------+
            |
            | (Reparametrization)
            v
+------------------------------------+
|                                    |
|           Decoder                  |
|                                    |
|  z -> [Linear -> ReLU -> BN]       |
|    -> [Linear -> ReLU -> BN]       |
|    -> [Linear -> BN] -> Output     |
|                                    |
+------------------------------------+
```

#### 3. Función de Pérdida

La función de pérdida utilizada en el entrenamiento del VAE es una combinación de la pérdida de reconstrucción (error cuadrático medio) y la divergencia KL, que penaliza la divergencia entre la distribución latente aprendida y una distribución normal, según lo descripto en el precedentemente.

#### 4 Entrenamiento

El proceso de entrenamiento y evaluación del AV se implementa mediante un pipeline optimizado para la convergencia y la evaluación continua. Los pesos de las capas lineales se inicializan uniformemente según la regla $y=1/\sqrt{n}$ para cada capa, garantizando un punto de partida adecuado para la optimización.

El entrenamiento se realizó en mini-batches. Durante cada epoch, se calcula la reconstrucción y los parámetros latentes, y la pérdida se computa como la suma de MSE y la divergencia KL. Esta pérdida se retropropaga, y los parámetros del modelo se actualizan mediante el optimizador Adam. El optimizador Adam fue seleccionado debido a su velocidad de convergencia y estabilidad, especialmente en problemas de alta dimensionalidad como el entrenamiento de un Autoencoder Variacional. Se monitoriza la convergencia imprimiendo la pérdida promedio cada 200 epochs.

Para la evaluación se implementa un ciclo de validación en un conjunto de datos de prueba. Este ciclo asegura que la evaluación del modelo esté desacoplada del proceso de entrenamiento, permitiendo un seguimiento preciso del rendimiento en datos no vistos.


### AV empleado en dataset de dos clases

Este trabajo presenta un Autoencoder Variacional Condicional (CVAE) desarrollado para trabajar con datasets multiclase severamente desbalanceados. El CVAE propuesto combina la capacidad de generación de un VAE tradicional con el condicionamiento explícito en las etiquetas de clase, lo que permite una modelización más precisa de los datos. Para abordar el desbalance de clases en el dataset GCM, que contiene 14 clases con distribuciones desiguales, se implementó una estrategia de ponderación de clases dentro de la función de pérdida, penalizando de manera diferenciada los errores de reconstrucción en función de la clase, mejorando así la capacidad del modelo para representar adecuadamente las clases minoritarias.

Los Autoencoders Variacionales Condicionales (CVAE) han demostrado ser eficaces en tareas de generación de datos condicionados a características específicas, como las etiquetas de clase. Sin embargo, en escenarios donde los datasets están desbalanceados, los modelos generativos pueden tender a favorecer las clases mayoritarias, ignorando las minoritarias. En este trabajo, abordamos este desafío mediante la implementación de un CVAE con una función de pérdida que incorpora ponderaciones de clase, adaptándose específicamente a las características del dataset GCM, compuesto por 14 clases desbalanceadas.

#### 2.1. Encoder

El encoder del CVAE toma tanto las características de entrada como las etiquetas de clase y las concatena, formando un vector combinado que es procesado a través de una serie de capas lineales con activación ReLU y normalización por lotes:

$h_1 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_1}[x, y] + b_1))$      
$h_2 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_2}h_1 + b_2))$   
$h_3 = \text{ReLU}(\text{BatchNorm}(\mathbf{W_3}h_2 + b_3))$   

#### 2.3. Decoder

El decoder también toma como entrada tanto el vector latente \(z\) como las etiquetas de clase \(y\), concatenándolos antes de reconstruir los datos originales:

$z' = \text{ReLU}(\text{BatchNorm}(\mathbf{W_4}[z, y] + b_4))$  
$\hat{x} = \text{Sigmoid}(\mathbf{W_5}z' + b_5)$ 

##### Diagrama de Arquitectura del CVAE

```markdown
+------------------------------------------------+
|                                                |
|                  Encoder                       |
|                                                |
|   Input + Label -> [Linear -> ReLU -> BN]      |
|                -> [Linear -> ReLU -> BN]       |
|                -> [Linear -> ReLU -> BN]       |
|                                                |
|         μ <-----------------+                  |
|         logσ² <-------------+                  |
|                                                |
+------------------------------------------------+
            |
            | (Reparametrization)
            v
+------------------------------------------------+
|                                                |
|                  Decoder                       |
|                                                |
|   z + Label -> [Linear -> ReLU -> BN]          |
|                -> [Linear -> ReLU -> BN]       |
|                -> [Sigmoid -> Output]          |
|                                                |
+------------------------------------------------+
```

#### 3. Función de Pérdida con Ponderación de Clases

Para enfrentar el desbalance de clases en el dataset GCM, se implementó una función de pérdida personalizada que incluye ponderaciones de clase. Estas ponderaciones penalizan más severamente los errores de reconstrucción en clases minoritarias, corrigiendo el sesgo inherente del modelo hacia las clases mayoritarias:

$\mathcal{L} = \frac{1}{N} \sum_{i=1}^{N} w_{y_i} \cdot \text{MSE}(x_i, \hat{x_i}) + \text{KL}(q(z|x) || p(z))
$

donde $(w_{y_i})$ representa el peso asignado a la clase $y_i$, basado en su frecuencia relativa en el dataset.

#### 4. Necesidad de Ponderación

El dataset GCM presenta un desafío significativo debido a su naturaleza multiclase y desbalanceada. Sin ponderación, el modelo tiende a minimizar la pérdida favoreciendo las clases mayoritarias, resultando en una representación latente deficiente para las clases minoritarias. La introducción de ponderaciones corrige este desbalance, permitiendo que el modelo aprenda de manera más equitativa las distribuciones latentes de todas las clases, mejorando así su capacidad de generalización.



-------------
-------------

El desarrollo del modelo de Autoencodificador Variacional (AV) en el marco de esta investigación se llevó a cabo mediante un enfoque sistemático. El proceso se dividió en dos etapas principales: el diseño y validación inicial de la arquitectura del modelo, seguido de la optimización de hiperparámetros para mejorar la calidad de los datos sintéticos generados. Cada una de estas etapas implicó una serie de decisiones clave y experimentos diseñados para garantizar que el modelo fuera no efectivo en la generación de datos sintéticos, sino también robusto y adaptable a una variedad de conjuntos de datos y problemas de selección de características.

En la primera etapa, se centró el esfuerzo en el diseño de la arquitectura del AV. Este proceso comenzó con la creación de una versión inicial y exploratoria del modelo, cuya finalidad era establecer una base sólida para las pruebas posteriores. La arquitectura del modelo fue concebida para manejar la alta dimensionalidad de los conjuntos de datos con los que se trabajaría. Específicamente, se optó por una estructura de red con 2 capas ocultas en el encoder y en el decoder, lo que permitió al modelo aprender representaciones latentes complejas y capturar las relaciones no lineales entre las variables de entrada.

El diseño del encoder del AV incluyó dos capas lineales, cada una seguida de una activación LeakyReLU. Esta elección de activación fue deliberada, dado que LeakyReLU es conocida por su capacidad para mitigar el problema de los gradientes que se desvanecen, una preocupación común en redes profundas. A partir de la salida del encoder, el modelo generaba dos vectores, uno para la media y otro para la varianza logarítmica de la distribución latente, componentes críticos para el proceso de reparametrización. Esta técnica de reparametrización, que permite al modelo generar nuevas muestras en el espacio latente, es un elemento central en la arquitectura de los AVs y fue implementada para permitir que el modelo aprendiera una representación compacta y continua de los datos.

El decoder, encargado de reconstruir los datos originales a partir del espacio latente, fue diseñado con una estructura simétrica a la del encoder, utilizando nuevamente activaciones LeakyReLU y finalizando con una función Sigmoid en la capa de salida. La función Sigmoid fue seleccionada debido a su capacidad para limitar la salida a un rango entre 0 y 1, lo que es particularmente útil para la normalización de los datos de entrada y salida.

La función de pérdida del modelo combinó la divergencia Kullback-Leibler (KLD) y la entropía cruzada binaria (binary cross-entropy). La KLD se utilizó para medir la diferencia entre la distribución aprendida por el modelo y una distribución normal estándar, mientras que la entropía cruzada binaria se empleó para evaluar el error de reconstrucción, es decir, qué tan bien el modelo era capaz de replicar los datos de entrada a partir del espacio latente. La combinación de estas dos pérdidas permitió al modelo equilibrar la fidelidad de la reconstrucción con la regularización del espacio latente, un aspecto esencial para evitar el sobreajuste y asegurar la capacidad de generalización del AV.

Tras validar la arquitectura inicial mediante pruebas preliminares, se procedió a la segunda etapa del proceso, enfocada en la optimización de los hiperparámetros del modelo. Esta etapa implicó ajustar la arquitectura y explorar diferentes configuraciones para mejorar la calidad de los datos sintéticos generados. Se identificaron varias áreas de mejora en la versión inicial del AV, lo que llevó a la implementación de una segunda versión con cambios significativos.

En esta segunda versión, se introdujeron capas de Batch Normalization después de cada capa lineal. La Batch Normalization fue seleccionada debido a su capacidad para estabilizar y acelerar el proceso de entrenamiento, lo que resultó en una convergencia más rápida y en una mejora en la precisión de la reconstrucción. Además, se experimentó con diferentes tamaños de las capas ocultas y del espacio latente, ajustando la arquitectura para optimizar la capacidad del modelo de capturar las características más relevantes de los datos.

Otro aspecto crítico de esta segunda fase fue la redefinición de la función de pérdida. Se desarrolló una nueva función de pérdida que combinaba el error cuadrático medio (MSE) con la divergencia KLD. Esta nueva función permitía una evaluación más precisa de la calidad de la reconstrucción, especialmente para datos con características continuas, mejorando así la capacidad del modelo para generar datos sintéticos que reflejaran de manera fiel las propiedades del conjunto de datos original.

A lo largo de esta etapa de optimización, se realizaron múltiples iteraciones de entrenamiento y evaluación, utilizando el optimizador Adam con una tasa de aprendizaje ajustada. Se experimentó con distintos tamaños del espacio latente, evaluando el balance entre la calidad de reconstrucción y la capacidad de generalización del modelo. Estos experimentos fueron clave para ajustar el AV a las necesidades específicas de los conjuntos de datos utilizados en la investigación, permitiendo una generación de datos sintéticos que no solo replicara los patrones de los datos originales, sino que también capturara la variabilidad inherente a estos.

En paralelo a la optimización del AV, se exploró la extensión del modelo a un Autoencodificador Variacional Condicional (CAV) para su aplicación en conjuntos de datos multiclase, como el dataset GCM. El CAV es una variante del AV que incorpora información de clase en el proceso de codificación y decodificación, permitiendo que el modelo condicione la generación de datos en función de las clases específicas. Esta capacidad es crucial para problemas donde las clases están desbalanceadas o presentan solapamiento, ya que permite una generación más controlada y representativa de los datos sintéticos.

El diseño del CAV incluyó modificaciones en la arquitectura del encoder y del decoder para incorporar las etiquetas de clase. Se ajustaron las dimensiones de entrada y de las capas ocultas para manejar tanto las características originales de los datos como la información de clase, lo que permitió al modelo aprender representaciones latentes que capturan mejor las diferencias entre clases. Durante el entrenamiento del CAV, se evaluó su desempeño en la generación de datos sintéticos multiclase, comparando la calidad de los datos generados con los obtenidos mediante el AV tradicional. Los resultados mostraron que el CAV podía generar datos que preservaban mejor las características distintivas de cada clase, mejorando así la aplicabilidad del modelo en problemas de selección de características en entornos multiclase.

En resumen, el proceso de construcción y optimización del modelo de Autoencodificador Variacional AV, y su extensión a CAV, fue un esfuerzo riguroso y detallado que involucró múltiples fases de diseño, evaluación y ajuste. El resultado final fue un modelo capaz de generar datos sintéticos de alta calidad que preservan las propiedades fundamentales de los datos originales, lo que representa una contribución significativa a la mejora de los algoritmos genéticos en la selección de características, especialmente en contextos de escasez de datos.

Durante el desarrollo de este trabajo, se enfrentaron una serie de desafíos que aportaron aprendizajes valiosos en el proceso de construcción y optimización del modelo de Autoencodificador Variacional Condicional (CVAE) para la generación de datos sintéticos en el contexto de selección de características.

## Busqueda de hiperparámetros

La búsqueda y ajuste de hiperparámetros para los modelos de Autoencodificadores Variacionales (VAE) y Condicionales (CVAE) se ha revelado como un proceso crucial para optimizar la generación de datos sintéticos y, en última instancia, mejorar el rendimiento de los modelos de aprendizaje automático que se entrenan con estos datos. A lo largo de esta etapa de investigación, se implementaron diversas estrategias para identificar las configuraciones óptimas de los modelos, así como para evitar el sobreajuste y garantizar la robustez de los resultados.

Uno de los primeros pasos fue ampliar la búsqueda de hiperparámetros, ajustando variables clave como las dimensiones latentes, las tasas de aprendizaje, y el número de neuronas en las capas ocultas. Un cambio significativo fue la implementación de un mecanismo de paciencia, configurado para detener el entrenamiento si no se observaba mejora en los datos de test durante 10 épocas consecutivas. Esta modificación tuvo un impacto directo en la calidad del modelo, ya que anteriormente, los modelos seguían entrenándose durante todas las épocas establecidas, lo que en muchos casos resultaba en un sobreajuste. La implementación de este corte temprano no solo mejoró la eficiencia del entrenamiento, sino que también contribuyó a reducir el error y mejorar la capacidad de generalización del modelo.

El análisis de los resultados obtenidos mediante estas configuraciones reveló que un MLP entrenado con datos sintéticos generados por un VAE podía igualar o incluso superar el rendimiento de un MLP entrenado con datos reales en algunos casos. Este hallazgo es particularmente notable, ya que sugiere que, bajo ciertas configuraciones, los datos sintéticos pueden ser tan útiles como los datos reales para el entrenamiento de modelos predictivos. Este fenómeno se observó de manera consistente en varios conjuntos de datos, como leukemia, madelon, y gisette, donde la precisión y la exactitud del modelo entrenado con datos sintéticos alcanzaron o superaron las métricas obtenidas con los datos originales.

Un hallazgo interesante se refiere a las dimensiones latentes del modelo. A medida que se ampliaba la búsqueda de hiperparámetros, se descubrió que las mejores configuraciones para la variable latente no eran necesariamente las más grandes. De hecho, en muchos casos, valores de latente_dim entre 3 y 100 ofrecieron los mejores resultados. Esto puede parecer contraintuitivo, ya que se podría suponer que un mayor espacio latente permitiría capturar más complejidad de los datos; sin embargo, estos resultados sugieren que un espacio latente excesivamente grande puede introducir ruido y hacer que el modelo pierda la capacidad de generalizar correctamente.

Las pruebas con diferentes arquitecturas también proporcionaron información valiosa. En el caso de leukemia, se exploraron modelos VAE de dos y tres capas, así como CVAE con múltiples capas, pero no se observaron mejoras significativas al aumentar la complejidad del modelo. En particular, se encontró que las configuraciones más simples, como un VAE de dos capas, ofrecían resultados tan buenos o incluso mejores que sus contrapartes más complejas. Esta observación refuerza la idea de que, en algunos casos, la simplicidad puede ser preferible y que la sobrecomplicación de la arquitectura no necesariamente se traduce en mejores resultados.

Por otro lado, los experimentos realizados en el dataset GCM, que es multiclase, presentaron un desafío diferente. A pesar de la implementación de un CVAE de tres capas, los resultados no mostraron mejoras sustanciales en comparación con un CVAE más simple de dos capas. Además, se observó una disminución en la capacidad del modelo para predecir correctamente clases con menor soporte en el conjunto de datos, lo que sugiere que la complejidad del modelo no fue capaz de capturar adecuadamente la variabilidad de las clases más pequeñas. Este resultado subraya la dificultad inherente al trabajo con conjuntos de datos multiclase, especialmente cuando las clases tienen distribuciones subyacentes similares o están desbalanceadas.

En cuanto a la búsqueda de hiperparámetros, se utilizaron tanto Grid Search como Optimización Bayesiana (BO). Cada una de estas técnicas tiene sus fortalezas, y la elección entre ellas depende en gran medida del objetivo de la búsqueda. Grid Search, por ejemplo, permite un control total sobre el espacio de búsqueda, lo que es útil para responder preguntas específicas, como la configuración óptima de la dimensión latente. Sin embargo, la BO demostró ser particularmente eficiente en la exploración de un espacio de hiperparámetros más amplio y menos definido, logrando un equilibrio entre la exploración y la explotación que resulta especialmente útil cuando se busca optimizar un modelo sin un conocimiento previo preciso del mejor rango de parámetros.

A pesar de los avances logrados, también se encontraron limitaciones. Por ejemplo, incrementar el tamaño de los datos sintéticos en leukemia no condujo a una mejora significativa en los resultados, lo que sugiere que, para ciertos datasets, los beneficios de aumentar los datos sintéticos son marginales una vez alcanzado un umbral de rendimiento. En el caso de GCM, los problemas de baja calidad en la reconstrucción de datos sintéticos por parte del CVAE sugieren que simplemente aumentar el tamaño del dataset no compensa por una arquitectura subóptima o por la dificultad inherente del conjunto de datos.

En resumen, la búsqueda de hiperparámetros y el ajuste de la arquitectura del VAE y CVAE revelaron la importancia de un enfoque balanceado que evite tanto la simplicidad excesiva como la complejidad innecesaria. Los resultados obtenidos muestran que, bajo ciertas configuraciones, los datos sintéticos pueden igualar o superar la utilidad de los datos reales en la formación de modelos predictivos, aunque la eficiencia y la calidad de estos resultados dependen en gran medida de la cuidadosa calibración de los hiperparámetros y de la adecuada elección de la arquitectura del modelo. Estos hallazgos no solo guían el diseño de futuros experimentos, sino que también proporcionan una base sólida para la implementación de técnicas de aumentación de datos en problemas de selección de características.

## Desafíos y aprendizajes en la optimización del CVAE

Uno de los experimentos más reveladores fue el relacionado con el aumento del tamaño del conjunto de datos sintéticos en el dataset GCM. Inicialmente, se logró incrementar las observaciones del conjunto de datos de entrenamiento a 3,000 muestras balanceadas, con 214 observaciones por clase. Este aumento resultó en una mejora significativa en la performance del modelo, logrando igualar los resultados obtenidos con el clasificador MLP entrenado con datos reales. Sin embargo, al continuar incrementando la cantidad de datos sintéticos a 6,000 muestras, se observó una degradación en el rendimiento. Esto sugiere la existencia de un umbral en la cantidad de datos sintéticos que, una vez superado, introduce ruido en el modelo en lugar de aportar valor. Este ruido puede estar relacionado con el solapamiento de las fronteras de decisión en las muestras generadas, lo que aumenta el error y disminuye la precisión del modelo.

Los resultados obtenidos en los experimentos también reflejan que los beneficios de la aumentación de datos tienen un límite. Superado este umbral, la generación adicional de datos no solo deja de ser útil, sino que puede ser perjudicial, como se evidenció en el experimento expN48. Este fenómeno destaca la importancia de una cuidadosa calibración en la cantidad de datos sintéticos generados, especialmente en conjuntos de datos con características complejas y altamente dimensionales como GCM.

Otro aspecto explorado fue la implementación de la pérdida L1 en lugar de MSE. Se realizaron pruebas, como el experimento expN46, para evaluar si la L1_loss podría ofrecer mejoras, pero los resultados no mostraron diferencias significativas en comparación con MSE. Este hallazgo sugiere que, al menos en este contexto específico, la L1_loss no proporciona un beneficio claro sobre el MSE para la tarea de generación de datos sintéticos.

Además, se experimentó con el uso de dropout como técnica de regularización. Se probaron tasas de dropout en un rango de 0.05 a 0.5 en distintas configuraciones de CVAE, tanto con arquitecturas pequeñas (100-500 neuronas por capa) como grandes (1,000-7,000 neuronas por capa). Aunque un experimento con una arquitectura más pequeña (expN59) mostró un resultado interesante con una accuracy de 0.38 en el clasificador MLP, estos resultados se mantuvieron por debajo de los mejores experimentos previos. Esto sugiere que el dropout, si bien útil en otros contextos, no aporta beneficios en configuraciones ya optimizadas del CVAE para este tipo de tareas.

Estos resultados llevaron a una reflexión sobre la falta de impacto positivo de ciertos ajustes, como la introducción de L1_loss y dropout. Es probable que la estabilidad y el buen rendimiento de las configuraciones ya validadas de CVAE, alcanzados a través de numerosos experimentos, limiten el potencial de mejora adicional mediante estos métodos. De hecho, en lugar de mejorar el rendimiento, estos cambios podrían estar degradando los resultados debido a la interferencia con una configuración ya afinada.

En resumen, estos desafíos y aprendizajes subrayan la importancia de un enfoque meticuloso y basado en la experimentación controlada para la optimización de modelos como el CVAE. Aunque técnicas como la aumentación de datos, L1_loss y dropout son poderosas en muchos escenarios, su efectividad depende en gran medida del contexto específico y de la etapa de desarrollo del modelo en la que se implementan. Estos hallazgos no solo aportan una comprensión más profunda del comportamiento del CVAE en la generación de datos sintéticos, sino que también guían futuras investigaciones hacia la identificación de límites efectivos en el uso de estas técnicas.