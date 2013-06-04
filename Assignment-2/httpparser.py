import sys

def httpParser(message):




        try:
                parsedValue = ''
                splitMessage = message.split()

                for i in splitMessage:
                        if i.upper()=='GET':

                                parsedValue = splitMessage[(splitMessage.index(i))+1]
                                break
                        if (i.upper()=='POST')|(i.upper()=='DELETE')|(i.upper()=='PUT')|(i.upper()=='DELETE')|(i.upper()=='HEAD')|(i.upper()=='OPTIONS')|(i.upper()=='TRACE')| (i.upper()=='CONNECT'):
                                return 'UNSUPPORTED METHOD'
                return parsedValue

        except RuntimeError as e:

                print 'A RUNTIME ERROR HAS OCCURED: ',e


        return parsedValue



def computeFileName(absoluteFilePath):

        try:
                fileName = ''
                absoluteFilePath = list(absoluteFilePath)
                absoluteFilePath = absoluteFilePath[1:]
                fileName = ''.join(absoluteFilePath)


        except RuntimeError as e:

                print 'A RUNTIME ERROR HAS OCCURED: ',e

        return fileName


