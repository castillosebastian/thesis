
# Algoritmos Genéticos {#sec-Capitulo4}

En este capítulos presentamos una descripción general de los AGs, exponemos brevemente sus características y describimos la implementación realizada en nuestro trabajo. Específicamente, comentaremos su componentes y operadores básicos, y presentaremos un script genérico de un AG implementado con la librería `DEAP` de Python, que puede ser adaptado para la selección de características en problemas de alta dimensionalidad. En el capítulo siguiente nos enfocaremos finalmente en los resultados obtenidos combinando ambas tecnologías para resolver problemas de selección de características.

## Elementos básicos de los Algoritmos Genéticos

Los Algoritmos Genéticos (AGs) son una clase de algoritmos de optimización inspirados en la evolución biológica y en la teoría de la selección natural. Los AGs se basan en el concepto de evolución de una población de soluciones potenciales a lo largo de múltiples generaciones, utilizando operadores genéticos como la selección, el cruce y la mutación para generar nuevas soluciones y mejorar la calidad de las mismas. 

En el siguiente fragmento de código presentamos las operaciones elementales de un AG, que como dice Goldberg son *extraordinariamente sencillas*. La secuencia de operaciones se inicializa con un conjunto de soluciones, denominado población. El ciclo iterativo principal del Algoritmo Genético genera nuevas soluciones candidatas descendientes mediante cruce y mutación hasta que la población esté completa. En cada iteración, los individuos son evaluados mediante una función de aptitud que mide su calidad en relación al problema a resolver (aquí, la función de aptitud es simplemente la suma de los valores de los genes, en contextos reales, esta función se ajusta a las necesidades del problema pudiendo ser una función de costo, una métrica de desempeño, entre otras). Los individuos más aptos son seleccionados para reproducirse, lo que implica la aplicación de operadores genéticos para generar nuevos individuos. Este proceso se repite a lo largo de múltiples generaciones, permitiendo que la población evolucione y se adapte a las condiciones del problema. 
    

```python 
import random

# Parámetros del Algoritmo Genético
num_individuals = 5
chromosome_length = 10
num_generations = 10
mutation_rate = 0.1

# Inicializar la población con individuos aleatorios
population = [[random.randint(0, 1) for _ in range(chromosome_length)] for _ in range(num_individuals)]

# Ejecutar el Algoritmo Genético
for generation in range(num_generations):
    # Calcular aptitud
    fitness_values = [sum(ind) for ind in population]

    # Crear nueva población
    new_population = []
    while len(new_population) < num_individuals:
        # Selección de dos padres
        parent1 = random.choices(population, weights=fitness_values)[0]
        parent2 = random.choices(population, weights=fitness_values)[0]

        # Cruce de un punto
        point = random.randint(1, chromosome_length - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        # Mutación
        for i in range(chromosome_length):
            if random.random() < mutation_rate:
                child1[i] = 1 - child1[i]
            if random.random() < mutation_rate:
                child2[i] = 1 - child2[i]

        new_population.append(child1)
        if len(new_population) < num_individuals:
            new_population.append(child2)

    # Reemplazar la población antigua con la nueva
    population = new_population

    # Mostrar la población actual y sus aptitudes
    print(f"Generación {generation + 1}:")
    for ind in population:
        print(f"Individuo: {ind}, Aptitud: {sum(ind)}")
    print()
```

