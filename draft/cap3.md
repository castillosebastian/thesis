# Autocodificadores Variacionales {#sec-Capitulo3}

En este capítulos presentamos la arquitectura del Autocodificador Variacional (VAE) que empleamos para la generación de datos sintéticos. Exponemos brevemente sus fundamentos teóricos, los pasos que hemos seguidos en su implementación en este trabajo y las variaciones introducidas para su apropiada aplicación a los problemas abordados. En el capítulo siguiente nos enfocaremos en los Algoritmos Genéticos, sus fundamentos y características. Finalmente, el último capítulo expondremos los resultados obtenidos combinando ambas tecnologías para resolver problemas de selección de características.

## Modelos generativos

Los modelos generativos (MG) son un amplio conjunto de algoritmos de aprendizaje automático que buscan modelar la distribución de probabilidad de datos observados $p(x)$. Estos modelos permiten generar nuevos datos que se asemejan a los datos originales, lo que los hace útiles en tareas de generación de datos sintéticos, imputación de datos faltantes, reducción de dimensionalidad y selección de características, entre otros.

Los modelos generativos pueden tener como *inputs* diferentes tipos de datos, como imágenes, texto, audio, entre otros. Por ejemplo, las imágenes son un tipo de datos para los cuales los MG han demostrado ser muy efectivos. En este caso, cada dato de entrada $x$ es una imagen que puede estar representada por un vector miles de elementos  que corresponden a los valores de píxeles. El objetivo de un modelo generativo es aprender las dependencias [@doerschTutorialVariationalAutoencoders2021]  entre los píxeles (e.g. pixeles vecinos tienden a tener valores similares) y poder generar nuevas imágenes que se asemejen a las imágenes originales.

Podemos formalizar esta idea asumiendo que tenemos ejemplos de datos $x$, distribuidos según una distribución de probabilidad no conocida que queremos modelo $p_\theta(x)$ para que sea capaz de generar datos similares a los originales. 

## Autocodificadores

Los autocodificadores son un tipo de MG especializado en la representación de un espacio de características dado en un espacio de menor dimensión [@delatorreAutocodificadoresVariacionalesVAE2023].  El objetivo de esta transformación es obtener una representación de baja dimensionalidad y mayor fidelidad posible del espacio original. Para ello el modelo debe aprender una representación significativa de los datos observados, reduciendo las señales de entrada a sus dimensiones más importantes. 

Los autocodificadores se componen de dos partes: un *codificador* y un *decodificador*. El *codificador* es una función que toma una observación $x_i$ y la transforma en un vector de menor dimensión $z$, mientras que el *decodificador* toma el vector $z$ y lo transforma en una observación $x_i'$ que -idealmente- se asemeja a la observación original. Este vector de menor dimensión $z$ es conocido como *espacio latente*.

En el proceso de aprendizaje de un autocodificador, la red modela la distribución de probabilidad de los datos de entrada $x$ y aprende a mapearlos a un espacio latente $z$. Para ello, se busca minimizar la diferencia entre la observación original $x_i$ y la reconstrucción $x_i'$, diferencia que se denomina *error de reconstrucción*. Esta optimización se realiza a través de una *función de pérdida* que se define como la diferencia entre $x_i$ y $x_i'$.

Formalmente, podemos establecer estas definiciones [@delatorreAutocodificadoresVariacionalesVAE2023]: 

- Sea $x$ el espacio de características de los datos de entrada y $z$ el espacio latente, ambos espacios son euclidianos, $x = \mathbb{R}^m$ y $z = \mathbb{R}^n$, donde $m > n$.
- Sea las siguientes funciones paramétricas $C_\theta: x \rightarrow z$ y $D_\phi: z \rightarrow x'$ que representan el codificador y decodificador respectivamente.
- Entonces para cada observación $x_i \in x$, el autocodificador busca minimizar la función de pérdida $L(x_i, D_\phi(E_\theta(x_i)))$. Ambas funciones $E_\theta$ y $D_\phi$ son redes neuronales profundas que se entrenan simultáneamente.

