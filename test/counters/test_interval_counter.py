import csv
from tempfile import NamedTemporaryFile
from data_feeder.csv_file_data_feeder import CsvFileDataFeeder
from counters.interval_counter import IntervalCounter


def test_interval_counter():
    stream_rows = [
        {'epoch': 1, 'x': 1, 'y': 1, 'z': 1},
        {'epoch': 2, 'x': 2, 'y': 2, 'z': 2},
        {'epoch': 3, 'x': 3, 'y': 3, 'z': 3},
        {'epoch': 4, 'x': 4, 'y': 4, 'z': 4},
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
        counter = IntervalCounter(data_feeder)

        assert counter.count() == len(stream_rows)
