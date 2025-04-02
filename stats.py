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

    # function computing the mean of the max waiting time
    def max_waiting_time(self):
        return max(req.get_waiting_time() for req in self.requests)

    # function computing the mean of the mean waiting time
    def mean_waiting_time(self):
        return np.mean([req.get_waiting_time() for req in self.requests])

    # function computing the variance of the waiting time
    def variance_of_waiting_time(self):
        return np.var([req.get_waiting_time() for req in self.requests])

    # function computing different percentiles of the waiting time
    def waiting_time_percentiles(self, percentiles=[50, 90, 95, 99]):
        waiting_times = [req.get_waiting_time() for req in self.requests]
        return np.percentile(waiting_times, percentiles)

    # function for finding how many clients have to wait more than a given amount of time
    # can be used to define a threshold for satisfaction
    # returns the number, the percentage and the variance of the times the threshold is exceeded
    def num_customers_above_threshold(self, threshold):
        wait_times = np.array([req.get_waiting_time() for req in self.requests])
        count_above = np.sum(wait_times > threshold)
        percentage_above = count_above/len(self.requests)
        return count_above, percentage_above, np.var(wait_times > threshold)


