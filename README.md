# csv2wav

.CSV to .WAV file converter.

## Quick Start

Download the `csv2wav.py` file.

To read a file `test.csv`, scaling the values by `0.01` (within the output range -1 to 1), and write the output to `test.wav`:

```bash
python3 csv2wav.py test.csv --scale 0.01
```

## Command-Line Options

```
usage: csv2wav.py [-h] [--frequency FREQUENCY] [--offset OFFSET] [--scale SCALE] [--first_col FIRST_COL] [--last_col LAST_COL] [--overwrite] [--out_file OUT_FILE] in_file [in_file ...]

Convert .csv file to .wav file

positional arguments:
  in_file               Input .csv file

options:
  -h, --help            show this help message and exit
  --out_file OUT_FILE   Output .wav file (default: input file with .wav extension)
  --frequency FREQUENCY Sample frequency (default 1000 Hz)
  --offset OFFSET       Offset value to add to the source value (default 0)
  --scale SCALE         Scale factor to scale the source values to the output range (-1,1) (default 1)
  --first_col FIRST_COL First column to convert (zero-indexed, negative values are counted from the end, default 0 -- the first column)
  --last_col LAST_COL   Last column to convert (zero-indexed, negative values are counted from the end, default -1 -- the last column)
  --overwrite           Overwrite output file if it already exists
```
