import argparse
from app.normalizer import FootballEventNormalizer

def main():
    parser = argparse.ArgumentParser(description='Process football event data.')
    parser.add_argument('input_file', nargs='?', default='input.csv', help='Path to the input CSV file (default: input.csv)')
    parser.add_argument('--output', default='jsonl', help='Output file extension (default: jsonl)')
    parser.add_argument('--test', action='store_true', help='Run tests')
    args = parser.parse_args()

    processor = FootballEventNormalizer(args.input_file, args.output)
    processor.run()

if __name__ == "__main__":
    main()