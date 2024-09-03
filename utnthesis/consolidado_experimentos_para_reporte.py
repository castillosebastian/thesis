import pandas as pd

# Read data
data = pd.read_csv('expga1/experiments_results.csv')

# Helper function to categorize experiments
def categorize_experiments(df, original_data_list, experiment_prefix, group_length):
    df = df[df['experiment_name'].str.contains(experiment_prefix)].copy()
    df.loc[:, 'experiment_group'] = df['experiment_name'].apply(lambda x: x[:group_length])
    df.loc[:, 'group'] = df['experiment_group'].apply(lambda x: 'original' if x in original_data_list else 'aumentados')
    return df

# Leukemia
leukemia_original_data = ['leukemia_base_0001', 'leukemia_base_0012', 'leukemia_base_0013']
leukemia = categorize_experiments(data, leukemia_original_data, 'leukemia', 18)
leukemia = leukemia[~leukemia['experiment_group'].isin(['leukemia_base_0003', 'leukemia_base_0006', 'leukemia_base_0007', 'leukemia_base_0008'])]
# Invert the order of categories for the 'Leukemia' subplot
leukemia['group'] = pd.Categorical(leukemia['group'], categories=['aumentados', 'original'], ordered=True)

# Gisette
gisette_original_data = ['gisette_base_0020', 'gisette_base_0022']
gisette = categorize_experiments(data, gisette_original_data, 'gisette', 17)
gisette_selected_experiments = ['gisette_base_0005', 'gisette_base_0020', 'gisette_base_0022']
gisette = gisette[gisette['experiment_group'].isin(gisette_selected_experiments)].copy()
gisette.loc[:, 'group'] = gisette['experiment_group'].apply(lambda x: 'original' if x in gisette_original_data else 'aumentados')

# Madelon
madelon_original_data = ['mandelon_base_0017', 'mandelon_base_0023']
madelon = categorize_experiments(data, madelon_original_data, 'mandelon', 18)
madelon = madelon[~madelon['experiment_group'].isin(['mandelon_base_0004', 'mandelon_base_0021'])]
madelon.loc[:, 'group'] = madelon['experiment_group'].apply(lambda x: 'original' if x in madelon_original_data else 'aumentados')

# GCM
gcm_original_data = ['gcm_base_0065', 'gcm_base_0063', 'gcm_base_0067', 'gcm_base_0070']
gcm = categorize_experiments(data, gcm_original_data, 'gcm', 13)
# Filter out some experiments containing 'gcm_base_006' or 'gcm_base_007'
gcm = gcm[gcm['experiment_group'].str.contains('0061|0066|0064|0069|0065|0063|0067|0070')].copy()

# Combine all filtered datasets into one
combined_data = pd.concat([leukemia, gisette, madelon, gcm])

# Save the combined data to a new CSV file
combined_data.to_csv('filtered_experiment_data.csv', index=False)

# Display the combined data (optional)
print(combined_data.head())
