#!/usr/bin/env python3
import csv
import wave
from pathlib import Path

def csv2wav(in_file, out_file = None, frequency = 1000, offset = 0, scale = 1, first_col = 0, last_col = -1, overwrite = False):
    if out_file == None:
        out_file = Path(in_file).stem + ".wav"

    print('READING:', in_file)

    # Read .csv file
    with open(in_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Adjust columns to match data, negative values are counted from the end
    if first_col < 0:
        first_col = len(data[0]) + first_col
    if last_col < 0:
        last_col = len(data[0]) + last_col
    num_channels = last_col - first_col + 1
    print('COLUMNS: ' + str(first_col) + ' to ' + str(last_col) + ' = ' + str(num_channels) + ' channels')
    print('ROWS: ' + str(len(data)))

    # Check extension of output file
    print('WRITING:', out_file)
    if out_file[-4:] != '.wav':
        print('ERROR: Output file must be .wav (for safety)')
        return 1
    if not overwrite and Path(out_file).exists():
        print('ERROR: Output file already exists.  To overwrite, specify --overwrite')
        return 1

    print('SAMPLE-RATE:', frequency)
    print('DURATION:', len(data) / frequency, 's')

    # Write .wav file
    with wave.open(out_file, 'w') as w:
        w.setnchannels(num_channels)
        w.setsampwidth(2)   # 16-bit signed integer
        w.setframerate(frequency)
        w.setnframes(len(data))
        w.setcomptype('NONE', 'not compressed')
        for row in data:
            for i in range(first_col, last_col + 1):
                value = float(row[i])
                value += offset     # User-supplied offset
                value *= scale      # User-supplied scale factor
                value *= 2**15      # Scale (-1,1) to full 16-bit signed integer range
                # Clamp to 16-bit signed range
                if value > 2**15 - 1:
                    value = 2**15 - 1
                if value < -2**15:
                    value = -2**15
                w.writeframesraw(int(value).to_bytes(2, 'little'))
    
    print('DONE')
    return 0

if __name__ == "__main__":
    print("csv2wav")
    # Read arguments
    import argparse
    parser = argparse.ArgumentParser(description='Convert .csv file to .wav file')
    parser.add_argument('in_file', nargs='+', help='Input .csv file')
    parser.add_argument('--out_file', help='Output .wav file (default: input file with .wav extension)')
    parser.add_argument('--frequency', type=int, default=1000, help='Sample frequency')
    parser.add_argument('--offset', type=float, default=0, help='Offset value to add to the source value')
    parser.add_argument('--scale', type=float, default=1, help='Scale factor to scale the source values to the output range (-1,1)')
    parser.add_argument('--first_col', type=int, default=0, help='First column to convert (zero-indexed, negative values are counted from the end)')
    parser.add_argument('--last_col', type=int, default=-1, help='Last column to convert (zero-indexed, negative values are counted from the end)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output file if it already exists')
    args = parser.parse_args()
    # Process each input file
    result = 0
    for in_file in args.in_file:
        result = csv2wav(in_file, args.out_file, args.frequency, args.offset, args.scale, args.first_col, args.last_col, args.overwrite)
        if result != 0:
            break
    exit(result)
