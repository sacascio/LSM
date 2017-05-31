#!/usr/bin/env python

import getopt
import sys
import os

# Prepared by Salvatore Cascio, Cisco Systems
# SC May 31, 2017

def onlineprintstatic(onlinefile):

    qp_online = open(onlinefile,'w')

    template = """; enter DNCS IP address to connect to DNCS
;
""" 
    qp_online.write(template)
    qp_online.close()
    return

def preconfigprintstatic(preconfigfile):

    qp_preconfig = open(preconfigfile,'w')

    template = """; QamProxy pre-config file
;
; configure Platform settings
;
object System
GratuitousArp Enabled
;
""" 
    qp_preconfig.write(template)
    qp_preconfig.close()
    return

def printdefperIP_online(qp_preconfig,dncsip,rfgwname):

    template = """object %s  
DNCSIpAddress %s
;
""" %(rfgwname,dncsip)
    qp_preconfig.write(template)
    return


def main(argv):
    writelog = 1
    
    try:
        opts,args = getopt.getopt(argv,"hd:f:n:q:e:",["dncsip=","file=","dncsname=","qamproxyip=","ermvip="])
    except getopt.GetoptError as err:
        print (istr(err))
        sys.exit(2)
    else:
        for opt,arg in opts:
            if opt == '-h':
                print (sys.argv[0] + " -d|--dncsip <dncs_ip> -f|--file <rfgw_file> -n|--dncsname <dncsname> -q|--qamproxyip <qam_proxy_ip> -e|--ermvip <ermvip> ")
                sys.exit(1)
            elif opt in ( "-f", "--file"):
                filename = arg
            elif opt in ( "-d", "--dncsip"):
                dncsip = arg
            elif opt in ( "-n", "--dncsname"):
                dncsname = arg
            elif opt in ( "-q", "--qamproxyip"):
                qamproxyip = arg
            elif opt in ( "-e", "--ermvip"):
                ermvip = arg
            else:
                assert False, "Unknown"
                sys.exit(2)

    if len(argv) == 0:
        print ("Usage: " +  sys.argv[0] + " -d|--dncsip <dncs_ip> -f|--file <rfgw_file> -n|--dncsname <dncsname> -q|--qamproxyip <qam_proxy_ip> -e|--ermvip <ermvip> No arguments given")
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
    
    try:
        qamproxyip
    except NameError:
        print ("QAM Proxy IP not specified (-q|--qamproxyip")
        sys.exit(1)
    
    try:
        ermvip
    except NameError:
        print ("ERM VIP not specified (-e|--ermvip")
        sys.exit(1)
    
    with open(filename,'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    num = len(content)
    content.sort() 
    numqp = num / 20
   
    # 20 RFGW-1 per QP
    if num % 20 != 0:
        numqp = numqp + 1

    start = 0
    
    for y in range (1,numqp+1):
        suffix = "%02d" % y
        gwprefix = "QP" + suffix + "_"
        onlinefile = "%s_QP_online.conf.%s" % (dncsname,suffix)
        preconfigfile = "%s_QP_preconfig.conf.%s" % (dncsname,suffix)
        onlineprintstatic(onlinefile)
        preconfigprintstatic(preconfigfile)
        qp_online = open(onlinefile,'a')
        qp_preconfig = open(preconfigfile,'a')
        end = start + 20
        if end > num:
            end = num
        for z in range(start,end):
            data =  content[z].split(",")
            rfgwname = gwprefix + data[0]
            printdefperIP_online(qp_online,dncsip,rfgwname)
            #printdefperIP_preconfig(qp_preconfig,dncsip,rfgwname)
        qp_online.close()
        qp_preconfig.close()
        start = start + 20

if __name__ == '__main__':
    main(sys.argv[1:])
