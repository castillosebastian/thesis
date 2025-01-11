import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer los datos
data = pd.read_csv('src/filtered_experiment_data_v2.csv')

# Filtrar los datos para cada dataset y categorizar los experimentos
all_leukemia = data[data['experiment_name'].str.contains('all_leukemia')].copy()
all_leukemia['group'] = pd.Categorical(all_leukemia['group'], categories=['aumentados', 'original'], ordered=True)


# split all leukemia 
all_lukemia_low = all_leukemia[all_leukemia['pob_ngenes_avg'] < 50]
all_lukemia_high = all_leukemia[all_leukemia['pob_ngenes_avg'] >= 50]
all_leukemia_high_low = all_lukemia_high[all_lukemia_high['pob_ngenes_avg'] < 250]
all_leukemia_high_high = all_lukemia_high[all_lukemia_high['pob_ngenes_avg'] >= 280]

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
    plt.savefig(f'boxplot_{dataset_name.lower()}_combined.png')
    plt.show()


plot_combined(all_lukemia_low, 'all_leukemia_35_med')
plot_combined(all_leukemia_high_low, 'all_leukemia_200_med')


############################################################################################################

# Assuming gcm DataFrame is already defined and has the necessary columns
# Discretize 'pob_ngenes_avg' into the specified categories
bins = [0, 50, 250, float('inf')]
labels = ['35_med', 'med_200', '300_med']
all_leukemia['ngenes_category'] = pd.cut(all_leukemia['pob_ngenes_avg'], bins=bins, labels=labels, right=False)

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Colors for original and aumentados data
colors = {'original': 'gray', 'aumentados': 'pink'}

# Create a boxplot
boxplot_data = []
boxplot_positions = []
boxplot_labels = []
current_position = 1

# Ensure the categories are in the specified order
ordered_categories = ['35_med', 'med_200', '300_med']

# Prepare data for boxplot
for category in ordered_categories:
    for label in ['original', 'aumentados']:
        group_data = all_leukemia[(all_leukemia['ngenes_category'] == category) & (all_leukemia['group'] == label)]['pob_accuracy_avg']
        boxplot_data.append(group_data)
        boxplot_positions.append(current_position)
        boxplot_labels.append(f"{category}-{label}")
        current_position += 1
    current_position += 1  # Add space between categories

# Create the boxplot
box = plt.boxplot(boxplot_data, positions=boxplot_positions, patch_artist=True, labels=boxplot_labels)

# Set colors for each boxplot
for patch, label in zip(box['boxes'], boxplot_labels):
    experiment_group = label.split('-')[-1].strip()  # Ensure to get 'original' or 'aumentados'
    patch.set_facecolor(colors[experiment_group])

# Set plot titles and labels
plt.title('Precisión según número de características seleccionadas all_leukemia')
plt.xlabel('Numero de características - grupo de experimento')
plt.ylabel('Precisión')
plt.tight_layout(rect=[0, 0.2, 1, 0.95])  # Adjust the bottom margin
plt.xticks(rotation=45)
plt.savefig('boxplot_all_leukemia_ngenes_accuracy.png')
plt.show()