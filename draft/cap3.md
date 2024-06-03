# Autocodificadores Variacionales {#sec-Capitulo3}

En este capítulos presentamos la arquitectura del Autocodificador Variacional (VAE) que empleamos para la generación de datos sintéticos. Exponemos brevemente los pasos seguidos en su construcción y las variaciones implementadas para su apropiada aplicación a los problemas abordados. En el capítulo siguiente nos enfocaremos en los Algoritmos Genéticos, sus fundamentos y características. Finalmente, el último capítulo expondremos los resultados obtenidos combinando ambas tecnologías para resolver problemas de selección de características.


## Introducción de los modelos generativos



## Autocodificadores

Los autocodificadores son un tipo de red neuronal especializada en la representación de un espacio de características dado en un espacio de menor dimensión. El objetivo de esta transformación es obtener una representación de baja dimensionalidad y la mayor fidelidad posible del espacio original. Para ello la red debe aprender una representación significativa de los datos observados, reduciendo las señales de entrada a sus factores determinantes. 

Los autocodificadores se componen de dos partes: un *codificador* y un *decodificador*. El *codificador* es una función que toma una observación $x$ y la transforma en un vector de menor dimensión $z$, mientras que el *decodificador* toma el vector $z$ y lo transforma en una observación $x'$ que se asemeja a la observación original. Este vector de menor dimensión $z$ es conocido como *espacio latente*.

En el proceso de aprendizaje de un autocodificador, la red modela la distribución de probabilidad de los datos de entrada $x$ y aprende a mapearlos a un espacio latente $z$. Para ello, se minimiza la diferencia entre la observación original $x$ y la reconstrucción $x'$, lo que se conoce como *error de reconstrucción*. Esta optimización se realiza a través de la *función de pérdida* que se define como la diferencia entre $x$ y $x'$.

Formalmente, podemos establecer hasta aquí estas definiciones: 

- Sea $X$ el espacio de características de los datos de entrada y $Z$ el espacio latente, ambos espacios son euclidianos, $X = \mathbb{R}^m$ y $Z = \mathbb{R}^n$, donde $m > n$.
- Sea las siguientes funciones paramétricas $C_\theta: X \rightarrow Z$ y $D_\phi: Z \rightarrow X'$ que representan el codificador y decodificador respectivamente.
- Entonces para cada observación $x \in X$, el autocodificador busca minimizar la función de pérdida $L(x, D_\phi(E_\theta(x)))$. Ambas funciones $E_\theta$ y $D_\phi$ son redes neuronales profundas que se entrenan simultáneamente.

Para optimizar un autocodificador se requiere un objeto matemático a optimizar que permita medir la diferencia entre la observación original y la reconstrucción. En la práctica, se utiliza generalmente la *distancia euclidiana* entre $x$ y $x'$, es decir, $||x - x'||^2$. La función de pérdida se define como la suma de estas distancias a lo largo de todo el conjunto de datos de entrenamiento. Tenemos entonces que: 

> $L(\theta, \phi)$ =  $argmin_{\theta, \phi} \sum_{i=1}^{N} ||x_i - D_\phi(C_\theta(x_i))||^2$

Donde $L(\theta, \phi)$ representa la función de pérdida que queremos minimizar: $\theta$ son los parámetros del codificador $C$ y $\phi$ son los parámetros del decodificados $D$.


<!---
https://chatgpt.com/share/c1e86afb-15e4-463c-ac87-6808816a6764
-->

## Autocodificadores y el problema de la generación de datos

A través de la representación de un espacio de características dado mediante un espacio latente de menor dimensión se busca modelar la distribución de probabilidad de los datos originales. En este proceso de aprendizaje, la optimización de la función de pérdida no tiene más restricciones que  minimizar la diferencia entre la observación original y la reconstrucción, dando lugar a espacios latentes discontinuos. Esto sucede porque la red puede aprender a representar los datos de entrada de manera eficiente sin necesidad de aprender una representación continua. En la arquitectura del autocodificador no hay determinantes para que dos puntos cercanos en el espacio de características se mapeen a puntos cercanos en el espacio latente. 

Por otro lado, la discontinuidad y la falta de regularidad en el espacio latente permite que sea posible que ciertas regiones de este espacio no tengan ninguna relación válida con el espacio de características. Esto puede ser un problema en la generación de datos, ya que la red puede generar representaciones alejadas de los datos originales.


<!---
https://towardsdatascience.com/understanding-variational-autoencoders-vaes-f70510919f73
Graficar: irregular latent space
-->


## Autocodificadores Variacionales

