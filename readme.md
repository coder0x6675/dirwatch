# Dirwatch

## Project status

This project was archived 2019 and is not under active development. It is only kept as a demo and proof of concept.

## Description

*dirwatch* is a script that is able to monitor directories and keep track of changes made between two points in time. It accomplishes this by taking a snapshot, or the "state", of a directory when run for the first time. On any succeedent runs, new snapshots are taken and compared against the old one. The "old" snapshot is renewed on every run.

The script is able to detect any added, removed or changed files. It is however not able to show what specific part of a files content that has changed. The snapshots will be stored in a `data.pickle` file in the current directory. To change this, edit the `DATA_PATH` variable at the top of the script.

**Note!** dirwatch completely ignores symlinks, meaning any added, removed or changed symlinks will not be logged.

## Installation

To be able to run this script, [the Python interpreter has to be installed](https://wiki.python.org/moin/BeginnersGuide/Download). No external libraries are used.

## Usage

``` bash
./dirwatch.py dir1 dir2 dir3 ...
```

The script takes in a number of directories as arguments and scans through each in order. If a directory does not exist, the script fails before any work is done.

Example:

```
$ ./dirwatch.py ~/Downloads

Warning: datafile not found, creating a new one
[CREATED] /home/user/Downloads/report.pdf
[CREATED] /home/user/Downloads/DejZtLt60ZI5RfyN--4-3is5.jpg
[CHANGED] /home/user/Downloads/download_log.txt
[CREATED] /home/user/Downloads/tmp.zip
```

