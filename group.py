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

    def generate_requests(self):
        """
        Generates a list of requests for a group over the simulation period.
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
                storage_id = self.select_storage_node()

                request = Request(group_id=self.group_id, movie_id=movie_id, storage_id=storage_id)
                request.time_creation = next_time
                
                # Set arrival time for each request
                self.calculate_time_arrived(request)

                requests.append(request)

        return requests

    def select_storage_node(self):

        available_nodes = {node: RHO_SEND_TIME[self.group_id][node] for node in GROUP_STORAGE_OPTIONS[self.group_id]}

        return min(available_nodes, key=available_nodes.get)

    def calculate_time_arrived(self, request:Request):
        """
        Set the arrival time for each request based on the group and storage node.
        If the arrival time is greater than the maximum arrival time, the request is not processed.
        :param request: Request object.
        """
        request.time_arrived = request.time_creation + request.time_request_send

        if request.time_arrived > TIME_INTERVALS[-1][1]:  # end of last interval
            request.processed = False
            request.time_handled = np.inf
            request.time_served = np.inf
