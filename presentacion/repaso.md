# Repaso para la defensa: preguntas y respuestas

Dudas que surgen al repasar la tesis, con la respuesta y, cuando corresponde, la conexión con el texto y con lo que puede preguntar el jurado. Lo que es conocimiento general y no está escrito en la tesis queda marcado como tal.

------------------------------------------------------------------------

## 1. Métricas para clases desbalanceadas

**Pregunta.** En clasificación con conjuntos desbalanceados, la exactitud puede ser alta porque es global y aun así el modelo predecir muy mal la clase minoritaria, que en fraude bancario o enfermedades raras es la que interesa. ¿Qué métrica representa también a la clase minoritaria y da una perspectiva más equilibrada del desempeño?

**Respuesta corta.** Métricas por clase, promediadas sin ponderar por frecuencia: recall y precisión de la clase minoritaria, la F1 que las combina, la F1 macro en multiclase, la exactitud balanceada y el AUC-ROC o, en desbalance fuerte, el AUC-PR.

**Por qué falla la exactitud.** Con 1% de fraude, un modelo que siempre dice "no fraude" tiene 99% de exactitud y recall cero en la clase que importa. La exactitud pesa cada observación por igual, así que la clase mayoritaria domina.

**Las métricas, de la más simple a la más completa.**

1. **Recall (sensibilidad) de la clase minoritaria.** De los casos reales, cuántos se detectaron. Importa en enfermedad rara, donde un falso negativo cuesta más que un falso positivo.
2. **Precisión de la clase minoritaria.** De los marcados como positivos, cuántos lo eran. Importa cuando cada alerta cuesta investigar, como en fraude.
3. **F1.** Media armónica de precisión y recall; castiga al modelo que sacrifica una por la otra. La media armónica, no la aritmética, impide que una precisión alta tape un recall bajo.
4. **F1 macro** (multiclase). F1 de cada clase, promediada sin ponderar: una clase de 5 muestras pesa igual que una de 50. Es la métrica del capítulo 2 de la tesis, elegida por GCM y sus 14 clases desbalanceadas, y la que deja ver que Breast o Prostate tienen F1 cero aunque la exactitud global sea razonable.
5. **Exactitud balanceada.** Promedio del recall de cada clase; el modelo trivial del ejemplo da 0,5. Es la métrica del desafío NIPS 2003 (tasa de error balanceado) que aparece en la respuesta (a) al jurado.
6. **AUC-ROC.** Independiente del umbral; mide si el modelo ordena positivos por encima de negativos. Límite: en desbalance extremo la tasa de falsos positivos se calcula sobre una clase enorme y puede verse alta aun con muchos falsos positivos en términos absolutos. Por eso en fraude se prefiere el **AUC-PR** (precisión contra recall), que mira solo la clase minoritaria.

**Conexión con la tesis.**

- El capítulo 2 reporta AUC y F1 macro, no exactitud, por esta razón (`utnthesis/Chapters/Capitulo2_v2.qmd`, líneas 62 a 68 definen ROC, F1 y macro-F1).
- La prueba del MLP con datos sintéticos de Leukemia es el ejemplo vivo: la exactitud sube de 0,81 a 0,95, pero el dato que más dice es que el recall de la clase minoritaria pasa de 0,56 a 0,89 (diapositiva 25). La tabla por clase de R5 muestra el fenómeno inverso en GCM: precisión 1,00 en varias clases con recall que cae, modelo más conservador.
- El AG usa exactitud en la función de aptitud. Es un flanco posible en el jurado. Respuesta: la aptitud se fijó para comparar con y sin aumentación bajo el mismo criterio, y el desbalance se atacó del lado del generador (AVC con pesos de clase y muestreo ponderado, diapositiva 13), no del lado de la métrica. Una aptitud con F1 macro o exactitud balanceada entra como trabajo futuro, aunque el capítulo 5 no lo diga así.

*La clasificación de las métricas y el comentario sobre AUC-PR son conocimiento general, no texto de la tesis.*

------------------------------------------------------------------------

## 2. Capítulo 3 paso a paso: del autocodificador al autocodificador variacional

Repaso guiado del capítulo 3 (`utnthesis/Chapters/Capitulo3_v2.qmd`), primero las intuiciones y al final el formalismo. Recorrido: (1) modelos generativos, (2) autocodificador, (3) por qué no sirve para generar, (4) el AV, (5) las dos fuerzas en tensión y la KL, (6) reparametrización, (7) AV condicional, (8) formalismo: verosimilitud, inferencia variacional, Jensen, ELBO, (9) lo implementado. Se va completando a medida que avanza el repaso.

### 2.1 Modelos generativos

Un clasificador aprende p(y|x), una frontera: "dado x, ¿qué clase es?". Un modelo generativo aprende cómo están distribuidos los datos mismos, p(x). Kingma, citado en la tesis: *simula la forma en que los datos son generados en el mundo real*. Si aprendió bien p(x) puede evaluar cuán verosímil es un dato nuevo y, sobre todo, producir datos nuevos que parezcan salidos de la misma fuente.

La clave es "aprender las dependencias": en una imagen, píxeles vecinos se parecen; en un microarreglo, genes de una misma vía se expresan juntos. Un generador que capturó esas dependencias produce muestras coherentes; uno que no, produce ruido con la media correcta.

### 2.2 El autocodificador

Red con forma de reloj de arena: el codificador C_θ comprime la observación x (7.129 genes en Leukemia) a un vector z mucho más corto, el espacio latente, y el decodificador D_φ reconstruye x a partir de z. Se entrenan juntos con un solo objetivo: que la reconstrucción x' se parezca a x, medido por el cuadrado de la distancia euclídea ‖x − x'‖². Nada más.

Intuición del cuello de botella: como z tiene menos dimensiones que x, la red no puede copiar; se queda con lo que más sirve para reconstruir y descarta lo redundante (*preservar la mayor cantidad de información relevante en un vector denso de menos dimensiones*). Compresión aprendida, parecida en espíritu a PCA pero no lineal.

Lo que importa para lo que sigue: el entrenamiento solo pide reconstruir bien los datos que vio. No pide nada sobre cómo se organiza el espacio latente entre medio de esos datos.

**Control.** Si a un autocodificador entrenado sobre Leukemia con z de 25 dimensiones se le da un z al azar, la salida puede no parecerse a ningún dato aunque el z viva en el mismo espacio latente que los datos reales. Eso es la discontinuidad.

### 2.2 bis. Las operaciones vectoriales dentro de las redes

