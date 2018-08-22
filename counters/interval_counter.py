from counters.counter_base import Counter


class IntervalCounter(Counter):
    """ Creates a trivial counter that simply counts the number of DataPoint objects that the data_feeder it gets
        initialized with produces
    """
    def count(self):
        count = 0
        for _ in self.data_stream:
            count += 1

        return count
