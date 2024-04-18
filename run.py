import argparse
from app.normalizer import FootballEventNormalizer
import unittest


def main():
    parser = argparse.ArgumentParser(description="Process football event data.")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="input.csv",
        help="Path to the input CSV file (default: input.csv)",
    )
    parser.add_argument(
        "--output", default="jsonl", help="Output file extension (default: jsonl)"
    )
    parser.add_argument("--test", action="store_true", help="Run tests")
    args = parser.parse_args()

    if args.test:
        test_suite = unittest.TestLoader().discover("app/tests")
        unittest.TextTestRunner().run(test_suite)
    else:
        processor = FootballEventNormalizer(args.input_file, args.output)
        processor.run()


if __name__ == "__main__":
    main()