**Pregunta.** ¿El input x se multiplica por un vector de pesos y se le agrega un sesgo?

Casi. Dos correcciones:

- **Es una matriz, no un vector.** Si la capa recibe x con m componentes y produce h con k componentes, los pesos son una matriz W de k × m: cada fila es el vector de pesos de una neurona y la capa calcula las k neuronas de una vez. El sesgo b sí es un vector de k componentes. En Leukemia, m = 7.129; con k = 1.000 neuronas, W₁ tiene 7.129.000 pesos. De ahí el costo de GCM con 16.063 variables.
- **Después del producto hay una no linealidad.** W·x + b es una transformación afín. Tres de esas encadenadas sin nada en el medio siguen siendo una sola transformación lineal (el autocodificador sería PCA). Lo que lo vuelve no lineal es la activación ReLU, que deja pasar los positivos y pone en cero los negativos.

**La cadena completa**, como está en el capítulo 3 (líneas 188 a 219). Cada capa oculta hace `h = ReLU(BatchNorm(W·entrada + b))`.

```
Codificador (achica):
x   (7.129)  →  h₁ = ReLU(BN(W₁x  + b₁))     (p. ej. 1.000)
             →  h₂ = ReLU(BN(W₂h₁ + b₂))     (p. ej. 500)
             →  h₃ = ReLU(BN(W₃h₂ + b₃))     (p. ej. 250)

Cabeza del latente (dos capas lineales independientes, sin BN ni ReLU):
μ      = W_μ h₃ + b_μ        (n, p. ej. 25)
log σ² = W_σ h₃ + b_σ        (n)

Muestreo:
z = μ + σ · ε,   ε ~ N(0, I)

Decodificador (agranda, simétrico):
z   (25)     →  h₄ = ReLU(BN(W₄z  + b₄))
             →  h₅ = ReLU(BN(W₅h₄ + b₅))
             →  x̂ = BN(W₆h₅ + b₆)             (7.129)
```

Tres detalles para poder explicar:

- **Dos cabezas.** μ y log σ² salen de la misma h₃ con matrices distintas, para aprender centro y dispersión por separado. Se predice log σ² y no σ porque el logaritmo puede ser cualquier real, mientras que σ debe ser positiva; así no hay que restringir la salida. Luego σ = exp(½ · log σ²).
- **Sin activación en μ, log σ² ni x̂.** Una ReLU en μ obligaría a centros no negativos; una en x̂ impediría reconstruir valores negativos, y los datos están estandarizados (media 0, desvío 1), así que la mitad son negativos.
- **BatchNorm.** Antes de la ReLU, reescala las activaciones del lote a media y varianza controladas, con dos parámetros aprendibles por neurona. El capítulo lo justifica por estabilidad y velocidad de convergencia; pasar de dos capas sin BN a tres con BN fue lo que mejoró la reconstrucción. Los tamaños de capa del esquema son ilustrativos; los reales se buscaron entre 50 y 5.000 neuronas y el latente entre 10 y 300.

### 2.2 ter. Los pasos con una observación y un ejemplo numérico

**Pregunta.** ¿Lo que ingresa es una observación, un vector de m dimensiones, que se multiplica por matrices? ¿El AV procesa observación por observación?

Sí. Conceptualmente procesa una observación (un paciente) por vez, y las mismas matrices W y sesgos b se aplican a todos los pacientes: un solo juego de parámetros tiene que servir para reconstruir a todos, y eso es "aprender la distribución". En la práctica se procesan lotes: B observaciones apiladas como filas de una matriz X (B × m), por eficiencia y porque BatchNorm necesita el lote para calcular medias y varianzas. El resultado por observación es el mismo que uno por uno, salvo por BatchNorm.

**Pasos para una observación x:**

1. Codificador, capa 1: pre₁ = W₁·x + b₁ → BatchNorm → ReLU → h₁.
2. Capas 2 y 3: igual, con W₂, b₂ y W₃, b₃ → h₃.
3. Cabeza del latente: μ = W_μ·h₃ + b_μ; log σ² = W_σ·h₃ + b_σ. Sin BatchNorm ni ReLU.
4. σ = exp(½ · log σ²), componente a componente.
5. Muestreo: ε ~ N(0, I); z = μ + σ · ε (producto componente a componente).
6. Decodificador, capas 4 y 5: W₄, b₄, BatchNorm, ReLU; W₅, b₅, BatchNorm, ReLU → h₅.
7. Salida: x̂ = BatchNorm(W₆·h₅ + b₆). Sin ReLU, para poder dar negativos.
8. Pérdida: ‖x − x̂‖² (MSE) más la KL calculada a partir de μ y log σ²; se suma sobre el lote.
9. Retropropagación: el gradiente corre hacia atrás por todas las capas y Adam ajusta todas las W y b. Siguiente lote.
10. Generación, terminado el entrenamiento: se descarta el codificador, se sortea z ~ N(0, I) y se ejecutan solo los pasos 6 y 7.

**Ejemplo en miniatura.** m = 4 genes estandarizados, una capa oculta de 3 neuronas, latente n = 2, decodificador de una capa. Sin BatchNorm (necesita un lote).

```
Entrada
x = [ 1,  0, −1,  2 ]                               (4 genes)

Paso 1: codificador
W₁ (3×4) = [ 0,5   0     1     0  ]      b₁ = [ 0   ]
           [ 0     1     0    −1  ]           [ 0,5 ]
           [ 1     1     1     1  ]           [ −1  ]

W₁·x = [ 0,5·1 + 0·0 + 1·(−1) + 0·2 ]   = [ −0,5 ]
       [ 0·1 + 1·0 + 0·(−1) + (−1)·2 ]   = [ −2   ]
       [ 1·1 + 1·0 + 1·(−1) + 1·2    ]   = [  2   ]

pre₁ = W₁·x + b₁ = [ −0,5  −1,5   1 ]
h₁   = ReLU(pre₁)  = [  0     0     1 ]        (los negativos se apagan)

Paso 3: cabeza del latente (n = 2)
W_μ (2×3) = [ 1   0   0,5 ]   b_μ = [0 0]  →  μ      = [  0,5  −0,5 ]
            [ 0   1  −0,5 ]
W_σ (2×3) = [ 0   0  −2   ]   b_σ = [0 0]  →  log σ² = [ −2     0   ]
            [ 0   0   0   ]

Paso 4: σ = exp(½·log σ²) = [ e⁻¹   e⁰ ] = [ 0,37   1 ]

Paso 5: muestreo
ε (sorteado) = [ 0,2  −1 ]
z = μ + σ · ε  = [ 0,5 + 0,37·0,2 ,  −0,5 + 1·(−1) ] = [ 0,57  −1,5 ]

Paso 6: decodificador
W₄ (3×2) = [ 1   0 ]   b₄ = [0 0 0]
           [ 0   1 ]
           [ 1   1 ]
W₄·z = [ 0,57  −1,5  −0,93 ]  →  h₄ = ReLU = [ 0,57   0   0 ]

Paso 7: salida
W₆ (4×3) = [  2   0   0 ]   b₆ = [ 0  0  0  0,3 ]
           [  0   1   0 ]
           [ −2   0   0 ]
           [  3   0   0 ]
x̂ = W₆·h₄ + b₆ = [ 1,15   0   −1,15   2,02 ]

Paso 8: pérdida de reconstrucción
x  = [ 1     0   −1     2    ]
x̂  = [ 1,15  0   −1,15  2,02 ]
MSE = (0,15² + 0² + 0,15² + 0,02²) / 4 ≈ 0,011
```