A pesar de su extraordinaria simpleza -o quizas gracias a ella-, los AG constituyen algoritmos robustos, capaces de encontrar soluciones efectivas en una amplia variedad de problemas de optimización. Dicha robustez está determinada, como bien sostiene Goldberg [-@goldbergdavide.GeneticAlgorithmsSearch1989], por una serie de características distintivas, que fortalecen su configuración de búsqueda, a saber: a) operan sobre un espacio *codificado* del problema y no sobre el espacio en su representación original; b) realizan la exploración evaluando una *población de soluciones* y no soluciones individuales; c) tienen como guía una *función objetivo* (también llamada *función de aptitud*) que no requiere derivación u otras funciones de cálculo; y d) suponen *métodos probabilísticos de transición* (operadores estocásticos) y no reglas determinísticas. Estas características permiten a los AG superar restricciones que tienen otros métodos de optimización, condicionados -por ejemplo- a espacios de búsqueda continuos, diferenciables o unimodales. Por ello, su aplicación se ha difundido notablemente, trascendiendo los problemas clásicos de optimización, aplicándose en distintas tareas [@vieQualitiesChallengesFuture2021] y a lo largo de diversas industrias [@jiaoSurveyEvolutionaryMultiobjective2023].

En lo que sigue expondremos brevemente cada una de estas características, destacando su relevancia en el contexto de los AGs y su aplicación en nuestra investigación.

## a) Codificación del espacio de búsqueda

Como señalamos, los AGs se distinguen de otros algoritmos por su capacidad para operar en un espacio codificado del problema, en lugar de operar directamente el espacio en su representación original. Esto sucede gracias a la transformación de las soluciones potenciales en cadenas de datos, comúnmente conocidas como **cromosomas**, que luego son objeto de transformación mediante operadores genéticos como la mutación y el cruce. La capacidad de los AGs para operar con estas representaciones codificadas determina su adaptabilidad y eficacia en una amplia gama de problemas de optimización.

La codificación adecuada del problema es un paso inicial clave para el correcto desempeño del algoritmo. La elección de la codificación depende de la naturaleza del problema y de las características de las soluciones que se buscan optimizar. Por ejemplo, en problemas de optimización combinatoria, dado que las soluciones pueden representarse como permutaciones, una opción intuitiva en términos de codificación es la secuencias de números enteros. Por otro lado, en problemas de optimización continua, como la optimización de funciones matemáticas, las soluciones pueden representarse como vectores de números reales, lo que sugiere una codificación real-valuada. Así, la elección de la codificación adecuada en principio no tiene una respuesta única, antes bien admite múltiples alternativas confiriendo flexibilidad al diseño del AG.

Dada la importancia que tiene la codificación, es fácil advertir que así como una elección adecuada de la estrategia de codificación puede facilitar la convergencia del AG hacia soluciones óptimas, una elección inadecuada puede tener consecuencias negativas en su desempeño. En efecto, una codificación inapropiada puede llevar a una exploración ineficaz del espacio de soluciones o incluso a la generación de soluciones inviables. Así, una codificación que no preserve la viabilidad de las soluciones durante la evolución, puede resultar en la convergencia prematura del AG hacia soluciones subóptimas.

La traducción entre la representación interna codificada (genotipo) y la solución en el contexto del problema (fenotipo) es un componente importante del diseño de los AGs [^genofenotipo]. Este mapeo no solo permite interpretar las soluciones generadas por el algoritmo, sino que también influye en la eficacia de los operadores genéticos. Ello así, por cuanto los operadores genéticos actúan directamente sobre la representación codificada, lo que puede afectar la exploración del espacio de soluciones y la convergencia del AG.

