from enum import Enum


class Collection:
    """Object to generic collection data"""

    def __init__(self, collection_ref: int, sequence_ref: int, pattern_ref: int):
        self.collection_ref = collection_ref
        self.sequence_ref = sequence_ref
        self.pattern_ref = pattern_ref

    def to_string(self):
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

    def to_string(self):
        string = Collection.to_string(self)
        string + (", {0}, {1}".format(self.event_type.name, self.sector))
        return string


class IndividualCollection(Collection):
    """Object to hold collection data"""

    def __init__(self, individual_id: int, collection_ref: int, sequence_ref: int, pattern_ref: int, dominant_hand: str,
                 dyslexia_status: str):
        Collection.__init__(self, collection_ref, sequence_ref, pattern_ref)
        self.individual_id = individual_id
        self.dominant_hand = dominant_hand
        self.dyslexia_status = dyslexia_status
        self.lift_sectors = []
        self.loop_sectors = []
        self.stasis_sectors = []
        self.sector_times = []
        self.error_count = -1

    def to_string(self):
        string = ("{0}, ".format(self.individual_id))
        string += Collection.to_string(self)
        string += (", {0}, {1}".format(self.dominant_hand, self.dyslexia_status))
        return string

    def append_event(self, event: EventCollection):
        if event.event_type == EventType.LIFT:
            self.lift_sectors.append(event.sector)
        elif event.event_type == EventType.LOOP:
            self.loop_sectors.append(event.sector)
        elif event.event_type == EventType.STOP:
            self.stasis_sectors.append(event.sector)
        return

    def get_error_count(self):
        if self.error_count == -1:
            self.error_count = len(self.lift_sectors) + len(self.loop_sectors) + len(self.stasis_sectors)
        return self.error_count