Para ver en el ejemplo:

- Las dimensiones encajan como una cadena: W₁ es 3×4 porque convierte 4 en 3; W_μ es 2×3 porque convierte 3 en 2; W₆ es 4×3 porque devuelve a 4. Una matriz k × m siempre convierte un vector de m en uno de k.
- μ y log σ² salen de la misma h₁ con matrices distintas: dos lecturas del mismo resumen.
- El mismo paciente con otro sorteo de ε da otro z y otra x̂: ahí está la variación del generador. Con ε = 0 saldría exactamente μ.
- La pérdida compara x̂ con el mismo x que entró, nunca con otro paciente. El autocodificador no necesita etiquetas: aprendizaje autosupervisado.
- Con un lote de B pacientes, X es B × 4 y se calcula X·W₁ᵀ + b₁ (B × 3) de una vez; BatchNorm normaliza cada una de las 3 columnas usando las B filas.

### 2.2 quater. Cómo se pronuncian los símbolos

| Símbolo | Qué es | Se dice |
| --- | --- | --- |
| μ | vector de medias del latente | "miu" (o "mu") |
| σ | vector de desvíos del latente | "sigma" |
| θ | parámetros del decodificador, p_θ | "tita" (o "theta") |
| φ | parámetros del codificador, q_φ | "fi" (es *phi*, no *pi*) |
| ε | ruido del muestreo, ε ~ N(0, I) | "épsilon" |
| ∼ | "tiene esta distribución" (ε ∼ N(0, I)) | "se distribuye según", "sigue una", o "sorteado de" |
| KL( q ‖ p ) | divergencia de Kullback-Leibler; las barras separan los argumentos en orden | "divergencia de Kúlbac-Láibler de q respecto de p", o "la KL" |
| ELBO | límite inferior de evidencia | "elbo", como una palabra |

Frases para decir en voz alta: q_φ(z|x) es "q sub fi de z dado x"; p_θ(x|z) es "p sub tita de x dado z"; ε ∼ N(0, I) es "épsilon sorteado de una normal estándar"; KL(q_φ(z|x) ‖ N(0, I)) es "la KL entre la distribución codificada y la normal estándar".

### 2.3 Por qué el autocodificador no sirve para generar

El espacio latente como un mapa: cada paciente real cae en un punto y el decodificador aprende a reconstruir bien esos puntos. La función de pérdida no dice nada sobre el resto del mapa: ni sobre los huecos, ni sobre si dos pacientes parecidos deben caer cerca (*no hay determinantes para que dos puntos cercanos en el espacio de características se mapeen a puntos cercanos en el espacio latente*).

Dos consecuencias distintas:

- **Huecos sin significado.** Regiones donde nunca cayó un dato; el decodificador nunca reconstruyó nada desde ahí y devuelve algo arbitrario. Es la Figura 3.2, figuras que *no encajan* entre las originales.
- **Sin interpolación.** Un z a mitad de camino entre dos pacientes reales no garantiza un "paciente intermedio": el camino puede atravesar un hueco.

Lo que se quiere de un generador es lo contrario: muestras *ni iguales a las originales ni totalmente distintas*. Para eso el mapa tiene que ser continuo (puntos cercanos dan salidas parecidas) y completo (cualquier región razonable produce algo con sentido). El autocodificador no garantiza ninguna de las dos cosas.

*Aviso para el jurado.* El capítulo dice que los autocodificadores "son un tipo de MG". En rigor, el autocodificador clásico es un modelo de representación, no generativo: no modela p(x) ni tiene mecanismo de muestreo; es el AV el que lo vuelve generativo. Si lo señalan, concederlo sin más; la frase está citada de de la Torre y no afecta nada.

### 2.4 El AV: cada dato es una nube, no un punto

El codificador deja de producir un punto z y produce dos vectores, medias μ y desvíos σ, que definen una normal en el espacio latente. Se toma una muestra z de esa normal y se decodifica. En la imagen del capítulo, μ fija el *centro* (dónde cae el paciente en el mapa) y σ el *área* (cuánto se puede mover alrededor).

Qué consigue:

- Como en cada paso de entrenamiento z es una muestra distinta de la nube, el decodificador tiene que reconstruir bien todo el entorno de μ, no un solo punto. Cada paciente pinta una zona del mapa, no un píxel: continuidad.
- La misma entrada da salidas ligeramente distintas (*incluso para el mismo dato observado, el dato de salida podrá ser diferente*): la variación está incorporada, es un generador por construcción.

Escapatoria que queda abierta: si la red hace σ → 0, cada nube se vuelve un punto y se vuelve al autocodificador con sus huecos. Hace falta una segunda fuerza que le prohíba achicar las nubes y que además las mantenga a todas en una misma región del mapa. Esa fuerza es la KL (2.5).

**Control.** ¿Por qué a la red le convendría llevar σ a cero si su único objetivo fuera reconstruir bien?

------------------------------------------------------------------------

## 3. PCA, EM y AV: el camino de la clase de CMU

Referencia: Bhiksha Raj, *Lecture 21: Variational Autoencoders*, Carnegie Mellon University Deep Learning (11-785), https://www.youtube.com/watch?v=LzEywGCT7-A. La clase construye el AV desde un modelo generativo lineal (PCA probabilístico, Tipping y Bishop 1999) entrenado por EM, y muestra que el AV es ese modelo con una red no lineal en el medio. Lo que sigue es el recorrido estándar de esa clase, no el transcripto; es conocimiento general y no está escrito así en la tesis.

