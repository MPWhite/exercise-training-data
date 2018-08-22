from typing import Iterator
from constants.data_format import DataPoint


class DataFeeder:
    """ Base class defining a get_data_stream method which reveals an iterator.
        For file sources, just iterate through lines in the file returning the row
        For active data sources, block until data is acquired then yield the captured data"""

    def get_data_stream(self) -> Iterator[DataPoint]:
        raise NotImplementedError
