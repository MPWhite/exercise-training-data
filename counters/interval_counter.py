from counters.counter_base import Counter
from data_feeder.data_feeder_base import DataFeeder


class IntervalCounter(Counter):
    """ Creates a trivial counter that simply counts the number of DataPoint objects that the data_feeder it gets
        initialized with produces
    """
    def __init__(self, data_feeder:DataFeeder):
        self.data_feeder = data_feeder

    def count(self):
        data_stream = self.data_feeder.get_data_stream()
        count = 0

        for _ in data_stream:
            count += 1

        return count
