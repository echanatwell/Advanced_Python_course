import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script similar to tail command')
    parser.add_argument('-f', '--filepaths', type=str, help='Paths to files', nargs='*')
    args = parser.parse_args()

    if args.filepaths:
        for filepath in args.filepaths:
            if len(args.filepaths) > 1:
                print(filepath)
            with open(filepath, 'r') as f:
                print(*f.readlines()[-10:], sep='\n')
    else:
        i = 0
        lines = []
        while True:
            lines.append(input())
            i += 1
            if i == 17:
                break
        print(*lines, sep='\n')

