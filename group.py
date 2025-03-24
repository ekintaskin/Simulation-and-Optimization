import numpy as np
import random
from request import Request

class Group:
    def __init__(self, group_id, activity_pattern, popularity_weights, storage_options):
        """
        :param group_id: Identifier of the group (G1, G2, G3).
        :param activity_pattern: List of request rates (requests per second for each time interval).
        :param popularity_weights: Dictionary mapping movie IDs to popularity values.
        :param storage_options: List of available storage nodes for the group.
        """
        self.group_id = group_id
        self.activity_pattern = activity_pattern
        self.popularity_weights = popularity_weights
        self.storage_options = storage_options
        self.current_time = 0

    def generate_requests(self, total_time=3600):
        """
        Generates a list of requests for a group over the simulation period.
        :param total_time: Total simulation duration (1 hour).
        :return: List of Request objects.
        """
        requests = []
        time_intervals = [0, 1200, 2400, total_time]  # 3 intervals: 0-20min, 20-40min, 40-60min

        for interval in range(3):
            request_rate = self.activity_pattern[interval]
            next_time = time_intervals[interval]

            while next_time < time_intervals[interval + 1]:
                # in Poisson process, the time between consecutive events follows an exponential distribution
                inter_arrival_time = np.random.exponential(1 / request_rate)
                next_time += inter_arrival_time

                if next_time >= total_time:
                    break

                # Weighted random selection
                movie_id = random.choices(list(self.popularity_weights.keys()),
                                          weights=list(self.popularity_weights.values()))[0]

                # Determine closest available storage node
                storage_id = self.select_storage_node()

                request = Request(group_id=self.group_id, movie_id=movie_id, time_creation=next_time)
                request.set_arrival_time(next_time + self.get_request_latency(storage_id))
                request.storage_id = storage_id

                requests.append(request)

        return requests

    def select_storage_node(self):
        latencies = {
            "G1": {"MSN": 0.5, "ASN1": 0.2},
            "G2": {"MSN": 0.5, "ASN1": 0.3, "ASN2": 0.4},
            "G3": {"MSN": 0.5, "ASN2": 0.2},
        }

        available_nodes = {node: latencies[self.group_id][node] for node in self.storage_options}

        return min(available_nodes, key=available_nodes.get)

    def get_request_latency(self, storage_id):
        latencies = {
            "G1": {"MSN": 0.5, "ASN1": 0.2},
            "G2": {"MSN": 0.5, "ASN1": 0.3, "ASN2": 0.4},
            "G3": {"MSN": 0.5, "ASN2": 0.2},
        }
        return latencies[self.group_id][storage_id]
