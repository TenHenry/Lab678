import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Data format converter.")
    parser.add_argument('input_file', type=str, help='Input file path.')
    parser.add_argument('output_file', type=str, help='Output file path.')
    args = parser.parse_args()
    return args.input_file, args.output_file

input_path, output_path = parse_arguments()
