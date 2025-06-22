import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Read and prepare data
df = pd.read_csv("benchmark_metrics.csv", sep=',')

# df_non_avg = df[df['run_ix'] != 'avg']

df = df[df['run_ix'] == 'avg']

# Create pivot table
pivot_overall = df.pivot_table(
    index='model',
    values=['ratio_success', 'generation_time_s', 'ratio_memory_usage_kb',
            'ratio_pep8_violations', 'ratio_runtime_time_s',
            'ratio_third_party_imports']
)

# Set up figure
fig, ax = plt.subplots(figsize=(15, 10))

# Define individual colormaps for each metric
colormaps = {
    'generation_time_s': 'YlOrRd_r',       # Time metrics (lower is better)
    'ratio_memory_usage_kb': 'Blues',      # Memory usage
    'ratio_pep8_violations': 'Purples_r',  # Violations (lower is better)
    'ratio_runtime_time_s': 'Greens',      # Runtime
    'ratio_success': 'RdYlGn',             # Success rate (higher is better)
    'ratio_third_party_imports': 'Reds'    # Third-party imports
}

# Create a mask to plot one column at a time
mask = np.zeros_like(pivot_overall, dtype=bool)

# Plot each column with its own colormap
for i, column in enumerate(pivot_overall.columns):
    mask[:] = True
    mask[:, i] = False  # Only show current column
    
    sns.heatmap(
        pivot_overall,
        annot=True,
        fmt='.2f',
        cmap=colormaps[column],
        mask=mask,
        ax=ax,
        cbar=False,
        annot_kws={'size': 16} # Adjust annotation size
    )

plt.rcParams.update({'font.size': 14})  # Increase base font size
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=14)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=14)
ax.set_title('Overall Model Performance Metrics', pad=20, fontsize=16)
ax.set_xlabel('Metrics', fontsize=14)
ax.set_ylabel('Models', fontsize=14)

plt.tight_layout()
plt.savefig("model_metrics_overall_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="temperature", y="ratio_success", hue="model", palette="Set2", width=0.6) 
plt.title("Success Ratio Distribution Across Models by Temperature")
plt.xlabel("Temperature")
plt.ylabel("Success Ratio")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("success_by_temperature_model.png", dpi=300)
plt.close()

# Success ratio by task and model
plt.figure(figsize=(10, 6))
pivot_task_model = df.pivot_table(index="task", columns="model", values="ratio_success")
sns.heatmap(pivot_task_model, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={"label": "Success Ratio"})
plt.title("Success Ratio per Task and Model")
plt.xlabel("Model")
plt.ylabel("Task")
plt.tight_layout()
plt.savefig("success_by_task_model.png", dpi=300)
plt.close()

# Heatmap: Correlation between metrics
metrics_cols = [
    "ratio_success",
    "ratio_pep8_violations",
    "ratio_avg_cyclomatic_complexity",
    "ratio_memory_usage_kb",
    "ratio_runtime_time_s",
    "ratio_std_lib_imports",
    "ratio_third_party_imports"
]

metrics_df = df[metrics_cols]

# Removing columns with zero standard deviation
metrics_df = metrics_df.loc[:, metrics_df.std() > 0]

corr = metrics_df.corr(numeric_only=True)

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar=True)
plt.title("Correlation Between Evaluation Metrics")
plt.tight_layout()
plt.savefig("metric_correlations_filtered.png", dpi=300)
plt.close()

# Number of tasks per model
total_per_model = df.groupby("model").size()

# Number of successful tasks per model with ratio_success == 1.0
success_per_model = df[df["ratio_success"] == 1.0].groupby("model").size()

# ratio of successful tasks to total tasks per model
success_ratio = (success_per_model / total_per_model).fillna(0).reset_index()
success_ratio.columns = ["model", "success_ratio"]
success_ratio = success_ratio.sort_values("success_ratio", ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=success_ratio,
    x="success_ratio",
    y="model",
    palette="crest"
)
plt.xlabel("Fraction")
plt.ylabel("Model")
plt.title("Proportion of Perfectly Solved Tasks per Model")
plt.xlim(0, 1.05)
plt.tight_layout()
# plt.savefig("success_ratio_per_model.png", dpi=300)
plt.close()