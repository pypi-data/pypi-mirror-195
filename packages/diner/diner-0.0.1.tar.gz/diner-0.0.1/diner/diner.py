#!/usr/bin/env python
# encoding=utf-8
import argparse

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='train')

    # Required
    parser.add_argument('sentence', type=str,
                        help='training set directory')

    # Tokenizer settings
    parser.add_argument('--max_length', default=25, type=int)


    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    print([w for w in args.sentence])


if __name__ == '__main__':
    main()