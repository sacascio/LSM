#!/usr/bin/env python

import getopt
import sys
import os

# Prepared by Salvatore Cascio, Cisco Systems
# May 31, 2017

def printstatic(onlinefile):

    qp_preconfig = open(onlinefile,'w')

    template = """; enter DNCS IP address to connect to DNCS
;
""" 
    qp_preconfig.write(template)
    qp_preconfig.close()
    return

def printdefperIP(qp_preconfig,dncsip,rfgwname):

    template = """object %s  
DNCSIpAddress %s
;
""" %(rfgwname,dncsip)
    qp_preconfig.write(template)
    return


def main(argv):
    writelog = 1
    
    try:
        opts,args = getopt.getopt(argv,"hd:f:n:",["dncsip=","file=","dncsname"])
    except getopt.GetoptError as err:
        print (istr(err))
        sys.exit(2)
    else:
        for opt,arg in opts:
            if opt == '-h':
                print (sys.argv[0] + " -d|--dncsip <dncs_ip> -f|--file <rfgw_file> -n|--dncsname <dncsname> ")
                sys.exit(1)
            elif opt in ( "-f", "--file"):
                filename = arg
            elif opt in ( "-d", "--dncsip"):
                dncsip = arg
            elif opt in ( "-n", "--dncsname"):
                dncsname = arg
            else:
                assert False, "Unknown"
                sys.exit(2)

    if len(argv) == 0:
        print ("Usage: " +  sys.argv[0] + "-d|--dncsip <dncs_ip> -f|--file <rfgw_file> -n|--dncsname <dncsname> No arguments given")
        sys.exit(1)

    try:
        filename
    except NameError:
        print ("Filename not specified (-f or --file)")
        sys.exit(1)
    
    try:
        dncsip
    except NameError:
        print ("DNCS IP not specified (-d|--dncsip")
        sys.exit(1)
    
    try:
        dncsname
    except NameError:
        print ("DNCS Name not specified (-n|--dncsname")
        sys.exit(1)
    
    with open(filename,'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    num = len(content)
    content.sort() 
    numqp = num / 20
    
    if num % 20 != 0:
        numqp = numqp + 1

    start = 0
    
    for y in range (1,numqp+1):
        suffix = "%02d" % y
        onlinefile = "%s_QP_online.conf.%s" % (dncsname,suffix)
        printstatic(onlinefile)
        qp_preconfig = open(onlinefile,'a')
        end = start + 20
        if end > num:
            end = num
        for z in range(start,end):
            data =  content[z].split(",")
            rfgwname = data[0]
            printdefperIP(qp_preconfig,dncsip,rfgwname)
        qp_preconfig.close()
        start = start + 20

if __name__ == '__main__':
    main(sys.argv[1:])