[^genofenotipo]: El **genotipo** se refiere a la representación interna de una solución en el AG. Es la "cromosoma" o la estructura de datos que codifica la información genética de un individuo. En la mayoría de los casos, el genotipo se representa como una cadena de bits (0 y 1), pero también puede ser una cadena de números, caracteres, o cualquier otra estructura adecuada dependiendo del problema. Por otro lado, el **fenotipo** es la manifestación externa o la interpretación del genotipo en el contexto del problema. Es la forma en que se evalúa la solución codificada por el genotipo. El fenotipo corresponde a la solución real en el espacio de búsqueda y es lo que se evalúa mediante la función de aptitud para determinar la calidad de un individuo. Por ejemplo, en un problema de selección de características donde cada característica puede ser incluida o excluida. El genotipo podría ser una cadena binaria donde cada bit representa si una característica está seleccionada (1) o no (0). Genotipo: `1100101`. Aquí, el genotipo representa la selección de ciertas características en un conjunto de datos. Este genotipo incluye las características 1, 2, 4, y 7, mientras que excluye las características 3, 5, y 6. El **fenotipo** es la manifestación externa o la interpretación del genotipo en el contexto del problema. Es la forma en que se evalúa la solución codificada por el genotipo. El fenotipo corresponde a la solución real en el espacio de búsqueda y es lo que se evalúa mediante la función de aptitud para determinar la calidad de un individuo. Siguiendo el ejemplo del genotipo `1100101`, el fenotipo sería la selección efectiva de características en un conjunto de datos. Si tenemos 7 características disponibles, el fenotipo se traduciría en el subconjunto de características seleccionadas por el genotipo. Por ejemplo: Características Disponibles: `[X1, X2, X3, X4, X5, X6, X7]`, Fenotipo: `[X1, X2, X4, X7]` En este caso, el fenotipo es el subconjunto de datos que incluye solo las características seleccionadas (X1, X2, X4, X7). Este subconjunto se utilizará para entrenar un modelo, y su desempeño será evaluado para determinar la aptitud del individuo.

Una de las principales ventajas de operar en un espacio codificado del problema radica en la posibilidad de aplicar operadores genéticos de manera eficiente, lo que permite una exploración exhaustiva del espacio de soluciones. En efecto, los operadores genéticos -que veremos en breve- son diseñados específicamente para actuar directamente sobre la representación codificada, generando nuevas soluciones de manera efectiva. 

Un proceso típico de codificación y decodificación en un AG incluye los siguientes pasos:

1.  **Espacio Original**: Representación directa del problema, por ejemplo, valores continuos o categóricos.
2.  **Codificación**: Traducción del espacio original a una forma binaria o simbólica.
3.  **Operadores Genéticos**: Aplicación de mutación, cruce y selección en la representación codificada.
4.  **Decodificación**: Traducción inversa de la solución codificada al espacio original para evaluación.

En el caso de nuestra investigación, dada la alta dimensionalidad de los datos y la complejidad de los modelos, la codificación adecuada de las soluciones fue un proceso fundamental para garantizar que los AGs puedan encontrar soluciones óptimas o cercanas al óptimo en tiempo razonable.

## b) Búsqueda por *población de soluciones*

Una de las características distintivas de los AGs es su enfoque en la evaluación de una **población** de soluciones en cada iteración, en lugar de centrarse en una única solución. Esta población de soluciones, también conocida como población de **individuos**, permite a los AGs explorar simultáneamente múltiples regiones del espacio de búsqueda, aumentando así la probabilidad de encontrar soluciones óptimas o cercanas al óptimo.

Como vimos en el ejemplo de más arriba, la población inicial regularmente se genera de manera aleatoria, y cada individuo dentro de esta población representa una solución potencial al problema. A lo largo de las generaciones, los AGs aplican operadores genéticos como selección, cruce y mutación para producir nuevas generaciones de individuos, mejorando iterativamente la calidad de las soluciones. 

Un esquema general del proceso de búsqueda por población en un AG se presenta a continuación:

**Esquema del proceso de búsqueda por población**

1.  **Población Inicial**: Generación aleatoria de un conjunto de individuos que representan soluciones potenciales.
2.  **Evaluación de Población**: Cada individuo es evaluado según una función de aptitud para determinar su calidad.
3.  **Operadores Genéticos**:
    -   **Selección**: Elegir individuos más aptos para reproducirse.
    -   **Cruce (Crossover)**: Combinar partes de dos individuos para crear uno nuevo.
    -   **Mutación**: Alterar aleatoriamente un individuo para introducir variabilidad.
4.  **Nueva Generación**: Creación de una nueva población basada en los individuos más aptos.
5.  **Iteración**: Repetición del proceso a través de múltiples generaciones hasta alcanzar un criterio de terminación.

