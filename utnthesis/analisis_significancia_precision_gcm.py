from scipy import stats

# Provided means
mean_aumentados = 0.541
mean_original = 0.497

# Provided standard deviations
std_aumentados = 0.033
std_original = 0.022

# Provided sample sizes
n_aumentados = 3133
n_original = 133

# Perform two-sample t-test (Welch’s t-test for unequal variances)
t_stat, p_value = stats.ttest_ind_from_stats(
    mean_aumentados, std_aumentados, n_aumentados,
    mean_original, std_original, n_original,
    #equal_var=False  # Apply Welch's correction for unequal variances
)

# Calculate percentage difference
percentage_difference = ((mean_aumentados - mean_original) / mean_original) * 100

# Draw conclusion
conclusion = ""
if p_value < 0.05:
    conclusion = f"The difference between the two means is statistically significant with a p-value of {p_value:.4g}. The percentage difference between the two means is {percentage_difference:.2f}%."
else:
    conclusion = f"The difference between the two means is not statistically significant with a p-value of {p_value:.4g}."

# Output results
print(f"t-statistic: {t_stat}, p-value: {p_value}")
print(f"Percentage difference: {percentage_difference:.2f}%")
print(conclusion)
