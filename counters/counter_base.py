from typing import Iterator
from constants.data_format import DataPoint
from data_feeder.data_feeder_base import DataFeeder


class Counter:
    """ An object that implements some version of counting for a given data stream produced by a data_feeder object.
        Various implementations of the counter can be built, but they should all have the `count_the_things` method
        that counts whatever features it's looking for out of the data_feeder's stream."""

    def __init__(self, data_stream: Iterator[DataPoint]):
        self.data_stream = data_stream

    def count(self) -> int:
        """ Counts the things that it finds """
        raise NotImplementedError
