class Collection:
    """Object to hold collection data"""

    def __init__(self, individual_id: int, collection_ref: int, sequence_ref: int, pattern_ref: int, dominant_hand: str):
        self.individual_id = individual_id
        self.collection_ref = collection_ref
        self.sequence_ref = sequence_ref
        self.pattern_ref = pattern_ref
        self.dominant_hand = dominant_hand
        self.lift_sectors = []
        self.loop_sectors = []
        self.stasis_sectors = []
        self.sector_times = []
        


