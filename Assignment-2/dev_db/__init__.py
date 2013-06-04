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
clientAddr=''
t_p = tuple()
prevTableName = str("/")	#starts with a junk	previousTableName
def evaluateQuery(query,cltAddr):#sumanth
	#evaluates a query supplied as a string in the format specified in the readme file
	try:
		global t_p
		global sFlag
		global clientAddr
		clientAddr = cltAddr
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
		exceptionFileHandler = open("exceptionLog.txt","a")	
		tableName = parser.getTableName(query)
		dictionary.getClst(query,"dev_db_tables/"+tableName+".txt")
		t = parser.getColumnName(query)
		
		if tableName != None:
			fileName = "dev_db_tables/"+tableName+".txt"
			if t_p == () or prevTableName != tableName:
				prevTableName = tableName
				tp = dictionary.createTable(fileName)
				t_p = tp
				sFlag = True
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
							rs = dictionary.printSelect(query,rs)
							dictionary.printTable(rs)
							return rs
						else:
							raise Exception("Null set")

				elif parser.write == True:
						ret = write(tableName, columnList, operatorList, valueList,d,tp[1])
						if ret:
							return ret
				
				elif parser.delete == True:
						delete(tableName, columnList, operatorList, valueList,d,tp[1])
						
			elif parser.write == False and parser.delete == False:
				if d != []:
					d = evalOpnd.eliminateDuplicate(d)
					dictionary.printTable(d)
					return d
				elif sFlag == False:
					dictionary.printSchema(tp[1])
				elif sFlag == True:
					print "New table created\n------------------"
					dictionary.printSchema(tp[1])
					sFlag = False
			else:
				raise Exception("error: Invalid syntax for (write|delete)")

	except IOError as e:
			exceptionFileHandler.write(time.ctime()+",FROM = "+str(clientAddr)+","+"query = "+query+",\t"+tableName+".txt: no such file found to load the table from\n")
			print "error: No such table found"
			return 'error: No such table found'
	except Exception as e:
			exceptionFileHandler.write(time.ctime()+",FROM = "+str(clientAddr)+","+"query = "+query+",\t"+str(e)+"\n")
			print e
			return str(e)



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
								return "error: incompatible operand types"
								break
						elif j == "<=":
							try:
								if float(l[i]) <= float(k):
									resultSet += [l.copy()]
							except ValueError as e:
								print "error: incompatible operand types"
								return "error: incompatible operand types"
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
								return "error: incompatible operand types"
								break			
						elif j == "<":
							try:
								if float(l[i]) < float(k):
									resultSet += [l.copy()]	
							except ValueError:
								print "error: incompatible operand types"			
								return "error: incompatible operand types"
								break
						elif j == "=":	
							try:
								if float(l[i])	== float(k):
									resultSet += [l.copy()]
							except ValueError:
								if l[i].lower() == k.lower():
									resultSet += [l.copy()]	
						else: 
							raise  parser.InvalidOperatorException ("error: Operator not valid")
							
					rs.append(resultSet)
					resultSet = []
				if rs == [[]]:
					raise Exception("Null set")
					
   				return rs
   	except parser.InvalidOperatorException as e:
   			print e
   			return str(e)
   	except KeyError as e:
   			print "error: Column not found", 
   			return "error: Column not found"
   			raise Exception(", invalid column name")






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
			return "Successfully written 1 ROW"
		else:
			raise Exception("Write error: enough columns not specified")
		#dictionary.printTable(d)	#switch on in debug mode
	except Exception as e:
		exceptionFileHandler.write(time.ctime()+",FROM = "+str(clientAddr)+","+str(e)+"\n")	
		print e
		return str(e)



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
			return "error: The specified row doesn't exist"
	except Exception as e:
		exceptionFileHandler.write(time.ctime()+",FROM = "+str(clientAddr)+","+str(e)+"\n")	
		print e
		return str(e)


if __name__ == "__main__":
		
		try:
			c = 0
			query = ""
			exceptionFileHandler = open("exceptionLog.txt","a")		
			exceptionFileHandler.write(time.ctime()+",FROM = "+str(clientAddr)+","+"Connection established\n")
			print "KDB shell Version 1.0, debugging mode"
			while True:
				print "KDB>",
				query = raw_input()
				c = time.time()
				evaluateQuery(query)				
				print "\n\nQuery execution time: "+str(time.time() - c)+"s"
		except KeyboardInterrupt as e:
			print "\nSuccessful exit"
			exceptionFileHandler.write(time.ctime()+",FROM = "+str(clientAddr)+","+"Sucessful exit\n")
			exceptionFileHandler.close()
		except Exception as e:
			exceptionFileHandler.write(time.ctime()+",FROM = "+str(clientAddr)+","+"query = "+query+",\t"+"Fatal exception:"+str(e)+"\n")	#fatal exception being printed to a file
			exceptionFileHandler.close()
			print "error: malformed or invalid query"	
