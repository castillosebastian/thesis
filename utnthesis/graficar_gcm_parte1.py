import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
data = pd.read_csv('experiments_results.csv')
# Helper function to categorize experiments
def categorize_experiments(df, original_data_list, experiment_prefix, group_length):
    df = df[df['experiment_name'].str.contains(experiment_prefix)].copy()
    df.loc[:, 'experiment_group'] = df['experiment_name'].apply(lambda x: x[:group_length])
    df.loc[:, 'group'] = df['experiment_group'].apply(lambda x: 'original' if x in original_data_list else 'aumentados')
    return df


# GCM
gcm_original_data = ['gcm_base_0037',
                     'gcm_base_0038',
                     'gcm_base_0039',
                     'gcm_base_0040']
gcm = categorize_experiments(data, gcm_original_data, 'gcm', 13)
gcm = gcm[gcm['experiment_group'].str.contains('0031|0033|0035|0036|0037|0038|0040')].copy()

# Configuración de la paleta de colores
custom_palette = {'original': 'gray', 'aumentados': 'pink'}

# Función para generar gráficos combinados
def plot_combined(dataset, dataset_name):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel izquierdo: pob_accuracy_avg
    sns.boxplot(ax=axes[0], x='group', y='pob_accuracy_avg', data=dataset, palette=custom_palette)
    sns.stripplot(ax=axes[0], x='group', y='pob_accuracy_avg', data=dataset, color='darkgrey', dodge=True)
    axes[0].set_title('Precisión obtenida en clasificación')
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Precisión')

    # Panel derecho: pob_ngenes_avg
    sns.boxplot(ax=axes[1], x='group', y='pob_ngenes_avg', data=dataset, palette=custom_palette)
    sns.stripplot(ax=axes[1], x='group', y='pob_ngenes_avg', data=dataset, color='darkgrey', dodge=True)
    axes[1].set_title('Características seleccionadas por el AG')
    axes[1].set_xlabel('')
    axes[1].set_ylabel('Número de Genes')

    # Ajustar el layout y guardar la figura
    plt.suptitle(f'Resultados para {dataset_name}', fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'boxplot_{dataset_name.lower()}_combined_part1.png')    
    plt.show()

# Generar gráficos combinados para cada dataset
plot_combined(gcm, 'GCM')


print(f"Tamaño aumentacion: {gcm['DAT_SIZE'].value_counts()}")
# get mean value of pob_accuracy_avg and pob_ngenes_avg for each group

mean_accuracy = gcm.groupby('group')['pob_accuracy_avg'].mean()
mean_ngenes = gcm.groupby('group')['pob_ngenes_avg'].mean()
print(f"Mean accuracy: {mean_accuracy}")
print(f"Mean ngenes: {mean_ngenes}")

