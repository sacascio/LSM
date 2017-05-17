#!/usr/bin/env python

#from __future__ import print_function
import getopt
import sys
import os

# Prepared by Salvatore Cascio, Cisco Systems
# May 16, 2017



def getpidtype(pidtype):
	if pidtype == 'Video':
		return 1
	if pidtype == 'Audio':
		return 81
	if pidtype == 'Private':
		return 5

def main(argv):
    writelog = 1
    
    try:
        opts,args = getopt.getopt(argv,"hf:z:",["file=","hub="])
    except getopt.GetoptError as err:
        print (istr(err))
        sys.exit(2)
    else:
        for opt,arg in opts:
            if opt == '-h':
                print (sys.argv[0] + " -f|--file <file_name>")
                sys.exit(1)
            elif opt in ( "-f", "--file"):
                filename = arg
            elif opt in ( "-z", "--hub"):
                hubname = arg
            else:
                assert False, "Unknown"
                sys.exit(2)

    if len(argv) == 0:
        print ("Usage: " +  sys.argv[0] + " -f|--file <file_name> -z|--hub <hub_name> No arguments given")
        sys.exit(1)

    try:
        filename
    except NameError:
        print ("Filename not specified (-f or --file)")
        sys.exit(1)
    
    try:
        hubname
    except NameError:
        print ("Hub not specified (-z or --hub)")
        sys.exit(1)

    sourcemac = {'sm':'NA'}
    struct = []
    
    # Sort input file to ensure rows are in order
    os.system('sort -u %s -o %s' % (filename,filename))
    
    with open(filename) as f:
	for x in f:
		elem = x.split("|")
		sourceid = elem[0]
		mac      = elem[1]
		mac      = mac[0:12]
		mac      = ":".join(mac[i]+mac[i+1] for i in range (0,12,2))
		key      = sourceid + mac
	
		if  sourcemac['sm'] == key:
			pidtype  = getpidtype(elem[-4])	
			inpid    = hex(int(elem[19])).replace('0x','').upper()
			outpid   = hex(int(elem[20])).replace('0x','').upper()
			struct.append(inpid)
			struct.append(outpid)
			struct.append(pidtype)
		else:
			if  sourcemac['sm'] != 'NA':
				print (','.join(map(str, struct))) 
				struct[:] = []
			sourcemac = { 'sm' : key }
			gwname   = elem[2]
			mpsrc    = elem[17]
			srmch    = elem[4]
			inudp    = elem[7].replace('.0','')
			outudp   = elem[8].replace('.0','')
			inmpeg   = elem[9]
			outmpeg  = elem[10]
			bw       = float(elem[11]) / 1000000
			if bw % 1 == 0:
				bw = int(bw)
			if bw < 1:
				bw = str(bw)
				bw = bw.replace('0.','.')
			pmt      = hex(int(elem[-3])).replace('0x','')
			pcr      = hex(int(elem[-2])).replace('0x','')
			pk       = hex(int(elem[14])).replace('0x','').upper()
			nds      = hex(int(elem[15])).replace('0x','').upper()
			nagra    = hex(int(elem[16])).replace('0x','').upper()
			pidtype  = getpidtype(elem[-4])	
			inpid    = hex(int(elem[19])).replace('0x','').upper()
			outpid   = hex(int(elem[20])).replace('0x','').upper()
		
			struct.append(sourceid)
			struct.append(mac)
			struct.append(mpsrc)
			struct.append(gwname)
			struct.append(srmch)
			struct.append(inudp)
			struct.append(outudp)
			struct.append(inmpeg)
			struct.append(outmpeg)
			struct.append(bw)
			struct.append(pmt)
			struct.append(pcr)
			struct.append(pk)
			struct.append(nds)
			struct.append(nagra)
			struct.append(inpid)
			struct.append(outpid)
			struct.append(pidtype)
	
	# Print last line of file
	print (','.join(map(str, struct)))
		
if __name__ == '__main__':
    main(sys.argv[1:])
