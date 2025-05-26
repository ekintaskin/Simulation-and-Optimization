# This script runs a simulation of a movie streaming system, optimizes the movie distribution along the storage nodes
#  using various methods, and compares the performance of the baseline and optimized systems based on waiting times.


from time import time
import numpy as np

from constants import INITIAL_MOVIE_HASHSET
from simulation import Simulation
from stats import Stats, plot_comparison_histogram, plot_baseline_histogram
from optimization import Optimization

# The simulation is now put in a function to allow for easier testing and modularity, particularly for plotting.
# This function runs the simulation for a specified number of runs and collects statistics.
def run_simulation(num_runs=100, movie_hashsets=None, threshold=60, print_results=False):
    """
    Run multiple simulations and collect statistics.

    Args:
        num_runs (int): Number of simulation runs.
        movie_hashsets (list): List of movie hashsets to use in the simulation.
        threshold (int): Acceptable max waiting time threshold in seconds.
        print_results (bool): Whether to print results for each run.

    Returns a dictionary of per-run metrics.
    """
    
    simulation = Simulation()

    # Initialize lists to store statistics for each run
    mean_waiting_times = []
    max_waiting_times = []
    var_waiting_times = []
    median_waiting_times = []
    waiting_time_percentiles = []
    bootstrap_mse_values = []
    customers_above_threshold = []

    # Run the simulation for the specified number of runs
    for i in range(num_runs):
        if print_results:
            print(f"Simulation run {i + 1}/{num_runs}")

        # Run simulation with/without optimized hashset
        requests = simulation.run(movie_hashsets=movie_hashsets)

        # Collect statistics
        stats = Stats(requests)
        waiting_times = stats.get_waiting_time()

        # Calculate statistics, and append them to the lists
        mean_waiting_times.append(np.mean(waiting_times))
        max_waiting_times.append(np.max(waiting_times))
        var_waiting_times.append(np.var(waiting_times))
        median_waiting_times.append(np.median(waiting_times))
        waiting_time_percentiles.append(np.percentile(waiting_times, [50, 90, 95, 99]))

        mse, _ = stats.mse_bootstrap(np.mean, num_bootstrap=100)
        bootstrap_mse_values.append(mse)

        count_above, _ = stats.num_customers_above_threshold(threshold)
        customers_above_threshold.append(count_above)

    return {
        "mean": mean_waiting_times,
        "max": max_waiting_times,
        "var": var_waiting_times,
        "median": median_waiting_times,
        "percentiles": waiting_time_percentiles,
        "bootstrap_mse": bootstrap_mse_values,
        "above_threshold": customers_above_threshold,
    }


