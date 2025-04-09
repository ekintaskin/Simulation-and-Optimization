import numpy as np
import matplotlib.pyplot as plt
from request import Request
# from storage import Storage

class Stats:
    def __init__(self, requests): # Will deal with "requests" in simulation.py where Stats is called upon
        # self.requests = [req for req in requests]
        # self.requests = [req for req in requests if req.processed]
        self.requests = [req for req in requests if isinstance(req, Request) and req.to_be_processed]
        
        # Unique print set to replace the ones below
        if not self.requests:
            print("No valid requests to process. Skipping statistics for this run.")
        
    
        # Prints added by Nathan to check if all the requests are correctly processed
        # Showed that 100% of them are processed as of March 26th and April 2nd
        # print(f"\n Total requests received: {len(requests)}")
        # print(f"Requests identified as processed: {len(self.requests)}\n")
        # print(f"First 5 processed request status: {[req.processed for req in self.requests[:5]]}")

    # function returning the waiting time
    # def waiting_time(self):
        # return (req.get_waiting_time() for req in self.requests)
            
    # function computing the mean of the max waiting time
    def max_waiting_time(self):
        return max(req.get_waiting_time() for req in self.requests)

    # function computing the mean of the mean waiting time
    def mean_waiting_time(self):
        return np.mean([req.get_waiting_time() for req in self.requests])

    # function computing the variance of the waiting time
    def var_waiting_time(self):
        return np.var([req.get_waiting_time() for req in self.requests])

    # function computing different percentiles of the waiting time
    def waiting_time_percentiles(self, percentiles=[50, 90, 95, 99]):
        waiting_times = [req.get_waiting_time() for req in self.requests]
        return np.percentile(waiting_times, percentiles)

    # function for finding how many clients have to wait more than a given amount of time
    # can be used to define a threshold for satisfaction
    # returns the number, the percentage and the variance of the times the threshold is exceeded
    def num_customers_above_threshold(self, threshold):
        waiting_times = np.array([req.get_waiting_time() for req in self.requests])
        count_above = np.sum(waiting_times > threshold)
        percentage_above = count_above/len(self.requests)*100
        return count_above, percentage_above#, np.var(wait_times > threshold)

    # function for computing the mean squared error of a statistic of choice and its bootstrapping equivalent
    def mse_bootstrap(self, f_statistic, num_bootstrap):
        """ Calculates the bootstrap MSE of a statistic of choice and returns the bootstrap statistics.

        Args:
            f_statistic (function): Function calculating the statistic of interest (e.g., mean, var, etc.).
                                    Must accept a NumPy array as input and return a scalar.
            num_bootstrap (int): Number of bootstrap draws.

        Returns:
            tuple: A tuple containing:
                - true_stat (float): The true statistic computed from the waiting times.
                - mse_bootstrap (float): The mean squared error (MSE) of the statistic of interest.
                - bootstrap_stats (list): The list of bootstrap statistics computed during resampling.

        Raises:
            ValueError: If there are no requests to process.
            TypeError: If f_statistic is not callable.
        """
        if len(self.requests) == 0:
            raise ValueError("No requests available to compute statistics.")
        
        if not callable(f_statistic):
            raise TypeError("f_statistic must be a callable function.")
        
        waiting_times = np.array([req.get_waiting_time() for req in self.requests])
        
        # Compute the true statistic from the waiting time
        true_stat = f_statistic(waiting_times)

        # Bootstrap resampling
        bootstrap_stats = []
        for _ in range(num_bootstrap):
            resampled_waiting_time = np.random.choice(waiting_times, size=len(waiting_times), replace=True)
            bootstrap_stats.append(f_statistic(resampled_waiting_time))
        
        # Compute MSE
        mse_bootstrap = float(np.mean((np.array(bootstrap_stats) - true_stat) ** 2))
        
        return (true_stat, mse_bootstrap, bootstrap_stats)
