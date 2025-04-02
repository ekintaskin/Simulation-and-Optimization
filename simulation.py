from typing import List
import numpy as np
import matplotlib.pyplot as plt

from request import Request
from group import Group
from storage import Storage
from constants import GROUP_IDS, STORAGE_IDS




class Simulation():
    def __init__(self):
        pass

    def run(self) -> List[Request]:
        """
        Run the simulation for a single run.
        :return: List of processed requests.
        """

        # generate requests
        requests = []
        for group_id in GROUP_IDS:

            group = Group(group_id=group_id)
            requests.extend(group.generate_requests())

        # sort requests by storage location
        requests_sorted = {id: [] for id in STORAGE_IDS}  
        for request in requests:
            requests_sorted[request.storage_id].append(request)

        # simulate storage
        storage = Storage()
        for storage_id, r_ in requests_sorted.items():
            if len(r_) > 0:
                requests_sorted[storage_id] = storage.process(r_)

        requests = []
        for r_ in requests_sorted.values():
            requests.extend(r_)
        return requests
            
            

def test_simulation():
    # Parameters
    num_runs = 100
    print_results = True

    # Simulation class
    simulation = Simulation()

    max_waiting_times = []
    mean_waiting_times = []
    median_waiting_times = []
    for i in range(num_runs):
        if print_results:
            print(f"Run {i + 1}")
        
        # run simulation
        requests = simulation.run()

        # calculate statistics here
        waiting_times = np.array([req.get_waiting_time() for req in requests])
        assert np.all(np.array(waiting_times) >= 0), "Waiting times should be non-negative"
        assert np.all(np.array(waiting_times) < np.inf), "Waiting times should be non-negative"
        max_waiting_times.append(np.max(waiting_times))
        mean_waiting_times.append(np.mean(waiting_times))
        median_waiting_times.append(np.median(waiting_times))

    # plot max, mean, and median waiting times
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))

    ax = axes[0]
    ax.hist(max_waiting_times, bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Histogram of Maximum Waiting Times per Run')
    ax.set_xlabel('Maximum Waiting Time (s)')
    ax.set_ylabel('Frequency')

    ax = axes[1]
    ax.hist(mean_waiting_times, bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Histogram of Mean Waiting Times per Run')
    ax.set_xlabel('Mean Waiting Time (s)')
    ax.set_ylabel('Frequency')

    ax = axes[2]
    ax.hist(median_waiting_times, bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Histogram of Median Waiting Times per Run')
    ax.set_xlabel('Median Waiting Time (s)')
    ax.set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_simulation()

