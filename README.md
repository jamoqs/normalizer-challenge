# Football Event Data Normalizer

This script processes football event data stored in a CSV file and normalizes it into JSONL format.

### Prerequisites
- Python 3.x

### Installation
Simply run the `run.py` script and ensure you have Python installed on your system.

### Running the Script
To run the script, open a terminal or command prompt, navigate to the directory containing `run.py`, and execute the following command:

By default the script will use the `input.csv` file in the same directory. If you want to use a different file, you can specify the path to the input file as an argument:

```bash
python run.py
```
### Command-line Options

```bash
[input_file] (optional): Path to the input CSV file. If not provided, the script will default to using input.csv.

--output extension (optional): Specifies the output file extension. The default is jsonl. Supported extensions include json and jsonl.

--test (optional): If included, runs tests to verify the functionality of the script.

--help (optional): Displays the help message.
```

### Example Usage

```bash
python run.py data.csv --output jsonl
```
This command processes the data stored in `data.csv` and outputs the normalized data in JSON format to a file named `output.json`.

## Development

### Dependencies

- `argparse`: Used for parsing command-line arguments.

### Running Tests

To run tests, include the `--test` flag when executing the script:

```bash
python run.py --test
```

License

This script is released under the MIT License. Feel free to modify and distribute it as needed.