**1. Un modelo generativo lineal: PCA probabilístico.** Cada paciente x se genera sorteando una causa oculta z ~ N(0, I) de pocas dimensiones y haciendo x = W·z + b + ruido gaussiano. Es un decodificador lineal. Tres propiedades lo hacen manejable: p(x) es gaussiana y se calcula en forma cerrada; la posterior p(z|x) ("dado este paciente, dónde está su z") también es gaussiana con fórmula exacta, su media es lineal en x, así que hay un codificador exacto y lineal; y cuando el ruido tiende a cero, la W óptima genera el mismo subespacio que las primeras componentes principales. El PCA clásico es el caso límite de este modelo generativo.

**2. Cómo se entrena: EM.** z nunca se observa. Expectation-Maximization alterna: paso E, con los parámetros actuales, calcular la posterior de z para cada paciente; paso M, dando esas z por buenas, reajustar W y b por mínimos cuadrados. Cada iteración no empeora la verosimilitud. En PCA probabilístico el paso E es exacto porque la posterior tiene fórmula.

**3. PCA clásico como autocodificador.** Un autocodificador con codificador y decodificador lineales entrenado por error cuadrático aprende el subespacio de las componentes principales (ver 2.2: capas lineales encadenadas valen lo mismo que una). El autocodificador clásico agrega la no linealidad; el PCA probabilístico agrega la parte generativa (prior sobre z y ruido). El AV agrega las dos.

**4. El salto al AV.** Reemplazar W·z + b por una red D_θ(z). Se gana que una z gaussiana puede convertirse en una x de cualquier forma: multimodal (14 tipos de tumor), con interacciones no lineales (el XOR de Madelon). Se pierden las tres propiedades del punto 1: p(x) ya no tiene fórmula (es la integral intratable, capítulo 3 línea 94); la posterior p(z|x) tampoco, así que el paso E de EM se vuelve imposible; y no hay solución cerrada para nada.

**5. La solución: aproximar el paso E con otra red.** Se aproxima la posterior con una gaussiana q_φ(z|x) cuyos μ y σ los produce el codificador. Es un paso E aproximado y aprendido: una red produce la posterior de un tiro para cualquier paciente (inferencia *amortizada*). En lugar de alternar E y M, se optimizan θ y φ a la vez por gradiente.

La identidad exacta que une las dos cosas, y que sirve para el formalismo del paso 8:

```
log p(x) = ELBO(q) + KL( q(z|x) ‖ p(z|x) )
```

EM pone q igual a la posterior exacta en el paso E: la KL se hace cero y la cota toca la verosimilitud. El AV no puede; maximiza el ELBO con la mejor q gaussiana que la red logre, y la brecha con la verosimilitud es lo mal que esa gaussiana aproxima la posterior real. **El AV es EM con un decodificador no lineal, un paso E aproximado por una red, y descenso por gradiente en lugar de alternancia.** Falta solo la reparametrización, que deja pasar el gradiente a través del sorteo de z.

**6. Comparación.**

| | PCA | Autocodificador | PCA probabilístico | AV |
| --- | --- | --- | --- | --- |
| Codificador | lineal, exacto (Wᵀ) | red no lineal | lineal, exacto (posterior gaussiana) | red no lineal, aproximado (q_φ) |
| Decodificador | lineal | red no lineal | lineal más ruido | red no lineal |
| Genera datos | no | no | sí, solo gaussianos | sí, de cualquier forma |
| Latente | ejes ortogonales de máxima varianza | sin estructura garantizada | gaussiano por construcción | empujado a gaussiano por la KL |
| Entrenamiento | valores propios | gradiente, error cuadrático | EM, solución cerrada | gradiente sobre el ELBO |
| Interpolar entre dos pacientes | mezclas lineales | sin garantía (huecos) | tiene sentido | tiene sentido y es no lineal |

**7. Si el jurado pregunta "¿por qué no PCA?".** PCA no genera, y su versión generativa solo produce datos gaussianos, con una sola moda y sin interacciones. GCM tiene 14 clases y Madelon es un XOR de cinco variables: ninguna se parece a una gaussiana. El AV conserva lo bueno de PCA, un latente compacto y gaussiano del que es fácil muestrear, y agrega un decodificador no lineal que convierte esa gaussiana en la forma real de los datos. La interpretación de Madelon (diapositiva 31: un latente de 25 no puede memorizar 480 variables de ruido y las deja cerca de la media) es lo mismo que hace una truncación de PCA, pero no lineal y preservando la estructura XOR que PCA no vería.

------------------------------------------------------------------------

## 4. Filmina por filmina

### Filmina 10 · La función de pérdida del autocodificador

```
L(θ, φ) = Σᵢ ‖ xᵢ − D_φ( C_θ( xᵢ ) ) ‖²
```

Es la única función que se optimiza en un autocodificador clásico: no hay una función del codificador y otra del decodificador.

**Pieza por pieza, de adentro hacia afuera.**

1. xᵢ: la observación i, un paciente, vector de m genes.
2. C_θ(xᵢ): el codificador aplicado a ese paciente, devuelve su z. θ son todos los pesos y sesgos del codificador.
3. D_φ(C_θ(xᵢ)): el decodificador aplicado a ese z, devuelve la reconstrucción x̂ᵢ. φ son los pesos del decodificador.
4. xᵢ − x̂ᵢ: el vector de errores, gen por gen.
5. ‖·‖²: cuadrado de la norma euclídea: cada error al cuadrado, sumados los m. Un solo número por paciente, su error de reconstrucción (en el ejemplo de 2.2 ter: 0,15² + 0² + 0,15² + 0,02² ≈ 0,045; el MSE divide además por m).
6. Σᵢ: se suma sobre todos los pacientes de entrenamiento. La pérdida total L es un escalar.
7. L(θ, φ): con los datos fijos, lo único que cambia la pérdida son los parámetros de las dos redes. Entrenar es buscar los θ y φ que la minimizan.

**Qué hace el entrenamiento.** Descenso por gradiente: derivada parcial de L respecto de cada peso, y cada peso se mueve en la dirección que baja L; retropropagación calcula todas las derivadas de la salida hacia la entrada. El codificador se entrena solo con el error que vuelve a través del decodificador: nadie le dice cómo debe ser z, solo recibe "con tu z el decodificador reconstruyó mal, modificate". Por eso θ y φ se entrenan a la vez y la fórmula los tiene a los dos.

