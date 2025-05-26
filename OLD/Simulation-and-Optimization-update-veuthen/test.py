# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 16:42:03 2025

@author: nveuthey

main.py but tested for 1 run to see the prints added in the different classes
"""

from simulation import Simulation
from stats import Stats
import numpy as np
import matplotlib.pyplot as plt
from request import Request
from storage import Storage
from group import Group


# Parameters
num_runs = 1
print_results = True
max_waiting_times = []

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
    if not stats.requests:
        print("No valid requests to process. Skipping statistics for this run.")
        continue

    max_waiting_time = max(req.get_waiting_time() for req in stats.requests)
    max_waiting_times.append(max_waiting_time)

    print(f"Mean of Max Waiting Time: {stats.mean_max_waiting_time():.2f} s")
    print(f"Mean of Mean Waiting Time: {stats.mean_of_mean_waiting_time():.2f} s")
    print(f"Variance of Waiting Time: {stats.variance_of_waiting_time():.2f}")
    print(f"Waiting Time 50th, 90th, 95th and 99th percentiles: {stats.waiting_time_percentiles()} \n")
    
    count_above_threshold, percentage_above_threshold, var_above_threshold = stats.num_customers_above_threshold(threshold=10)
    print(f"Customers above 10s: {count_above_threshold}, In percentage: {percentage_above_threshold}, Variance: {var_above_threshold:.2f}")
    
stats.plot_max_waiting_time_histogram(max_waiting_times, bins=20)




# # Plot the histogram of max waiting times
# final_stats = Stats(stats.requests)
# final_stats.plot_max_waiting_time_histogram(max_waiting_times)

