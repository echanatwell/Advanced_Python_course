import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script similar to nl -b command')
    parser.add_argument('-f', '--filepath', type=str, help='Path to file to enumerate lines', default='')
    args = parser.parse_args()

    if args.filepath:
        with open(args.filepath, 'r') as f:
            for i, line in enumerate(f.readlines(), start=1):
                print(i, line)
    else:
        i = 1
        while True:
            line = input()
            print(i, line)
            i += 1

