import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'filtered_experiment_data.csv'
df = pd.read_csv(file_path)

# Filter experiments containing 'leukemia' in the 'experiment_group' variable
leukemia_df = df[df['experiment_group'].str.contains('leukemia', case=False, na=False)]


# Create a new DataFrame for the combined boxplot
combined_df = pd.DataFrame({
    'value': pd.concat([leukemia_df['all_feature_acc'], leukemia_df[leukemia_df['group'] == 'original']['pob_accuracy_avg'], leukemia_df[leukemia_df['group'] == 'aumentados']['pob_accuracy_avg']]),
    'metric': ['all_feature_acc'] * len(leukemia_df) + ['pob_accuracy_avg_original'] * len(leukemia_df[leukemia_df['group'] == 'original']) + ['pob_accuracy_avg_aumentados'] * len(leukemia_df[leukemia_df['group'] == 'aumentados'])
})

# Update labels as per the provided names
combined_df['metric'] = combined_df['metric'].replace({
    'Precisión de todas las características': 'características_completas',
    'Precisión de la población (original)': 'sub-espacio_original',
    'Precisión de la población (aumentados)': 'sub-espacio_aumentado'
})

# Plot combined boxplot with updated labels and specific colors
plt.figure(figsize=(12, 8))
sns.boxplot(x='metric', y='value', data=combined_df, palette={'características_completas': 'white', 'sub-espacio_original': 'gray', 'sub-espacio_aumentado': 'pink'})
plt.title('Boxplot Combinado para características_completas y sub-espacios por Grupo')
plt.xlabel('Métricas')
plt.ylabel('Precisión')
plt.show()



# Summarize the dataset
# Extract the relevant columns
focused_df = leukemia_df[['experiment_group', 'group', 'POP_SIZE', 'PROB_MUT', 'PX', 'GMAX', 'DAT_SIZE']]

# Save the dataframe to a CSV file
output_file_path = 'leukemia_ag_params.csv'
focused_df.to_csv(output_file_path, index=False)

# Group by 'experiment_group' and 'group'
grouped_df = leukemia_df.groupby(['experiment_group', 'group']).agg({       
    'all_feature_ngenes': 'mean',
    'all_feature_acc': 'mean',
    'pob_accuracy_avg': 'mean',
    'pob_ngenes_avg': 'mean',
    'pob_accuracy_std': 'mean',
    'pob_ngenes_std': 'mean'
}).reset_index().round(2)

# Save the summarized dataset
output_path = 'leukemia_result_summary.csv'
grouped_df.to_csv(output_path, index=False)
