import csv
from tempfile import NamedTemporaryFile
from multiplex_stream.stream_splitter import StreamSplitter
from counters.null_counter import NullCounter
from counters.interval_counter import IntervalCounter
from data_feeder.csv_file_data_feeder import CsvFileDataFeeder


def test_multiplex_stream():
    # Stream with 3 null counts
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
        counter_classes = [IntervalCounter, NullCounter, NullCounter]

        stream_splitter = StreamSplitter(data_feeder, counter_classes)
        counts = stream_splitter.execute_multi_count()

        # Verify that we got as many counts as we passed in counters
        assert len(counts) == len(counter_classes)

        # Verify each count is the correct count
        for i in range(len(counter_classes)):
            # Interval simply counts the number of data points
            if counter_classes[i] == IntervalCounter:
                assert counts[i] == len(stream_rows)
            # Null counts the number of nulls -- in this case, 3
            elif counter_classes[i] == NullCounter:
                assert counts[i] == 3