def main():
    # === General Parameters ===
    num_runs = 100
    threshold = 60
    print_results = False

    # === Optimization Parameters ===
    optimization_fct_names = [
        "random",
        "replace_one", 
        "replace_two",
        "swap_one", 
        "swap_two",
        "swap_three",
        "replace_one_fill", 
        "replace_two_fill",
        "replace_three_fill",
    ]
    num_optimization_iters = 100
    num_iters_per_optimization = 250

    metric_fct = np.mean # The metric function to optimize. Options: np.mean, np.median, np.max, np.var
    use_control_variate = True # Use control variate to reduce variance in the optimization process
    use_mean_rate_constraint = True # Use mean rate constraint to ensure the average waiting time is below a certain threshold
    save_optimization_fct_history = False # Save the history of the optimization function values
    choose_optimization_fct_randomly = False # Choose the optimization function randomly for each iteration
    decreasing_tolerance = True # Decrease the tolerance for the optimization process over time

    overall_start_time = time() 

    # === Run Baseline Simulation ===
    print("Running baseline simulations...")
    baseline_stats = run_simulation(
        num_runs=num_runs,
        movie_hashsets=INITIAL_MOVIE_HASHSET,
        threshold=threshold,
        print_results=print_results
    )

    baseline_end_time = time()
    print(f"Baseline simulation time: {baseline_end_time - overall_start_time:.2f} seconds")

    # === Run Optimization ===
    # Necessary only once, as the optimization function is not called in the simulation.

    # When dealing with plotting, be careful to comment out this optimization block if the optimized solution is already known.
    # This is to avoid re-running the optimization process unnecessarily. 
    # Don't forget to uncomment it if you want to run the optimization process again.

    """
    print("Running optimization...")
    optimizer = Optimization(print_results=True, random_seed=0) # Set a random seed for reproducibility
    best_hashset, best_metric = optimizer(
        optimization_fct_names=optimization_fct_names,
        num_optimization_iters=num_optimization_iters,
        num_iters_per_optimization=num_iters_per_optimization,
        metric_fct=metric_fct,
        use_control_variate=use_control_variate,
        use_mean_rate_constraint=use_mean_rate_constraint,
        save_optimization_fct_history=save_optimization_fct_history,
        choose_optimization_fct_randomly=choose_optimization_fct_randomly,
        decreasing_tolerance=decreasing_tolerance,
    )

    optimization_end_time = time()
    print(f"\nFinal best hashset:\n{best_hashset}")
    print(f"Best waiting time metric: {best_metric:.2f}")
    print(f"Optimization time: {optimization_end_time - baseline_end_time:.2f} seconds") 
    """


    # When dealing with plotting, it saves time and ressources to comment out the optimization block if the optimized solution is already known.
    # Simply copy the optimized hashset and metric here to avoid re-running the optimization process unnecessarily.
    # This is the best hashset found during the optimization process
    best_hashset = {'ASN1': {8, 2, 6, 7}, 'ASN2': {8, 9, 5, 7}, 'MSN': {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}} 
    



    # === Run Optimized Simulation ===
    # The optimized simulation is run with the best hashset found during the optimization process.
    print("Running optimized simulations...")
    optimized_stats = run_simulation(
        num_runs=num_runs,
        movie_hashsets=best_hashset,
        threshold=threshold,
        print_results=print_results
    )

    final_time = time()
    # print(f"Optimized simulation time: {final_time - optimization_end_time:.2f} seconds") # To comment/uncomment depdening if we run the optimization process or not
    print(f"\nTotal runtime: {final_time - overall_start_time:.2f} seconds")
    
    # === Comparison Plots ===
    # Plot histograms comparing the baseline and optimized simulation statistics
    # When dealing with plotting, if the optimized solution is already known,
    # be careful to comment out the optimization block and uncomment the best_hashset line just above the current line.
    # This is to avoid re-running the optimization process unnecessarily. 

    plot_comparison_histogram(
        baseline_stats["max"],
        optimized_stats["max"],
        "Histogram of Maximum Waiting Times",
        "Maximum Waiting Time (s)"
    )

    plot_comparison_histogram(
        baseline_stats["mean"],
        optimized_stats["mean"],
        "Histogram of Mean Waiting Times",
        "Mean Waiting Time (s)"
    )

    plot_comparison_histogram(
        baseline_stats["median"],
        optimized_stats["median"],
        "Histogram of Median Waiting Times",
        "Median Waiting Time (s)"
    )

    plot_comparison_histogram(
        baseline_stats["var"],
        optimized_stats["var"],
        "Histogram of Waiting Time Variance",
        "Variance"
    )

    plot_comparison_histogram(
        baseline_stats["above_threshold"],
        optimized_stats["above_threshold"],
        "Histogram of Customers Waiting > Threshold",
        "Number of Customers"
    )

    # Plot Baseline-only histograms
    plot_baseline_histogram(
        baseline_stats["max"],
        "Baseline Histogram of Maximum Waiting Times",
        "Maximum Waiting Time (s)"
    )

    plot_baseline_histogram(
        baseline_stats["mean"],
        "Baseline Histogram of Mean Waiting Times",
        "Mean Waiting Time (s)"
    )

    plot_baseline_histogram(
        baseline_stats["median"],
        "Baseline Histogram of Median Waiting Times",
        "Median Waiting Time (s)"
    )

    plot_baseline_histogram(
        baseline_stats["var"],
        "Baseline Histogram of Waiting Time Variance",
        "Variance"
    )

    plot_baseline_histogram(
        baseline_stats["above_threshold"],
        "Baseline Histogram of Customers Waiting > Threshold",
        "Number of Customers"
    )


if __name__ == "__main__":
    main()