Para optimizar un autocodificador se requiere una función que permita medir la diferencia entre la observación original y la reconstrucción. En la práctica, se utiliza generalmente la *distancia euclidia* entre $x_i$ y $x_i'$, es decir, $||x_i - x_i'||^2$. La función de pérdida se define como la suma de todas las distancias a lo largo del conjunto de datos de entrenamiento. Tenemos entonces que: 

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

Dado un conjunto de datos de entrada $x = \{x_1, x_2, ..., x_N\}$, donde $x_i \in \mathbb{R}^m$, se asume que cada muestra es generada por un mismo proceso o sistema subyacente cuya distribución de probabilidad se desconoce y se busca modelar. El modelo buscado procura aprender $p_\theta(x)$, donde $\theta$ son los parámetros de la función. En su versión logarítimica[^1] se expresa como: 

[^1]: Esta función se lee como la log-verosimilitud de los datos observados $x$ bajo el modelo $p_\theta(x)$ y es igual a la suma de las log-verosimilitudes de cada dato de entrada $x_i$.


> $\log p_\theta(x) = \sum_{x_i \in x} \log p_\theta(x)$

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

> $\log p_\theta(x) \geq \left(\mathbb{E}_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)] - \text{KL}(q_\phi(z|x) \| p_\theta(z)) \right)$ [^convexidadlogaritmos]

[^convexidadlogaritmos] Nótese que ese límite es siempre inferior y esto deriba de una de las propiedades de las funciones convexas. Esta propiedad, denominada *desigualdad de Jensen*, establece que el valor esperado de una función convexa es siempre menor o igual a la función de la esperanza. O sea, $\mathbb{E}[f(x)] \leq f(\mathbb{E}[x])$. En este caso, la función logaritmo es cóncava, por lo que la desigualdad se invierte: $\log(\mathbb{E}[x]) \geq \mathbb{E}[\log(x)]$.

Donde:

- $\mathbb{E}_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)]$ es el valor esperado (*esperanza*[^esperanza]) de la log-verosimilitud bajo la aproximación variacional, y determina la precision de la reconstrucción de los datos de entrada.   
[^esperanza]:La esperanza es esencialmente un promedio ponderado de todos los posibles valores que puede tomar la variable aleatoria, donde los pesos son las probabilidades de esos valores. En un VAE, donde consideramos una distribución aproximada $q_\phi(z|x)$ para el espacio latente, la expresión citada es la esperanza de la log-verosimilitud bajo esta distribución.En la práctica se usa **muestreo** para aproximarla, es decir, en lugar de calcular la integral (o suma) exacta, se toman muestras $z^{(i)}$ de la distribución $q_\phi(z|x)$ y se calcula el promedio de las log-verosimilitudes correspondientes:

    $[ \mathbb{E}_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)] \approx \frac{1}{N} \sum_{i=1}^N \log p_\theta (x|z^{(i)})]$

    Aquí, $N$ es el número de muestras. 

- $\text{KL}(q_\phi(z|x) \| p_\theta(z))$ es la divergencia de Kullback-Leibler entre la distribución aproximada $q_\phi(z|x)$ y la distribución *a priori* de las variables latentes  $p_\theta(z)$, y determina la regularización del espacio latente.

Maximizando esta cota inferior (*ELBO*), se optimizan simultáneamente los parámetros $\theta$ del modelo y los parámetros $\phi$ de la distribución aproximada, permitiendo una inferencia eficiente y escalable en modelos con variables latentes.

El objetivo de aprendizaje del AV se da entonces por:

> $\mathcal{L}_\theta,_\phi(x) = \max(\phi,\theta) \left( E_{z \sim q_\phi(z|x)} [\log p_\theta (x|z)] - \text{KL}(q_\phi(z|x) \| p_\theta(z)) \right),$

Como puede apreciearse en la ecuación anterior la función de pérdida del AV se compone de dos términos: el primero es la esperanza de la log-verosimilitud bajo la aproximación variacional y el segundo es la divergencia de Kullback-Leibler relacionada a la reconstrucción de los datos y la regularización del espacio latente. Existe entre ambos términos una relación de compromiso que permite al AV aprender una representación representativa de los datos de entrada y, al mismo tiempo, un espacio latente continuo y regularizado. Cuanto mayor sea la divergencia de Kullback-Leibler, más regularizado será el espacio latente y más suave será la distribución de probabilidad de los datos generados. Cuanto menor sea la divergencia de Kullback-Leibler, más se parecerá la distribución de probabilidad de los datos generados a la distribución de probabilidad de los datos de entrada, sin embargo, el espacio latente será menos regularizado y la generación de datos mas ruidosa.

