import random

from constants import MU_SERVE_TIME, RHO_SEND_TIME, MOVIE_SIZES

class Request:
    
    def __init__(self, group_id, movie_id, storage_id):
        """
        Initialize a Request object with automatic timing calculations.
        
        Args:
            group_id: Identifier for the group making the request (1, 2, or 3)
            movie_id: Identifier for the requested movie (0-9)
            storage_id: Identifier for the storage location (MSN, ASN1, ASN2)
        """
        # Basic request properties
        self.group_id = group_id
        self.movie_id = movie_id
        self.storage_id = storage_id
        
        # Timing variables
        self.time_creation = None
        self.time_arrived = None
        self.time_handled = None
        self.time_served = None

        # Processed flag
        self.processed = False
        
        # Calculate timing values
        self.time_request_send = self._calculate_send_time()
        self.time_movie_service = self._calculate_service_time()
    
    def _calculate_send_time(self):
        """Calculate transmission time based on group and storage node."""
        if self.group_id in RHO_SEND_TIME and self.storage_id in RHO_SEND_TIME[self.group_id]:
            return RHO_SEND_TIME[self.group_id][self.storage_id]
        return None
    
    def _get_movie_size_category(self):
        """Get the size category of the movie for service time calculation."""
        size = MOVIE_SIZES.get(self.movie_id)
        if size is None:
            return None
            
        if 700 <= size <= 900:
            return "small"
        elif 900 < size <= 1100:
            return "medium"
        elif 1100 < size <= 1500:
            return "large"
        return None
    
    def _calculate_service_time(self):
        """Calculate deterministic service time based on group, storage node, and movie size."""
        size_category = self._get_movie_size_category()
        if (self.group_id in MU_SERVE_TIME and 
            self.storage_id in MU_SERVE_TIME[self.group_id] and 
            size_category in MU_SERVE_TIME[self.group_id][self.storage_id]):
            return MU_SERVE_TIME[self.group_id][self.storage_id][size_category]
        return None
    
    def __str__(self):
        """Return a string representation of the Request."""
        return f"Request(group={self.group_id}, movie={self.movie_id}, storage={self.storage_id})"
    



    
    # def set_storage_id(self, storage_id):
    #     """Set the storage ID and recalculate timing values."""
    #     self.storage_id = storage_id
    #     self.time_request_send = self._calculate_send_time()
    #     self.time_movie_service = self._calculate_service_time()
    
    # def generate_handling_time(self):
    #     """Generate random handling time (exponential with mean 0.5 seconds)."""
    #     self.handling_time = random.expovariate(1/0.5)
    #     return self.handling_time
    
    # def generate_random_service_time(self):
    #     """Generate random part of service time (uniform between 0.3 and 0.7 seconds)."""
    #     self.random_service_time = random.uniform(0.3, 0.7)
    #     return self.random_service_time
    
    # def set_creation_time(self, time):
    #     """Set the creation time of the request."""
    #     self.time_creation = time
    #     return self
    
    # def calculate_arrival_time(self):
    #     """Calculate and set the arrival time based on creation time and transmission time."""
    #     if self.time_creation is not None and self.time_request_send is not None:
    #         self.time_arrived = self.time_creation + self.time_request_send
    #     return self.time_arrived
    
    # def set_arrival_time(self, time):
    #     """Set the arrival time of the request."""
    #     self.time_arrived = time
    #     return self
    
    # def set_handled_time(self, time):
    #     """Set the time when the request started being processed."""
    #     self.time_handled = time
    #     return self
    
    # def calculate_served_time(self):
    #     """Calculate and set the served time based on handled time and processing times."""
    #     if (self.time_handled is not None and 
    #         self.handling_time is not None and 
    #         self.time_movie_service is not None and 
    #         self.random_service_time is not None):
    #         self.time_served = (self.time_handled + 
    #                            self.handling_time + 
    #                            self.time_movie_service + 
    #                            self.random_service_time)
    #     return self.time_served
    
    # def set_served_time(self, time):
    #     """Set the time when the request was completed."""
    #     self.time_served = time
    #     return self
    
    # def get_total_service_time(self):
    #     """Get the total time needed to serve the movie."""
    #     if self.time_movie_service is not None and self.random_service_time is not None:
    #         return self.time_movie_service + self.random_service_time
    #     return None
    
    # def get_waiting_time(self):
    #     """Calculate the waiting time (time_handled - time_arrived)."""
    #     if self.time_handled is not None and self.time_arrived is not None:
    #         return self.time_handled - self.time_arrived
    #     return None
    
    # def get_processing_time(self):
    #     """Calculate the processing time (time_served - time_handled)."""
    #     if self.time_served is not None and self.time_handled is not None:
    #         return self.time_served - self.time_handled
    #     return None
    
    # def get_total_time(self):
    #     """Calculate the total time (time_served - time_arrived)."""
    #     if self.time_served is not None and self.time_arrived is not None:
    #         return self.time_served - self.time_arrived
    #     return None
    
