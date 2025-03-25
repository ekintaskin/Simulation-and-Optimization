import random

class Request:
    # Static data tables from the PDF
    # Table 4: Time needed to send a request [in seconds]
    REQUEST_TIMES = {
        1: {"MSN": 0.5, "ASN1": 0.2},              # Group 1 (French)
        2: {"MSN": 0.5, "ASN1": 0.3, "ASN2": 0.4}, # Group 2 (Swiss German)
        3: {"MSN": 0.5, "ASN2": 0.2}               # Group 3 (Italian)
    }
    
    # Table 5: Time needed to serve a movie – deterministic part [in seconds]
    SERVICE_TIMES = {
        # Group 1 (French)
        1: {
            "MSN": {"700-900": 9, "900-1100": 12, "1100-1500": 15},
            "ASN1": {"700-900": 3, "900-1100": 4, "1100-1500": 5}
        },
        # Group 2 (Swiss German)
        2: {
            "MSN": {"700-900": 8, "900-1100": 11, "1100-1500": 14},
            "ASN1": {"700-900": 4, "900-1100": 5, "1100-1500": 6},
            "ASN2": {"700-900": 5, "900-1100": 6, "1100-1500": 7}
        },
        # Group 3 (Italian)
        3: {
            "MSN": {"700-900": 10, "900-1100": 13, "1100-1500": 16},
            "ASN2": {"700-900": 4, "900-1100": 5, "1100-1500": 6}
        }
    }
    
    # Movie sizes in MB (from Table 1)
    MOVIE_SIZES = {
        0: 850, 1: 950, 2: 1000, 3: 1200, 4: 800,
        5: 900, 6: 1000, 7: 750, 8: 700, 9: 1100
    }
    
    def __init__(self, group_id, movie_id, storage_id=None):
        """
        Initialize a Request object with automatic timing calculations.
        
        Args:
            group_id: Identifier for the group making the request (1, 2, or 3)
            movie_id: Identifier for the requested movie (0-9)
            storage_id: Identifier for the storage location (MSN, ASN1, ASN2)
                        If None, will be determined based on availability
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
        
        # Calculate timing values if storage_id is provided
        if storage_id:
            self.request_transmission_time = self._calculate_transmission_time()
            self.movie_service_time = self._calculate_service_time()
        else:
            self.request_transmission_time = None
            self.movie_service_time = None
            
        # These will be generated dynamically
        self.handling_time = None
        self.random_service_time = None
    
    def _calculate_transmission_time(self):
        """Calculate transmission time based on group and storage node."""
        if self.group_id in self.REQUEST_TIMES and self.storage_id in self.REQUEST_TIMES[self.group_id]:
            return self.REQUEST_TIMES[self.group_id][self.storage_id]
        return None
    
    def _get_movie_size_category(self):
        """Get the size category of the movie for service time calculation."""
        size = self.MOVIE_SIZES.get(self.movie_id)
        if size is None:
            return None
            
        if 700 <= size < 900:
            return "700-900"
        elif 900 <= size < 1100:
            return "900-1100"
        elif 1100 <= size <= 1500:
            return "1100-1500"
        return None
    
    def _calculate_service_time(self):
        """Calculate deterministic service time based on group, storage node, and movie size."""
        size_category = self._get_movie_size_category()
        if (self.group_id in self.SERVICE_TIMES and 
            self.storage_id in self.SERVICE_TIMES[self.group_id] and 
            size_category in self.SERVICE_TIMES[self.group_id][self.storage_id]):
            return self.SERVICE_TIMES[self.group_id][self.storage_id][size_category]
        return None
    
    def set_storage_id(self, storage_id):
        """Set the storage ID and recalculate timing values."""
        self.storage_id = storage_id
        self.request_transmission_time = self._calculate_transmission_time()
        self.movie_service_time = self._calculate_service_time()
    
    def generate_handling_time(self):
        """Generate random handling time (exponential with mean 0.5 seconds)."""
        self.handling_time = random.expovariate(1/0.5)
        return self.handling_time
    
    def generate_random_service_time(self):
        """Generate random part of service time (uniform between 0.3 and 0.7 seconds)."""
        self.random_service_time = random.uniform(0.3, 0.7)
        return self.random_service_time
    
    def set_creation_time(self, time):
        """Set the creation time of the request."""
        self.time_creation = time
        return self
    
    def calculate_arrival_time(self):
        """Calculate and set the arrival time based on creation time and transmission time."""
        if self.time_creation is not None and self.request_transmission_time is not None:
            self.time_arrived = self.time_creation + self.request_transmission_time
        return self.time_arrived
    
    def set_arrival_time(self, time):
        """Set the arrival time of the request."""
        self.time_arrived = time
        return self
    
    def set_handled_time(self, time):
        """Set the time when the request started being processed."""
        self.time_handled = time
        return self
    
    def calculate_served_time(self):
        """Calculate and set the served time based on handled time and processing times."""
        if (self.time_handled is not None and 
            self.handling_time is not None and 
            self.movie_service_time is not None and 
            self.random_service_time is not None):
            self.time_served = (self.time_handled + 
                               self.handling_time + 
                               self.movie_service_time + 
                               self.random_service_time)
        return self.time_served
    
    def set_served_time(self, time):
        """Set the time when the request was completed."""
        self.time_served = time
        return self
    
    def get_total_service_time(self):
        """Get the total time needed to serve the movie."""
        if self.movie_service_time is not None and self.random_service_time is not None:
            return self.movie_service_time + self.random_service_time
        return None
    
    def get_waiting_time(self):
        """Calculate the waiting time (time_handled - time_arrived)."""
        if self.time_handled is not None and self.time_arrived is not None:
            return self.time_handled - self.time_arrived
        return None
    
    def get_processing_time(self):
        """Calculate the processing time (time_served - time_handled)."""
        if self.time_served is not None and self.time_handled is not None:
            return self.time_served - self.time_handled
        return None
    
    def get_total_time(self):
        """Calculate the total time (time_served - time_arrived)."""
        if self.time_served is not None and self.time_arrived is not None:
            return self.time_served - self.time_arrived
        return None
    
    def __str__(self):
        """Return a string representation of the Request."""
        return f"Request(group={self.group_id}, movie={self.movie_id}, storage={self.storage_id})"