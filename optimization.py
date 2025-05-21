import numpy as np
import pandas as pd
import copy
from typing import Dict, Set
import matplotlib.pyplot as plt

from simulation import Simulation
from stats import Stats
from constants import STORAGE_IDS, STORAGE_SIZES, MOVIES_IDS, MOVIE_SIZES, STORAGE_HANDLE_TIME_BETA, TIME_INTERVALS
from utils import compute_mean_request_rate, compute_overall_request_rate


class Optimization():

    def __init__(self, print_results=False, random_seed=42):
        """
        :param print_results: whether to print the results
        :param random_seed: random seed for reproducibility
        """
        self.print_results = print_results
        self.rng = np.random.default_rng(random_seed)

    def __call__(
        self, 
        optimization_fct_names, 
        num_optimization_iters=10, 
        num_iters_per_optimization=10, 
        metric_fct=np.mean, 
        use_mean_rate_constraint=False, 
        use_control_variate=False,
        save_optimization_fct_history=False,
        choose_optimization_fct_randomly=False,
    ):
        """
        Optimize the storage configuration based on the requests and storage.
        :param optimization_fct_names: list of names of function to optimize Variable Neighbourhood Search (VNS) 
                                        is used to optimize the function in a cyclic manner
        :param num_optimization_iters: number of optimization iterations
        :param num_iters_per_optimization: number of iterations per optimization
        :param metric_fct: function to calculate the metric (e.g. mean, median)
        :param use_mean_rate_constraint: whether to use the mean rate constraint
        :param use_control_variate: whether to use the control variate method
        :param save_optimization_fct_history: whether to save the optimization function history
        :param choose_optimization_fct_randomly: whether to choose the optimization function randomly
        :return: best movie hashset and its corresponding best metric
        """
        # Simulation class
        simulation = Simulation()

        best_metric = np.inf
        best_hashset = None
        fct_count = 0
        constraint_approved = None
        for i in range(num_optimization_iters):
            if self.print_results:
                print(f"\nIteration {i + 1}/{num_optimization_iters} using function {optimization_fct_names[fct_count]}")

            # Randomly choose the optimization function
            if choose_optimization_fct_randomly:
                fct_count = self.rng.integers(0, len(optimization_fct_names))

            # Call optimization function
            optimization_fct = getattr(self, optimization_fct_names[fct_count])
            movie_hashsets = optimization_fct(best_hashset=best_hashset)

            # Compute mean request rate per node and interval for constraints
            if use_control_variate or use_mean_rate_constraint:
                mean_request_rate = compute_mean_request_rate(movies_hashsets=movie_hashsets)
                mu_CV = np.max(np.array([mean_request_rate[storage_id] for storage_id in STORAGE_IDS]).flatten())

                constraint_approved = self.CONSTRAINT_mean_request_rate(mean_request_rate)
                if use_mean_rate_constraint and not constraint_approved:
                    if self.print_results:
                        print(f"Request rate greater than handling rate. Skipping...")
                    continue

            metrics = []
            control_variates = []
            for _ in range(num_iters_per_optimization):                
                # run simulation
                requests = simulation.run(movie_hashsets=movie_hashsets)

                # get Statistics
                stats = Stats(requests)
                waiting_times = stats.get_waiting_time()
                metrics.append(metric_fct(waiting_times))
                if use_control_variate: control_variates.append(self.observed_max_request_rate(requests))

            # update the best configuration if the mean metric is lower
            metrics_mean = np.mean(metrics) if not use_control_variate else self.control_variate_estimate(np.array(metrics), np.array(control_variates), mu_CV)
            if metrics_mean < best_metric:
                best_metric = metrics_mean
                best_hashset = movie_hashsets

                if self.print_results:
                    print(f"New best metric: {best_metric:.2f}.")
                    print(f"New best hashsets: {best_hashset}")

                # save the optimization function history
                if save_optimization_fct_history:
                    with open("optimization_fct_history.csv", "a") as f:
                        f.write(f"{i}, {optimization_fct_names[fct_count]}, {best_metric:.3f}, {constraint_approved}\n")
            else:
                # Variable Neighbourhood Structure (VNS): update the function to optimize
                fct_count += 1
                if fct_count >= len(optimization_fct_names):
                    fct_count = 0

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
    
    def remove_three(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing three movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._remove(best_hashset=best_hashset, num_movies_to_remove=3)
    
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
    
    def replace_three(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by replacing three movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=3, fill_storage=False)
    
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
    
    def replace_three_fill(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by removing three movies and filling the storage with random movies.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._replace(best_hashset=best_hashset, num_movies_to_replace=3, fill_storage=True)
    
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
    
    def swap_three(self, best_hashset:Dict[str, Set[int]]=None):
        """
        Optimize the movie hashset by swapping two movies between ASN1 and ASN2.
        :param best_hashset: best movie hashset from previous iteration
        :return: optimized movie hashsets
        """
        return self._swap(best_hashset=best_hashset, num_movies_to_swap=3)
    
    def _remove(self, best_hashset:Dict[str, Set[int]]=None, num_movies_to_remove=1):
        """
        Optimize the movie hashset by removing movies.
        :param best_hashset: best movie hashset from previous iteration
        :param num_movies_to_remove: number of movies to remove
        :return: optimized movie hashsets
        """
        best_hashset = copy.deepcopy(best_hashset)

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
        best_hashset = copy.deepcopy(best_hashset)

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

        return next_hashset

    def CONSTRAINT_mean_request_rate(self, mean_request_rate):
        """
        Constraint function to check if the mean request rate is at most the handling rate.
        :param mean_request_rate: mean request rate per storage node and interval
        :return: True if the constraint is satisfied, False otherwise
        """
        handling_rate = 1/STORAGE_HANDLE_TIME_BETA
        for storage_id in STORAGE_IDS:
            for interval in range(len(mean_request_rate[storage_id])):
                if mean_request_rate[storage_id][interval] > handling_rate:
                    return False
        return True

    def observed_request_rate(self, requests, total_duration):
        """
        compute the overall request rate (# requests / total duration = sum_node # requests_node / total_duration)
        :param requests: (unfiltered) requests generated by the simulation
        :param total_duration: total duration of the time intervals
        :return: overall request rate
        """
        return len(requests)/total_duration

    def observed_max_request_rate(self, requests):
        """
        compute the maximum request rate per storage node and time interval
        :param requests: (unfiltered) requests generated by the simulation
        :return: maximum rate per storage node and time interval
        """
        rates = []
        for storage_id in STORAGE_IDS:
            for time_interval in TIME_INTERVALS:
                duration = time_interval[1] - time_interval[0]
                filtered_requests = [r for r in requests if
                                     r.storage_id == storage_id and time_interval[0] <= r.time_creation <=
                                     time_interval[1]]
                rates.append(len(filtered_requests) / duration)
        return max(rates)

    def control_variate_estimate(self, X, Y, mu):
        """
        Control variate function to calculate the expected statistics using a function of the request rates f(rates) as a control variate.
        :param X: statistic T(requests) of the requests waiting time per simulation
        :param Y: f(rates) per simulation
        :param mu: theoretical overall request rate
        :return: control estimate of the expected T(requests)
        """
        # linear regression
        X_mean = np.mean(X)
        Y_mean = np.mean(Y)
        delta_X = X - X_mean
        delta_Y = Y - Y_mean

        a = np.sum(delta_X * delta_Y)/np.sum(delta_Y**2)
        b = X_mean - a * Y_mean

        return b + a*mu



def test_optimization():
    """
    Test the optimization class.
    """
    # This is the recommended list of optimization functions to use
    optimization_fct_names = [
        "random",
        "replace_one", 
        "replace_two",
        "swap_one", 
        "swap_two",
        "swap_three",
        "replace_one_fill", 
        "replace_two_fill",
    ]

    optimization = Optimization(
        print_results=True,
        random_seed=0,
    )
    best_hashset, waiting_time_best = optimization(
        optimization_fct_names=optimization_fct_names,
        num_optimization_iters=100, 
        num_iters_per_optimization=33,
        metric_fct=np.mean,
        use_control_variate=True,
        use_mean_rate_constraint=True,
        save_optimization_fct_history=False,
        choose_optimization_fct_randomly=True,
    )

    print(f"\n\nFinal hashset: {best_hashset}")
    print(f"Final waiting time: {waiting_time_best:.2f}")


if __name__ == "__main__":
    test_optimization()