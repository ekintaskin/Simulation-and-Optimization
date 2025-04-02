import numpy as np
from functools import cmp_to_key
from typing import List

from distributed.profile import process

from request import Request
from constants import BOUND_SERVE_TIME, STORAGE_HANDLE_TIME_BETA


class Storage:
    def __init__(self):
        """
        Initialize parameters for the storage node.
        """
        self.min_serve = BOUND_SERVE_TIME[0]
        self.max_serve = BOUND_SERVE_TIME[1]

    def process(self, requests:List[Request]):
        """
        Simulate the queue of requests by processing in-place the request (handling and serving) by order of arrival
        on a First-Come-First-Served basis. In particular, draw Delta t_handle ~ Exp(lambda_handle) and
        Delta t_serve ~ mu(group, movie) + U(min_serve, max_serve) for each request.
        :param: requests (list<Request>): list of requests to be processed
        :return: arrival_sorted_requests (list<Request>): list of requests sorted by arrival time
        """
        n_request = len(requests)
        if n_request == 0: return  # nothing to process

        # Sort requests by arrival time
        arrival_sorted_requests = sorted(requests, key=cmp_to_key(lambda x,y: x.time_arrived - y.time_arrived))

        # Process requests in order of arrival
        deltas_time_handle = np.random.exponential(scale=STORAGE_HANDLE_TIME_BETA, size=n_request)  # generate in batch for efficiency
        deltas_time_serve_random = np.random.uniform(self.min_serve, self.max_serve, size=n_request)  # generate in batch for efficiency

        process_start_time = arrival_sorted_requests[0].time_arrived
        for request, delta_time_handle, delta_time_serve_random in zip(arrival_sorted_requests, deltas_time_handle, deltas_time_serve_random):
            process_start_time = max(process_start_time, request.time_arrived)  # wait until the next request arrives
            if request.to_be_processed:  # check if request is within processing time
                request.time_handled = process_start_time + delta_time_handle
                request.time_served = request.time_handled + request.time_movie_service + delta_time_serve_random

                process_start_time = request.time_handled # request.time_served  # need to check if this is the correct time to start the next request (@served or @handled)

        return arrival_sorted_requests
