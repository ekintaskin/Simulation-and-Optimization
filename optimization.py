import numpy as np
from typing import Dict, Set

from simulation import Simulation
from stats import Stats
from constants import STORAGE_IDS, STORAGE_SIZES, MOVIES_IDS, MOVIE_SIZES


class Optimization():

    def __init__(self, print_results=False, random_seed=42):
        """
        :param print_results: whether to print the results
        :param random_seed: random seed for reproducibility
        """
        self.print_results = print_results
        self.rng = np.random.default_rng(random_seed)

    def __call__(self, optimization_fct_name, num_optimization_iters=10, num_iters_per_optimization=10, metric_fct=np.mean):
        """
        Optimize the storage configuration based on the requests and storage.
        :param optimization_fct: name of function to optimize
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
                print(f"Optimization Iteration {i + 1}/{num_optimization_iters}...")

            # Call optimization function
            optimization_fct = getattr(self, optimization_fct_name)
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
            
            # if the storage is MSN, add all movies
            if id == "MSN":
                movie_hashsets[id] = set(MOVIES_IDS)
                continue

            # if the storage is ASN1 or ASN2, randomly select movies
            movie_hashsets[id] = set()
            capacity = STORAGE_SIZES[id]
            while capacity > 0:

                # get random movie id
                movie_id = self.rng.choice(list(MOVIES_IDS)).item()

                # check if the movie is not already in the hashset
                if movie_id not in movie_hashsets[id]:

                    # check if there is enough capacity to add the movie
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
    
    def replace_one(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing one movie and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=1)
    
    def replace_two(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing two movies and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=2)
    
    def replace_three(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing three movies and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=3)
    
    def _replace(self, best_hashset:Dict[str, Set[int]]=None, num_movies_to_replace=1):
        """
        Optimize the movie hashset by removing movies and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :param num_movies_to_replace: number of movies to replace
        :return: optimized movie hashsets
        """
        # initialize the movie hashsets with a random configuration
        if best_hashset is None:
            return self.random()
        
        next_hashset:Dict[str, Set[int]] = {}
        for storage_id, movie_set in best_hashset.items():

            # if the storage is MSN, add all movies
            if storage_id == "MSN":
                next_hashset[storage_id] = MOVIES_IDS
                continue

            # if the storage is ASN1 or ASN2, remove one movie and fill the hashset with random movies
            movie_to_remove = self.rng.choice(tuple(movie_set), size=num_movies_to_replace, replace=False)
            for movie_id in movie_to_remove:
                movie_set.remove(movie_id)

            capacity = STORAGE_SIZES[storage_id] - sum([MOVIE_SIZES[i] for i in movie_set])
            for movie_id in self.rng.permutation(list(MOVIES_IDS)):
                movie_id = movie_id.item()

                # check if the movie is not already in the hashset
                if movie_id in movie_set:
                    continue

                # check if there is enough capacity to add the movie
                if capacity - MOVIE_SIZES[movie_id] >= 0:
                    movie_set.add(movie_id)
                    capacity -= MOVIE_SIZES[movie_id]

            next_hashset[storage_id] = movie_set

        return next_hashset

        




def test_optimization():
    """
    Test the optimization class.
    """
    optimization = Optimization(
        print_results=True,
    )
    best_hashset, waiting_time_best = optimization(
        optimization_fct_name="replace_two", 
        num_optimization_iters=25, 
        num_iters_per_optimization=10,
        metric_fct=np.mean,
    )

    print(f"\n\nFinal hashset: {best_hashset}")
    print(f"Final waiting time: {waiting_time_best:.2f}")

if __name__ == "__main__":
    test_optimization()
