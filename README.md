sudoku
======

Python program that solves sudoku puzzles. This program is a demonstration of
the backtracking algorithm:

https://en.wikipedia.org/wiki/Sudoku_solving_algorithms

The program takes an optional single argument which is a puzzle file. The file
is simply 9 lines of 9 characters, representing a Sudoku puzzle. Each character
is either a number from 1 through 9, or a space. If no file is specified the
program starts with an empty grid.

An example of a puzzle file is:

     3   6 12
    4  1 9  3
    1 5  38  
    2    4   
     4     7 
       9    6
      78  1 5
    8  3 1  7
    62 7   3 

When this file is passed to the sudoku program it shows the following:

    ┌───────┬───────┬───────┐
    │   3   │     6 │   1 2 │
    │ 4     │ 1   9 │     3 │
    │ 1   5 │     3 │ 8     │
    ├───────┼───────┼───────┤
    │ 2     │     4 │       │
    │   4   │       │   7   │
    │       │ 9     │     6 │
    ├───────┼───────┼───────┤
    │     7 │ 8     │ 1   5 │
    │ 8     │ 3   1 │     7 │
    │ 6 2   │ 7     │   3   │
    └───────┴───────┴───────┘
    press any key to continue

After pressing a key the program will begin solving the puzzle. If the program
is running in slow mode (the -s option) you will see the program modifying the
puzzle until a solution is found. If the program is not in slow mode it will
just display the solution.

    ┌───────┬───────┬───────┐
    │ 7 3 9 │ 4 8 6 │ 5 1 2 │
    │ 4 8 2 │ 1 5 9 │ 7 6 3 │
    │ 1 6 5 │ 2 7 3 │ 8 9 4 │
    ├───────┼───────┼───────┤
    │ 2 7 8 │ 6 1 4 │ 3 5 9 │
    │ 9 4 6 │ 5 3 8 │ 2 7 1 │
    │ 5 1 3 │ 9 2 7 │ 4 8 6 │
    ├───────┼───────┼───────┤
    │ 3 9 7 │ 8 6 2 │ 1 4 5 │
    │ 8 5 4 │ 3 9 1 │ 6 2 7 │
    │ 6 2 1 │ 7 4 5 │ 9 3 8 │
    └───────┴───────┴───────┘
    51 iterations, press any key to exit

When a solution is found the number of iterations required to solve the puzzle
is shown. Pressing a key will exit the program.

The command line syntax for the program is:

    usage: sudoku [-h] [-s] [-d] [-t] [puzzle]

    Sudoku puzzle solver.

    positional arguments:
      puzzle           puzzle file

    optional arguments:
      -h, --help       show this help message and exit
      -s, --slow       slow mode: show puzzle being solved
      -d, --debug      don't use curses to run in a debugger
      -t, --traceback  display call stack when exceptions are raised