La diversidad genética dentro de la población es fundamental para la eficacia de los AGs, ya que permite a los algoritmos explorar de manera más exhaustiva el espacio de características y evitar la convergencia prematura hacia soluciones subóptimas. En efecto, consideremos una población homogénea donde todos los individuos son idénticos. En este caso, la capacidad del AG para explorar nuevas regiones del espacio de búsqueda se ve severamente limitada, lo que puede resultar en una convergencia temprana hacia soluciones subóptimas. Por el contrario, una población diversa, donde cada individuo representa una solución única, permite al AG explorar una variedad de soluciones y adaptarse a las condiciones cambiantes del problema.

A modo de ejemplo consideremos estas dos población de 5 individuos codificados como sigue:

Población A, con 5 individuos de longitud 5, de alta diversidad:

-   Individuo 1: `11001`
-   Individuo 2: `10110`
-   Individuo 3: `01101`
-   Individuo 4: `11100`
-   Individuo 5: `00011`

Población B, con 5 individuos de longitud 5, de baja diversidad:

-   Individuo 1: `11111`
-   Individuo 2: `11111`
-   Individuo 3: `11111`
-   Individuo 4: `11111`
-   Individuo 5: `11111`

Como podemos advertir en este ejemplo, cada individuo representa una solución potencial al problema, donde cada bit en la cadena codificada corresponde a una característica que puede ser seleccionada o excluida. En estas poblaciónes los individuos de A son distintos entre sí, lo que permite al AG explorar una variedad de soluciones y adaptarse a las condiciones cambiantes del problema, mientras que los individuos de B son idénticos, lo que limita la capacidad del AG para explorar nuevas regiones del espacio de búsqueda.

## c) Función de aptitud y evaluación de soluciones

La función de aptitud es el núcleo que dirige el proceso evolutivo en los AGs, determinando qué soluciones sobreviven y se propagan a la siguiente generación. Su diseño y correcta implementación son esenciales para asegurar que el AG no solo converja hacia soluciones de alta calidad, sino que también lo haga de manera eficiente y efectiva, especialmente en problemas donde las evaluaciones de aptitud son costosas o complejas.

En el proceso evolutivo de los AGs, La función de aptitud se aplica al **fenotipo** de cada solución, es decir, a su manifestación en el contexto del problema a resolver, después de que el **genotipo** (la representación codificada de la solución) ha sido transformado. Esta evaluación cuantifica qué tan bien una solución potencial cumple con los objetivos del problema, asignándole un valor numérico que refleja su desempeño relativo en comparación con otras soluciones dentro de la población.

El diseño de la función de aptitud es un aspecto crítico del proceso de modelado en los AGs, ya que guía la dirección de la búsqueda evolutiva. Específicamente, la función de aptitud debe estar alineada con los objetivos del problema, reflejando correctamente las restricciones necesarias a satisfacer. En situaciones de optimización multiobjetivo, donde varios criterios deben ser optimizados simultáneamente, es común que funciones de aptitud individuales se combinen en una única métrica a través de técnicas como la suma ponderada de los valores de aptitud individuales. En el contexto de nuestra investigación, orientada a la selección de características, la función de aptitud combina la aptitud de un individuo en términos de precisión y el tamaño del conjunto de características seleccionadas (veremos un ejemplo en breve).

En línea con lo anterior, la evaluación precisa de las soluciones mediante la función de aptitud puede constituir un proceso sujeto a multiples restricciones. Aunque la asignación de valores de aptitud más bajos a soluciones subóptimas y más altos a soluciones superiores pueda parecer un criterio ineludible, en la práctica, este proceso requiere comunmente consideraciones adicionales. Por ejemplo, en problemas con restricciones, una solución que se acerque significativamente al óptimo global pero que infrinja requerimientos esenciales del problema debería recibir una calificación de aptitud inferior a una solución factible aunque menos cercana al óptimo con el fin de orientar la búsqueda hacia soluciones viables. Con esa lógica, en la optimización multiobjetivo es necesario establecer criterios para ponderar la proximidad al óptimo, especialmente cuando los distintos objetivos compiten entre sí.

