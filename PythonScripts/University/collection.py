from enum import Enum


class Collection:
    """Object to generic collection data"""

    def __init__(self, collection_ref: int, sequence_ref: int, pattern_ref: int):
        self.collection_ref = collection_ref
        self.sequence_ref = sequence_ref
        self.pattern_ref = pattern_ref

    def __str__(self):
        string = ("{0}, {1}, {2}".format(self.collection_ref, self.sequence_ref, self.pattern_ref))
        return string


class EventType(Enum):
    LIFT = 0
    LOOP = 1
    STOP = 2


class EventCollection(Collection):
    def __init__(self, collection_ref: int, sequence_ref: int, pattern_ref: int, event_type: EventType, sector: int):
        Collection.__init__(self, collection_ref, sequence_ref, pattern_ref)
        self.event_type = event_type
        self.sector = sector

    def __str__(self):
        string = ("{0}, {1}, {2}".format(Collection.__str__(self), self.event_type.name, self.sector))
        return string


class IndividualCollection(Collection):
    """Object to hold collection data"""

    def __init__(self, individual_id: int, collection_ref: int, sequence_ref: int, pattern_ref: int, dominant_hand: str,
                 dyslexia_status: str):
        Collection.__init__(self, collection_ref, sequence_ref, pattern_ref)
        self.individual_id = individual_id
        self.dominant_hand = dominant_hand
        self.dyslexia_status = dyslexia_status
        self.events = []
        self.sector_times = []
        self.valid_sectors = []
        self.invalid_sectors = []
        self.error_count = -1
        self.number_of_sectors = 7 if pattern_ref == 3 else 8

    def __str__(self):
        string = ("{0}, {1}, {2}, {3} ".format(self.individual_id, Collection.__str__(self), self.dominant_hand,
                                               self.dyslexia_status))
        return string

    def add_event(self, event: EventCollection):
        if event.collection_ref == self.collection_ref and event.pattern_ref == self.pattern_ref and event.sequence_ref == self.sequence_ref:
            self.events.append(event)
            return

    def get_invalid_sectors(self):
        invalid = []
        for event in self.events:
            invalid.append(event.sector)

        invalid = set(invalid)
        invalid = list(invalid)
        invalid.sort()
        self.invalid_sectors = invalid
        return self.invalid_sectors

    def get_valid_sectors(self):
        valid = []
        for i in range(1, self.number_of_sectors + 1):
            if i in self.invalid_sectors:
                pass
            else:
                valid.append(i)
        self.valid_sectors = valid
        return self.valid_sectors

    def get_error_count(self):
        self.error_count = len(self.events)
        return self.error_count
