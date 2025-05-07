import numpy as np
import copy
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

            #########################
            # TODO: add compute_mean_request_rate
            #########################

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
    
    def remove_one(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing one movie.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._remove(best_hashset=best_hashset, num_movies_to_remove=1)
    
    def remove_two(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing two movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._remove(best_hashset=best_hashset, num_movies_to_remove=2)
    
    def replace_one(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by replacing one movie.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=1, fill_storage=False)
    
    def replace_two(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by replacing two movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=2, fill_storage=False)
    
    def replace_one_fill(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing one movie and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=1, fill_storage=True)
    
    def replace_two_fill(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing two movies and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=2, fill_storage=True)
    
    def swap_one(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by swapping one movie between ASN1 and ASN2.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._swap(best_hashset=best_hashset, num_movies_to_swap=1)
    
    def swap_two(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by swapping two movies between ASN1 and ASN2.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._swap(best_hashset=best_hashset, num_movies_to_swap=2)
    
    def _remove(self, best_hashset:Dict[str, Set[int]]=None, num_movies_to_remove=1):
        """
        Optimize the movie hashset by removing movies.
        :param best_hashset: best movie hashset from previous iteration
        :param num_movies_to_remove: number of movies to remove
        :return: optimized movie hashsets
        """
        best_hashset = copy(best_hashset)

        # initialize the movie hashsets with a random configuration
        if best_hashset is None:
            return self.random()
        
        next_hashset:Dict[str, Set[int]] = {}
        for storage_id, movie_set in best_hashset.items():

            # if the storage is MSN, add all movies
            if storage_id == "MSN":
                next_hashset[storage_id] = MOVIES_IDS
                continue

            # if the storage is ASN1 or ASN2, remove the movies
            movie_to_remove = self.rng.choice(tuple(movie_set), size=num_movies_to_remove, replace=False)
            for movie_id in movie_to_remove:
                movie_set.remove(movie_id)

            next_hashset[storage_id] = movie_set

        return next_hashset
    
    def _replace(self, best_hashset:Dict[str, Set[int]]=None, num_movies_to_replace=1, fill_storage=False):
        """
        Optimize the movie hashset by removing movies and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :param num_movies_to_replace: number of movies to replace
        :param fill_storage: if True, remove movies and fill the storage completly with random movies
                             if False, replace movies, i.e. keep the same number of movies
        :return: optimized movie hashsets
        """
        best_hashset = copy(best_hashset)

        # initialize the movie hashsets with a random configuration
        if best_hashset is None:
            return self.random()
        
        # remove the movies from the hashset
        next_hashset = self._remove(best_hashset=best_hashset, num_movies_to_remove=num_movies_to_replace)
        
        # add the movies to the hashset
        for storage_id, movie_set in next_hashset.items():

            # continue if the storage is MSN
            if storage_id == "MSN":
                continue

            added_movies_count = 0
            capacity = STORAGE_SIZES[storage_id] - sum([MOVIE_SIZES[i] for i in movie_set])
            for movie_id in self.rng.permutation(list(MOVIES_IDS)):
                movie_id = movie_id.item()

                # check if the movie is not already in the hashset
                if movie_id in movie_set:
                    continue

                # check if there is enough capacity to add the movie
                if capacity - MOVIE_SIZES[movie_id] < 0:
                    continue

                # add the movie to the hashset
                movie_set.add(movie_id)
                capacity -= MOVIE_SIZES[movie_id]
                added_movies_count += 1

                # stop if the movies should only be replaced without filling the storage
                if not fill_storage and (added_movies_count == num_movies_to_replace):
                    break

            next_hashset[storage_id] = movie_set

        return next_hashset
    
    def _swap(self, best_hashset:Dict[str, Set[int]]=None, num_movies_to_swap=1):
        """
        Optimize the movie hashset by swapping movies between ASN1 and ASN2.
        :param best_hashset: best movie hashset from previous iteration
        :param num_movies_to_swap: number of movies to swap
        :return: optimized movie hashsets
        """
        best_hashset = copy.deepcopy(best_hashset)

        # initialize the movie hashsets with a random configuration
        if best_hashset is None:
            return self.random()
        
        # swap the movies between ASN1 and ASN2
        next_hashset:Dict[str, Set[int]] = None
        iter = 0
        while True:
            next_hashset = copy.deepcopy(best_hashset)

            # try max 1000 times to find a valid configuration
            iter += 1
            if iter > 1000:
                break

            # choose random movies to swap
            movies_to_swap_asn1 = self.rng.choice(tuple(best_hashset["ASN1"]), size=num_movies_to_swap, replace=False)
            movies_to_swap_asn2 = self.rng.choice(tuple(best_hashset["ASN2"]), size=num_movies_to_swap, replace=False)

            # remove movies from ASN1 and ASN2 and add them to the other storage
            for movie_id in movies_to_swap_asn1:
                next_hashset["ASN1"].remove(movie_id)
                next_hashset["ASN2"].add(movie_id.item())

            for movie_id in movies_to_swap_asn2:
                next_hashset["ASN2"].remove(movie_id)
                next_hashset["ASN1"].add(movie_id.item())
                
            # verify if the storage capacity is not exceeded
            if STORAGE_SIZES["ASN1"] < sum([MOVIE_SIZES[i] for i in next_hashset["ASN1"]]):
                continue
            if STORAGE_SIZES["ASN2"] < sum([MOVIE_SIZES[i] for i in next_hashset["ASN2"]]):
                continue
            if len(next_hashset["ASN1"]) < len(best_hashset["ASN1"]):
                continue
            if len(next_hashset["ASN2"]) < len(best_hashset["ASN2"]):
                continue
            break

        print(f"best_hashset: {best_hashset}")
        print(f"next_hashset: {next_hashset}")

        return next_hashset
    
    

        

# TODO:
# - implement optimization function scheduling


def test_optimization():
    """
    Test the optimization class.
    """
    optimization = Optimization(
        print_results=True,
        random_seed=3,
    )
    best_hashset, waiting_time_best = optimization(
        optimization_fct_name="swap_one", 
        num_optimization_iters=25, 
        num_iters_per_optimization=10,
        metric_fct=np.mean,
    )

    print(f"\n\nFinal hashset: {best_hashset}")
    print(f"Final waiting time: {waiting_time_best:.2f}")

if __name__ == "__main__":
    test_optimization()