Otro aspecto importante en la función de aptitud es la minimización del número de evaluaciones necesarias para alcanzar el óptimo o una solución lo suficientemente cercana a este. En muchos casos, cada evaluación de aptitud puede ser costosa en términos de tiempo y recursos computacionales, especialmente cuando la evaluación implica la simulación de modelos complejos o el entrenamiento de algoritmos de aprendizaje automático. Por ello, reducir el número de evaluaciones de aptitud es fundamental para mejorar la eficiencia del AG, sin sacrificar la calidad de las soluciones generadas. Este aspecto fue particularmente relevante en nuestra investigación, donde la evaluación de la función de aptitud implicaba el entrenamiento y validación de modelos de clasificación en conjuntos de datos de alta dimensionalidad. La técnica de paralelización y la evaluación diferencial de las soluciones fueron estrategias clave para reducir el tiempo de ejecución, aunque demandó una infraestructura computacional adecuada (más sobre esto en el próximo capítulo).

## d) Operadores estocásticos y esquemas genéticos

Como hemos señalado los AGs emplean **métodos probabilísticos de transición** conformados por **operadores estocásticos**, que introducen aleatoriedad en el proceso evolutivo. Esto determina que las transformaciones dentro de un AG no siguen un camino determinista hacia la solución óptima; en su lugar, cada generación de soluciones es producto de un proceso estocástico controlado. 

Los **operadores genéticos** fundamentales en este proceso son la **selección**, el **cruce (crossover)** y la **mutación**. Los mismos son responsables de la generación de nuevas soluciones, e inciden directamente en la evolución de los  patrones genéticos que los AG tienden a preservar y reproducir. Patrones que se conocen como **esquemas** [-@goldbergdavide.GeneticAlgorithmsSearch1989].

Según explica Goldberg, los **esquemas** son estructuras genéticas que se repiten en la población y que influyen en la evolución de los individuos. Estos esquemas pueden ser de **orden bajo** (pocos genes) o de **orden alto** (más genes), y de **longitud de definición baja** (pocos bits) o de **longitud de definición alta** (más bits). En su operatoria, los AGs tienden a favorecer los esquemas de orden bajo y longitud de definición baja que muestran un rendimiento mejor que la media. Este fenómeno, conocido como **Teorema del Esquema**, proporciona una base para entender cómo la selección y los operadores estocásticos actúan en conjunto para guiar la evolución hacia soluciones óptimas. Veamos esto en detalle.

El operador de **selección** opera identificando y preservando los esquemas con aptitudes superiores a la media de la población. En términos probabilísticos, los esquemas con mejor aptitud tienen una mayor probabilidad de ser seleccionados y reproducidos en la siguiente generación. Esta selección basada en aptitud es clave para mantener y amplificar características beneficiosas dentro de la población. Dicho esto, la selección por sí sola no es suficiente para garantizar la exploración global del espacio de búsqueda, de ahí la importancia del cruce y la mutación.

El operador de **cruce** permite la recombinación de material genético entre dos o más soluciones. En un AG, la función principal del cruce es preservar y mejorar las características exitosas encontradas en los padres, mientras introduce suficiente variación para explorar nuevas áreas del espacio de búsqueda. Por ejemplo, en la representación binaria, un cruce de un punto dividirá dos soluciones en una posición elegida aleatoriamente y combinará segmentos de ambas para crear nuevos individuos. Este proceso asegura la transmisión de esquemas de orden bajo y longitud de definición baja, mientras introduce nuevas combinaciones genéticas que pueden llevar a soluciones más adaptativas.

Un ejemplo de cruce de un punto entre dos soluciones binarias sería:

-   Padre 1: `110010`
-   Padre 2: `101101`
-   Punto de Cruce: `3`
-   Hijo 1: `110101`
-   Hijo 2: `101010`