Los Autocodificadores Variacionales (AVs) buscan resolver los problemas de discontinuidad y falta de regularidad en el espacio latente de los autocodificadores. Comparten con estos últimos la arquitectura *codificador-decodificador*, pero introducen importantes modificaciones. 

Los AVs son modelos generativos capaces de aprender una representación latente de datos observados y generar nuevas muestras con similares características [@kingmaIntroductionVariationalAutoencoders2019]. En esta arquitectura la red codificadora, también llamada *red de reconocimiento*, transforma la distribución de probabilidad de los datos de entrada en una distribución de probabilidad -generalmente más simple (e.g. distribucion normal multivaridada)- en el espacio latente. La red decodificadora, también llamada *red generativa*, transforma la distribución de probabilidad del espacio latente en una distribución de probabilidad en el espacio de características. 

Veamos a continuación este proceso en detalle dado su importancia en el contexto del presente trabajo.

Sea un conjunto de datos de entrada $X = \{x_1, x_2, ..., x_N\}$, donde $x_i \in \mathbb{R}^m$, y constituye una muestra generada de un proceso desconocido y subyacente cuya distribución de probabilidad se ignora. El modelo paramétrico que se busca aprender es $p_\theta(x)$, donde $\theta$ son los parámetros del modelo. En su versión logarítimica se expresa como: 

> $\log p_\theta(X) = \sum_{x \in X} \log p_\theta(x)$

La forma más común de calcular el parámetro $\theta$ es a través de función de *máxima verosimilitud*. 

> $\theta^* = \arg \max_\theta \log p_\theta(X)$

En el contexto de los AVs, el objetivo es modelar la distribución de probabilidad de los datos observados $x$ a través de una distribución de probabilidad en un espacio latente $z$. Es decir, se busca modelar la distribución de probabilidad conjunta de variables observadas y latentes en lugar de la distribución de probabilidad de las variables observadas.

Por esa razón, la distribución de probabilidad conjunta de $x$ y $z$ se expresa como:

> $p_\theta(x, z) = p_\theta(x|z) p(z)$ 

En este punto surge un problema: para calcular la verosimilitud de los datos observados es preciso marginalizar la distribución de probabilidad conjunta con respecto a las variables latentes. Esto se expresa como:

> $p_\theta(x) = \int p_\theta(x|z) p(z) \, dz$

Esta integral puede ser intratable en la práctica, especialmente cuando el espacio latente $z$ es de alta dimensión. Supondría calcular la integral de todas las posibles configuraciones de $z$ en el espacio latente. 

Para abordar este problema, se acude a la inferencia variacional que introduce una aproximación $q_\phi(z|x)$ a la verdadera distribución posterior $p_\theta(z|x)$. En lugar de maximizar directamente la verosimilitud marginal, se maximiza una cota inferior conocida como la *evidence lower bound* (ELBO):

> $\log p_\theta(x) \geq \left(\mathbb{E}_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)] - \text{KL}(q_\phi(z|x) \| p(z)) \right)$

Donde:

- $\mathbb{E}_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)]$ es la esperanza de la log-verosimilitud bajo la aproximación variacional.
- $\text{KL}(q_\phi(z|x) \| p(z))$ es la divergencia de Kullback-Leibler entre la distribución aproximada $q_\phi(z|x)$ y la distribución *a priori* de las variables latentes  $p(z)$.

Así, maximizando esta cota inferior (ELBO), se optimizan simultáneamente los parámetros $\theta$ del modelo y los parámetros $\phi$ de la distribución aproximada, permitiendo una inferencia eficiente y escalable en modelos con variables latentes.

El objetivo de aprendizaje del AV se da entonces por:

> $\mathcal{L}_{AV}(x; \theta, \phi) = \max(\phi,\theta) \left( E_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)] - \text{KL}(q_\phi(z|x) \| p(z)) \right),$

Como puede apreciearse en la ecución anterior la función de pérdida del AV se compone de dos términos: el primero es la esperanza de la log-verosimilitud bajo la aproximación variacional y el segundo es la divergencia de Kullback-Leibler relacionada a la reconstrucción de los datos y la regularización del espacio latente, respectivamente. Existe entre ambos términos una relación de compromiso que permite al AV aprender una representación significativa de los datos de entrada y un espacio latente continuo y regularizado. Cuanto mayor sea la divergencia de Kullback-Leibler, más regularizado será el espacio latente y más suave será la distribución de probabilidad de los datos generados. Cuanto menor sea la divergencia de Kullback-Leibler, más se parecerá la distribución de probabilidad de los datos generados a la distribución de probabilidad de los datos de entrada, sin embargo, el espacio latente será menos regularizado y la generación de datos mas ruidosa.