<!---
Girin, Dynamical Variational Autoencoders: A Comprehensive Review
-->

# Consultas varias

#### Logaritmos

La razón de emplear logaritmo como función objetivo para el cálculo de la verosimilitud radica en su conveniencia para el cálculo. El logaritmo convierte la probabilidad conjunta (que se calcula como el producto de las probabilidades condicionales) en una suma de logaritmos, lo que facilita el cálculo y evita problemas de precisión numérica: $\log(ab) = \log(a)+\log(b)$. 


#### Probabilidad conjunta

La probabilidad conjunta en el contexto de los Autoencoders Variacionales (VAEs) se refiere a la distribución conjunta de los datos observados \(x\) y las variables latentes \(z\). En los VAEs, esta probabilidad conjunta se modela de manera que podamos descomponerla y manejarla más fácilmente. Aquí te explico cómo se calcula la probabilidad conjunta:

### Probabilidad Conjunta en VAEs:

1. **Definición**:
   - La probabilidad conjunta \(p_\theta(x, z)\) describe cómo los datos observados \(x\) y las variables latentes \(z\) se relacionan en el modelo.

2. **Descomposición de la Probabilidad Conjunta**:
   - La probabilidad conjunta se descompone usando la regla de la cadena de probabilidad:
     \[
     p_\theta(x, z) = p_\theta(x|z) \, p_\theta(z)
     \]
   - Aquí, \(p_\theta(x|z)\) es la probabilidad condicional de los datos observados \(x\) dados los latentes \(z\), y \(p_\theta(z)\) es la probabilidad prior de las variables latentes.

### Componentes de la Probabilidad Conjunta:

1. **Probabilidad Condicional \(p_\theta(x|z)\)**:
   - Esta distribución describe cómo se generan los datos observados a partir de las variables latentes. En VAEs, esto suele estar modelado por una red neuronal que toma \(z\) como entrada y produce una distribución sobre \(x\).

2. **Probabilidad Prior \(p_\theta(z)\)**:
   - Esta es la distribución a priori sobre las variables latentes \(z\). En VAEs, se suele asumir que \(z\) sigue una distribución normal multivariada:
     \[
     p_\theta(z) = \mathcal{N}(z; 0, I)
     \]
   - Aquí, \(\mathcal{N}(z; 0, I)\) es una distribución normal con media cero y matriz de covarianza identidad.

### Ejemplo de Cálculo:

Supongamos que estamos trabajando con un modelo VAE simple donde:

- \(p_\theta(x|z)\) es una distribución normal con media y varianza determinadas por una red neuronal parametrizada por \(\theta\).
- \(p_\theta(z)\) es una distribución normal estándar.

La probabilidad conjunta se calcula como:

1. **Obteniendo el prior**:
   \[
   p_\theta(z) = \mathcal{N}(z; 0, I)
   \]

2. **Obteniendo la probabilidad condicional**:
   - Supongamos que la red neuronal parametrizada por \(\theta\) produce una media \(\mu_\theta(z)\) y una desviación estándar \(\sigma_\theta(z)\) para \(x\) dado \(z\).
   - Entonces, \(p_\theta(x|z)\) es:
     \[
     p_\theta(x|z) = \mathcal{N}(x; \mu_\theta(z), \sigma_\theta(z)^2)
     \]

3. **Calculando la probabilidad conjunta**:
   - La probabilidad conjunta es el producto de estas dos distribuciones:
     \[
     p_\theta(x, z) = p_\theta(x|z) \, p_\theta(z)
     \]
   - Sustituyendo las distribuciones normales, se tiene:
     \[
     p_\theta(x, z) = \mathcal{N}(x; \mu_\theta(z), \sigma_\theta(z)^2) \, \mathcal{N}(z; 0, I)
     \]

