#!/usr/bin/env python

import getopt
import sys
import os

# Prepared by Salvatore Cascio, Cisco Systems
# May 31, 2017

def printstatic(ermip,lsmip):

    erm_preconfig = open("ERM_preconfig.txt",'w')

    template = """; ERM_preprovision with VIP
;
; configure Platform settings
;
object System
GratuitousArp Enabled
;
; configure ErmWebService protocol adaptor settings
;
; set VIP *note: must reset ERM process for VIP to take affect*
;
;
object ResourceManager
ServiceAddress %s
;
; configure ErmWebService protocol adaptor settings
;
; *** note: must configure the LSM ip address and port in the SMNotify URL ***
;
object ErmWebService
SMNotifyUrl http://%s:9003/sm/SessNotify
ErmMode Classic
ErmSesIdMode DsmccAsIs
;
; configure RA GenericQamSrm
;
; *** note: must restart ERM after changing GQI version
;
object GenericQamSrm
GqiVersion V3_0
;
; configure RA EisScs 
;
object EisScs
ScsPort 1500
ScgIdMin 4000
;
""" %(ermip,lsmip)

    erm_preconfig.write(template)
    erm_preconfig.close()
    return

def printdefperIP(erm_preconfig,rfgwname,rfgwip):

    template = """; create Rfgw %s and set to OutOfService
;
create Rfgw1 %s
CtrlIpAddress=%s
Protection Automatic
LinearSupport Enabled
AdminState=Maintenance
PortTable.AdminState.1 InService
PortTable.AdminState.2 InService
PortTable.AdminState.3 InService
PortTable.AdminState.4 InService
PortTable.AdminState.5 InService
PortTable.AdminState.6 InService
PortTable.AdminState.7 InService
PortTable.AdminState.8 InService
PortTable.AdminState.9 InService
PortTable.AdminState.10 InService
PortTable.AdminState.11 InService
PortTable.AdminState.12 InService
;
""" %(rfgwname,rfgwname,rfgwip)
    erm_preconfig.write(template)
    return


def main(argv):
    writelog = 1
    
    try:
        opts,args = getopt.getopt(argv,"he:l:f:",["ermip=","lsmip=","rfgwfile="])
    except getopt.GetoptError as err:
        print (istr(err))
        sys.exit(2)
    else:
        for opt,arg in opts:
            if opt == '-h':
                print (sys.argv[0] + " -e|--ermip <erm_ip> -l|--lsmip <lsm_ip> -f|--file <rfgw_file> ")
                sys.exit(1)
            elif opt in ( "-f", "--file"):
                filename = arg
            elif opt in ( "-l", "--lsmip"):
                lsmip = arg
            elif opt in ( "-e", "--ermip"):
                ermip = arg
            else:
                assert False, "Unknown"
                sys.exit(2)

    if len(argv) == 0:
        print ("Usage: " +  sys.argv[0] + " -e|--ermip <erm_ip> -l|--lsmip <lsm_ip> -f|--file <rfgw_file> No arguments given")
        sys.exit(1)

    try:
        filename
    except NameError:
        print ("Filename not specified (-f or --file)")
        sys.exit(1)
    
    try:
        lsmip
    except NameError:
        print ("LSM IP not specified (-l|--lsmip")
        sys.exit(1)
    
    try:
        ermip
    except NameError:
        print ("ERM IP not specified (-e|--ermip")
        sys.exit(1)

    printstatic(ermip,lsmip)
    
    erm_preconfig = open("ERM_preconfig.txt",'a')

    with open(filename,'r') as f:
        for x in f:
            x = x.strip()
            elem = x.split(",")
            rfgwname = elem[0]
            rfgwip   = elem[1]
            printdefperIP(erm_preconfig,rfgwname,rfgwip)
    erm_preconfig.close()

if __name__ == '__main__':
    main(sys.argv[1:])
