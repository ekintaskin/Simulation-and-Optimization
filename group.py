from request import Request

class Group:

    def __init__(self):
        """
        Initialize parameters for the group
        """
        raise NotImplementedError

    def generate_requests(self):
        """
        Generate requests for the group
        :return: list of requests emitted by this group
        """
        raise NotImplementedError