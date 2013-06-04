#!/usr/bin/python
from assignment4_3 import *

if __name__ == "__main__":
	try:
		f = open("very_long_list.txt")
		f1 = open("priceList.tab","a")
		#f1.write("Model\tprice\n")
		for i in f.readlines():
			phone = PhoneDetails(i)
			phone.findAll()
			f1.write(str(phone.model)+"\t"+str(phone.price)+"\n")
			print "Processed url = ", i
		f1.close()
		f.close()
	except Exception as e:
		print type(e)