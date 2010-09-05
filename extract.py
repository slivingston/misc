#!/usr/bin/env python
#
# Extract numbers from ngspice output (printed to STDOUT).
# Input is read from STDIN, result is dumped to STDOUT. Use
# shell redirection to read from / write to files.
#
# Scott Livingston
# 23 Mar 2010.


try:

    #print "plot '-' using 2:4"

    ex_mode = False
    while True:
        line = raw_input()
        if ex_mode:
            line_cols = line.split()
            try:
                if len(line_cols) == 0:
                    raise ValueError
                current_ind = int(line_cols[0])
                print line
            except ValueError:
                ex_mode = False
        if line[:5] == 'Index':
            ex_mode = True
            raw_input() # Eat the next line, which should simply be a divider consisting of the character "-" repeated.


except EOFError:
    #print 'e'
    exit(0)
except:
    print 'Error during processing'
    exit(-1)

