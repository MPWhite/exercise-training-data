import csv
from tempfile import NamedTemporaryFile
from data_feeder.csv_file_data_feeder import CsvFileDataFeeder
from counters.null_counter import NullCounter


def test_null_counter():
    # Has 3 null point values in it
    stream_rows = [
        {'epoch': 0, 'x': 0, 'y': 0, 'z': 0},
        {'epoch': 1, 'x': 1, 'y': 1, 'z': 1},
        {'epoch': 2, 'x': 2, 'y': 2, 'z': 2},
        {'epoch': 0, 'x': 0, 'y': 0, 'z': 0},
        {'epoch': 3, 'x': 3, 'y': 3, 'z': 3},
        {'epoch': 4, 'x': 4, 'y': 4, 'z': 4},
        {'epoch': 0, 'x': 0, 'y': 0, 'z': 0},
        {'epoch': 5, 'x': 5, 'y': 5, 'z': 5}
    ]

    with NamedTemporaryFile(mode='w+') as fixture_file:

        # Write our rows to the buffer
        writer = csv.DictWriter(fixture_file, fieldnames=stream_rows[0].keys())
        writer.writeheader()
        for row in stream_rows:
            writer.writerow(row)
        fixture_file.flush()

        # Initialize the counter object by creating a feeder object
        data_feeder = CsvFileDataFeeder(fixture_file.name)
        counter = NullCounter(data_feeder)

        assert counter.count() == 3