**Por qué el cuadrado de la distancia euclídea.**

- Diferenciable en todo punto; el gradiente es 2(x̂ − x), proporcional al error.
- Trata cada gen por igual y como cantidad continua; tiene sentido con datos estandarizados. Es la razón del capítulo para preferir MSE a entropía cruzada en generación (línea 170).
- Lectura probabilística, útil para el paso 8: minimizar ‖x − x̂‖² es maximizar la verosimilitud si x = x̂ + ruido gaussiano. El término de reconstrucción del ELBO, E[log p_θ(x|z)], es este mismo error cuadrático con otro nombre.

**"Sin restricción sobre la estructura del espacio latente".** z no aparece en la fórmula. L solo mide la distancia entre entrada y salida; cualquier z que reconstruya bien es igual de bueno. La red puede ubicar los pacientes en el latente donde quiera, con huecos, y la pérdida no se entera: discontinuidad. El AV agrega un segundo término que sí habla de z, la KL (origen en el respaldo R7).

**Notación, por si el jurado afina.** La ecuación del capítulo (línea 38) escribe `L(θ,φ) = argmin Σ …`. En rigor L es la suma y el argmin devuelve los parámetros óptimos: lo correcto sería `(θ*, φ*) = argmin L(θ,φ)`. La filmina muestra solo la suma, que es lo correcto. Si lo señalan sobre el documento, concederlo como errata de notación.

### Filmina 10 bis · Cómo z se decodifica en x̂

**Pregunta.** ¿Las transformaciones son multiplicación matricial? ¿Cómo hace z para producir x reconstruido?

Sí: multiplicación matriz-vector, suma de un vector de sesgos y una no linealidad componente a componente, repetido capa por capa. El decodificador recorre el camino inverso con matrices que agrandan:

```
z   (25)                                   un paciente comprimido
 │  W₄ (500 × 25) · z + b₄  →  BatchNorm  →  ReLU
h₄  (500)
 │  W₅ (1.000 × 500) · h₄ + b₅  →  BatchNorm  →  ReLU
h₅  (1.000)
 │  W₆ (7.129 × 1.000) · h₅ + b₆  →  BatchNorm           (sin ReLU)
x̂   (7.129)                                el paciente reconstruido
```

Cada fila de W₆ corresponde a un gen de salida y tiene 1.000 pesos que dicen cuánto aporta cada neurona de h₅ a ese gen. El valor reconstruido del gen j es el producto escalar de la fila j con h₅, más bⱼ: 7.129 productos escalares dan los 7.129 genes. Los pesos de esas filas son los que el gradiente ajustó para que, con un paciente real a la entrada, el gen j saliera parecido al original. En el ejemplo de 2.2 ter: la fila `[2 0 0]` de W₆ reconstruye el gen 1 como 2 × 0,57 = 1,15 y la fila `[−2 0 0]` el gen 3 como −1,15.

Dos aclaraciones:

- El decodificador no invierte las matrices del codificador: W₄ no es la inversa de W₃ (no son cuadradas y la ReLU destruye información). Son matrices independientes, entrenadas para deshacer la compresión lo mejor posible en promedio.
- Lo generativo está en los pesos, no en z: z son 25 números sorteados de una normal. Todo lo que el modelo sabe sobre cómo es un paciente (qué genes van juntos, en qué rangos) está en W₄, W₅, W₆ y sus sesgos. Por eso basta el decodificador para generar.

### Filmina 10 ter · Qué hace BatchNorm

**Pregunta.** ¿BatchNorm resta el promedio y multiplica por el desvío?

Resta el promedio y **divide** por el desvío (estandariza), y después multiplica por γ y suma β, dos parámetros aprendibles por neurona.

```
para cada neurona k, sobre las B observaciones del lote:
  media_k   = promedio de las B activaciones de la neurona k
  var_k     = varianza de esas B activaciones
  a_norm    = (a − media_k) / √(var_k + ε)        ← estandariza
  salida    = γ_k · a_norm + β_k                  ← reescala, aprendible
```

- **El promedio es sobre el lote, no sobre el paciente.** Para la neurona k se toman sus B valores, uno por observación, y se calcula media y varianza de esos B. Por eso necesita lotes. El ε evita dividir por cero.
- **γ y β devuelven la libertad.** Solo estandarizar obligaría a media 0 y varianza 1 en toda capa; con γ y β la red aprende la escala y el centro de cada neurona, y hasta puede deshacer la normalización (γ = √var, β = media).
- **En inferencia no hay lote.** Al generar de a una muestra se usan la media y varianza globales acumuladas durante el entrenamiento (promedio móvil de los lotes). En PyTorch, `model.eval()` antes de generar; si no, cada muestra se normaliza contra sí misma y sale mal.

Por qué ayuda (capítulo 3, línea 176): sin BatchNorm, cuando cambian los pesos de la capa 1 cambia la distribución de lo que recibe la capa 2, que debe readaptarse todo el tiempo (*covariate shift* interno). Con entradas de escala estable en cada capa se puede usar mayor tasa de aprendizaje y converge más rápido. Fue lo que destrabó la calidad de reconstrucción al pasar de dos a tres capas.

### Filmina 11 · La caja de reparametrización

**Pregunta.** En el esquema, la caja azul entre codificador y decodificador dice z = μ + σ · ε y lleva el rótulo "reparametrización". ¿Qué resuelve y por qué se llama así?

**El problema.** La pérdida se calcula sobre x̂, que sale del decodificador, que recibe z. Para entrenar el codificador hace falta el gradiente de la pérdida respecto de μ y σ, y de ahí hacia atrás respecto de φ. Pero si z "se sortea de N(μ, σ²)", entre μ, σ y z no hay una fórmula: hay un sorteo. La retropropagación necesita una cadena de operaciones deterministas (sumas, productos, activaciones) para aplicar la regla de la cadena, y sortear no es una de ellas. El gradiente llega hasta z y ahí se corta: nunca alcanza al codificador.

**El truco.** Sortear z de N(μ, σ²) es exactamente lo mismo que sortear ε de N(0, I) y calcular z = μ + σ · ε (es como se sortea de cualquier normal: una estándar, escalada y desplazada). La distribución de z es idéntica, pero la segunda forma de escribirlo cambia todo para el gradiente:

- z pasa a ser una operación determinista, una suma y un producto, de μ, σ y ε.
- Todo el azar queda en ε, que no depende de ningún parámetro: entra de afuera, como un dato más.
- Entonces ∂z/∂μ = 1 y ∂z/∂σ = ε, y la regla de la cadena sigue hacia atrás hasta el codificador sin interrupción.

