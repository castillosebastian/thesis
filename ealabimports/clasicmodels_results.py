import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

ealab = "/home/sebacastillo/ealab/"
current = "/home/sebacastillo/thesis/utnthesis/"


# Define your file paths
file_paths = [
    ealab + "exp/leukemia_base_allfeatures/classifiers_AUC.csv",
    ealab + "exp/gisette_base_allfeatures/classifiers_AUC.csv",
    ealab + "exp/madelon_base_allfeatures/_classifiers_AUC.csv",
    ealab + "exp/gcm_base_allfeatures/classifiers_AUC_v2.csv"
]

source_file_names = ["leukemia", "gisette", "madelon", "gcm"]
processed_dfs = []
for path, name in zip(file_paths, source_file_names):
    df = pd.read_csv(path)
    df['Dataset'] = name  # Add a new column with the file name    
    df.rename(columns={
        'Unnamed: 0': 'Models',
        'Training AUC': 'Train',
        'Test AUC': 'Test'
        }, inplace=True)  # Rename 'Unnamed: 0' to 'models'    
    selected_columns = ['Dataset', 'Models', 'Train', 'Test', 'Time Taken (minutes)']
    df = df[selected_columns]  # Select only the specified columns    
     # Round numeric columns
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:
            df[column] = df[column].round(2)
    processed_dfs.append(df)

# Combine the datasets
clasical_models = pd.concat(processed_dfs, ignore_index=True)
#clasical_models.to_csv(current + 'clasica_model.csv' , index=False)

# Grouping models
model_groups = {
    'LDA': 'g1', 'QDA': 'g1', 'Ridge': 'g1', 'SGD': 'g1',
    'AdaBoost': 'g2', 'Bagging': 'g2', 'Extra Trees Ensemble': 'g2', 
    'Gradient Boosting': 'g2', 'Random Forest': 'g2', 'DTC': 'g2', 'ETC': 'g2',
    'BNB': 'g3', 'GNB': 'g3',
    'KNN': 'g4',
    'LSVC': 'g5', 'NuSVC': 'g5', 'SVC': 'g5',
    'MLP': 'g6'
}

# Add a group column based on models
clasical_models['Group'] = clasical_models['Models'].map(model_groups)

# Sort the DataFrame by Group and then Models
clasical_models.sort_values(by=['Group', 'Models'], inplace=True)

# Split into separate DataFrames for each dataset
df_leukemia = clasical_models[clasical_models['Dataset'] == 'leukemia']
df_madelon = clasical_models[clasical_models['Dataset'] == 'madelon']
df_gisette = clasical_models[clasical_models['Dataset'] == 'gisette']
df_gcm = clasical_models[clasical_models['Dataset'] == 'gcm']

# Pivot each DataFrame
pivot_leukemia = df_leukemia.pivot(index='Models', columns='Dataset', values=['Train', 'Test'])
pivot_madelon = df_madelon.pivot(index='Models', columns='Dataset', values=['Train', 'Test'])
pivot_gisette = df_gisette.pivot(index='Models', columns='Dataset', values=['Train', 'Test'])
pivot_gcm = df_gcm.pivot(index='Models', columns='Dataset', values=['Train', 'Test'])

# Rename columns for clarity
pivot_leukemia.columns = [f'Leukemia {col}' for col in pivot_leukemia.columns]
pivot_madelon.columns = [f'Madelon {col}' for col in pivot_madelon.columns]
pivot_gisette.columns = [f'Gisette {col}' for col in pivot_gisette.columns]
pivot_gcm_columns = [f'GCM {col}' for col in pivot_gcm.columns]

# Concatenate the DataFrames horizontally
combined_pivot = pd.concat([pivot_leukemia, pivot_madelon, pivot_gisette, pivot_gcm], axis=1)

# Reset index to make 'Models' a column
combined_pivot.reset_index(inplace=True)

# After concatenating, reset index to make 'Models' a column
combined_pivot.reset_index(inplace=True)

# Sort the combined pivot table by the group
combined_pivot['Group'] = combined_pivot['Models'].map(model_groups)
combined_pivot.sort_values(by=['Group', 'Models'], inplace=True)

# Drop the Group column after sorting
combined_pivot.drop(columns=['Group'], inplace=True)

# Save the combined pivot table
combined_pivot.to_csv(current + 'combined_model_performance.csv', index=False)

# Create the heatmap
long_df = clasical_models.melt(id_vars=['Models', 'Dataset', 'Group'], 
                                value_vars=['Train', 'Test'], 
                                var_name='AUC Type', 
                                value_name='AUC Value')

# Create a pivot table for the heatmap
pivot_df = long_df.pivot_table(index=['Group', 'Models'], 
                               columns=['Dataset', 'AUC Type'], 
                               values='AUC Value')

# Plot the heatmap
cmap = LinearSegmentedColormap.from_list('gray_pink', ['gray', 'pink'], N=256)
plt.figure(figsize=(12, 10))
sns.heatmap(pivot_df, annot=True, cmap=cmap, fmt=".2f")

plt.title('Mapa de Calor con resultados por Modelo (Entrenamiento y Testeo)')
plt.ylabel('Modelos por Grupo')
plt.xlabel('Datasets estudiados y rendimiento de modelos (AUC para problemas binarios y F1 multiclases)')
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# Save the heatmap to a file
plt.savefig(current + 'model_performance_heatmap_grouped.png', bbox_inches='tight')

plt.show()



