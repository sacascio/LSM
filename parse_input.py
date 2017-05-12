#!/usr/bin/env python

import getopt
import sys
import subprocess
import os
import openpyxl
from openpyxl.workbook import workbook
from argparse import Namespace



# Prepared by Salvatore Cascio, Cisco Systems
# May 12, 2017

# Script assumptions:
#    1. Input file must be xls or xlsx
#    2. Input data must be the first worksheet


# Open file if exists


# Read each cell and write to new input file


def isNum(*args):
    allfailed = 0
    all = args
    for a in all:
        isvnum = a.isnumeric()
        if isvnum == False:
            print (a + " is not a valid Number" )
            allfailed = 1
        

    return allfailed
  

def main(argv):
    
    try:
        opts,args = getopt.getopt(argv,"hf:",["file="])
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
        
        
    
    if not os.path.isfile(filename):
        print('Filename ' + filename + " does not exist")
        sys.exit(4)
        
    workbook = openpyxl.load_workbook(filename)
    
    sessionsheet = workbook.worksheets[0]
    
    for row in range (1, sessionsheet.max_row+1):
        sessionid,macsessid,gwname,gwip,input_gbe,tsid,frequency,inudp,outudp,inmpeg,outmpeg,bw,ingbeip,outgbeip,pk,nds,nagra,sn,modulation,inpid,outpid,type,pmt,pcr = (sessionsheet['A' + str(row)].value).split("|")
        validnums   = isNum(sessionid,input_gbe,tsid,frequency,inudp,outudp,inmpeg,outmpeg,bw,pk,nds,nagra,inpid,outpid,pmt,pcr)
        
        if validnums == 1:
            print('Row %s has failures' % row)
            print('****************************\n\n')
        
        """
        validsessid = isValidSessId(macsessid)
        validip     = isValidIP(gwip,ingbeip,outgbeip)
        validMod    = isValidMod(modulation)
        validtype   = isValidType(type)
        
        
        if validnums & validsessid & validip & validMod & validtype:
            #Write to log file
        """
        
    
    
    
    
        
    
    
    
if __name__ == '__main__':
    main(sys.argv[1:])