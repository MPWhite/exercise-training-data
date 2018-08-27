# Replaces loads of functions with non-blocking alternatives
# Should be at the top of the file
from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool
from itertools import tee
from typing import List, Iterator, Tuple
from constants.data_format import DataPoint
from data_feeder.data_feeder_base import DataFeeder
from counters.counter_base import Counter


def execute_single_count(arg_tuple: Tuple[Iterator[DataPoint], Counter.__class__]):
    stream = arg_tuple[0]
    counter_class = arg_tuple[1]
    counter = counter_class(stream)
    return counter.count()


class StreamSplitter:
    """ Takes a single DataFeeder instance and a list of counters. From there, it will split the datafeeder
        iterable into multiple, initialize all the counters using the multiplexed stream, and execute the
        count in parallel.
    """

    def __init__(self, data_feeder:DataFeeder, counter_classes: List[Counter.__class__]):
        self.data_feeder = data_feeder
        self.counter_classes = counter_classes

    def execute_multi_count(self) -> List[int]:
        # Initialize a pool for multiprocessing of size num_classes
        pool = Pool(size=len(self.counter_classes))

        # Split data stream
        stream = self.data_feeder.get_data_stream()
        data_streams = tee(stream, len(self.counter_classes))
        # Remove references to original stream to make it impossible to manipulate (Fucks up the other streams)
        del stream

        # Set up arg list
        arg_list = [(data_streams[i], self.counter_classes[i]) for i in range(len(self.counter_classes))]

        results = pool.map(execute_single_count, arg_list)
        return results
