#!/usr/bin/python
import pickle
from socket import *

s= ""
rs = ""
l = []



def printTable(a):
        """Prints the result as a formatted table, accepts an input of a list of a list of dictionaries"""
        for key, value in a[0].iteritems():
                print  "%12s\t" %(key),
        print ''
        for i in range(len(a)):
                for key, value in a[i].iteritems():
                        print "%12s\t" %(value),
                print ''




try:
	sock = socket(AF_INET,SOCK_STREAM)
	while True:
		sock.connect(("localhost",12346))
		query = raw_input("enter query:\n")
		sock.send(query)
		rs = sock.recv(100000)
		l = pickle.loads(rs)
		if type(l) == list:	
			printTable(l)	
		elif type(l) == str:
			print l	
		sock.close()
		sock = socket(AF_INET,SOCK_STREAM)
except KeyboardInterrupt as e:
	print "successful exit"
except error as e:
	print "TCP socket error: "+str(e)
except Exception as e:
	print "Unknown exception:"+str(e)