#!/usr/bin/python
"""This module is not intended to be exposed to the user"""
import traceback


# The following are a sequence of test values, don't modify if you don't know what you're doing
l1 = ['a','b','c','d','e','f']
l2 = ['d','e']
l3 = ['g']
l4 = ['b','g','k']
l5 = ['c','a']

global debug
debug = False

def getOperatorList(query):
    l = []
    operatorList = []
    l = query.split("@")[1]
    l = list(str(l))
    for i in l:
        if i == "|" or i == "&":
            operatorList.append(i)
    return operatorList
def join(list1,list2):
	list3 = []
	for i in list1:
		if i in list2:
			list3.append(i)
	return list3

def eval(opndList, query):
	try:
		resultSet = []
		operatorList = []
		rs = []
		i = 0
		if debug ==False:
			opndList = opndList
			operatorList = getOperatorList(query)
		else:
			opndList = [l1,l2,l3,l4,l5]
			operatorList = query
		while i<len(operatorList):
			if operatorList[i] == "&":
				k = i
				opndList[k] = join(opndList[k],opndList[k+1])
				operatorList.pop(k)
				opndList.pop(k+1)
				print 
				i = 0
				continue
			i = 1+1

		for i in opndList:
			resultSet.append(i)
		for i in resultSet:
			for j in i:
				rs.append(j)
		resultSet = eliminateDuplicate(rs)
		return resultSet
	except Exception as e:
			print e
			print "error: unable to evalute query"


def eliminateDuplicate(l1):
	l2 = []
	for i in l1:
			if i not in l2:
				l2.append(i)

	return l2

if __name__ == "__main__":
	try:
		debug = True
		print "KDB shell, version 1.0"
		#while True:
		print "KDB>",
		#query = raw_input()
		print eval([l1,l2,l3,l4,l5],["&","&","&","&"])
	except KeyboardInterrupt as e:
			print "Successful exit"
	except Exception as e:
			print e