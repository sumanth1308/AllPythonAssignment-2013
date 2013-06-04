import sys, traceback
global clst	
def createTable(fileName):
	"""Constructs an in memory database using the fileName provided"""
	try:

		fileHandler = open(fileName,"r")
		l = []
		d = {}
		global clst
		clst = []
		columnString = fileHandler.readline()
		clst+=columnString.split(",")
		clst[-1] = "".join(list(clst[-1])[:-1])
		for i in fileHandler:
			k = i.split(",")
			k[-1] = "".join(list(k[-1])[:-1])
			for m,j in zip(clst,k):
				d[m] = j
			l += [d]
			d = {}
		fileHandler.close()
		return l,clst
	except IOError as e:
			print "error: no such table found"
	except Exception as e:
			raise Exception("error: in table creation")

def printDatabaseAsList(dataBase):
		"""Prints database as a list of dictionaries"""
		print dataBase


def getClst(query,fileName):
		"""Stores the ColumnNames specified in the first row of the input file"""
		global clst		
		fileHandler = open(fileName,"r")
		clst = []
		columnString = fileHandler.readline()
		clst+=columnString.split(",")
		clst[-1] = "".join(list(clst[-1])[:-1])
		fileHandler.close()
def closeConnection(fileHandler):
		"""closes the database connection to an input file, although it is present in the memory"""
		fileHandler.close()

def printTable(a):
	"""Prints the result as a formatted table, accepts an input of a list of a list of dictionaries"""
	for key, value in a[0].iteritems():
		print  "%12s\t" %(key),
	print ''
	for i in range(len(a)):
		for key, value in a[i].iteritems():
			print "%12s\t" %(value),
		print ''

def printSchema(d):
	"""Prints the schema of a newly created table"""
	for i in d:	
		print i+"\t\t",
def printSelect(query,rs):
	"""Prints selected columns from the result set rs"""
	try:
		d = {}
		k = 0
		rsNew = []
		list1 = query.split("@")
		list2 = list1[2].split(",")
		for i in list2:
				k = list2.index(i) 
				list2[k] = i.strip()

		for i in list2:
			if i not in clst:
				raise Exception("ColumnName in select string not valid")

		for i in rs:
				for j in list2:
					d[j] = i[j]

				rsNew.append(d)
				d = {}
		return rsNew
	except Exception as e:
			print e
			raise Exception(e)
if __name__ == "__main__":
	try:
		print "KDB version 1.0, debugging mode"
		print "KDB> running query against test database"
		print "KDB> query = read db"
		
		l = createTable("db.txt")
		printDatabaseAsList(l)
	except Exception as e:
			print e
