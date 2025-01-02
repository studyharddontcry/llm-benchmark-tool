import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from scipy.stats import normal

def generate_data(n, normal=True):
    """
    Generate n random data points from a normal distribution with mean 0 and standard deviation 1, or a uniform distribution if `normal` is False.
    """
    if normal:
        data = np.random.normal(size=n)
    else:
        data = np.random.uniform(size=n)
    return data

def calculate_statistics(data):
    """
    Calculate basic statistics for a set of data, such as mean, standard deviation, minimum, maximum, and median.
    """
    mean = np.mean(data)
    stddev = np.std(data)
    min_val = np.min(data)
    max_val = np.max(data)
    median = np.median(data)
    return {
        'mean': mean,
        'standard deviation': stddev,
        'minimum': min_val,
        'maximum': max_val,
        'median': median
    }

def plot_data(data):
    """
    Plot the data using Matplotlib or Seaborn.
    """
    if len(data) < 10:
        plt.scatter(data, c='blue')
        plt.show()
    else:
        plt.boxplot(data)
        plt.show()

def main():
    n = int(input('Enter the number of data points: '))
    normal = bool(input('Is the data from a normal distribution? (y/n): '))
    
    data = generate_data(n, normal=normal)
    statistics = calculate_statistics(data)
    print(statistics)
    plot_data(data)
    
if __name__ == '__main__':
    main()