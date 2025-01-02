import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_random_data(N=100, normal=True):
    if normal:
        # Generate random data from a normal distribution
        data = np.random.randn(N)
    else:
        # Generate random data from a uniform distribution between 0 and 1
        data = np.random.rand(N)
    
    return data

def calculate_statistics(data):
    statistics = {
        'mean': np.mean(data),
        'std_dev': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'median': np.median(data),
        'range': np.ptp(data)  # Range is max - min
    }
    
    return statistics

def visualize_data(data, statistics):
    plt.figure(figsize=(12, 6))

    # Boxplot of the data's distribution
    plt.subplot(2, 2, 1)
    sns.boxplot(x=data)
    plt.title('Boxplot')
    plt.xlabel('Data')

    # Scatter plot of data points against each other (if N is large enough)
    if len(data) > 50:
        plt.subplot(2, 2, 2)
        plt.scatter(range(len(data)), data)
        plt.title('Scatter Plot')
        plt.xlabel('Index')
        plt.ylabel('Value')

    # Histogram of the data with different bins
    plt.subplot(2, 2, 3)
    sns.histplot(data, kde=True)
    plt.title('Histogram')
    plt.xlabel('Data')
    
    # Violin plot of the data's distribution
    plt.subplot(2, 2, 4)
    sns.violinplot(data)
    plt.title('Violin plot')
    plt.xlabel('Data')
    
    plt.tight_layout()
    plt.show()

def main():
    N = int(input("Enter the number of data points (default: 100): ") or "100")
    normal = input("Generate data from a normal distribution? (y/n): ").strip().lower() == 'y'
    
    data = generate_random_data(N, normal)
    statistics = calculate_statistics(data)

    print("\nStatistics:")
    for key, value in statistics.items():
        print(f"{key}: {value}")

    visualize_data(data, statistics)

if __name__ == "__main__":
    main()