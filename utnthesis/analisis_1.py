import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Leer los datos
data = pd.read_csv('src/filtered_experiment_data.csv')

# Ajuste del filtro para 'Madelon'
datasets = {
    'Leukemia': data[data['experiment_name'].str.contains('leukemia')].copy(),
    'Gisette': data[data['experiment_name'].str.contains('gisette')].copy(),
    'Madelon': data[data['experiment_name'].str.contains('mandelon')].copy(),
    'GCM': data[data['experiment_name'].str.contains('gcm')].copy(),
}

# Configurar la categoría 'group' para cada dataset
for dataset in datasets.values():
    dataset['group'] = pd.Categorical(dataset['group'], categories=['aumentados', 'original'], ordered=True)

# Crear listas para almacenar los resultados
accuracy_metrics = []
ngenes_metrics = []

# Función para calcular métricas, generar análisis, y recolectar datos para CSV
def calculate_metrics_and_generate_report(dataset, dataset_name):
    report = f"Análisis de resultados para el dataset {dataset_name}:\n"
    
    for metric in ['pob_accuracy_avg', 'pob_ngenes_avg']:
        report += f"\nMétrica: {metric}\n"
        
        for group in dataset['group'].cat.categories:
            group_data = dataset[dataset['group'] == group][metric]
            
            if group_data.empty:
                report += f"\nGrupo: {group}\n  - No hay datos suficientes para calcular las métricas.\n"
                continue
            
            mean = group_data.mean()
            std_dev = group_data.std()
            iqr = np.percentile(group_data, 75) - np.percentile(group_data, 25)
            
            report += f"\nGrupo: {group}\n"
            report += f"  - Media: {mean:.3f}\n"
            report += f"  - Desviación Estándar: {std_dev:.3f}\n"
            report += f"  - Rango Intercuartil (IQR): {iqr:.3f}\n"
            
            # Guardar métricas para CSV
            if metric == 'pob_accuracy_avg':
                accuracy_metrics.append({'Dataset': dataset_name, 'Group': group, 'Mean': mean, 'StdDev': std_dev, 'IQR': iqr})
            else:
                ngenes_metrics.append({'Dataset': dataset_name, 'Group': group, 'Mean': mean, 'StdDev': std_dev, 'IQR': iqr})
        
        # Comparación entre grupos
        original_data = dataset[dataset['group'] == 'original'][metric]
        aumentados_data = dataset[dataset['group'] == 'aumentados'][metric]
        original_mean = original_data.mean()
        aumentados_mean = aumentados_data.mean()
        comparison = "mayor" if original_mean > aumentados_mean else "menor"
        report += f"\nComparación entre grupos para {metric}:\n"
        if metric == 'pob_accuracy_avg':
            report += f"  La media del grupo 'original' es {comparison} que la del grupo 'aumentados'.Cuanto mayor sea la precisión, mejor.\n"
        else:
            report += f"  El número medio de características seleccionadas es {comparison} en el grupo 'original' comparado con el grupo 'aumentados'.\n"
            efficiency_comparison = "más eficiente" if aumentados_mean < original_mean else "menos eficiente"
            report += f"  Esto sugiere que la selección de características fue {efficiency_comparison} en el grupo 'aumentados'.\n"
    
    # Realizar prueba estadística para pob_accuracy_avg y agregar al informe
    t_stat, p_val = ttest_ind(aumentados_data, original_data, equal_var=False)
    report += f"\nPrueba estadística para pob_accuracy_avg:\n"
    report += f"T-statistic: {t_stat:.3f}, P-value: {p_val:.3f}\n"
    if p_val < 0.05:
        report += "La diferencia en la precisión entre los grupos es estadísticamente significativa.\n"
    else:
        report += "No hay evidencia suficiente para afirmar que la diferencia en la precisión entre los grupos es significativa.\n"
    
    report += "\n" + "="*50 + "\n"
    
    return report

# Generar el reporte para cada dataset y guardar en un archivo TXT
full_report = ""
for dataset_name, dataset in datasets.items():
    full_report += calculate_metrics_and_generate_report(dataset, dataset_name)

# Guardar el análisis en un archivo de texto
with open('analisis_metrico_resultados.txt', 'w') as f:
    f.write(full_report)

# Guardar los resultados en CSVs
# round to 2 decimal places
accuracy_df = pd.DataFrame(accuracy_metrics).round(3)
ngenes_df = pd.DataFrame(ngenes_metrics).round(3)

accuracy_df.to_csv('accuracy_metrics.csv', index=False)
ngenes_df.to_csv('ngenes_metrics.csv', index=False)

print("Análisis completado y archivos generados.")
