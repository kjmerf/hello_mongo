#! /usr/bin/env python3


def get_words(file):
    """Read codenames file"""

    with open(file) as f:
        word_list = []
        for line in f.readlines():
            word_list.append(line.split("\t"))

    return [item.strip("\n") for sublist in word_list for item in sublist]
