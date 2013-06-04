#!/usr/bin/python 
"""This module is not intended to be exposed to the user"""
import traceback
import dictionary
class MalformedQueryException(Exception):
        value = ''
        def __init__(self,value):
                self.value = value
        def __str__(self):
                return repr(self.value)



class InvalidOperatorException(Exception):
        value = ''
        def __init__(self,value):
                self.value = value
        def __str__(self):
                return repr(self.value)

global select
def getTableName(query):
	try:

	 	tableName = ""
		global read 
		global write
		global delete
		tableName = ""
		read = False
		write = False
		list1 = []
		list2 = []
		list1 = list1 + query.split("@")	
		list2 = list1[0].split()
		if(len(list2) != 2):
				raise MalformedQueryException("error: '(read|write|delete)' or tableName not specified")
		else:
			if(list2[0] == "read"):
				read = True
				write = False
				delete = False
			elif(list2[0] == "write"):
				read =False
				write = True
				delete = False
			elif(list2[0] == "delete"):
				read = False
				write = False
				delete = True
			else:
				raise MalformedQueryException("error: Invalid operation, only (read|write|delete) permitted")
		tableName = list2[1]

		return tableName
	except MalformedQueryException as e:
			print e
			raise Exception("")

	except KeyboardInterrupt as e:
			print "Sucessful exit"
	except Exception as e:
			print e

def getColumnName(query):
	try:
		k = []		
		list1 = []
		list2 = []
		list3 = []
		list4 = []
		columnList = []
		operatorList = []
		valueList = [] 
		global select
		list1 = query.split("@")
		if len(list1) == 2 or len(list1) == 3:
			if len(list1) == 3:
				select = True
			else:
				select = False

			list3 = list1[1].split("&")
			for i in list3:
				list4 = i.split("|")
				for j in list4:
					list2.append(j)

			for i in list2:
				if i.split(">=") != [i]:
					k = i.split(">=")
					print k,i.split(">=")
					columnList.append(k[0].strip())
					valueList.append(k[1].strip())
					operatorList.append(">=")	
				elif i.split("<=") != [i]:
					k=i.split("<=")
					columnList.append(k[0].strip())
					valueList.append(k[1].strip())
					operatorList.append("<=")	
				elif i.split("~=") != [i]:
					k=i.split("~=")
					columnList.append(k[0].strip())
					valueList.append(k[1].strip())
					operatorList.append("~=")	
				elif i.split(">") != [i]:
					k=i.split(">")
					columnList.append(k[0].strip())
					valueList.append(k[1].strip())
					operatorList.append(">")	
				elif i.split("<") != [i]:
					k=i.split("<")
					columnList.append(k[0].strip())
					valueList.append(k[1].strip())
					operatorList.append("<")	
				elif i.split("=") != [i]:
					k=i.split("=")
					columnList.append(k[0].strip())
					valueList.append(k[1].strip())
					operatorList.append("=")	
				else:	
					raise InvalidOperatorException("ERROR: Operator not valid!")
			return  [columnList,operatorList,valueList]
		else:

			return [dictionary.clst,[],[]]
		
	except InvalidOperatorException as e:
			print e,
			raise Exception(" or a missing operand/expression list, after & or | or @")
	except Exception as e:
			print "error: Malformed query"

if __name__ == "__main__":
		
		try:
			print "KDB shell Version 1.0, debugging mode"
			while True:
				print "KDB>",
				query = raw_input()
				print "Return value of getTableName(str query) = "+getTableName(query)
				print "Return value of getColumnName(str query) = ",getColumnName(query)
		except KeyboardInterrupt as e:
				print "Successful exit"
		except Exception as e:
			print e