### Integración en el Contexto de VAEs:

En los VAEs, la probabilidad conjunta \(p_\theta(x, z)\) se usa en el cálculo de la verosimilitud marginal \(p_\theta(x)\) y en la maximización de la ELBO. Para calcular la verosimilitud marginal, integramos \(z\) sobre la probabilidad conjunta:

\[
p_\theta(x) = \int p_\theta(x, z) \, dz = \int p_\theta(x|z) \, p_\theta(z) \, dz
\]

Dado que esta integral suele ser intratable, los VAEs utilizan una distribución aproximada \(q_\phi(z|x)\) y optimizan la ELBO:

\[
\log p_\theta(x) \geq \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) \parallel p_\theta(z))
\]

### Resumen:

La probabilidad conjunta \(p_\theta(x, z)\) en los VAEs se descompone en la probabilidad condicional \(p_\theta(x|z)\) y la probabilidad prior \(p_\theta(z)\). Esta descomposición permite manejar y optimizar el modelo de manera efectiva, incluso cuando la integración exacta es intratable.


#### Derivación del ELBO

Para entender mejor cómo se usa el logaritmo en la derivación de la ELBO, consideremos el siguiente desarrollo:

1. **Log-verosimilitud marginal**:
   $\log p_\theta(x) = \log \left( \int p_\theta(x, z) \, dz \right)$

2. **Aplicando el truco de la variación**:
   $\log p_\theta(x) = \log \left( \int q_\phi(z|x) \frac{p_\theta(x, z)}{q_\phi(z|x)} \, dz \right) $

3. **Aplicando la desigualdad de Jensen**:
   $\log p_\theta(x) \geq \mathbb{E}_{q_\phi(z|x)} \left[ \log \left( \frac{p_\theta(x, z)}{q_\phi(z|x)} \right) \right]$

4. **Descomponiendo la fracción dentro del logaritmo**:
   $\log p_\theta(x) \geq \mathbb{E}_{q_\phi(z|x)} \left[ \log p_\theta(x|z) + \log p_\theta(z) - \log q_\phi(z|x) \right]$

5. **Resultando en la ELBO**:
   $\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) \parallel p_\theta(z))$

Vamos a revisar y explicar cada paso de la derivación de la cota inferior variacional (ELBO) para los Autoencoders Variacionales (VAEs).

### Paso 1: Log-verosimilitud marginal

La log-verosimilitud marginal de los datos observados \(x\) se expresa como:

\[
\log p_\theta(x) = \log \left( \int p_\theta(x, z) \, dz \right)
\]

**Explicación**:
- Aquí, \(p_\theta(x, z)\) es la probabilidad conjunta de los datos observados \(x\) y las variables latentes \(z\).
- La integral \(\int p_\theta(x, z) \, dz\) marginaliza sobre todas las posibles configuraciones de \(z\) para obtener la probabilidad marginal de \(x\).

### Paso 2: Aplicando el truco de la variación

Introducimos una distribución variacional \(q_\phi(z|x)\) para aproximar la verdadera posterior \(p_\theta(z|x)\):

\[
\log p_\theta(x) = \log \left( \int q_\phi(z|x) \frac{p_\theta(x, z)}{q_\phi(z|x)} \, dz \right)
\]

**Explicación**:
- Multiplicamos y dividimos por \(q_\phi(z|x)\), una distribución aproximante que parametrizamos con \(\phi\).
- Esto es válido porque \(\frac{q_\phi(z|x)}{q_\phi(z|x)} = 1\), y permite reformular la integral de una manera que facilita la aplicación de la desigualdad de Jensen.

### Paso 3: Aplicando la desigualdad de Jensen

Aplicamos la desigualdad de Jensen a la expresión anterior para obtener una cota inferior:

\[
\log p_\theta(x) \geq \mathbb{E}_{q_\phi(z|x)} \left[ \log \left( \frac{p_\theta(x, z)}{q_\phi(z|x)} \right) \right]
\]

**Explicación**:
- La desigualdad de Jensen establece que \(\log \mathbb{E}[X] \geq \mathbb{E}[\log X]\) para una variable aleatoria \(X\).
- Aquí, \(X\) es \(\frac{p_\theta(x, z)}{q_\phi(z|x)}\), y estamos tomando la esperanza con respecto a la distribución \(q_\phi(z|x)\).

