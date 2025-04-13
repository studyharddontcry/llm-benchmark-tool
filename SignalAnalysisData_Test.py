import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('signal-analysis-sample-data.txt')

# View first few rows
print(df.head())

# Get basic information about the dataframe
print(df.info())

# Descriptive statistics
print(df.describe())

# Select specific columns
df_subset = df[['Time (s)', 'Voltage (V)']]

# Filter rows
df_filtered = df[df['Pressure (kPa)'] > 102.0]

# Create new columns
# df['new_column'] = df['column1'] + df['column2']

# Group by and aggregate
df_grouped = df.groupby('Pressure (kPa)').mean()

# Sort values
df_sorted = df.sort_values('Time (s)', ascending=False)

# Line plot
plt.figure(figsize=(10, 6))
plt.plot(df['Time (s)'], df['Conductivity (μS/cm)'])
plt.title('Conductivity over Time')
plt.xlabel('Time (s)')
plt.ylabel('Conductivity (μS/cm)')
plt.show()

# Scatter plot
plt.scatter(df['Temperature (°C)'], df['Pressure (kPa)'])
plt.title('Scatter Plot')
plt.show()

# Histogram
# plt.hist(df['Pressure (kPa)'], bins=20)
# plt.title('Histogram')
# plt.show()

import seaborn as sns

# Set seaborn style
sns.set_style("whitegrid")

# Scatter plot with regression line
sns.regplot(x='Temperature (°C)', y='Pressure (kPa)', data=df)
plt.title('Scatter Plot with Regression Line')
plt.show()

# Box plot
sns.boxplot(x='category', y='value', data=df)
plt.title('Box Plot')
plt.show()

# Heatmap
correlation = df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()