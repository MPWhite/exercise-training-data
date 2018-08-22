import csv
import pytest
from tempfile import NamedTemporaryFile
from constants.data_format import dict_to_data_point
from data_feeder.csv_file_data_feeder import CsvFileDataFeeder, TimestepCsvFileDataFeeder


def test_csv_file_data_feeder():
    stream_rows = [
        {'epoch': 1, 'x': 1, 'y': 1, 'z': 1},
        {'epoch': 2, 'x': 2, 'y': 2, 'z': 2},
        {'epoch': 3, 'x': 3, 'y': 3, 'z': 3},
        {'epoch': 4, 'x': 4, 'y': 4, 'z': 4},
        {'epoch': 5, 'x': 5, 'y': 5, 'z': 5}
    ]
    # Open a named temp file
    with NamedTemporaryFile(mode='w+') as fixture_file:

        # Write our rows to the buffer
        writer = csv.DictWriter(fixture_file, fieldnames=stream_rows[0].keys())
        writer.writeheader()
        for row in stream_rows:
            writer.writerow(row)

        # Actually write them
        fixture_file.flush()

        # Initialize the feeder object and get the stream
        data_feeder = CsvFileDataFeeder(fixture_file.name)
        test_data_stream = data_feeder.get_data_stream()

        # Iterate through the rows, making sure we get our data back in order
        for row in stream_rows:
            expected_data_point = dict_to_data_point(row)
            next_data_point = next(test_data_stream)
            assert expected_data_point == next_data_point

        # Make sure that we don't get any other rows
        with pytest.raises(StopIteration):
            next(test_data_stream)


def test_timestep_csv_file_data_feeder():
    stream_rows = [
        {'epoch': 1, 'x': 1, 'y': 1, 'z': 1},
        {'epoch': 2, 'x': 2, 'y': 2, 'z': 2},
        {'epoch': 3, 'x': 3, 'y': 3, 'z': 3},
        {'epoch': 4, 'x': 4, 'y': 4, 'z': 4},
        {'epoch': 5, 'x': 5, 'y': 5, 'z': 5}
    ]
    # Open a named temp file
    with NamedTemporaryFile(mode='w+') as fixture_file:

        # Write our rows to the buffer
        writer = csv.DictWriter(fixture_file, fieldnames=stream_rows[0].keys())
        writer.writeheader()
        for row in stream_rows:
            writer.writerow(row)

        # Actually write them
        fixture_file.flush()

        # Initialize the feeder object and get the stream
        data_feeder = TimestepCsvFileDataFeeder(fixture_file.name)
        test_data_stream = data_feeder.get_data_stream()

        # Iterate through the rows, making sure we get our data back in order
        for row in stream_rows:
            expected_data_point = dict_to_data_point(row)
            next_data_point = next(test_data_stream)
            assert expected_data_point == next_data_point

        # Make sure that we don't get any other rows
        with pytest.raises(StopIteration):
            next(test_data_stream)
