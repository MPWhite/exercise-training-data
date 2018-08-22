import csv
from data_feeder.data_feeder_base import DataFeeder
from constants.data_format import dict_to_data_point
from time import sleep


class CsvFileDataFeeder(DataFeeder):
    """ A file-based implementation of DataFeeder."""

    def __init__(self, filepath):
        self.filepath = filepath

    def get_data_stream(self):
        """ Open the file that we are pointed to and yield the rows. This function is idempotent, although
            there is no guarantee that other DataFeeders will be as well.
        """
        with open(self.filepath) as f:
            reader = csv.DictReader(f)

            for row in reader:
                yield dict_to_data_point(row)


class TimestepCsvFileDataFeeder(CsvFileDataFeeder):
    """ Implements real time-step operations using CsvFileDataFeeder's implementation. """

    # Hardcoded frequency at 60 hz
    # Need to hardcode suggests a need for bootstrap funcs from env variables eventually
    FREQUENCY = 60

    def get_data_stream(self):
        """ Wait a hot sec before yielding our row"""
        stream = super().get_data_stream()

        for row in stream:
            sleep(1 / self.FREQUENCY)
            yield row
