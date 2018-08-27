from counters.counter_base import Counter
from constants.data_format import NullDataPoint


class NullCounter(Counter):
    """ A class that counts the 'null' data_points produced by a given file. These are human-produced, and serve as an
        authoritative reference for the number of reps in any given data source
    """
    def count(self):
        count = 0

        for data_point in self.data_stream:
            if data_point == NullDataPoint:
                count += 1

        # Files are prefaced and terminated with null points, so if we have more than zero, we
        # delete 1 to get actual count
        return count
