from group import Group
from storage import Storage
from constants import GROUP_IDS
from stats import Stats



class Simulation():
    def __init__(self):
        pass

    def run(self):

        # generate requests
        requests = []
        for group_id in GROUP_IDS:

            group = Group(group_id=group_id)
            requests.extend(group.generate_requests())      # Modification from Nathan
            
        # Print how many requests were generated
        print(f"Generated {len(requests)} requests for all groups.\n")

        # simulate storage
        storage = Storage()
        # requests = storage.process(requests)
        storage.process(requests)
        
        print(f"Processed {sum(req.to_be_processed for req in requests)} out of {len(requests)} requests.\n")


        # # Calculate statistics      # Addition from Nathan
        # stats = Stats(requests)     # Addition from Nathan

        # return requests, stats      # Modification from Nathan
        
        return requests
            



