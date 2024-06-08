# Autocodificadores Variacionales {#sec-Capitulo3}

En este capítulos presentamos la arquitectura del Autocodificador Variacional (VAE) que empleamos para la generación de datos sintéticos. Exponemos brevemente sus fundamentos teóricos, los pasos que hemos seguidos en su implementación en este trabajo y las variaciones introducidas para su apropiada aplicación a los problemas abordados. En el capítulo siguiente nos enfocaremos en los Algoritmos Genéticos, sus fundamentos y características. Finalmente, el último capítulo expondremos los resultados obtenidos combinando ambas tecnologías para resolver problemas de selección de características.

## Modelos generativos

Los modelos generativos (MG) son un amplio conjunto de algoritmos de aprendizaje automático que buscan modelar la distribución de probabilidad de datos observados $p(x)$. Estos modelos permiten generar nuevos datos que se asemejan a los datos originales, lo que los hace útiles en tareas de generación de datos sintéticos, imputación de datos faltantes, reducción de dimensionalidad y selección de características, entre otros.

Los modelos generativos pueden tener como imputs diferentes tipos de datos, como imágenes, texto, audio y video, entre otros. Por ejemplo, las imágenes son un tipo de datos para los cuales los MG han demostrado ser muy efectivos. En este caso, cada dato de entrada $x$ es una imagen que puede estar representada por un vector miles de elementos  que corresponden a los valores de píxeles. El objetivo de un modelo generativo es aprender las dependencias entre los píxeles (e.g. pixeles vecinos tienden a tener valores similares) y poder generar nuevas imágenes que se asemejen a las imágenes originales.

Podemos formalizar esta idea asumiendo que tenemos ejemplos de datos $x$, distribuidos según una distribución de probabilidad no conocida que queremos modelo $p_\theta(x)$ para que sea capaz de generar datos similares a los originales. 

## Autocodificadores

Los autocodificadores son un tipo de MG especializado en la representación de un espacio de características dado en un espacio de menor dimensión [@delatorreAutocodificadoresVariacionalesVAE2023].  El objetivo de esta transformación es obtener una representación de baja dimensionalidad y mayor fidelidad posible del espacio original. Para ello el modelo debe aprender una representación significativa de los datos observados, reduciendo las señales de entrada a sus dimensiones más importantes. 

Los autocodificadores se componen de dos partes: un *codificador* y un *decodificador*. El *codificador* es una función que toma una observación $x_i$ y la transforma en un vector de menor dimensión $z$, mientras que el *decodificador* toma el vector $z$ y lo transforma en una observación $x_i'$ que -idealmente- se asemeja a la observación original. Este vector de menor dimensión $z$ es conocido como *espacio latente*.

En el proceso de aprendizaje de un autocodificador, la red modela la distribución de probabilidad de los datos de entrada $x$ y aprende a mapearlos a un espacio latente $z$. Para ello, se busca minimizar la diferencia entre la observación original $x_i$ y la reconstrucción $x_i'$, diferencia que se denomina *error de reconstrucción*. Esta optimización se realiza a través de una *función de pérdida* que se define como la diferencia entre $x_i$ y $x_i'$.

Formalmente, podemos establecer estas definiciones: 

- Sea $x$ el espacio de características de los datos de entrada y $z$ el espacio latente, ambos espacios son euclidianos, $x = \mathbb{R}^m$ y $z = \mathbb{R}^n$, donde $m > n$.
- Sea las siguientes funciones paramétricas $C_\theta: x \rightarrow z$ y $D_\phi: z \rightarrow x'$ que representan el codificador y decodificador respectivamente.
- Entonces para cada observación $x_i \in x$, el autocodificador busca minimizar la función de pérdida $L(x_i, D_\phi(E_\theta(x_i)))$. Ambas funciones $E_\theta$ y $D_\phi$ son redes neuronales profundas que se entrenan simultáneamente.

