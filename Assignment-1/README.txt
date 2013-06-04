K-DataBase, version 1.0 beta
-------------------------------------------------------------------------------------------------------------------------------

It is advised that you read this before you fork or make use of the code in this repository in any form.
The code consists of a light weight in-memory database server written in python supporting - 
a. Read 
b. Delete
c. Write
Operations.
Note: Creation of a database table also works if the schema is specified in the input file without any records 
-------------------------------------------------------------------------------------------------------------------------------

Usage:
--------------------
1. Input file syntax: 

a. mandatory first line containing the schema(containing only the column names), ex: column1, column2, column3..... 
b. Optional record lines, each containing the same no. of comma separated values as specified in the schema row
c. The input file must contain an empty new line in as the very last record
d. The extension the input file must be .txt
ex: db.txt and k.txt included in the package
e. The input file must be present in the same directory as __init__.py, else the fully qualified path name must be specified
2. Interactive shell session:

a. query syntax:


(read|write|delete) <tableName>[@<expressionList>[@<columnList>]]

tableName - Input file name without the extension
expressionList - columnName <relop> Value [(& or |) columnName <relop> Value [expressionList]]
columnName - Any valid columnName that a record can have as specified in the schema, column names are case sensitive
Value - Any value that a field of a record can take
relops supported:
greater than				>
lesser than 				<
equal to 					=
greater than or equal to	>=
less than or equal to		<=
not equal to 				~=
<columnList> - specifies the list of columns that must be printed in the result set
examples:
read <tableName>				lists all records of the entire table

NOTE: 
a. write and delete require that all the column names be specified in the expresssion list, all the values after the second @ will be ignored.
b. The ~= operator treats the RHS as a string and establishes inequality between two strings, and hence is to be used with caution


b. exit using control + c

APIs exposed:
-------------------
module name: dev_db
method name: dev_db.evaluateQuery(query) - evaluates the query specified as a string



Important Information:
-----------------------
a. The server only maintains an in memory database
b. The creators of KDB are not responsible in anyway whatsoever for any accidental/intentional damage caused, and hence comes with NO WARRANTY