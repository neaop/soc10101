# Object class.
from enum import Enum


# Generic parent class for object inheritance.
class Collection:
    # Generic constructor.
    def __init__(self, collection_ref: int, sequence_ref: int, pattern_ref: int):
        self.collection_ref = collection_ref
        self.sequence_ref = sequence_ref
        self.pattern_ref = pattern_ref

    # String method.
    def __str__(self):
        string = ("{0}, {1}, {2}".format(self.collection_ref, self.sequence_ref, self.pattern_ref))
        return string


# Enum to classify different error event types.
class EventType(Enum):
    LIFT = 0
    LOOP = 1
    STOP = 2


# Object to retain specific details of error events.
class EventCollection(Collection):
    # Constructor.
    def __init__(self, collection_ref: int, sequence_ref: int, pattern_ref: int, event_type: EventType, sector: int):
        Collection.__init__(self, collection_ref, sequence_ref, pattern_ref)
        self.event_type = event_type
        self.sector = sector
        self.additional = -1

    # String method.
    def __str__(self):
        string = ("{0}, {1}, {2}, {3}".format(Collection.__str__(self), self.event_type.name, self.sector, self.additional))
        return string


# Object to hold details of a specific collection sequence.
class SequenceCollection(Collection):
    # Constructor.
    def __init__(self, individual_id: int, collection_ref: int, sequence_ref: int, pattern_ref: int, dominant_hand: str,
                 dyslexia_status: str):
        Collection.__init__(self, collection_ref, sequence_ref, pattern_ref)
        self.individual_id = individual_id
        self.dominant_hand = dominant_hand
        self.dyslexia_status = dyslexia_status
        self.events = []
        self.sector_times = []
        self.total_time = -1
        self.total_sad = -1
        self.first_error = -1
        self.sector_ips = []
        self.average_ip = -1
        self.valid_sectors = []
        self.invalid_sectors = []
        self.error_count = -1
        self.number_of_sectors = 7 if pattern_ref == 3 else 8

    # String method.
    def __str__(self):
        string = ("{0}, {1}, {2}, {3} ".format(self.individual_id, Collection.__str__(self), self.dominant_hand,
                                               self.dyslexia_status))
        return string

    # Append error events that occurred in this sequence to object.
    def add_event(self, event: EventCollection):
        # Compare event details to sequence's.
        if event.collection_ref == self.collection_ref \
                and event.pattern_ref == self.pattern_ref \
                and event.sequence_ref == self.sequence_ref:
            self.events.append(event)
            return

    # Return sectors in which errors occurred.
    def get_invalid_sectors(self):
        invalid = []

        # Append event sector IDs.
        for event in self.events:
            invalid.append(event.sector)

        # Remove duplicate sector numbers.
        invalid = set(invalid)
        invalid = list(invalid)
        invalid.sort()

        # Update object variables.
        self.invalid_sectors = invalid
        self.error_count = len(self.events)
        return

    # Return sectors in which no error events occurred.
    def get_valid_sectors(self):
        valid = []
        # Loop through each sector in pattern.
        for i in range(1, self.number_of_sectors + 1):
            if i in self.invalid_sectors:
                pass
            # If no error occurred in current sector.
            else:
                valid.append(i)
        # Update object variable with valid sector ids.
        self.valid_sectors = valid
        return

    # Return number of error events in sequence.
    def get_error_count(self):
        self.error_count = len(self.events)
        return self.error_count

    # Calculate the Index of Performance for each sector.
    def calculate_sector_ips(self, sector_ids: list):
        for i in range(self.number_of_sectors):
            # IP = ID/MT | divide by 1000 to convert micro to millisecond.
            self.sector_ips.append(sector_ids[i] / (self.sector_times[i] / 1000))
        # Add average IP to object variables.
        self.average_ip = sum(self.sector_ips) / len(self.sector_ips)
        return
