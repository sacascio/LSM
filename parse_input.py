#!/usr/bin/env python

import getopt
import sys
import os
import openpyxl
import string
from openpyxl.workbook import workbook
from IPy import IP
import re

# Prepared by Salvatore Cascio, Cisco Systems
# May 12, 2017

# Script assumptions:
#    1. Input file must be xls or xlsx, each field in pipe seperated format all in column A
#    2. Input data must be the first worksheet

def isValidFreq(frequency):
	if ( (57000000 <= int(frequency) <= 963000000) & (int(frequency) % 3) ) == 0:
		return 1
	else:
		print('Invalid frequency provided, %s' % frequency)
		return 0


def isValidType(type):
    if bool(re.search('Audio|Video|Private', type)) == True:
        return 1
    else:
        print ('Invalid PID type provided.  Expected Audio, Video or Private.  Provided %s' % type)
        return 0
    

def isValidMod(modulation):
    if modulation == 'Qam256':
        return 1
    else:
        print('Invalid QAM modulation provided.  Expected Qam256, Provided %s' % modulation)
        return 0
    
    
def isNum(*args):
    isValid = 1
    all = args
    for a in all:
        isvnum = a.isnumeric()
        if isvnum == False:
            print (a + " is not a valid Number" )
            isValid = 0
        

    return isValid

def isValidIP(*args):
    isValid = 1
    all = args
    for a in all:
        try:
            IP(a)
        except:
            print (a + ' is not a valid IPv4 address')
            isValid = 0
            
    return isValid
     

def isValidSessId(macsessid):
    isValid = 1
    sessmac = macsessid.split("/")
    isValidnum = isNum(sessmac[1])
    if isValidnum == 0:
        print(sessmac[1] + " is not a valid Number, part of session MAC " + macsessid)
        
    if len(sessmac[0]) != 12:
            print(sessmac[0] + ' is not valid.  MAC address length is %s. Expecting 12' % len(sessmac[0]))
            isValid = 0
    else:
        if all(c in string.hexdigits for c in sessmac[0]) == False:
            print(sessmac[0] + " is not a valid MAC address, part of session mac " + macsessid)
            isValid = 0
        
    return isValid
    
  

def main(argv):
    writelog = 1
    
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
    
    f = open('hub_parsed.txt', 'w')
    
    for row in range (1, sessionsheet.max_row+1):
        sessionid,macsessid,gwname,gwip,input_gbe,tsid,frequency,inudp,outudp,inmpeg,outmpeg,bw,ingbeip,outgbeip,pk,nds,nagra,sn,modulation,inpid,outpid,type,pmt,pcr = (sessionsheet['A' + str(row)].value).split("|")
        f.write(sessionsheet['A' + str(row)].value)
        f.write("|\n")
        validnums     = isNum(sessionid,input_gbe,tsid,frequency,inudp,outudp,inmpeg,outmpeg,bw,pk,nds,nagra,inpid,outpid,pmt,pcr)
        validsessid   = isValidSessId(macsessid)
        validip       = isValidIP(gwip,ingbeip,outgbeip)
        validMod      = isValidMod(modulation)
        validtype     = isValidType(type)
	validFreq     = isValidFreq(frequency) 
  
        if ( (not validnums) | (not validsessid) | (not validip) | (not validMod) | (not validtype) | (not validFreq ) ):
            print('Row %s has failures' % row)
            print('************************************************************************\n\n')
            writelog = 0
            
    f.close()
    workbook.close()
    
    if writelog == 0:
        os.remove('hub_parsed.txt')
    else:
        print('input file for LSM created: hub_parsed.txt')
    
        
if __name__ == '__main__':
    main(sys.argv[1:])