```
eps = torch.randn_like(sigma)      # ε ~ N(0, I), sin gradiente
z   = mu + sigma * eps             # determinista en mu y sigma
```

**Por qué se llama así.** Parametrizar una variable aleatoria es decir de qué depende. Antes, z estaba parametrizada por la distribución, z ∼ N(μ, σ²): los parámetros entran dentro del sorteo. Después queda parametrizada por una función, z = μ + σ · ε con ε ∼ N(0, I): los parámetros entran en una fórmula y el sorteo ya no depende de ellos. Se *re*-parametrizó: la misma variable aleatoria, escrita con otra dependencia de sus parámetros. Es el nombre que le dieron Kingma y Welling (2013), *reparameterization trick*.

**En el esquema.** La caja azul es la fórmula determinista. Por eso tiene entradas desde la izquierda, μ y σ, que vienen del codificador y llevan gradiente, y una entrada desde arriba, ε ∼ N(0, I), que es la única flecha aleatoria y no lleva gradiente a ningún lado. El rótulo nombra ese reordenamiento: el sorteo se sacó del camino entre codificador y decodificador y se lo puso en una entrada lateral.

Para decirlo en la defensa: "como el azar está todo en épsilon, que no depende de los pesos, el gradiente puede atravesar el sorteo y llegar al codificador" (guion de la filmina 11, sección 6). Desarrollo en el recorrido del capítulo 3, paso 2.6, cuando se llegue.

### Filmina 3 · Qué significa el ε del ruido

**Pregunta.** En x̃ = x + ε, ¿qué es ε?

ε (épsilon) es el término de error: la diferencia entre el valor observado x̃ ("x tilde") y el valor verdadero x que se quería medir. Para un gen de un microarreglo: x es la expresión real, x̃ el número que entregó el escáner, ε todo lo que se metió en el medio (ruido del detector, variación de la hibridación, errores de transcripción). Misma idea que en regresión, y = βx + ε, donde ε es lo que el modelo no explica.

Supuestos habituales sobre ε:

- **Aleatorio y de media cero.** No sesga en promedio; si lo hiciera sería error sistemático, que se corrige con calibración y no con más datos.
- **Gaussiano**, ε ~ N(0, σ²): muchas perturbaciones pequeñas e independientes sumadas dan una campana (teorema central del límite). Con ese supuesto, mínimos cuadrados es máxima verosimilitud (ver filmina 10).
- **Independiente de x.** Cuando el ruido crece con el valor (típico en microarreglos) se toma logaritmo antes; es el log₂ de la figura de Leukemia.

Conexión con la tesis (capítulo 1, línea 144): el AV atenúa el ruido porque el paso codificar-decodificar proyecta a un latente de pocas dimensiones y reconstruye desde ahí. El latente no tiene lugar para guardar ε, que es distinto en cada observación y sin patrón, así que x̂ se parece más a x que a x̃. Madelon es el caso límite: 480 de 500 variables son puro ε y el AV con latente de 25 las devuelve cerca de su media (filmina 30).

*Posible objeción.* El capítulo trata bajo "ruido" dos cosas: valores corrompidos (eso es ε) y características irrelevantes o redundantes (variables enteras sin información, no un error de medición). La tarjeta las separa: la fórmula es lo primero, la línea de abajo lo segundo. La fórmula x̃ = x + ε no está escrita en la tesis; es la formalización estándar del ruido aditivo.

### Filmina 4 · De dónde sale 2ⁿ y por qué base 2

**Pregunta.** En los métodos envolventes se dice que evaluar 2ⁿ subconjuntos es intratable: ¿de dónde surge esa formalización y por qué base 2?

Cada variable tiene dos estados posibles: entra en el subconjunto o no. Con n variables y una decisión sí/no independiente por cada una, hay 2 × 2 × … × 2 = 2ⁿ subconjuntos distintos: el tamaño del conjunto de partes de un conjunto de n elementos. La filmina 14 lo muestra literalmente: el cromosoma es una cadena de n bits, uno por variable, y 2ⁿ es la cantidad de cadenas binarias de largo n. Cada cadena es un subconjunto candidato que el envolvente tendría que evaluar entrenando un clasificador.

"Intratable" es un término de complejidad computacional: un problema es tratable si se resuelve en tiempo polinómico en el tamaño de la entrada; 2ⁿ es exponencial y crece más rápido que cualquier polinomio. La selección exacta de subconjuntos es NP-difícil (Amaldi y Kann, 1998). Esto es conocimiento general; la tesis solo enuncia los 2ⁿ (capítulo 1, línea 103).

| n variables | 2ⁿ subconjuntos |
| --- | --- |
| 10 | 1.024 |
| 20 | ~1 millón |
| 30 | ~1.000 millones |
| 500 (Madelon) | ~3 × 10¹⁵⁰ |
| 7.129 (Leukemia) | ~10²¹⁴⁶ |
| 16.063 (GCM) | ~10⁴⁸³⁵ |

Referencia: átomos del universo observable, ~10⁸⁰; con 300 variables ya se supera. Y cada evaluación de un envolvente es entrenar y validar un clasificador.

*Matiz.* 2ⁿ incluye el subconjunto vacío y el completo; la intratabilidad se refiere al peor caso de la búsqueda exacta. El AG no recorre ese espacio: lo muestrea guiado por la aptitud, evaluando población × generaciones cromosomas (unos miles) en lugar de 2ⁿ. Es la justificación de la línea de cierre de la filmina 4.

### Filmina 4 · ¿Los filtros multivariados ignoran las interacciones?

**Pregunta.** En los métodos de filtro, para los multivariados, ¿es válido decir que no consideran las interacciones entre características?

No. El capítulo 1 (línea 101, citando a Bolón-Canedo) distingue: los filtros univariados evalúan cada característica por separado y "no consideran posibles dependencias entre las características" (chi-cuadrado, ganancia de información); los multivariados "evalúan la relevancia de forma conjunta" y "pueden manejar características redundantes" (selección hacia adelante y hacia atrás como filtro, análisis de correlación; también CFS y mRMR, que la tesis no nombra).

La distinción precisa: lo que define a un filtro no es ignorar las dependencias sino medirlas con un criterio estadístico independiente del clasificador (correlación, información mutua), mientras que el envolvente las evalúa a través del desempeño del modelo. Un filtro multivariado detecta que dos genes son redundantes; no puede saber si la combinación de tres genes individualmente irrelevantes le sirve al clasificador (el XOR de Madelon). Esa es la interacción en el sentido de Fisher y sigue siendo territorio del envolvente.

