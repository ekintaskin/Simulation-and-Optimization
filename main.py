from simulation import Simulation
from time import time
from stats import Stats
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Parameters
    num_runs = 100 # Number of simulation runs
    threshold = 60 # Acceptable max waiting time threshold in seconds
    print_results = True

    # Initialize lists to store statistics
    max_waiting_times = []
    mean_waiting_times = []
    var_waiting_times = []
    median_waiting_times = []
    waiting_time_percentiles = []
    bootstrap_mean_waiting_times = []

    # Initialize run time
    run_start_time = time()

    # Simulation class
    simulation = Simulation()

    for i in range(num_runs):
        if print_results:
            print(f"Run {i + 1}")
        
        # run simulation
        requests = simulation.run()

        # Initialize Statistics
        stats = Stats(requests)
        waiting_time = stats.get_waiting_time()

        # Calculate statistics
        max_waiting_time = np.max(waiting_time)
        max_waiting_times.append(max_waiting_time)

        mean_waiting_time = np.mean(waiting_time)
        mean_waiting_times.append(mean_waiting_time)

        var_waiting_time = np.var(waiting_time)
        var_waiting_times.append(var_waiting_time)

        median_waiting_time = np.median(waiting_time)
        median_waiting_times.append(median_waiting_time)

        waiting_time_percentile = np.percentile(waiting_time, [50, 90, 95, 99])
        waiting_time_percentiles.append(waiting_time_percentile)

        (true_mean_waiting_time, bootstrap_mean_waiting_time_mse, bootstrap_waiting_time_stats) = stats.mse_bootstrap(np.mean, num_bootstrap=100)
        bootstrap_mean_waiting_times.append(bootstrap_mean_waiting_time_mse)

        print(f"Mean, Median, Max and Variance of Waiting Time: {mean_waiting_time:.2f} s, {median_waiting_time:.2f} s, {max_waiting_time:.2f} s,  {var_waiting_time:.2f} s")
        
        # Print the first few bootstrap statistics for inspection
        # print(f"First 5 Bootstrap Mean Computations: {bootstrap_waiting_time_stats[:5]}")

        print(f"MSE of the Bootstrap Mean Waiting Time compared to true Mean: {bootstrap_mean_waiting_time_mse:.2f} s")
        
        print(f"Maximum Waiting Time 50th, 90th, 95th and 99th percentiles: {waiting_time_percentile} \n")

        count_above_threshold, percentage_above_threshold = stats.num_customers_above_threshold(threshold)
        print(f"Customers above {threshold:.2f} s: {count_above_threshold}, In percentage: {percentage_above_threshold:.2f} % \n")


    plt.figure(figsize=(8, 6))
    plt.hist(max_waiting_times, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Maximum Waiting Times')
    plt.xlabel('Maximum Waiting Time (s)')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.hist(mean_waiting_times, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Mean Waiting Times')
    plt.xlabel('Mean Waiting Time (s)')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.hist(median_waiting_times, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Median Waiting Times')
    plt.xlabel('Median Waiting Time (s)')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.hist(var_waiting_times, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Waiting Times Variance')
    plt.xlabel('Waiting Time Variance (s)')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.hist(count_above_threshold, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Customers waiting more than the threshold')
    plt.xlabel('Waiting Time Variance (s)')
    plt.ylabel('Frequency')
    plt.show()



    run_end_time = time()
    print(f"Elapsed time: {run_end_time - run_start_time:.2f} seconds")

if __name__ == "__main__":
    main()