### Paso 4: Descomponiendo la fracción dentro del logaritmo

Descomponemos el logaritmo de la fracción:

\[
\log p_\theta(x) \geq \mathbb{E}_{q_\phi(z|x)} \left[ \log p_\theta(x|z) + \log p_\theta(z) - \log q_\phi(z|x) \right]
\]

**Explicación**:
- La fracción \(\frac{p_\theta(x, z)}{q_\phi(z|x)}\) se descompone usando las propiedades de los logaritmos:
  \[
  \frac{p_\theta(x, z)}{q_\phi(z|x)} = \frac{p_\theta(x|z) p_\theta(z)}{q_\phi(z|x)}
  \]
- Al tomar el logaritmo de esta fracción, obtenemos:
  \[
  \log \left( \frac{p_\theta(x, z)}{q_\phi(z|x)} \right) = \log p_\theta(x|z) + \log p_\theta(z) - \log q_\phi(z|x)
  \]

### Paso 5: Resultando en la ELBO

La expresión final se convierte en la Evidencia Inferior Variacional (ELBO):

\[
\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) \parallel p_\theta(z))
\]

**Explicación**:
- El primer término \(\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]\) es la esperanza (media) de la log-verosimilitud condicional, evaluada con respecto a la distribución \(q_\phi(z|x)\).
- El segundo término \(D_{\text{KL}}(q_\phi(z|x) \parallel p_\theta(z))\) es la divergencia de Kullback-Leibler, que mide la diferencia entre la distribución aproximada \(q_\phi(z|x)\) y la prior \(p_\theta(z)\).
- Maximizar la ELBO implica maximizar la verosimilitud condicional esperada y minimizar la divergencia KL, lo que ajusta \(q_\phi(z|x)\) para que sea una buena aproximación de \(p_\theta(z|x)\).

### Resumen:

La derivación muestra cómo se obtiene una cota inferior variacional (ELBO) para la log-verosimilitud marginal de los datos. Este enfoque permite optimizar modelos generativos complejos como los VAEs, donde la integración exacta es intratable. La ELBO se convierte en la función objetivo que los VAEs maximizan durante el entrenamiento, balanceando la precisión de la reconstrucción y la regularización de la estructura latente.

# Perdida en el VAE

### Relación entre la Distancia Euclídea y el Error Cuadrático Medio

La **distancia euclídea** y el **error cuadrático medio (MSE, por sus siglas en inglés)** están estrechamente relacionados:

1. **Distancia Euclídea**:
   - Es una medida de la distancia directa (en línea recta) entre dos puntos en un espacio euclidiano.
   - Para dos puntos \( \mathbf{x} \) y \( \mathbf{y} \) en un espacio n-dimensional, se define como:
     \[
     d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}
     \]

2. **Error Cuadrático Medio (MSE)**:
   - Es una medida estadística que cuantifica la diferencia promedio al cuadrado entre los valores estimados por un modelo y los valores reales.
   - Para un conjunto de valores predichos \( \hat{y} \) y valores reales \( y \), se define como:
     \[
     \text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (\hat{y}_i - y_i)^2
     \]
   - El MSE es proporcional al cuadrado de la distancia euclídea entre los valores predichos y los reales.

En resumen, el MSE es esencialmente la distancia euclídea al cuadrado promedio entre los puntos predichos y los puntos reales. 

### Relación con la Entropía Cruzada

La **entropía cruzada** es una métrica de pérdida diferente y se usa comúnmente en problemas de clasificación:

1. **Entropía Cruzada**:
   - Mide la discrepancia entre dos distribuciones de probabilidad: la distribución verdadera \( p \) y la distribución estimada \( q \).
   - Para una clasificación binaria, se define como:
     \[
     H(p, q) = -\frac{1}{n} \sum_{i=1}^{n} [y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i)]
     \]
   - Aquí, \( y \) es el valor verdadero (0 o 1) y \( \hat{y} \) es el valor predicho (probabilidad).

