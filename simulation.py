from group import Group
from storage import Storage
from constants import GROUP_IDS, STORAGE_IDS




class Simulation():
    def __init__(self):
        pass

    def run(self):

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
    for i in range(num_runs):
        if print_results:
            print(f"Run {i + 1}")
        
        # run simulation
        requests = simulation.run()

        # calculate statistics here

if __name__ == "__main__":
    test_simulation()

