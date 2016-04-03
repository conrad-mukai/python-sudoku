sudoku
======

Python program that solves sudoku puzzles.

The program takes a single argument which is a puzzle file. The file is
simply 9 lines of 9 characters, representing a Sudoku puzzle. Each character
is either a number from 1 through 9, or a space. For example:

     3   6 12
    4  1 9  3
    1 5  38  
    2    4   
     4     7 
       9    6
      78  1 5
    8  3 1  7
    62 7   3 

When this file is passed to the sudoku program it spits out the following:


    PUZZLE:
    -------------------------
    |   3   |     6 |   1 2 |
    | 4     | 1   9 |     3 |
    | 1   5 |     3 | 8     |
    -------------------------
    | 2     |     4 |       |
    |   4   |       |   7   |
    |       | 9     |     6 |
    -------------------------
    |     7 | 8     | 1   5 |
    | 8     | 3   1 |     7 |
    | 6 2   | 7     |   3   |
    -------------------------

    SOLUTION:
    -------------------------
    | 7 3 9 | 4 8 6 | 5 1 2 |
    | 4 8 2 | 1 5 9 | 7 6 3 |
    | 1 6 5 | 2 7 3 | 8 9 4 |
    -------------------------
    | 2 7 8 | 6 1 4 | 3 5 9 |
    | 9 4 6 | 5 3 8 | 2 7 1 |
    | 5 1 3 | 9 2 7 | 4 8 6 |
    -------------------------
    | 3 9 7 | 8 6 2 | 1 4 5 |
    | 8 5 4 | 3 9 1 | 6 2 7 |
    | 6 2 1 | 7 4 5 | 9 3 8 |
    -------------------------

The puzzle is echoed in a familiar form, followed by its solution. This puzzle
and other examples can be found in the puzzles directory.

The command line syntax for the program is:

    usage: sudoku [-h] [-r] [-t] [-v] puzzle

    Sudoku puzzle solver.

    positional arguments:
      puzzle           puzzle file

    optional arguments:
      -h, --help       show this help message and exit
      -r, --rating     provide difficulty rating of puzzle
      -t, --traceback  display call stack when exceptions are raised
      -v, --verbose    run in verbose mode, show solution progress
