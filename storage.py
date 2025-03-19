import numpy as np
from request import Request
from functools import cmp_to_key

class Storage:

    def __init__(self, rho_arrival, lambda_handle, mus_serve, bound_serve, max_arrival_time):
        """
        Initialize parameters for the storage
        :param rho_arrival (list<float>): arrival delay for each group
        :param lambda_handle (float): handling rate
        :param mus_serve (array<int> [3, #grp]): deterministic service time by movie size (small, medium, large) and group
        :param bound_serve (tuple<float, float>): bounds for uniform distribution of service time
        :param max_arrival_time (float): maximum arrival time for requests to be considered
        """
        self.rho_arrival = rho_arrival
        self.lambda_handle = lambda_handle
        self.mu_small_serve = mus_serve[0]
        self.mu_medium_serve = mus_serve[1]
        self.mu_large_serve = mus_serve[2]
        self.min_serve = bound_serve[0]
        self.max_serve = bound_serve[1]
        self.max_arrival_time = max_arrival_time

    def process(self, requests):
        """
        Simulate the queue of requests by processing in-place the request (handling and serving) by order of arrival
        on a First-Come-First-Served basis. In particular, draw Delta t_handle ~ Exp(lambda_handle) and
        Delta t_serve ~ mu(group, movie) + U(min_serve, max_serve) for each request.
        :param: requests (list<Request>): list of requests to be processed
        """
        n_request = len(requests)
        if n_request == 0: return  # nothing to process

        # Set arrival time for each request
        for request in requests:
            request.arrival_time = request.time_creation + self.rho_arrival[request.group_id]
            if request.arrival_time > self.max_arrival_time:
                request.processed = False
                request.time_handled = np.infty
                request.time_served = np.infty

        # Sort requests by arrival time
        arrival_sorted_requests = sorted(requests, key=cmp_to_key(lambda x,y: x.time_arrived - y.time_arrived))

        # Process requests in order of arrival
        deltas_time_handle = np.random.exponential(1/self.lambda_handle, size=n_request)  # generate in batch for efficiency
        deltas_time_serve_random = np.random.uniform(self.min_serve, self.max_serve, size=n_request)  # generate in batch for efficiency

        process_start_time = arrival_sorted_requests[0].time_arrived
        for request, delta_time_handle, delta_time_serve_random in zip(arrival_sorted_requests, deltas_time_handle, deltas_time_serve_random):
            request.time_handled = process_start_time + delta_time_handle
            request.time_served = request.time_handled + self.mu(request) + delta_time_serve_random
            request.processed = True

            process_start_time = request.time_served  # need to check if this is the correct time to start the next request (@served or @handled)

    def mu(self, request):
        """
        Return deterministic service time for a request based on the group and movie size.
        :param request (Request): request processed
        :return: deterministic service time for the request
        """
        if request.movie_size <= 900: return self.mu_small_serve[request.group_id]
        elif request.movie_size <= 1100: return self.mu_medium_serve[request.group_id]
        elif request.movie_size <= 1500: return self.mu_large_serve[request.group_id]
        else: raise ValueError(f'Invalid movie size {request.movie_size} [Mb] for movie {request.movie_id}')