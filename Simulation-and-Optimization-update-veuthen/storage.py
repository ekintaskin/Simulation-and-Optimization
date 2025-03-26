import numpy as np
from functools import cmp_to_key
from typing import List

from request import Request
from constants import BOUND_SERVE_TIME, STORAGE_HANDLE_TIME_LAMBDA


class Storage:

    def __init__(self):
        """
        Initialize parameters for the storage node.
        """
        self.lambda_handle = STORAGE_HANDLE_TIME_LAMBDA # QUESTION: is this correct?
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
        deltas_time_handle = np.random.exponential(1/self.lambda_handle, size=n_request)  # generate in batch for efficiency
        deltas_time_serve_random = np.random.uniform(self.min_serve, self.max_serve, size=n_request)  # generate in batch for efficiency

        process_start_time = arrival_sorted_requests[0].time_arrived
        for request, delta_time_handle, delta_time_serve_random in zip(arrival_sorted_requests, deltas_time_handle, deltas_time_serve_random):
            request.time_handled = process_start_time + delta_time_handle
            request.time_served = request.time_handled + request.time_movie_service + delta_time_serve_random
            request.processed = True

            process_start_time = request.time_served  # need to check if this is the correct time to start the next request (@served or @handled)

            # Print added by Nathan for seeing what happens in the for loop
            print(f"Request: Group {request.group_id}, Movie: {request.movie_id}, "
                  f"Arrival: {request.time_arrived:.2f}s, "
                  f"Handled: {request.time_handled:.2f}s, "
                  f"Served: {request.time_served:.2f}s, "
                  f"Handling Time: {delta_time_handle:.2f}s, "
                  # f"Deterministic Service Time: {self.mu(request):.2f}s, "
                  f"Random Service Time: {delta_time_serve_random:.2f}s")

        return arrival_sorted_requests
