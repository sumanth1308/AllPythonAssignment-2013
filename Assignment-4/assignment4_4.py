from assignment4_3 import *
import argparse
import sys
import time
from Orange import orange
import urllib2
global fileName
global trainingFlag
global currentPhoneRating
global f
global fileHandler
global mFileHandler
global f2
global f3
def parseArg():
    try:
        global fileName 
        fileName = ''
        global trainingFlag
        parser = argparse.ArgumentParser()
        trainingFlag = False
        parser.add_argument('-f', action='store',dest='file',type=str,default="long_list.txt",help="File containing list of urls")
        parser.add_argument('-t', action='store_true',dest='train',help="toggle training mode, defaults to False")
        results = parser.parse_args()
        if results.file:
            fileName = results.file
        else:
            raise Exception("error: input file argument is missing")
        if results.train:
            trainingFlag = results.train
    except Exception as e:
        print e
        sys.exit(0)
def makeExampleTabbedFile(phone):
    #wifi 1    touch .5    multi_touch 1    nfc 1    display_density 2   display_size 1    primary_camera    primary_camera_resolution 1   secondary_camera    secondary_camera_resolution 0.5    tt_3g 2   tt_2g    model
    #The headers of the file are already prepared
    global currentPhoneRating
    global fileHandler
    global f2
    global mFileHandler
    global f3
    s = ""
    if currentPhoneRating < 3:
        s = "low"
    elif currentPhoneRating < 7:
        s = "mid"
    else:
        s = "high"
    if trainingFlag:
        fileHandler.write(str(phone.isWifiEnabled)+"\t"+str(phone.isTouchEnabled)+"\t"+str(phone.isMultiTouchEnabled)+"\t"+str(phone.isNFCEnabled)+"\t"+str(phone.displayDensity)+"\t"+str(phone.displaySize)+"\t"+str(phone.primaryCamera)+"\t"+str(phone.primaryCameraResolution)+"\t"+str(phone.secondaryCamera)+"\t"+str(phone.secondaryCameraResolution)+"\t"+str(phone.talktime_3g)+"\t"+str(phone.talktime_2g)+"\t"+str(s)+"\n")
        f2.write(str(phone.isWifiEnabled)+"\t"+str(phone.isTouchEnabled)+"\t"+str(phone.isMultiTouchEnabled)+"\t"+str(phone.isNFCEnabled)+"\t"+str(phone.displayDensity)+"\t"+str(phone.displaySize)+"\t"+str(phone.primaryCamera)+"\t"+str(phone.primaryCameraResolution)+"\t"+str(phone.secondaryCamera)+"\t"+str(phone.secondaryCameraResolution)+"\t"+str(phone.talktime_3g)+"\t"+str(phone.talktime_2g)+"\t"+str(phone.price)+"\n")
    else:

        mFileHandler.write(str(phone.isWifiEnabled)+"\t"+str(phone.isTouchEnabled)+"\t"+str(phone.isMultiTouchEnabled)+"\t"+str(phone.isNFCEnabled)+"\t"+str(phone.displayDensity)+"\t"+str(phone.displaySize)+"\t"+str(phone.primaryCamera)+"\t"+str(phone.primaryCameraResolution)+"\t"+str(phone.secondaryCamera)+"\t"+str(phone.secondaryCameraResolution)+"\t"+str(phone.talktime_3g)+"\t"+str(phone.talktime_2g)+"\n")        
        f3.write(str(phone.isWifiEnabled)+"\t"+str(phone.isTouchEnabled)+"\t"+str(phone.isMultiTouchEnabled)+"\t"+str(phone.isNFCEnabled)+"\t"+str(phone.displayDensity)+"\t"+str(phone.displaySize)+"\t"+str(phone.primaryCamera)+"\t"+str(phone.primaryCameraResolution)+"\t"+str(phone.secondaryCamera)+"\t"+str(phone.secondaryCameraResolution)+"\t"+str(phone.talktime_3g)+"\t"+str(phone.talktime_2g)+"\n")        
def computeRating(phone):
    global currentPhoneRating
    currentPhoneRating = 0
    if phone.isWifiEnabled:
        currentPhoneRating += 1
    if phone.isTouchEnabled:
        currentPhoneRating += 0.5
    if phone.isMultiTouchEnabled:
        currentPhoneRating += 1
    if phone.isNFCEnabled:
        currentPhoneRating += 1
    if phone.displayDensity != -1:
        k = int(phone.displayDensity)/326   #326 pixels per inch is considered as the standard
        if k > 1:
            k = 1
        currentPhoneRating += k
    if phone.displaySize != -1:
        k = float(phone.displaySize)/4.0    #4.0 inches is considered as the appropriate display size
        if k > 1:
            k = 1
        currentPhoneRating += k
    if phone.primaryCameraResolution != -1:
        k = float(phone.primaryCameraResolution)/8  #an 8 mega pixel camera is considered as the standard
        if k > 1:
            k = 1
        currentPhoneRating += k
    if phone.secondaryCameraResolution != -1:
        k = float(phone.secondaryCameraResolution)/1    #a 1 mega pixel secondart camera is considered to the standard
        if k > 1:
            k = 1
        currentPhoneRating += k
    if phone.talktime_3g != -1:
        k = float(phone.talktime_3g)/8      #a hrs of 3g talktime is the standard
        if k > 1:
            k = 1
        currentPhoneRating += k        