La viñeta de la filmina quedó: "Univariados: ignoran las dependencias entre variables. Multivariados: las miden con un criterio estadístico, no con el desempeño del modelo."

------------------------------------------------------------------------

## 5. Autocodificador y autocodificador variacional en un párrafo cada uno

**Autocodificador.** Es una red neuronal formada por dos funciones paramétricas entrenadas conjuntamente: un codificador C_θ: ℝᵐ → ℝⁿ, que transforma cada observación xᵢ en un vector latente zᵢ = C_θ(xᵢ) de dimensión n < m, y un decodificador D_φ: ℝⁿ → ℝᵐ, que reconstruye x̂ᵢ = D_φ(zᵢ). En la implementación de la tesis, ambos son redes de tres capas lineales, cada una seguida de normalización por lotes y activación ReLU; el codificador reduce la dimensión en cada capa y el decodificador la expande de forma simétrica, sin activación en la capa de salida para poder reproducir los valores negativos de los datos estandarizados. La única señal de aprendizaje es el error de reconstrucción: se minimiza L(θ, φ) = Σᵢ ‖xᵢ − D_φ(C_θ(xᵢ))‖², el cuadrado de la distancia euclídea sumado sobre el conjunto de entrenamiento, por descenso de gradiente con retropropagación a través de las dos redes. Como la pérdida depende solo de la entrada y de la salida, no impone ninguna estructura sobre el espacio latente: el modelo aprende una compresión no lineal fiel a los datos vistos, pero su espacio latente puede ser discontinuo y por eso no sirve como generador.

**Autocodificador variacional.** Conserva la arquitectura codificador-decodificador, pero cambia lo que el codificador produce y lo que se optimiza. El codificador q_φ(z|x) ya no devuelve un punto sino los parámetros de una distribución normal en el espacio latente: un vector de medias μ y uno de log-varianzas log σ², obtenidos por dos capas lineales independientes sobre la última capa oculta. El vector latente se obtiene por reparametrización, z = μ + σ · ε con ε ~ N(0, I), lo que permite retropropagar a través del muestreo; el decodificador p_θ(x|z) reconstruye x̂ a partir de z con la misma estructura simétrica. Se fija una distribución a priori p(z) = N(0, I). La función objetivo es el límite inferior de evidencia (ELBO): maximizar E_{z~q_φ(z|x)}[log p_θ(x|z)] − KL(q_φ(z|x) ‖ p(z)). En la implementación se minimiza su negativo como la suma del error cuadrático medio de reconstrucción, balanceado por clase en los problemas multiclase, y la divergencia KL, que para dos normales tiene forma cerrada: −½ Σⱼ (1 + log σⱼ² − μⱼ² − σⱼ²). El primer término exige reconstruir fielmente; el segundo obliga a que las distribuciones codificadas se mantengan cerca de la normal estándar, lo que vuelve el espacio latente continuo y regularizado. Por eso, entrenado el modelo, basta muestrear z de N(0, I) y decodificarlo para generar observaciones nuevas; y el compromiso entre los dos términos es lo que condicionó la calidad de reconstrucción en la primera etapa de GCM.

**En paralelo.**

| | Autocodificador | Autocodificador variacional |
| --- | --- | --- |
| Codificador | z = C_θ(x), un punto de ℝⁿ | q_φ(z\|x): dos salidas, μ y log σ² |
| Vector latente | determinístico | z = μ + σ · ε, ε ~ N(0, I) |
| Decodificador | x̂ = D_φ(z) | x̂ = D_θ(z), misma estructura |
| Función de pérdida | Σ ‖x − x̂‖² | Σ ‖x − x̂‖² + KL(q_φ(z\|x) ‖ N(0, I)) |
| Espacio latente | sin restricción; puede ser discontinuo | empujado hacia N(0, I); continuo |
| Generación | no: un z arbitrario no tiene significado | sí: z ~ N(0, I) y decodificar |

*Notación.* En la tesis, la sección de autocodificadores usa θ para el codificador y φ para el decodificador (C_θ, D_φ); la sección variacional usa φ para el codificador (q_φ) y θ para el decodificador (p_θ), que es la convención de Kingma. La tabla sigue a cada sección. La forma cerrada de la KL no está escrita en la tesis; es la expresión estándar para dos gaussianas y es lo que calcula el código.

------------------------------------------------------------------------

## 6. Cómo presentar oralmente las dos funciones de pérdida

Cada guion sigue el orden en que conviene recorrer la fórmula con la mano: de adentro hacia afuera, nombrando primero los símbolos y después lo que la fórmula hace. Lo que va entre corchetes es la indicación de gesto o de ritmo, no se dice.

### Filmina 10 · Autocodificador

> [Señalar el esquema de la izquierda.] "Un autocodificador son dos redes neuronales encadenadas. [Señalar x.] Entra una observación, x, un vector con tantas componentes como características tiene el problema: en Leucemia, siete mil. [Recorrer el trapecio del codificador.] El codificador, C, es una pila de capas que van reduciendo esa dimensión; cada capa multiplica el vector por una matriz de pesos, suma un sesgo y aplica una no linealidad. [Señalar z.] A la salida queda z, el vector latente: la misma observación comprimida en unas pocas dimensiones, que es lo que llamamos espacio latente. [Recorrer el trapecio del decodificador.] El decodificador, D, es la imagen especular: desde z vuelve a ensanchar hasta recuperar la dimensión original. [Señalar x̂.] Su salida es x sombrero, la reconstrucción, que tiene la misma forma que la entrada y se compara con ella. Las dos redes se entrenan juntas con una única función de pérdida, que es esta."
>
> [Bajar a la fórmula.] "Esta es la única función que se optimiza en un autocodificador. [Señalar x sub i.] Tomo una observación, una observación, x sub i. [Señalar C sub theta.] La paso por el codificador, C, cuyos pesos llamo theta, y obtengo su vector latente. [Señalar D sub phi.] Ese vector lo paso por el decodificador, D, con pesos phi, y obtengo la reconstrucción. [Señalar la resta.] Comparo la reconstrucción con la observación original, gen por gen, y elevo al cuadrado la distancia euclídea: ese es el error de reconstrucción de esa observación, un solo número. [Señalar la sumatoria.] Sumo ese error sobre todas las observaciones de entrenamiento, y esa suma es la pérdida L, que depende de theta y de phi porque, con los datos fijos, lo único que puedo mover son los pesos de las dos redes. Entrenar es buscar los pesos que hacen L lo más chica posible, por descenso de gradiente, con el error retropropagándose desde la salida hasta la entrada a través de las dos redes a la vez."
>
> [Pausa. Señalar el esquema de la derecha.] "Fíjense qué no aparece en esta fórmula: z. La pérdida compara entrada y salida, y nada más. Cualquier forma de ubicar las observaciones en el espacio latente que reconstruya bien es igual de buena para ella. Por eso el espacio latente puede quedar discontinuo, con regiones donde nunca cayó un dato, como la zona punteada del esquema: si tomo un punto de ahí y lo decodifico, la salida no guarda relación con los datos. Por eso un autocodificador clásico no sirve como generador. [Pasar a la 11.]"

