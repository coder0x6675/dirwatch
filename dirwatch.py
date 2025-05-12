#!/usr/bin/env python

import os
import sys
import pickle
import hashlib

from datetime import datetime


DATA_PATH = r"./data.pickle"


class SnapShot:

    def __init__(self, path):
        """ Performs the initial snapshot """
        self.path = path
        self.timestamp = datetime.now()
        self.tree = {}
        self.update()

    def span(self):
        """ Lists all files within a directory """
        tree = {}
        for root, dirs, files in os.walk(self.path):
            for file in files:
                path = f"{root}/{file}"
                try:
                    tree[path] = hash_sha512(path)
                except PermissionError:
                    print(f"Warning: File not readable, skipping {path}", file=sys.stderr)
        return tree

    def update(self):
        """ Updates the snapshot by comparing the known with the current directory state """
        old_tree = self.tree
        new_tree = self.span()

        #ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        #print(f"Changes since last snapshot ({ts}):")

        all_files = old_tree.keys() | new_tree.keys()
        for file in all_files:
            in_old_tree = file in old_tree
            in_new_tree = file in new_tree

            if in_old_tree and not in_new_tree:
                print(f"[REMOVED] {file}")
            elif in_new_tree and not in_old_tree:
                print(f"[CREATED] {file}")
            elif old_tree[file] != new_tree[file]:
                print(f"[CHANGED] {file}")

        self.tree = new_tree
        self.timestamp = datetime.now()


def fail(*args, **kwargs):
    """ Exits the program gracefully upon error """
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


def hash_sha512(path):
    """ Calculates the sha-2 512 hash of the specified file """
    bufferSize = 65536
    sha512 = hashlib.sha512()
    if not os.path.isfile(path):
        print(f"Warning: Ignoring content of special file {path}", file=sys.stderr)
        return ""
    with open(path, "rb") as fd:
        data = fd.read(bufferSize)
        while data:
            sha512.update(data)
            data = fd.read(bufferSize)
    return sha512.hexdigest()


def save_data(path, data):
    """ Saves object to file in pickle format """
    with open(DATA_PATH, "wb") as fd:
        pickle.dump(data, fd)


def load_data(path):
    """ Loads pickled data from file """
    if not os.path.exists(path):
        print("Warning: datafile not found, creating a new one", file=sys.stderr)
        data = {}
    else:
        try:
            with open(DATA_PATH, "rb") as fd:
                data = pickle.load(fd)
        except Exception:
            fail("Error: could not open the datafile")
    return data


def main():

    # Argument error checks
    if len(sys.argv) <= 1:
        fail("Usage: dirwatch [DIRECTORIES]")
    for path in sys.argv[1:]:
        if not os.path.isdir(path):
            fail(f"Error: Unable to find directory {path}")

    # Check directores for changes
    data = load_data(DATA_PATH)
    for path in sys.argv[1:]:
        if path in data:
            data[path].update()
        else:
            data[path] = SnapShot(path)
    save_data(data, data)


if __name__ == "__main__":
    main()