Para optimizar un autocodificador se requiere una función que permita medir la diferencia entre la observación original y la reconstrucción. En la práctica, se utiliza generalmente la *distancia euclidia* entre $x_i$ y $x_i'$, es decir, $||x_i - x_i'||^2$. Esta función de pérdida se define como la suma de todas las distancias a lo largo del conjunto de datos de entrenamiento. Tenemos entonces que: 

> $L(\theta, \phi)$ =  $argmin_{\theta, \phi} \sum_{i=1}^{N} ||x_i - D_\phi(C_\theta(x_i))||^2$

Donde $L(\theta, \phi)$ representa la función de pérdida que queremos minimizar: $\theta$ son los parámetros del codificador $C$ y $\phi$ son los parámetros del decodificados $D$.


<!---
https://chatgpt.com/share/c1e86afb-15e4-463c-ac87-6808816a6764
-->

## Autocodificadores y el problema de la generación de datos

En el proceso de aprendiza antes descripto, la optimización no está sujeta a otra restricción mas que  minimizar la diferencia entre la observación original y la reconstrucción, dando lugar a espacios latentes generalmente discontinuos. Esto sucede porque la red puede aprender a representar los datos de entrada de manera eficiente sin necesidad de aprender una representación continua. En la arquitectura del autocodificador no hay determinantes para que dos puntos cercanos en el espacio de características se mapeen a puntos cercanos en el espacio latente. 

Esta discontinuidad en el espacio latente hace posible que ciertas regiones de este espacio no tengan ninguna relación válida con el espacio de características. Esto es un problema en la generación de datos, ya que la red podrá generar representaciones alejadas de los datos originales.


<!---
https://towardsdatascience.com/understanding-variational-autoencoders-vaes-f70510919f73
Graficar: irregular latent space
-->


## Autocodificadores Variacionales

<!---
An Introduction to Variational Autoencoders, KINGMA,2019
-->

Los Autocodificadores Variacionales (AVs) buscan resolver los problemas de discontinuidad y falta de regularidad en el espacio latente de los autocodificadores. Comparte con estos últimos la arquitectura *codificador-decodificador*, pero introducen importantes modificaciones en su funcionamiento. 

En esta arquitectura en lugar de realizar transformaciones determinísticas de los datos de entrada a un espacio latente, se busca modelar la distribución de probabilidad de los datos de entrenamiento aproximando la distribución *a posteriori* de las variables latentes $p(z|x)$.

Así, la red codificadora, también llamada *red de reconocimiento*, transforma la distribución de probabilidad de los datos de entrada en una distribución de probabilidad -generalmente más simple (e.g. distribucion normal multivaridada)- en el espacio latente. La red decodificadora, también llamada *red generativa*, transforma la distribución de probabilidad del espacio latente en una distribución de probabilidad en el espacio de características. 

Dado un conjunto de datos de entrada $x = \{x_1, x_2, ..., x_N\}$, donde $x_i \in \mathbb{R}^m$, se asume que cada muestra es generada por un mismo proceso o sistema subyacente cuya distribución de probabilidad se desconoce y se busca modelar. El modelo buscado procura aprender $p_\theta(x)$, donde $\theta$ son los parámetros de la función. En su versión logarítimica se expresa como: 

> $\log p_\theta(x) = \sum_{x_i \in x} \log p_\theta(x)$

<!---
Esta función se lee como la log-verosimilitud de los datos observados $x$ bajo el modelo $p_\theta(x)$ y es igual a la suma de las log-verosimilitudes de cada dato de entrada $x_i$.
-->

La forma más común de calcular el parámetro $\theta$ es a través del estimador de *máxima verosimilitud*, cuya función de optimización es: 

> $\theta^* = \arg \max_\theta \log p_\theta(x)$, 

es decir, buscamos los parámetros $\theta$ que maximizan la log-verosimilitud asignada a los datos por el modelo. 

