from group import Group
from storage import Storage
from constants import GROUP_IDS




class Simulation():
    def __init__(self):
        pass

    def run(self):

        # generate requests
        requests = []
        for group_id in GROUP_IDS:

            group = Group(group_id=group_id)
            requests += group.generate_requests()

        # simulate storage
        storage = Storage()
        requests = storage.process(requests)

        return requests
            
            