En este caso, el cruce de un punto en la posición 3 divide los padres en dos segmentos y combina los segmentos para generar dos nuevos individuos. Este proceso de cruce permite la recombinación de material genético entre los padres, preservando y mejorando las características exitosas encontradas en ellos.

El operador de **mutación**, por su parte, introduce cambios aleatorios en las soluciones existentes, actuando como un mecanismo de perturbación que permite al AG escapar de óptimos locales y explorar más exhaustivamente el espacio de soluciones. La mutación puede variar desde simples alteraciones de bits en cadenas binarias hasta ajustes en representaciones continuas mediante la adición de ruido gaussiano. En términos del Teorema del Esquema, la mutación afecta la probabilidad de preservación de esquemas, especialmente aquellos de mayor orden, pero es crucial para asegurar que el AG mantenga la capacidad de descubrir nuevas áreas del espacio de búsqueda.

Un ejemplo de mutación en una solución binaria sería:

-   Solución Original: `110010`
-   Posición de Mutación: `4`
-   Solución Mutada: `110110`


A esta altura ha de ser evidente que la preservación de ciertos patrones genéticos de aptitud superior es fundamental para la evolución de la población en un AG. La teoría de los esquemas, que se basa en el concepto de esquemas genéticos, proporciona un marco formal para entender cómo los operadores genéticos actúan en conjunto para guiar la evolución hacia soluciones óptimas. 

Goldberg nos presenta, en relación a este punto, lo que se conoce como la **Ecuación del Esquema**, que es una herramienta teórica que permite predecir la evolución de los esquemas en una población a lo largo de múltiples generaciones. Esta ecuación tiene en cuenta factores como la aptitud de los esquemas, la probabilidad de cruce y mutación, la longitud de definición y el orden de los esquemas, y proporciona una guía para entender cómo los esquemas se propagan y se mantienen en la población.

La Ecuación del Esquema predice el número esperado de copias de un esquema $H$ en la próxima generación $t+1$, dado su número de copias en la generación actual $t$. Se expresa de la siguiente manera:

$
m(H, t+1) \geq m(H, t) \cdot \frac{f(H)}{\bar{f}} \cdot \left[ 1 - p_c \frac{\delta(H)}{l-1} \right] \cdot \left(1 - p_m\right)^{o(H)}
$

Donde:
- $m(H, t)$ es el número de copias del esquema $H$ en la generación $t$.
- $f(H)$ es la aptitud promedio de los individuos que pertenecen al esquema $H$.
- $\bar{f}$ es la aptitud promedio de la población total.
- $p_c$ es la probabilidad de cruce.
- $\delta(H)$ es la longitud de definición del esquema $H$, que es la distancia entre el primer y el último gen fijo en el esquema.
- $l$ es la longitud del cromosoma.
- $p_m$ es la tasa de mutación.
- $o(H)$ es el orden del esquema, es decir, el número de posiciones fijas en el esquema.

Consideremos un ejemplo con los siguientes parámetros:

- Longitud del cromosoma: $l = 6$
- Esquema $H = 1\ast0\ast1\ast$ (donde $\ast$ puede ser 0 o 1)
- Población actual tiene 100 individuos.
- $m(H, t) = 20$ (es decir, 20 individuos coinciden con el esquema $H$).
- Aptitud promedio de la población $\bar{f} = 15$.
- Aptitud promedio de los individuos que coinciden con el esquema $H$, $f(H) = 18$.
- Probabilidad de cruce $p_c = 0.7$.
- Tasa de mutación $p_m = 0.01$.
- Longitud de definición del esquema $\delta(H) = 4$ (dado que las posiciones fijas son 1, 3 y 5, la distancia entre las posiciones es 4).
- Orden del esquema $o(H) = 3$ (el número de posiciones fijas es 3).

Aplicando estos valores a la Ecuación del Esquema:

1. **Factor de Selección**: 
   $
   \frac{f(H)}{\bar{f}} = \frac{18}{15} = 1.2
   $
   Esto indica que los individuos que coinciden con el esquema $H$ tienen una aptitud superior a la media y, por lo tanto, es más probable que sean seleccionados.

