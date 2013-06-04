#! /usr/bin/python
try:
 import threading
 import httpparser  #user defined httpparser 
 import sys
 import argparse
 import time
 import dev_db
 import pickle
 from socket import *
except ImportError as e:
        print 'ERROR IN IMPORTING PYTHON LIBRARIES: ',e




#IncompatibleFileType exception class
class IncompatibleFileTypeException(Exception):
        value = ''
        def __init__(self,value):
                self.value = value
        def __str__(self):
                return repr(self.value)


#class to implement client threads
class clientConnectionSocket(threading.Thread):
 def __init__(self,clientaddr):
  threading.Thread.__init__(self)
  self.clientaddr = clientaddr
 def run(self):
    try:
           exceptionFileHandler = open("exceptionLog.txt","a")
           connectionLog = open("connectionLog.txt","a")
           clientSocket = connectionSocket
           message = clientSocket.recv(512)
           httpResponse = ''
           fileContents = ''
           #parse the http message      
           message = message.strip("\n")
           print "query = ",message
           rString = dev_db.evaluateQuery(message,self.clientaddr)
           rString = pickle.dumps(rString)
           clientSocket.send(rString)


    except IOError as e:
           exceptionFileHandler.write('File not found to load a table from, server terminating'+str(time.ctime())+"\n")
           clientSocket.send('File not found to load a table from, server terminating'+time.ctime())


    except IncompatibleFileTypeException as e:
           exceptionFileHandler.write(str(e.value)+"\n")
           clientSocket.send(e.value)

           

    clientSocket.close()
    connectionLog.write('TCP connection to:'+str(self.clientaddr)+'closed'+str(time.ctime())+"\n")
    print 'TCP connection to:',self.clientaddr,'closed', time.ctime()



 #serverPort = 12345
def parseArg(): 
 try:
     parser = argparse.ArgumentParser()
     global serverPort
     global serverName
     parser.add_argument('-p', action='store',dest='serverPort',type=int,default=12345,help="Port number to be used by the server")
     parser.add_argument('-n', action='store',dest='serverName',type=str,default="",help="Name or IPv4 address to be used by the server")
     results = parser.parse_args()
     if results.serverPort:
      serverPort = int(results.serverPort)
     if results.serverName:
      serverName = results.serverName


     if serverPort < 1024 or serverPort > 65355:
      raise ValueError("port No should be a value between 1024 to 65355")
 except ValueError:
   printstr(str(e))
   sys.exit(0)
 except IOError, msg:
   parser.error(str(msg))





try:
 serverPort = 12345
 serverName = ''
 parseArg()
 exceptionFileHandler = open("exceptionLog.txt","a")
 connectionLog = open("connectionLog.txt","a")
 serverSocket = socket(AF_INET, SOCK_STREAM)
 serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
 serverSocket.bind((serverName, serverPort))
 #listen for incoming connections on the serverSocket
 serverSocket.listen(5)

 #cmdline

 print "Server Process started", time.ctime()
 connectionLog.write("Server Process started"+time.ctime()+"\n")
 print 'SERVER READY TO RECIEVE DATA:\n-------------------------------------'
 print 'SERVER CONSOLE:\n-------------------------------------'
 threads = []
 while 1:
        #create client thread if there is an incoming client request
        connectionSocket, clientAddress = serverSocket.accept()
        print "TCP connection to:",clientAddress,"active", time.ctime()
        connectionLog.write("TCP connection to:"+str(clientAddress)+"active"+str(time.ctime())+"\n")
        #connectionLog
        

        clientThread = clientConnectionSocket(clientAddress)
        threads.append(clientThread)
        clientThread.start()

        #NOTE:server should be terminated using a keyboard interrupt
except (error,timeout) as e:           #socket.error and socket.timeout
        exceptionFileHandler.write('A SOCKET ERROR HAS OCCURED \n'+ str(e)+"\n")
        print 'A SOCKET ERROR HAS OCCURED \n', e
        exceptionFileHandler.close()
        connectionLog.close()
    
except IOError as e:
        exceptionFileHandler.write('INPUT/OUTPUT ERROR \n'+ str(e)+"\n")
        print 'INPUT/OUTPUT ERROR \n',e
        exceptionFileHandler.close()
        connectionLog.close()
        
except KeyboardInterrupt as e:
  #connection log
        connectionLog.write("Server process terminated "+ str(time.ctime())+"\n")
        print "Server process terminated ", time.ctime()
        print "Waiting for the remainging threads to join"
        #This code was added after the evaluation
        for t in threads:
          t.join()
        exceptionFileHandler.close()
        connectionLog.close()
    

