#!/usr/bin/env python
import argparse
import random
from typing import Iterator, List, Tuple
import logging

def prepare_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('train', type=str, help='train tag file')
    parser.add_argument('dev', type=str, help='development tag file')
    parser.add_argument('test', type=str, help='test tag file')
    parser.add_argument('--seed', type=int, help='random seed')

    return parser


def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines


def write_tags(path: str, corpus: Iterator[List[List[str]]]):
    with open(path, 'w') as target:
        lines = []
        for line in corpus:
            for tags in line: # reverse line.split() in read_tags
                text = " ".join(tags) + '\n'
                lines.append(text)
            lines.append("\n") # end of the line
        target.writelines(lines)


def main(args: argparse.Namespace):
    # TODO: do the work here.

    # Seeding the global random number generator.
    random.seed(args.seed)

    # Read all of the input data in using the above snippet.
    corpus = list(read_tags(args.input))

    # Split the data into an 80% training set, 10% development set, and 10% test set.
    random.shuffle(corpus)
    train = corpus[:int(len(corpus)*0.8)]
    development = corpus[int(len(corpus)*0.8):int(len(corpus)*0.9)]
    test = corpus[int(len(corpus)*0.9):]

    # Write the training set to the train path.
    write_tags(args.train, train)
    train = read_tags(args.train)

    # Write the development set to the dev path.
    write_tags(args.dev, development)
    development = read_tags(args.dev)

    # Write the testing set to the test path.
    write_tags(args.test, test)
    test = read_tags(args.test)


if __name__ == "__main__":
    # TODO: declare arguments.
    parser = prepare_parser()

    # TODO: parse arguments and pass them to `main`.
    main(parser.parse_args())
