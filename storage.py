class Storage:

    def __init__(self):
        """
        Initialize parameters for the storage
        """
        raise NotImplementedError

    def process(self, requests):
        """
        Simulate the queue of requests
        :param: requests (list<Request>): list of requests to be processed
        """
        raise NotImplementedError