#!/usr/bin/python
"""This module evalutes the query and is dependent on the following modules
	a. parser
	b. dictionary
	c. evalOpnd
	Query excecution starts from evaluateQuery(str query)
"""
import sys, traceback
import parser
import dictionary
import evalOpnd
import time

t_p = tuple()
prevTableName = str()
def evaluateQuery(query):
	#evaluates a query supplied as a string in the format specified in the readme file
	try:
		global t_p
		t = []
		tableName = ""
		fileName = ""
		global prevTableName
		columnList = []
		operatorList = []
		valueList = []
		rs = []
		tp = tuple()
		d = []
		tableName = parser.getTableName(query)
		dictionary.getClst(query,tableName+".txt")
		t = parser.getColumnName(query)
		
		if tableName != None:
			fileName = tableName+".txt"
			if t_p == () or prevTableName != tableName:
				prevTableName = tableName
				tp = dictionary.createTable(fileName)
				t_p = tp
			else:
				tp = t_p
			d = tp[0]
			if (t[1] != []) and (t[2] != []):
				columnList = t[0]
				operatorList = t[1]
				valueList = t[2]
				if parser.read == True and parser.select == False:
						rs = read(tableName, columnList, operatorList, valueList,d)
						rs = evalOpnd.eval(rs,query)
						if rs != []:
							dictionary.printTable(rs)
							return rs
						else:
							raise Exception("Null set")
				elif parser.read == True and parser.select == True:
						rs = read(tableName, columnList, operatorList, valueList,d)
						rs = evalOpnd.eval(rs,query)
						if rs != []:
							dictionary.printSelect(query,rs)
							return rs
						else:
							raise Exception("Null set")

				elif parser.write == True:
						write(tableName, columnList, operatorList, valueList,d,tp[1])
				
				elif parser.delete == True:
						delete(tableName, columnList, operatorList, valueList,d,tp[1])
						
			elif parser.write == False and parser.delete == False:
				if d != []:
					dictionary.printTable(evalOpnd.eliminateDuplicate(d))
				else:
					print "New table created\n------------------"
					dictionary.printSchema(tp[1])

			else:
				raise Exception("error: Invalid syntax for (write|delete)")

	except IOError as e:
			print "error: No such table found"
			exceptionFileHandler = open("exceptionLog.txt","a")
			exceptionFileHandler.write(time.asctime()+","+str(e)+"\n")	#fatal exception being printed to a separate file
			exceptionFileHandler.close()
	except Exception as e:
			print e
			exceptionFileHandler = open("exceptionLog.txt","a")
			exceptionFileHandler.write(time.asctime()+","+str(e)+"\n")	#fatal exception being printed to a separate file
			exceptionFileHandler.close()


def read(tableName, columnList, operatorList, valueList,d):
	"""reads the specified datasets from the database
        read<space><tablename>
        """
	try:	
				resultSet = []
				rs = []
				for i,j,k in zip(columnList, operatorList, valueList):
					for l in d:
						if j == ">=":
							try:
								if float(l[i]) >= float(k):
									resultSet += [l.copy()]
							except ValueError:
								print "error: incompatible operand types"
								break
						elif j == "<=":
							try:
								if float(l[i]) <= float(k):
									resultSet += [l.copy()]
							except ValueError as e:
								print "error: incompatible operand types"
								break
						elif j == "~=":
							try:
								if float(l[i])	!= float(k):
									resultSet += [l.copy()]			
							except ValueError:
								if l[i].lower() != k.lower():
									resultSet += [l.copy()]
									
						elif j == ">":
							try:
								if float(l[i]) > float(k):
									resultSet += [l.copy()]
							except ValueError:
								print "error: incompatible operand types"		
								break			
						elif j == "<":
							try:
								if float(l[i]) < float(k):
									resultSet += [l.copy()]	
							except ValueError:
								print "error: incompatible operand types"			
								break
						elif j == "=":	
							try:
								if float(l[i])	== float(k):
									resultSet += [l.copy()]
							except ValueError:
								if l[i].lower() == k.lower():
									resultSet += [l.copy()]	
						else: 
							raise  parser.InvalidOperatorException ("ERROR: Operator not valid")
							
					rs.append(resultSet)
					resultSet = []
				if rs == [[]]:
					raise Exception("Null set")
   				return rs
   	except parser.InvalidOperatorException as e:
   			print e
   			exceptionFileHandler = open("exceptionLog.txt","a")
			exceptionFileHandler.write(time.asctime()+","+str(e))	#fatal exception being printed to a separate file
			exceptionFileHandler.close()
   	except KeyError as e:
   			print "error: Column not found", 
   			exceptionFileHandler = open("exceptionLog.txt","a")
			exceptionFileHandler.write(time.asctime()+","+str(e))	#fatal exception being printed to a separate file
			exceptionFileHandler.close()
   			raise Exception(", invalid column name\n")






def write(tableName, columnList, operatorList, valueList,d,clst):
	"""writes an entire row, specifying all the rows is mandatory"""
	try:
		if(len(columnList) == len(valueList) == len(clst)):
			tmp = {}
			for i in clst:
				tmp[i] = None

			for i,j in zip(columnList,valueList):
					tmp[i] = j
			d.append(tmp)
		else:
			raise Exception("Write error: enough columns not specified")
		#dictionary.printTable(d)	#switch on in debug mode
	except Exception as e:
		print e



def delete(tableName, columnList, operatorList, valueList,d,clst):
	"""deletes an entire row, specifying all the rows is mandatory"""
	try:
		if(len(columnList) == len(valueList) == len(clst)):
			tmp = {}
			for i in clst:
				tmp[i] = None

			for i,j in zip(columnList,valueList):
					tmp[i] = j
			d.remove(tmp)
		else:
			raise Exception("Delete error: enough columns not specified")
		#dictionary.printTable(d)	#switch on in debug mode
	except ValueError as e:
			print "error: The specified row doesn't exist"
	except Exception as e:
		print e


if __name__ == "__main__":
		
		try:
			c = 0

			print "KDB shell Version 1.0, debugging mode"
			while True:
				print "KDB>",
				query = raw_input()
				c = time.time()
				evaluateQuery(query)				
				print "\n\nQuery execution time: "+str(time.time() - c)+"s"
		except KeyboardInterrupt as e:
			print "\nSuccessful exit"
			exceptionFileHandler = open("exceptionLog.txt","a")
			exceptionFileHandler.write(time.asctime()+","+'Program terminated\n')	#fatal exception being printed to a separate file
			exceptionFileHandler.close()
		except Exception as e:
			exceptionFileHandler = open("exceptionLog.txt","a")
			exceptionFileHandler.write(time.asctime()+","+str(e)+"\n")	#fatal exception being printed to a separate file
			exceptionFileHandler.close()
			print "error: malformed or invalid query"	
