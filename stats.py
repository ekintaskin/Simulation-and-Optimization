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

    def get_waiting_time(self):
        """Returns the waiting times as a NumPy array."""
        return np.array([req.get_waiting_time() for req in self.requests])

    # Realisation that the mean, max and var functions were useless compared to np ones

    # def max_waiting_time(self):
    #     return np.max(self.get_waiting_time())

    # def mean_waiting_time(self):
    #     return np.mean(self.get_waiting_time())

    # def var_waiting_time(self):
    #     return np.var(self.get_waiting_time())

    # # function computing different percentiles of the waiting time
    # def waiting_time_percentiles(self, percentiles=[50, 90, 95, 99]):
    #     waiting_times = [req.get_waiting_time() for req in self.requests]
    #     return np.percentile(waiting_times, percentiles)

    def num_customers_above_threshold(self, threshold):
        waiting_times = self.get_waiting_time()
        count_above = np.sum(waiting_times > threshold)
        percentage_above = count_above / len(self.requests) * 100
        return count_above, percentage_above

    def user_satisfaction(self, waiting_times, critical_wait_time=120, decay_rate=0.025):
        """Calculates user satisfaction in [0,1], 1 being completely satisfied,
            based on waiting times using a sigmoid map.

        Args:
            waiting_times (list): List of waiting times.
            critical_wait_time (float): Critical waiting time threshold (at which the satisfaction is 0.5).
            decay_rate (float): Decay rate for the exponential function.

        Returns:
            float: User satisfaction score in [0,1].
        """
        exp_decay = np.exp(-decay_rate * (waiting_times - critical_wait_time))
        return exp_decay / (1 + exp_decay)

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
        
        waiting_times = self.get_waiting_time()
        true_stat = f_statistic(waiting_times)

        bootstrap_stats = []
        for _ in range(num_bootstrap):
            resampled_waiting_time = np.random.choice(waiting_times, size=len(waiting_times), replace=True)
            bootstrap_stats.append(f_statistic(resampled_waiting_time))
        
        mse_bootstrap = float(np.mean((np.array(bootstrap_stats) - true_stat) ** 2))
        
        return (true_stat, mse_bootstrap, bootstrap_stats)
