# Repositorio de Tesis de Maestría en la UTN-Paraná Minería de Datos    

# Tema:

- Autoencoder Variacionales y Algoritmos Genéticos   

# Renderizar la tesis: 

```bash
cd utnthesis
quarto render     
```

# Fuente de la plantilla: 

- https://github.com/nmfs-opensci/quarto-thesis    


# Apuntes para redactar la tesis

## Introducción
-Fijar el nivel preciso de expectativas.
-Dejar bien en claro “lo que s´ı” se va a resolver en este trabajo
    a- Contexto problemático
    b- Estado del arte (¿qué se ha hecho? ¿qué se ha probado? ¿qué se ha probado y no ha funcionado? Describir el nicho.)
    c- Aporte Original (¿Qué se va a hacer? ¿Por qué puede resolver el problema? )

## Métodos (Algoritmo propuesto o Desarrollo)
-Explicar cómo se resolvió el problema. Hay que explicar todo de manera genérica, prescindiendo de los detalles de implementación, datos y resultados.
-Se puede presentar la solución high level, o un algoritmo propuesto.
-Las sub-secciones desarrollan la solución propuesta.
-Esta sección es la más técnica y debe permitir que el lector pueda replicar el trabajo.
-El mejor texto es el breve y fácil de entender.

## Datos y diseño experimental
-Incluye estrategias de validación y métricas utilizadas.

## Resultados y discusión
-Determinar cuáles son los resultados más relevantes. Presentar gráficos y  tables (no más de 4).
-Es Importante notar que no deben incluirse todas las pruebas fallidas.
-Figuras explicar detalladamente como leerlas. Explicar lo importante de cada figura. 
-Connectar con trabajos previos, a quién se le gano y porqué ganamos!!!
-Cerrar en positivo. Indicar limitaciones del trabajo.
-Tener en cuenta que en el proceso de investigación y descubrimiento, mil cosas pueden fallar y andar mal. Pero a la hora de redactar y describir el trabajo, hay que contar lo que sí funcionar, lo que sirve y lo que permitirá avanzar.
-Por eso, para cáda experimento pensar ¿cuál es el resultado positivo que nos deja?

## Conclusiones
-A quien le interesa el trabajo, lee el título, el resumen y el capítulo de conclusiones. Por eso, hay que convencer al lector de que el trabajo es importante y que vale la pena leerlo. Pasado en tiempos verbales.
-Se puede agregar un capítulo de futuro trabajo.



# Estructura de la tesis por Dr. Matías Gerard e implementada por Lic. Claudio Sebastian Castillo

Capítulo 1: 

Introducción. Acá presentamos el problema general de selección de características, su importancia. Algunas aproximaciones y los problemas/limitaciones que presentan. También se habla del problema del desbalance de datos o la poca cantidad de patrones. Se proponen los evolutivos como método de selección asociado al clasificador y se proponen los VAEs como solución al desbalance y la falta de datos. Se describe brevemente la propuesta/hipótesis de trabajo y se describe la estructura de la tesis.

    -Problema de selección de características Gerard-Vignolo
    -Problema de desbalance de datos y poca cantidad de datos
    -Propuesta de AG para selección de características
    -Propuesta de VAEs para aumentación de datos y desbalance de datos


Capítulo 2: 

Análisis preliminar. Describir la motivación del capítulo (línea de base), la teoría de los modelos de ML usados, y las características de los datasets. La descripción de los modelos debe ser a nivel teórico, general, de manera que se entiendan los algoritmos. Las implementaciones se pueden mencionar luego en los capítulos correspondientes (y el detalle de las mismas puede ir a un apéndice). También se deberían presentar las métricas que vas a usar en la tesis para evaluar los distintos modelos. Tené en cuenta que acá se emplean TODAS las features para hacer clasificación y se observan correlaciones que hacen pensar que se podrían descartar algunas features. Se puede reutilizar lo escrito en el Capítulo 1. Faltaría completar con más tablas, gráficos y resultados obtenidos.

    -Explicación de los modelos de ML usados
    -Características de los datasets
    -IMPORTANTE: Métricas para evaluar los distintos modelos y las que se usarán en la tesis
    -Observación de correlaciones en las features

