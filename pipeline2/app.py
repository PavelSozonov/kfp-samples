import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate a text file with repeated strings.')
    parser.add_argument('str_amount', type=int, help='Number of "hello world" strings to write.')
    parser.add_argument('output_path', type=str, help='Path to the output file.')
    args = parser.parse_args()

    with open(args.output_path, 'w') as f:
        for _ in range(args.str_amount):
            f.write("hello world\n")

if __name__ == '__main__':
    main()
