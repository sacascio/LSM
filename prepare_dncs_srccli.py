#!/usr/bin/env python

#from __future__ import print_function
import getopt
import sys
import os


# Prepared by Salvatore Cascio, Cisco Systems
# May 17, 2017
# This script takes the prepared LSM File, pulls out the unique MAC and Session ID, and finds the srcCli equivalent in the prepared srcCli data that was run by getCFsessions.pl
# Pre requisites:
#	1. LSM input file is prepared.  Used with option l|--lsm
#	2. Dump srcCli session script (getCFsessions.pl) is prepared. Used with option d|--dncs

def loadsrccli(dncsfilename):
	srcCli = {}
	with open(dncsfilename,"r") as f:
		for line in f:
			line       = line.rstrip()	
			origline   = line
			line       = line.split(',')
			kp         = line[0] + line[1]
			srcCli[kp] = origline
			
	return srcCli

def main(argv):
    writelog = 1
    
    try:
        opts,args = getopt.getopt(argv,"hl:d:",["lsm=","dncs="])
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(2)
    else:
        for opt,arg in opts:
            if opt == '-h':
                print (sys.argv[0] + " -l|--lsm <lsm_file_name> -d|--dncs <dncs source cli file>")
                sys.exit(1)
            elif opt in ( "-d", "--dncs"):
                dncsfilename = arg
            elif opt in ( "-l", "--lsm"):
                lsmfilename  = arg
            else:
                assert False, "Unknown"
                sys.exit(2)

    if len(argv) == 0:
        print ("Usage: " +  sys.argv[0] + " -l|--lsm <lsm_file_name> -d|--dncs <dncs source cli file>  No arguments given")
        sys.exit(1)

    try:
        dncsfilename 
    except NameError:
       	print ("DNCS Filename not specified. Use option -d or --dncs ")
       	sys.exit(1)
    else:
	if not os.path.isfile(dncsfilename):
		print "File %s not found on the filesystem for DNCS Source CLI" %dncsfilename
		sys.exit(1)

    try:
        lsmfilename 
    except NameError:
       	print ("LSM Filename not specified.  Use option -l or --lsm ")
       	sys.exit(1)
    else:
	if not os.path.isfile(lsmfilename):
		print "File %s not found on the filesystem for LSM" %lsmfilename
		sys.exit(1)
    
    sourcemac = {}
    
    srcclisess = loadsrccli(dncsfilename)
 
    with open(lsmfilename) as f:
	for x in f:
		elem = x.split("|")
		sourceid = elem[0]
		mac      = elem[1]
		mac      = mac[0:12]
		mac      = ":".join(mac[i]+mac[i+1] for i in range (0,12,2))
		key      = sourceid + mac
	
		if  (not sourcemac.has_key(key)):
			sourcemac[key] = [sourceid,mac]

	for x in sourcemac.keys():
		if srcclisess.has_key(x):
			print srcclisess[x]
		else:
			print("WARNING!! NO DNCS SOURCE CLI FOUND FOR SESSION ID %s, MAC ADDRESS %s!!") %(sourcemac[x][0],sourcemac[x][1])
		
if __name__ == '__main__':
    main(sys.argv[1:])