Recomendación de Matías:
Comentario general del capítulo. El documento está escrito correctamente y no he encontrado problemas en lo experimental. Sin embargo, creo que la estructura del capítulo hace difícil seguir el desarrollo. Si bien se observa una evolución de los conceptos a lo largo de la escritura, mi opinión es que deberían enfatizarse aún más las diferencia entre la introducción/elementos teóricos y los experimentos. Al leer el documento esperaba encontrar una estructura similar a la de los papers en cada capítulo contando cuál es el problema abordado, qué se necesita saber de la teoría para entenderlo, y luego pequeñas subsecciones encadenadas que planteen experimentos, muestren los resultados y los analicen, dando pie a nuevos experimentos. Por último, una sección que sea un cierre del capítulo (conclusión) y explique cómo seguir (preámbulo del capítulo siguiente).
Personalmente creo que debería haber 3/4 secciones bien diferenciadas:
- Introducción/Marco Teórico: Puede ser una sola sección o 2 secciones, depende de cómo lo plantees. Pero debería entenderse el por qué del capítulo (qué se desea hacer). Por ejemplo, a grandes rasgos, explicar que la falta de datos o el desbalance es un problema, que hay muchas técnicas, pero los VAE son una familia prometedora y el marco teórico que escribiste explicando cómo funcionan y las diferencias.
- Resultados y Discusión. Para cada método que presentás hiciste experimentos, pero no los mostrás de forma individual. Creo que cada subsección debería tener los resultados de cada método con el análisis correspondiente. Luego, podés presentar una subsección que resuma todos los experimentos, con los resultados más importantes comparados. Eso facilitaría el análisis. Además, se mezcla el estudio de problemas binarios y multiclase. Una mayor separación y análisis individual podría enriquecer el documento. No es necesario escribir 5 páginas en cada caso. Tal vez una breve descripción del experimento, los resultados (tablas, gráficos o lo q





Capítulo 3: 

Experimentos VAEs. Describir la motivación del capítulo (evaluación de métodos para aumentación de datos) y la teoría de los modelos neuronales usados. La descripción de los modelos debe ser a nivel teórico, general, de manera que se entiendan los algoritmos. Las implementaciones se pueden mencionar luego en los capítulos correspondientes (y el detalle de las mismas puede ir a un apéndice). Se puede reutilizar lo escrito en el Capítulo 2. Faltaría completar con más tablas, gráficos y resultados obtenidos.

    -Descripción teórica de los VAEs
    -Descripción de los experimentos
    -Resultados de los experimentos

Capítulo 4: 

Integración de VAEs a los AG (o algo así): Describir la motivación del capítulo (evaluación de métodos para aumentación de datos en el contexto de los AG y su impacto) y la teoría de los algoritmos genéticos. La descripción de estos algoritmos debe ser a nivel teórico, general, de manera que se entienda el funcionamiento. Las implementaciones se pueden mencionar luego en los capítulos correspondientes (y el detalle de las mismas puede ir a un apéndice). Se puede reutilizar lo escrito en los Capítulos 3 y 4. Faltaría completar con más tablas, gráficos y resultados obtenidos. Hay que tener en claro que habrá experimentos con y sin VAEs, así que debe ser clara la lógica en que se presentan los experimentos.
y67
    -Descripción teórica de los AG
    -Integración de VAEs a los AG
    -Descripción de los experimentos
    -Resultados de los experimentos

Capítulo 5: 

Conclusiones --> Se puede reutilizar lo escrito en el Capítulo 5.


Aclaración:

- En cada Capítulo debe haber una descripción de lo que se abordará, una presentación de los elementos teóricos necesarios, descripción de los datos (si no fueron presentados) y de los experimentos. 
- Cada uno de ellos debe llevar una explicación de lo que se quiere hacer, cómo se hizo, cuáles fueron los resultados (mostrando tablas, gráficos, etc) y el análisis de los mismos.
- En las Secciones experimentales, sugiero separar las mismas en Experimentos para problemas de 2 clases y problemas multi-clase. Los resultados son diferentes, y el desempeño también. Creo que es importante resaltar que para 2 clases anda bien y que en multi-clase hay que seguir trabajando, pero que hay resultados prometedores.

