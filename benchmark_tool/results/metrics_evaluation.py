import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Read and prepare data
df = pd.read_csv("benchmark_metrics.csv", sep=',')
df = df[df['run_ix'] == 'avg']  # Filter to keep only the average rows

# First heatmap: Overall model performance
pivot_overall = df.pivot_table(
    index='model',
    values=['ratio_success', 'generation_time_s', 'ratio_memory_usage_kb', 'ratio_pep8_violations', 'ratio_runtime_time_s', 'ratio_std_lib_imports', 'ratio_third_party_imports']
)

# Create first heatmap for overall metrics
plt.figure(figsize=(12, 8))
sns.heatmap(
    pivot_overall,
    annot=True,
    fmt='.2f',
    cmap='RdYlGn',
    center=0.5,
    robust=True
)

plt.title('Overall Model Performance Metrics')
plt.ylabel('Model')
plt.xlabel('Metrics')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('model_metrics_overall_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Second heatmap: Task-specific performance
pivot_tasks = df.pivot_table(
    index='model',
    columns='task',
    values='ratio_success'
)

plt.figure(figsize=(15, 8))
sns.heatmap(
    pivot_tasks,
    annot=True,
    fmt='.2f',
    cmap='RdYlGn',
    center=0.5,
    robust=True
)

plt.title('Model Success Rate by Task')
plt.ylabel('Model')
plt.xlabel('Task')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('model_metrics_by_task_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
