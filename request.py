import numpy as np

from constants import MU_SERVE_TIME, RHO_SEND_TIME, MOVIE_SIZES, TIME_INTERVALS

class Request:
    
    def __init__(self, group_id, movie_id, storage_id, time_creation):
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
        self.time_creation = time_creation
        self.time_arrived = None
        self.time_served = None
        
        # Calculate timing values
        self.time_request_send = self._calculate_send_time()
        self.time_movie_service = self._calculate_service_time()
        self.time_arrived = self.time_creation + self.time_request_send

        # Check if arrival is within processing bounds
        if self.time_arrived > TIME_INTERVALS[-1][1]:  # end of last interval
            self.to_be_processed = False
            self.time_handled = np.inf
            self.time_served = np.inf
        else:
            self.to_be_processed = True

    def get_waiting_time(self):
        """Calculate the waiting time (time_served - time_creation)."""
        if self.time_creation is None or self.time_served is None:
            return None
        if not self.to_be_processed:
            return None
        return self.time_served - self.time_creation

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
