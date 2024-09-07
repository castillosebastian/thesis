
# Presentación


# AV

Los autoencoders variacionales (VAEs) asignan los datos de entrada *x* a una distribución de probabilidad a posteriori *p(z|x)*. Específicamente, asumiendo una distribución gaussiana para *p(z|x)*, los VAEs asignan determinísticamente los datos de entrada *x* a la media *μz|x* y la desviación estándar *Σz|x* para construir la distribución posteriori *p(z|x)*. Luego, se construye una variable latente *z* muestreando de la distribución posterior. Finalmente, el decodificador asigna determinísticamente la variable latente *z* de vuelta a los datos de entrada reconstruidos *x* [30], [31].

La función de costo total para los VAEs consiste en el error de reconstrucción y un término de regularización que impone que la distribución del espacio latente *p(z|x)* sea cercana a la distribución previa *p(z) = N(0, I)*. Esto promueve la ortogonalidad/independencia del eje *z* y regulariza los pesos de la red.

Los VAEs ofrecen las siguientes ventajas:

- Proyectar los datos en un espacio de menor dimensión.
- Aproximar la distribución posterior *p(z|x)*.
- Generar nuevos datos sintéticos a partir del espacio latente inferido.

