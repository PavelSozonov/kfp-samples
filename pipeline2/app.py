import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Generate a text file with repeated strings.')
    parser.add_argument('str_amount', type=int, help='Number of "hello world" strings to write.')
    parser.add_argument('output_path', type=str, help='Path to the output file.')
    args = parser.parse_args()

    # Ensure the directory for the output file exists
    output_dir = os.path.dirname(args.output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the specified number of "hello world" strings to the output file
    with open(args.output_path, 'w') as f:
        for _ in range(args.str_amount):
            f.write("hello world\n")

if __name__ == '__main__':
    main()
