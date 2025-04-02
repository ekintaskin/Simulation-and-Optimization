from simulation import Simulation
from time import time
from stats import Stats
import matplotlib.pyplot as plt


def main():
    # Parameters
    num_runs = 100
    threshold = 30
    print_results = True
    max_waiting_times = []
    mean_waiting_times = []
    var_waiting_times = []
    bootstrap_mean_waiting_times = []

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

        # Calculate statistics

        max_waiting_time = stats.max_waiting_time()
        max_waiting_times.append(max_waiting_time)

        mean_waiting_time = stats.mean_waiting_time()
        mean_waiting_times.append(mean_waiting_time)

        var_waiting_time = stats.var_waiting_time()
        var_waiting_times.append(var_waiting_time)

        # (true_mean_waiting_time, bootstrap_mean_waiting_time)  = stats.mse_bootstrap(mean_waiting_time, num_bootstrap=100)
        # bootstrap_mean_waiting_times.append(bootstrap_mean_waiting_time)

        print(f"Max Waiting Time: {stats.max_waiting_time():.2f} s")
        print(f"Mean, Max and Variance of Waiting Time: {stats.mean_waiting_time():.2f} s,  {stats.max_waiting_time():.2f} s,  {stats.var_waiting_time():.2f} s")
        # print(f"Bootstrap Mean Waiting Time: {bootstrap_mean_waiting_time:.2f} s")
        print(f"Waiting Time 50th, 90th, 95th and 99th percentiles: {stats.waiting_time_percentiles()} \n")

        count_above_threshold, percentage_above_threshold = stats.num_customers_above_threshold(threshold)
        print(f"Customers above 30s: {count_above_threshold}, In percentage: {percentage_above_threshold:.2f} % \n")


    plt.figure(figsize=(8, 6))
    plt.hist(max_waiting_times, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Maximum Waiting Times per Run')
    plt.xlabel('Maximum Waiting Time (s)')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.hist(mean_waiting_times, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Mean Waiting Times per Run')
    plt.xlabel('Mean Waiting Time (s)')
    plt.ylabel('Frequency')
    plt.show()



    run_end_time = time()
    print(f"Elapsed time: {run_end_time - run_start_time:.2f} seconds")

if __name__ == "__main__":
    main()