2. **Probabilidad de Conservación ante el Cruce**:
   $
   1 - p_c \frac{\delta(H)}{l-1} = 1 - 0.7 \cdot \frac{4}{6-1} = 1 - 0.7 \cdot 0.8 = 1 - 0.56 = 0.44
   $
   Hay un 44% de probabilidad de que el esquema $H$ se conserve tras el cruce.

3. **Probabilidad de Conservación ante la Mutación**:
   $
   (1 - p_m)^{o(H)} = (1 - 0.01)^{3} = 0.99^3 \approx 0.9703
   $
   El esquema $H$ tiene aproximadamente un 97% de probabilidad de no ser destruido por la mutación.

4. **Cálculo Final**:
   $
   m(H, t+1) \geq 20 \cdot 1.2 \cdot 0.44 \cdot 0.9703 \approx 20 \cdot 0.5127 = 10.254
   $
   Por lo tanto, en la próxima generación, se espera que haya al menos 10 copias del esquema $H$ en la población.

Este cálculo muestra cómo el esquema $H$, que tiene una aptitud superior a la media y ciertas características de proximidad posicional (es decir, una longitud de definición baja), es favorecido en la reproducción y es probable que se mantenga en la población. 

Con los elementos vistos hasta aquí podemos pasar, en la parte final del presente capítulo, a la implementación de un Algoritmo Genético. 

## Implementación de un Algoritmo Genético para la selección de características

En esta sección se describe la implementación que hemos realizado de AG, usando la librería `DEAP` de Python, para la selección de características en problemas de alta dimensionalidad. La implementación se centra en la optimización simultánea de la precisión de un modelo de clasificación y la reducción del número de características seleccionadas, utilizando operadores genéticos clásicos como el cruce y la mutación, junto con técnicas avanzadas de evaluación y selección.

La configuración inicial del AG a lo largo de los distintos experimentos que formaron parte de esta investigación (y que revisaremos en detalle en el próximo capítulo) incluyó: 

- **Población inicial**: individuos generados aleatoriamente, cada uno representado como una lista de bits de longitud igual al número de características.
- **Función de aptitud**: Maximización de la precisión del modelo de clasificación y minimización del número de características activas.
- **Operadores genéticos**: Selección por torneo, cruce de dos puntos y mutación por inversión de bits.
- **Parámetros del AG**: Probabilidad de mutación (e.g.`PROB_MUT = 0.1`), probabilidad de cruce (e.g. `PX = 0.75`), número máximo de generaciones (e.g.`GMAX = 15`).
- **Evaluación de características**: Análisis de la frecuencia de activación de las características a lo largo de las generaciones.
- **Criterio de terminación**: Convergencia o número máximo de generaciones alcanzado.
- **Análisis de resultados**: Selección de las características más relevantes basadas en su frecuencia de activación.

En cada experimento, la implementación del AG comienza con la definición de los componentes básicos del algoritmo. Se define una función de aptitud (`fitness`) orientada a maximizar, que evalúa cada individuo en función de dos criterios: la precisión (`accuracy`) del modelo de clasificación entrenado con las características seleccionadas, y la fracción de características activas. Esta función de aptitud está diseñada para balancear la necesidad de un modelo predictivo preciso con la simplicidad y la eficiencia del modelo, evitando el sobreajuste y facilitando la interpretación del modelo final.

Los individuos, representados como listas de bits, se construyen utilizando una función de construcción de genes que genera un bit aleatorio basado en una probabilidad definida (`p_indpb`). Estos individuos se agrupan en una población inicial, que luego se somete a un proceso evolutivo. Durante la evolución, los individuos se seleccionan mediante la técnica de torneo, donde aquellos con mejor aptitud tienen una mayor probabilidad de ser elegidos para reproducción. Los individuos seleccionados se cruzan utilizando un operador de cruce de dos puntos (`cxTwoPoint`), que intercambia segmentos de los cromosomas de los padres para generar descendientes con combinaciones genéticas novedosas. Posteriormente, se aplica un operador de mutación que invierte los bits en el cromosoma según la probabilidad de mutación definida, asegurando que el AG mantenga la capacidad de explorar nuevas regiones del espacio de búsqueda.

