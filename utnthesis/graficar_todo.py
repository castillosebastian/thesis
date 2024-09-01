import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer los datos
data = pd.read_csv('filtered_experiment_data.csv')

# Filtrar los datos para cada dataset y categorizar los experimentos
leukemia = data[data['experiment_name'].str.contains('leukemia')].copy()
leukemia['group'] = pd.Categorical(leukemia['group'], categories=['aumentados', 'original'], ordered=True)
gisette = data[data['experiment_name'].str.contains('gisette')].copy()
gisette['group'] = pd.Categorical(gisette['group'], categories=['aumentados', 'original'], ordered=True)
madelon = data[data['experiment_name'].str.contains('mandelon')].copy()
madelon['group'] = pd.Categorical(madelon['group'], categories=['aumentados', 'original'], ordered=True)
gcm = data[data['experiment_name'].str.contains('gcm')].copy()
gcm['group'] = pd.Categorical(gcm['group'], categories=['aumentados', 'original'], ordered=True)

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

# Generar gráficos combinados para cada dataset
plot_combined(leukemia, 'Leukemia')
plot_combined(gisette, 'Gisette')
plot_combined(madelon, 'Madelon')
plot_combined(gcm, 'GCM')

# Gráfico combinado original (pob_accuracy_avg) para los 4 datasets
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Leukemia
sns.boxplot(ax=axes[0, 0], x='group', y='pob_accuracy_avg', data=leukemia, palette=custom_palette)
sns.stripplot(ax=axes[0, 0], x='group', y='pob_accuracy_avg', data=leukemia, color='darkgrey', dodge=True)
axes[0, 0].set_title('Leukemia')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('')
axes[0, 0].set_xticks([])  # Remove x-axis labels

# Gisette
sns.boxplot(ax=axes[0, 1], x='group', y='pob_accuracy_avg', data=gisette, palette=custom_palette)
sns.stripplot(ax=axes[0, 1], x='group', y='pob_accuracy_avg', data=gisette, color='darkgrey', dodge=True)
axes[0, 1].set_title('Gisette')
axes[0, 1].set_xlabel('')
axes[0, 1].set_ylabel('')
axes[0, 1].set_xticks([])  # Remove x-axis labels

# Madelon
sns.boxplot(ax=axes[1, 0], x='group', y='pob_accuracy_avg', data=madelon, palette=custom_palette)
sns.stripplot(ax=axes[1, 0], x='group', y='pob_accuracy_avg', data=madelon, color='darkgrey', dodge=True)
axes[1, 0].set_title('Madelon')
axes[1, 0].set_xlabel('')
axes[1, 0].set_ylabel('')
axes[1, 0].set_xticks([])  # Remove x-axis labels

# GCM
sns.boxplot(ax=axes[1, 1], x='group', y='pob_accuracy_avg', data=gcm, palette=custom_palette)
sns.stripplot(ax=axes[1, 1], x='group', y='pob_accuracy_avg', data=gcm, color='darkgrey', dodge=True)
axes[1, 1].set_title('GCM')
axes[1, 1].set_xlabel('')
axes[1, 1].set_ylabel('')
axes[1, 1].set_xticks([])  # Remove x-axis labels


# Etiquetas comunes
fig.text(0.03, 0.5, 'Precisión', ha='center', va='center', rotation='vertical', fontweight='bold')
# Add a legend for the data categories
legend_labels = ['Datos Aumentados', 'Datos Originales']
colors = ['pink', 'gray']
handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
fig.legend(handles, legend_labels, loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.05))
plt.suptitle('Precisión obtenida en clasificación con datos originales vs datos aumentados', y=0.95, fontweight='bold')
plt.tight_layout(rect=[0, 0.95, 0.95, 1])
plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)
plt.savefig('boxplot_resultados_precision.png')
plt.show()


# Gráfico combinado nuevo (pob_ngenes_avg) para los 4 datasets
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Leukemia
sns.boxplot(ax=axes[0, 0], x='group', y='pob_ngenes_avg', data=leukemia, palette=custom_palette)
sns.stripplot(ax=axes[0, 0], x='group', y='pob_ngenes_avg', data=leukemia, color='darkgrey', dodge=True)
axes[0, 0].set_title('Leukemia')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('')
axes[0, 0].set_xticks([])  # Remove x-axis labels

# Gisette
sns.boxplot(ax=axes[0, 1], x='group', y='pob_ngenes_avg', data=gisette, palette=custom_palette)
sns.stripplot(ax=axes[0, 1], x='group', y='pob_ngenes_avg', data=gisette, color='darkgrey', dodge=True)
axes[0, 1].set_title('Gisette')
axes[0, 1].set_xlabel('')
axes[0, 1].set_ylabel('')
axes[0, 1].set_xticks([])  # Remove x-axis labels

# Madelon
sns.boxplot(ax=axes[1, 0], x='group', y='pob_ngenes_avg', data=madelon, palette=custom_palette)
sns.stripplot(ax=axes[1, 0], x='group', y='pob_ngenes_avg', data=madelon, color='darkgrey', dodge=True)
axes[1, 0].set_title('Madelon')
axes[1, 0].set_xlabel('')
axes[1, 0].set_ylabel('')
axes[1, 0].set_xticks([])  # Remove x-axis labels

# GCM
sns.boxplot(ax=axes[1, 1], x='group', y='pob_ngenes_avg', data=gcm, palette=custom_palette)
sns.stripplot(ax=axes[1, 1], x='group', y='pob_ngenes_avg', data=gcm, color='darkgrey', dodge=True)
axes[1, 1].set_title('GCM')
axes[1, 1].set_xlabel('')
axes[1, 1].set_ylabel('')
axes[1, 1].set_xticks([])  # Remove x-axis labels

# Etiquetas comunes
fig.text(0.03, 0.5, 'Número de Genes', ha='center', va='center', rotation='vertical', fontweight='bold')
# Add a legend for the data categories
legend_labels = ['Datos Aumentados', 'Datos Originales']
colors = ['pink', 'gray']
handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
fig.legend(handles, legend_labels, loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.05))
plt.suptitle('Número de genes seleccionados con datos originales vs datos aumentados', y=0.95, fontweight='bold')
plt.tight_layout(rect=[0, 0.95, 0.95, 1])
plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)
plt.savefig('boxplot_resultados_ngenes.png')
plt.show()

############################################################################################################

# Assuming gcm DataFrame is already defined and has the necessary columns
# Discretize 'pob_ngenes_avg' into the specified categories
bins = [0, 100, 300, 600, float('inf')]
labels = ['45_med', 'med_200', '450_med', '750_med']
gcm['ngenes_category'] = pd.cut(gcm['pob_ngenes_avg'], bins=bins, labels=labels, right=False)

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
ordered_categories = ['45_med', 'med_200', '450_med', '750_med']

# Prepare data for boxplot
for category in ordered_categories:
    for label in ['original', 'aumentados']:
        group_data = gcm[(gcm['ngenes_category'] == category) & (gcm['group'] == label)]['pob_accuracy_avg']
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
plt.title('Precisión según número de características seleccionadas GCM')
plt.xlabel('Numero de características - grupo de experimento')
plt.ylabel('Precisión')
plt.tight_layout(rect=[0, 0.2, 1, 0.95])  # Adjust the bottom margin
plt.xticks(rotation=45)
plt.savefig('boxplot_gcm_ngenes_precision.png')
plt.show()