La entropía cruzada es particularmente útil en problemas donde los resultados son probabilidades, mientras que el MSE es más adecuado para problemas de regresión donde las predicciones son valores continuos.

### Métrica de Pérdida en VAE

En un **Variational Autoencoder (VAE)**, se utilizan dos tipos de métricas de pérdida:

1. **Reconstrucción**:
   - Mide la diferencia entre la entrada original y la salida reconstruida por el decodificador.
   - Comúnmente, se usa el error cuadrático medio (MSE) para datos continuos o la entropía cruzada para datos binarios.

2. **Regularización (KL Divergence)**:
   - Es una medida de cuán diferente es la distribución latente aprendida \( q(z|x) \) de la distribución prior \( p(z) \), usualmente una distribución normal.
   - La divergencia KL (Kullback-Leibler) se define como:
     \[
     D_{\text{KL}}(q(z|x) \| p(z)) = \int q(z|x) \log \frac{q(z|x)}{p(z)} dz
     \]

La pérdida total de un VAE es una combinación de estas dos métricas:
\[
\text{Pérdida total} = \text{Pérdida de reconstrucción} + D_{\text{KL}}(q(z|x) \| p(z))
\]

En resumen, en los VAE se utiliza una métrica de pérdida compuesta que incluye tanto el error cuadrático medio (o la entropía cruzada) para la reconstrucción, como la divergencia KL para la regularización.


# Cambio de Signo en la optimización

La diferencia entre la representación teórica y la implementación práctica de la pérdida en un Variational Autoencoder (VAE) radica en el contexto de la optimización que se está realizando. Vamos a explorar esto con más detalle.

### Teoría: Evidencia Inferior Variacional (ELBO)

En la teoría, cuando derivamos el objetivo de un VAE, estamos maximizando la evidencia inferior variacional (ELBO) de la probabilidad logarítmica de los datos:

\[
\log p(x) \geq \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) \| p(z))
\]

Aquí:
- \(\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]\) es el término de reconstrucción esperado.
- \(D_{\text{KL}}(q_\phi(z|x) \| p(z))\) es la divergencia KL entre la distribución aproximada \(q_\phi(z|x)\) y la distribución prior \(p(z)\).

Nuestro objetivo es maximizar el ELBO para que la aproximación sea lo más cercana posible a la verdadera distribución de los datos.

### Práctica: Minimización de la Pérdida

En la práctica, al entrenar modelos de machine learning, trabajamos con optimizadores que minimizan una función de pérdida. Para convertir el problema de maximización del ELBO en un problema de minimización, simplemente negamos el ELBO:

\[
\text{Pérdida} = -\left(\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) \| p(z))\right)
\]

Esto se puede reescribir como:

\[
\text{Pérdida} = D_{\text{KL}}(q_\phi(z|x) \| p(z)) - \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)]
\]

Sin embargo, en la implementación, generalmente se presenta de una manera que suma los términos, ya que es más intuitivo trabajar con términos de pérdida positiva:

\[
\text{Pérdida} = -\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] + D_{\text{KL}}(q_\phi(z|x) \| p(z))
\]

### Reconstrucción y KL en Práctica

Para simplificar aún más, cuando implementamos esto en código, el término de reconstrucción negativo se convierte en una pérdida de reconstrucción positiva (por ejemplo, MSE o entropía cruzada), y la divergencia KL ya es una medida positiva:

```python
# Reconstrucción (usualmente como pérdida positiva)
reconstruction_loss = ((x - x_hat) ** 2).sum()  # MSE

# Divergencia KL (siempre positiva)
kl_loss = autoencoder.encoder.kl

# Pérdida total como suma de términos positivos
loss = reconstruction_loss + kl_loss

# Paso de retropropagación
loss.backward()
optimizer.step()
```

### Resumen

En resumen, aunque teóricamente maximizamos el ELBO y esto involucra una resta, en la práctica minimizamos la pérdida negando el ELBO y reescribiendo los términos para trabajar con sumas de cantidades positivas. Esto es porque los optimizadores como SGD, Adam, etc., están diseñados para minimizar funciones de pérdida.



---

Con estas sugerencias, el texto debería ser más claro y preciso en su explicación de los VAE.