Dicho lo anterior, cabe resaltar que, en el contexto de los AVs, el objetivo es modelar la distribución de probabilidad de los datos observados $x$ a través de una distribución de probabilidad conjunta de variables observadas y latentes. Así, la función de verosimilitud de los datos observados se expresa como:

> $p_\theta(x, z) = p_\theta(x|z) p_\theta(z)$,  

que permite hacer explícita la dependencia de $x$ respecto de $z$.

En este punto surge un problema: para calcular la verosimilitud de los datos observados es preciso marginalizar la distribución de probabilidad conjunta con respecto a la variable latente. Esto se define como *probabilidad marginal* y se expresa como:

> $p_\theta(x) = \int p_\theta(x|z)p_\theta(z)dz$

Nótese que esta integral puede ser intratable en la práctica, debido a que no dispone de una solución analítica definida ni tampoco una solución numérica eficiente: $p_\theta(x)$ puede ser multimodal o de alta dimensionalidad, dificultando el cálculo de la integral. 

Para abordar este problema, se acude a la inferencia variacional que introduce una aproximación $q_\phi(z|x)$ a la verdadera distribución posterior $p_\theta(z|x)$. Generalmente se emplea la distribución normal multivariada para aproximar la distribución *a posteriori*, con media y varianza parametrizadas por la red neuronal. Sin embargo, la elección de la distribución no necesariamente tiene que pasar por una distribución normal pues lo importante es que sea una distribución que permita la diferenciación y el cálculo de la divergencia entre ambas distribuciones (por ejemplo si $X$ es binaria la distribución $p_\theta(x|z)$ puede ser una distribución de Bernoulli).

Así, en lugar de maximizar directamente la verosimilitud marginal, se maximiza una cota inferior conocida como *límite inferior de evidencia* (*ELBO* son sus siglas en ingles), dando lugar a la función:

> $\log p_\theta(x) \geq \left(\mathbb{E}_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)] - \text{KL}(q_\phi(z|x) \| p_\theta(z)) \right)$

Donde:

- $\mathbb{E}_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)]$ es la esperanza de la log-verosimilitud bajo la aproximación variacional, y determina la precision de la reconstrucción de los datos de entrada.
- $\text{KL}(q_\phi(z|x) \| p_\theta(z))$ es la divergencia de Kullback-Leibler entre la distribución aproximada $q_\phi(z|x)$ y la distribución *a priori* de las variables latentes  $p_\theta(z)$, y determina la regularización del espacio latente.

Maximizando esta cota inferior (*ELBO*), se optimizan simultáneamente los parámetros $\theta$ del modelo y los parámetros $\phi$ de la distribución aproximada, permitiendo una inferencia eficiente y escalable en modelos con variables latentes.

El objetivo de aprendizaje del AV se da entonces por:

> $\mathcal{L}_\theta,_\phi(x) = \max(\phi,\theta) \left( E_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)] - \text{KL}(q_\phi(z|x) \| p_\theta(z)) \right),$

Como puede apreciearse en la ecuación anterior la función de pérdida del AV se compone de dos términos: el primero es la esperanza de la log-verosimilitud bajo la aproximación variacional y el segundo es la divergencia de Kullback-Leibler relacionada a la reconstrucción de los datos y la regularización del espacio latente. Existe entre ambos términos una relación de compromiso que permite al AV aprender una representación representativa de los datos de entrada y, al mismo tiempo, un espacio latente continuo y regularizado. Cuanto mayor sea la divergencia de Kullback-Leibler, más regularizado será el espacio latente y más suave será la distribución de probabilidad de los datos generados. Cuanto menor sea la divergencia de Kullback-Leibler, más se parecerá la distribución de probabilidad de los datos generados a la distribución de probabilidad de los datos de entrada, sin embargo, el espacio latente será menos regularizado y la generación de datos mas ruidosa.

<!---
Girin, Dynamical Variational Autoencoders: A Comprehensive Review
-->
