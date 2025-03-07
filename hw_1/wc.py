import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script similar to wc command')
    parser.add_argument('-f', '--filepaths', type=str, help='Paths to files', nargs='*')
    args = parser.parse_args()

    if args.filepaths:
        total = [0, 0, 0]
        for filepath in args.filepaths:
            with open(filepath, 'rb') as f:
                n_bytes = len(f.read())
            with open(filepath, 'r') as f:
                lines = f.readlines()
                n_lines = len(lines)
                n_words = 0
                for line in lines:
                    n_words += len([w for w in line.split() if w])
            print(n_lines, n_words, n_bytes, filepath)
            total[0] += n_lines
            total[1] += n_words
            total[2] += n_bytes
        if len(args.filepaths) > 1:
            print('total', *total)
    else:
        try:
            n_lines = 0
            n_words = 0
            n_bytes = 0
            while True:
                line = input()
                n_lines += 1
                n_words += len([w for w in line.split() if w])
                n_bytes += len(line.encode("utf-8"))
        except KeyboardInterrupt:
            print(n_lines, n_words, n_bytes)