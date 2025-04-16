import numpy as np
from typing import Dict, Set

from simulation import Simulation
from stats import Stats
from constants import STORAGE_IDS, STORAGE_SIZES, MOVIES_IDS, MOVIE_SIZES


class Optimization():

    def __init__(self, optimization_fct_name, print_results=False, random_seed=42):
        """
        :param optimization_fct: name of function to optimize
        :param print_results: whether to print the results
        :param random_seed: random seed for reproducibility
        """
        self.optimization_fct_name = optimization_fct_name
        self.print_results = print_results
        self.rng = np.random.default_rng(random_seed)

    def __call__(self, num_optimization_iters=10, num_iters_per_optimization=10, metric_fct=np.mean):
        """
        Optimize the storage configuration based on the requests and storage.
        :param num_optimization_iters: number of optimization iterations
        :param num_iters_per_optimization: number of iterations per optimization
        :param metric_fct: function to calculate the metric (e.g. mean, median)
        :return: best movie hashset and its corresponding best metric
        """
        # Simulation class
        simulation = Simulation()

        best_metric = np.inf
        best_hashset = None
        for i in range(num_optimization_iters):
            if self.print_results:
                print(f"Optimization Iteration {i + 1}")

            # Call optimization function
            optimization_fct = getattr(self, self.optimization_fct_name)
            movie_hashsets = optimization_fct(best_hashset=best_hashset)

            metrics = []
            for _ in range(num_iters_per_optimization):                
                # run simulation
                requests = simulation.run(movie_hashsets=movie_hashsets)

                # get Statistics
                stats = Stats(requests)
                waiting_times = stats.get_waiting_time()
                metrics.append(metric_fct(waiting_times))

            # update the best configuration if the mean metric is lower
            metrics_mean = np.mean(metrics)
            if metrics_mean < best_metric:
                best_metric = metrics_mean
                best_hashset = movie_hashsets

                if self.print_results:
                    print(f"New best metric:  {best_metric:.2f}.")
                    print(f"Movie hashsets: {best_hashset}\n")

        return best_hashset, best_metric


    def random(self, best_hashset=None):
        """
        Randomly generate a movie hashset for each storage option.
        :param best_hashset: not used
        :return: movie hashsets
        """
        
        movie_hashsets: Dict[str, Set[int]] = {}
        for id in STORAGE_IDS:
            movie_hashsets[id] = set()

            capacity = STORAGE_SIZES[id]
            while capacity > 0:

                # get random movie id
                movie_id = self.rng.choice(list(MOVIES_IDS)).item()

                # check if the movie is already in the hashset
                if movie_id not in movie_hashsets[id]:

                    # check if the movie can be added to the hashset
                    if capacity - MOVIE_SIZES[movie_id] >= 0:
                        movie_hashsets[id].add(movie_id)
                        capacity -= MOVIE_SIZES[movie_id]

                # check if the hashset is full
                if len(movie_hashsets[id]) == len(MOVIES_IDS):
                    break

                # check if smallest movie size is larger than the remaining capacity
                remaining_movie_ids = MOVIES_IDS - movie_hashsets[id]
                remaining_movie_sizes = [MOVIE_SIZES[i] for i in remaining_movie_ids]
                if capacity < min(remaining_movie_sizes):
                    break

        return movie_hashsets



def test_optimization():
    """
    Test the optimization class.
    """
    optimization = Optimization(
        optimization_fct_name="random", 
        print_results=True,
    )
    best_hashset, waiting_time_best = optimization(
        num_optimization_iters=25, 
        num_iters_per_optimization=10,
        metric_fct=np.mean,
    )

    print(f"\n\nFinal hashset: {best_hashset}")
    print(f"Final waiting time: {waiting_time_best:.2f}")

if __name__ == "__main__":
    test_optimization()
