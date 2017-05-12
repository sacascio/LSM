#!/usr/bin/env python

import getopt
import sys
import subprocess
import os


# Script options


# Open file if exists


# Read each cell and write to new input file



def main(argv):
    
    try:
        opts,args = getopt.getopt(argv,"f:",["file="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    else:
        for opt,arg in opts:
            if opt == '-h':
                print sys.argv[0] + " -f|--file <file_name>"
                sys.exit(1)
            elif opt in ( "-f", "--file"):
                filename = arg
            else:
                assert False, "Unknown"
                sys.exit(2)

    if len(argv) == 0:
        print "Usage: " +  sys.argv[0] + " -f|--file <file_name> No arguments given"
        sys.exit(1)

    try:
        filename
    except NameError:
        print "Filename not specified (-f or --file)"
        sys.exit(1)
    
    
if __name__ == '__main__':
    main(sys.argv[1:])