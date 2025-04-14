import numpy as np
from dask.array import average
from numba import float64

from constants import *

def movie_to_storage_map(group_id, movies_hashsets=INITIAL_MOVIE_HASHSET):
    """
    Maps movies to their respective storage nodes for a specific group.
    :param group_id: specified group
    :param movies_hashsets: movie hashset defining the storage configuration (by default the initial configuration)
    :return: dictionary of movies to storage nodes (movie_id, storage_id)
    """

    movie_to_storage = {movie_id: 'MSN' for movie_id in MOVIES_IDS}

    for movie_id in MOVIES_IDS:
        available_nodes = {node: RHO_SEND_TIME[group_id][node] for node in GROUP_STORAGE_OPTIONS[group_id] if
                           movie_id in movies_hashsets[node]}
        movie_to_storage[movie_id] = min(available_nodes, key=available_nodes.get)

    return movie_to_storage

def group_movie_to_storage_map(movies_hashsets=INITIAL_MOVIE_HASHSET):
    """
    Maps groups and movies to their respective storage nodes in the form of a dictionary for fast-access lookups.
    :param movies_hashsets: movie hashset defining the storage configuration (by default the initial configuration)
    :return: dictionary of group and movies to storage nodes (group_id, (movie_id, storage_id))
    """

    group_movie_to_storage = {group_id: movie_to_storage_map(group_id, movies_hashsets) for group_id in GROUP_IDS}

    return group_movie_to_storage

def compute_mean_request_rate(movies_hashsets=INITIAL_MOVIE_HASHSET):
    """
    Computes the mean request rate for a given movie hashset for each time interval per storage node.
    :param movies_hashsets: movie hashset defining the storage configuration (by default the initial configuration)
    :return: mean request rate per storage node for each time interval (storage node x time interval)
    """

    mean_request_rate = {storage_id: [0 for _ in TIME_INTERVALS] for storage_id in STORAGE_IDS}
    map = group_movie_to_storage_map(movies_hashsets)

    # compounding total request number per storage in each interval
    for group_id in GROUP_IDS:
        normalized_movie_weights = np.array(list(GROUP_MOVIE_POPULARITIES[group_id].values()))*1.
        normalized_movie_weights /= np.sum(normalized_movie_weights)

        for interval in range(len(TIME_INTERVALS)):
            t_start, t_end = TIME_INTERVALS[interval]
            duration = t_start - t_end

            average_number_requests = GROUP_ACTIVITIES[group_id][interval] * duration

            for movie_id, movie_weight in zip(MOVIES_IDS, normalized_movie_weights):
                storage_id = map[group_id][movie_id]
                mean_request_rate[storage_id][interval] += average_number_requests * movie_weight

    # computing rate
    for storage_id in STORAGE_IDS:
        for interval in range(len(TIME_INTERVALS)):
            t_start, t_end = TIME_INTERVALS[interval]
            duration = t_start - t_end
            mean_request_rate[storage_id][interval] /= duration

    return mean_request_rate