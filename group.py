import numpy as np
import random
from request import Request
from constants import TIME_INTERVALS, GROUP_ACTIVITIES, GROUP_MOVIE_POPULARITIES, RHO_SEND_TIME, GROUP_STORAGE_OPTIONS



class Group:
    def __init__(self, group_id):
        """
        :param group_id: Identifier of the group (G1, G2, G3).
        :param popularity_weights: Dictionary mapping movie IDs to popularity values.
        """
        self.group_id = group_id
        self.current_time = 0

    def generate_requests(self, movies_hashsets):
        """
        Generates a list of requests for a group over the simulation period.
        :param movies_hashsets: Dictionary mapping storage node IDs to hashsets of movie IDs contained on storage nodes.
        :return: List of Request objects.
        """
        requests = []
        total_time = TIME_INTERVALS[-1][1] # end of last interval

        for interval in range(3):
            request_rate = GROUP_ACTIVITIES[self.group_id][interval]
            next_time = TIME_INTERVALS[interval][0] # start of interval

            while next_time < TIME_INTERVALS[interval][1]:
                # in Poisson process, the time between consecutive events follows an exponential distribution
                inter_arrival_time = np.random.exponential(1 / request_rate)
                next_time += inter_arrival_time

                if next_time >= total_time:
                    break

                # Weighted random selection
                movie_id = random.choices(list(GROUP_MOVIE_POPULARITIES[self.group_id].keys()),
                                          weights=list(GROUP_MOVIE_POPULARITIES[self.group_id].values()))[0]

                # Determine closest available storage node
                storage_id = self.select_storage_node(movie_id, movies_hashsets)

                request = Request(group_id=self.group_id, movie_id=movie_id, storage_id=storage_id, time_creation=next_time)
                requests.append(request)

        return requests

    def generate_requests_batch(self, movies_hashsets):
        """
        Optimized version of the generate_requests using batch generation of the Poisson process.
        Generates a list of requests for a group over the simulation period.
        :param movies_hashsets: Dictionary mapping storage node IDs to hashsets of movie IDs contained on storage nodes.
        :return: List of Request objects.
        """
        requests = []

        n_interval = len(GROUP_ACTIVITIES[self.group_id])
        for interval in range(n_interval):
            request_rate = GROUP_ACTIVITIES[self.group_id][interval]
            start_time, end_time = TIME_INTERVALS[interval]

            n_event_interval = np.random.poisson(request_rate * (end_time - start_time))  # the number of events in a given time interval t in a Poisson process is Poi(lambda * t)
            event_times = np.random.uniform(start_time, end_time, n_event_interval)  # given the number of events, the event times are uniformly distributed in the interval
            # event_times.sort()  # not needed since sorted in storage for arrival times

            movie_ids = random.choices(list(GROUP_MOVIE_POPULARITIES[self.group_id].keys()), weights=list(GROUP_MOVIE_POPULARITIES[self.group_id].values()), k=n_event_interval)
            selected_nodes = self.select_storage_node_batch(movie_ids, movies_hashsets)

            for time_creation, movie_id, storage_id in zip(event_times, movie_ids, selected_nodes):
                request = Request(group_id=self.group_id, movie_id=movie_id, storage_id=storage_id, time_creation=time_creation)
                requests.append(request)

        return requests


    def select_storage_node(self, movie_id, movies_hashsets):

        available_nodes = {node: RHO_SEND_TIME[self.group_id][node] for node in GROUP_STORAGE_OPTIONS[self.group_id] if movie_id in movies_hashsets[node]}

        return min(available_nodes, key=available_nodes.get)

    def select_storage_node_batch(self, movie_ids, movies_hashsets):
        available_nodes = GROUP_STORAGE_OPTIONS[self.group_id]
        # if movie is not available in a storage node, its rho_send_time is read as infinity
        selected_nodes = [min(available_nodes, key=lambda node: RHO_SEND_TIME[self.group_id][node] if movie_id in movies_hashsets[node] else np.infty) for movie_id in movie_ids]

        return selected_nodes