Duración: unos 80 segundos. Si hay que recortar, el primer párrafo se reduce a "dos redes encadenadas: el codificador comprime x en z y el decodificador reconstruye x sombrero a partir de z".

### Filmina 11 · Autocodificador variacional

> [Señalar el esquema.] "El autocodificador variacional conserva la arquitectura de recién: [recorrer de izquierda a derecha] la observación x entra por la izquierda, el codificador la comprime, el decodificador la reconstruye y a la derecha sale x sombrero. Lo que cambia está en el medio. [Señalar mu y sigma.] El codificador ya no termina en un vector sino en dos, mu y sigma, de la misma dimensión que el latente: son dos capas de salida en paralelo sobre la última capa oculta. [Señalar la caja azul.] Y entre el codificador y el decodificador aparece un paso nuevo, el sorteo de z, que recibe mu y sigma desde la izquierda y, desde arriba, un ruido épsilon tomado de una normal estándar. Lo que entra al decodificador no es lo que produjo el codificador, sino una muestra."
>
> "Es decir, el modelo agrega dos cosas: cambia lo que produce el codificador y agrega un término a la pérdida. El codificador ya no devuelve una posición en el espacio latente sino los parámetros de una distribución sobre él: mu dice dónde está el centro y sigma cuánto se extiende en cada eje. La codificación es esa distribución, una nube, no un punto; y z es una muestra de ella."
>
> [Señalar la caja azul y la flecha de épsilon.] "Esta caja es la reparametrización. Sortear z de una normal con media mu y desvío sigma es lo mismo que sortear épsilon de una normal estándar y calcular mu más sigma por épsilon. Escrito así, z es una suma y un producto, y el azar quedó todo en épsilon, que entra desde arriba y no depende de ningún peso. Por eso el gradiente puede atravesar el sorteo y llegar al codificador; sin este paso, el codificador no se podría entrenar."
>
> [Bajar a la fórmula.] "La pérdida tiene ahora dos términos. [Señalar el primero.] El primero es el mismo error de reconstrucción de recién: la observación contra su reconstrucción, al cuadrado. [Señalar el segundo.] El segundo es la divergencia de Kullback-Leibler entre la distribución que el codificador le asignó a esa observación, q sub phi de z dado x, y la normal estándar. Mide cuánto se aleja esa nube de una normal centrada en cero con desvío uno, y penaliza ese alejamiento."
>
> "Los dos términos tiran en direcciones opuestas. El de reconstrucción quiere nubes chicas y separadas, porque así cada z identifica sin ambigüedad a su observación; llevado al extremo, sigma tiende a cero y volvemos al autocodificador con sus huecos. El término KL quiere nubes anchas y todas centradas en el mismo lugar, porque así se parecen a la normal estándar; llevado al extremo, todas las nubes son iguales y el decodificador no puede distinguir una observación de otra. El entrenamiento encuentra el compromiso: nubes que se solapan lo suficiente para cubrir el espacio sin huecos, pero no tanto como para perder la información. Ese compromiso es lo que vuelve el espacio latente continuo y, al mismo tiempo, es un punto delicado: si la KL domina, se reconstruye mal. Lo vamos a ver en la primera etapa de GCM."
>
> [Cierre.] "Y por eso el modelo genera: terminado el entrenamiento, sorteo z de la normal estándar, que es justamente donde el término KL obligó a que estuvieran todas las nubes, lo paso por el decodificador, y obtengo una observación nueva. [Pasar a la 12, el AV condicional. Si preguntan de dónde sale esta suma: respaldo R7.]"

Duración: unos 120 segundos. Si hay que recortar, el recorrido del esquema se reduce a "misma arquitectura; el codificador produce mu y sigma, y z se sortea antes de decodificar", la reparametrización se reduce a "z igual a mu más sigma por épsilon: el azar queda en épsilon y el gradiente atraviesa el sorteo", y se omite el párrafo de los dos extremos (sigma a cero y nubes iguales) y se deja solo "los dos términos tiran en direcciones opuestas y el entrenamiento encuentra el compromiso".

### Si preguntan

- **"¿Mu y sigma no son dos vectores, es decir, puntos?"** Sí, son dos vectores de dimensión d, pero no son la codificación: son sus parámetros. Mu es el centro de una normal y sigma su extensión en cada eje; lo que el decodificador recibe es un z distinto cada vez, sorteado de esa normal, así que a lo largo del entrenamiento la observación ocupa una región del mapa y no un punto. "Se codifica como una distribución" abrevia "el codificador produce los parámetros de una distribución".
- **"¿Por qué el error cuadrático y no otra distancia?"** Porque es diferenciable en todo punto, pesa a todos los genes por igual, y equivale a máxima verosimilitud si se asume ruido gaussiano en la reconstrucción; eso es lo que lo conecta con el término de reconstrucción del ELBO del respaldo R7.
- **"¿Cómo se calcula la KL?"** Para dos normales tiene forma cerrada: menos un medio de la suma, sobre las dimensiones del latente, de uno más log sigma al cuadrado menos mu al cuadrado menos sigma al cuadrado. No hay que muestrear nada para calcularla.
- **"¿Qué pesa más, reconstrucción o KL?"** En la tesis, igual peso, sin coeficiente; una ponderación de la KL, o su recocido durante el entrenamiento, es el primer trabajo futuro, motivado por lo que pasó en GCM.
- **"¿Por qué N(0, I) como prior?"** Simplifica el cálculo, hace las dimensiones latentes independientes y es de donde después se muestrea; nada obliga a que sea normal, solo que permita diferenciar y calcular la divergencia (capítulo 3, nota al pie sobre la normal multivariada).
