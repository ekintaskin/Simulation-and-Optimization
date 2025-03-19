class Request:
    def __init__(self, group_id=None, movie_id=None, time_creation=None):
        """
        Initialize a Request object.

        Args:
            group_id: Identifier for the group making the request
            movie_id: Identifier for the requested movie
            storage_id: Identifier for the storage location
        """
        self.time_creation = time_creation  # When the request was created
        self.time_arrived = None  # When the request arrived in the system
        self.time_handled = None  # When the request started being processed
        self.time_served = None  # When the request was completed
        self.group_id = group_id  # Group identifier
        self.movie_id = movie_id  # Movie identifier
        self.storage_id = None  # Storage identifier

    def set_creation_time(self, time):
        """Set the creation time of the request."""
        self.time_creation = time

    def set_arrival_time(self, time):
        """Set the arrival time of the request."""
        self.time_arrived = time

    def set_handled_time(self, time):
        """Set the time when the request started being processed."""
        self.time_handled = time

    def set_served_time(self, time):
        """Set the time when the request was completed."""
        self.time_served = time

    def get_waiting_time(self):
        """Calculate the waiting time (time_handled - time_arrived)."""
        if self.time_handled and self.time_arrived:
            return self.time_handled - self.time_arrived
        return None

    def get_processing_time(self):
        """Calculate the processing time (time_served - time_handled)."""
        if self.time_served and self.time_handled:
            return self.time_served - self.time_handled
        return None

    def get_total_time(self):
        """Calculate the total time (time_served - time_arrived)."""
        if self.time_served and self.time_arrived:
            return self.time_served - self.time_arrived
        return None

    def __str__(self):
        """Return a string representation of the Request."""
        return f"Request(group_id={self.group_id}, movie_id={self.movie_id}, storage_id={self.storage_id})"