if __name__ == "__main__":  
    parseArg()
    try:
        pList = []
        f = open(fileName,"r")
        if trainingFlag:
            z = open("Log.txt","a")
            z.write("Training started at time:"+time.ctime()+"\n")
            z.close()
            fileHandler = open("exampleTable.tab","a")
            f2 = open("exampleCost.tab","a")
        else:
            z = open("Log.txt","a")
            z.write("Analysis started at time:"+time.ctime()+"\n")
            z.close()            
            mFileHandler = open("one.tab","w")
            f3 = open("two.tab","w")
            mFileHandler.write("wifi\ttouch\tmulti_touch\tnfc\tdisplay_density\tdisplay_size\tprimary_camera\tprimary_camera_resolution\tsecondary_camera\tsecondary_camera_resolution\ttt_3g\ttt_2g\tclassification\ndiscrete\tdiscrete\tdiscrete\tdiscrete\tcontinuous\tcontinuous\tdiscrete\tcontinuous\tdiscrete\tcontinuous\tcontinuous\tcontinuous\tdiscrete\n\t\t\t\t\t\t\t\t\t\t\t\tclass\n")
            f3.write("wifi\ttouch\tmulti_touch\tnfc\tdisplay_density\tdisplay_size\tprimary_camera\tprimary_camera_resolution\tsecondary_camera\tsecondary_camera_resolution\ttt_3g\ttt_2g\tclassification\ndiscrete\tdiscrete\tdiscrete\tdiscrete\tcontinuous\tcontinuous\tdiscrete\tcontinuous\tdiscrete\tcontinuous\tcontinuous\tcontinuous\tdiscrete\n\t\t\t\t\t\t\t\t\t\t\t\tclass\n")
        for i in f.readlines():
                phone = PhoneDetails(i)
                phone.findAll()
                pList.append(phone)
                computeRating(phone)
                #print phone.model, " rating computed = ", currentPhoneRating
                makeExampleTabbedFile(phone)
                print "processed url = ", i
        f.close()
        if trainingFlag: 
            fileHandler.close() 
            f2.close()
            z = open("Log.txt","a")
            z.write("Training completed at time:"+time.ctime()+"\n")
            z.close()
            print "Training set generated, re-run program to test it"
        else:
            mFileHandler.close()
            f3.close()
            print "Input file generated"
            data = orange.ExampleTable(r'exampleTable.tab')
            classifier = orange.BayesLearner(data)
            data = orange.ExampleTable(r'one.tab')
            data_1 = orange.ExampleTable(r'exampleCost.tab')
            classifier_1 = orange.BayesLearner(data_1)
            data_1 = orange.ExampleTable(r'two.tab')
            for i in range(len(data)):
                c = classifier(data[i])
                c_1 = classifier_1(data_1[i])
                print pList[i].model,"{", 
                for l,j in zip(data.domain.attributes, data[i]):
                    print l.name,":",j,",",
                print "} classified as", c , "\n projected cost = ",c_1, "euros"
            z = open("Log.txt","a")
            z.write("Analysis completed at time:"+time.ctime()+"\n")
            z.close()        

    except urllib2.URLError as e:
        z = open("Log.txt","a")
        z.write("Program terminated at time:"+time.ctime()+"due to:"+str(e)+"\n")
        z.close()
        print "Not connected to a network or entered an invalid url name, please try again"
    except KeyboardInterrupt as e:
        z = open("Log.txt","a")
        z.write("Program terminated at time:"+time.ctime()+"due to: KeyboardInterrupt\n")
        z.close()        
        print "successfull exit"
    except IOError as e:
        z = open("Log.txt","a")
        z.write("Program terminated at time:"+time.ctime()+"due to:"+str(e)+"\n")
        z.close()
        print "The file probably doesn't exist"
    except Exception as e:
        #f.close()
        #fileHandler.close()
        z = open("Log.txt","a")
        z.write("Program terminated at time:"+time.ctime()+"due to:"+str(e)+"\n")
        z.close()
        print "Unknown exception ",e
