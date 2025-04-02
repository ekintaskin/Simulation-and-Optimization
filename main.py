from simulation import Simulation
from stats import Stats
# import numpy as np
import matplotlib.pyplot as plt


def main():
    # Parameters
    num_runs = 100
    print_results = True
    max_waiting_times = []
    mean_waiting_times = []

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
        
        print(f"Max Waiting Time: {stats.max_waiting_time():.2f} s")
        print(f"Mean Waiting Time: {stats.mean_waiting_time():.2f} s")
        print(f"Variance of Waiting Time: {stats.variance_of_waiting_time():.2f}")
        print(f"Waiting Time 50th, 90th, 95th and 99th percentiles: {stats.waiting_time_percentiles()} \n")
        
        count_above_threshold, percentage_above_threshold, var_above_threshold = stats.num_customers_above_threshold(threshold=10)
        print(f"Customers above 10s: {count_above_threshold}, In percentage: {percentage_above_threshold}, Variance: {var_above_threshold:.2f}")
     

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



if __name__ == "__main__":
    main()