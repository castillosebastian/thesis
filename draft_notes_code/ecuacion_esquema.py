# Definición de los parámetros del ejemplo
m_H_t = 20  # Número de copias del esquema H en la generación t
f_H = 18  # Aptitud promedio de los individuos que pertenecen al esquema H
f_avg = 15  # Aptitud promedio de la población total
p_c = 0.7  # Probabilidad de cruce
delta_H = 4  # Longitud de definición del esquema H
l = 6  # Longitud del cromosoma
p_m = 0.01  # Tasa de mutación
o_H = 3  # Orden del esquema

# Cálculo del factor de selección
selection_factor = f_H / f_avg

# Cálculo de la probabilidad de conservación ante el cruce
crossover_preservation_prob = 1 - p_c * (delta_H / (l - 1))

# Cálculo de la probabilidad de conservación ante la mutación
mutation_preservation_prob = (1 - p_m) ** o_H

# Cálculo final del número esperado de copias del esquema H en la generación t+1
m_H_t_plus_1 = m_H_t * selection_factor * crossover_preservation_prob * mutation_preservation_prob

print(m_H_t_plus_1)