A lo largo de las generaciones, el AG monitoriza y registra diversas estadísticas de la población, como la aptitud promedio, la precisión y el número de genes activos. Estas métricas permiten evaluar el progreso del algoritmo y la convergencia hacia soluciones óptimas. Al final del proceso evolutivo, se realiza un análisis de las características seleccionadas, calculando la frecuencia de activación de cada característica a lo largo de las generaciones y seleccionando las más recurrentes como las más relevantes. Este enfoque permite identificar un subconjunto óptimo de características que no solo maximiza la precisión del modelo, sino que también minimiza su complejidad.

A continuación, y con fines ilustrativos, se presenta un script genérico de un Algoritmo Genético implementado con la librería `DEAP` de Python, que puede ser adaptado para la selección de características en problemas de alta dimensionalidad. Este script incluye la definición de los componentes básicos del AG que vimos antes, como la función de aptitud, los operadores genéticos y los parámetros del algoritmo, así como la configuración de la población inicial y la ejecución del proceso evolutivo a lo largo de 15 generaciones.

```python
import random
import numpy as np
from deap import base, creator, tools
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Parámetros del Algoritmo Genético
PROB_MUT = 0.1        # Probabilidad de mutación
PX = 0.75             # Probabilidad de cruce
GMAX = 15             # Número máximo de generaciones
POP_SIZE = 20         # Tamaño de la población

# Carga del conjunto de datos de ejemplo
data = load_breast_cancer()
X = data.data
y = data.target

# División del conjunto de datos en entrenamiento y prueba
Xtrain, Xtest, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tamaños derivados
DAT_SIZE = Xtrain.shape[0]
IND_SIZE = Xtrain.shape[1]
PM = 1 / IND_SIZE    # Probabilidad de mutación por gen

# Definición de la función de fitness
def fitness(individual, Xtrain, Xtest, y_train, y_test):
    """Función de aptitud para evaluar la calidad de un individuo."""
    if not any(individual):
        return 0,  # Evita seleccionar individuos sin genes activos
    
    X_train = Xtrain[:, individual]
    X_test = Xtest[:, individual]

    model = MLPClassifier(hidden_layer_sizes=(5, 3), max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    # Minimización del número de características seleccionadas
    n_genes = np.sum(individual)
    alpha = 0.5  # Ponderación entre precisión y número de genes

    return alpha * accuracy + (1 - alpha) * (1 - n_genes / IND_SIZE),

# Configuración del entorno evolutivo
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", lambda: random.random() < PM)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=PROB_MUT)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", fitness, Xtrain=Xtrain, Xtest=Xtest, y_train=y_train, y_test=y_test)

# Función principal del Algoritmo Genético
def main():
    # Inicialización de la población
    population = toolbox.population(n=POP_SIZE)

    # Evaluación inicial
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Bucle evolutivo
    for gen in range(GMAX):
        # Selección y reproducción
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))
        
        # Aplicación del cruce y mutación
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < PX:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < PROB_MUT:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluación de los nuevos individuos
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Reemplazo de la población
        population[:] = offspring

        # Recopilación de estadísticas
        fits = [ind.fitness.values[0] for ind in population]
        print(f"Generación {gen + 1} - Mejor fitness: {max(fits):.4f} - Promedio fitness: {np.mean(fits):.4f}")

    # Mejor individuo al finalizar
    best_ind = tools.selBest(population, 1)[0]
    print("\nMejor individuo encontrado: ", best_ind)
    print(f"Fitness: {best_ind.fitness.values[0]:.4f}")
    print(f"Número de características seleccionadas: {np.sum(best_ind)}")

if __name__ == "__main__":
    main()
```