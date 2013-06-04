from BeautifulSoup import *
from urllib2 import *
import re
class PhoneDetails():
    #variables related to the phone
    model = str()
    wifiString = str()
    secondaryCameraString = str()
    price = int()
    isTouchEnabled = bool()
    isNFCEnabled = bool()
    displayDensity = float()
    isMultiTouchEnabled = bool()
    displaySize = float()
    displaySizeString = str()
    touchString = str()
    multiTouchString = str()
    secondaryCameraResolution = float()
    secondaryCamera = bool()
    primaryCameraString = str()
    primaryCameraResolution = str()
    primaryCamera = bool()
    dimensions = str()
    talktimeString = str()
    operatingSystem = str()
    
    is3GEnabled = bool()
    isWifiEnabled = bool()
    #2G and 3G talktimes
    talktime_3g = float()
    talktime_2g = float()
    height = float()
    width = float()
    length = float()
    
    #internal class variables
    page = str()
    
    def __init__(self, url):#not completed
        self.model = "N/A"
        self.wifiString = "N/A"
        self.secondaryCamera = False
        self.isTouchEnabled = False
        self.isMultiTouchEnabled = False
        self.isNFCEnabled = False
        self.displayDensity = -1
        self.multiTouchString = "N/A"
        self.touchString = "N/A"
        self.displaySizeString = "N/A"
        self.price = -1 
        self.displaySize = -1
        self.secondaryCameraResolution = -1
        self.secondaryCameraString = "N/A" 
        self.primaryCamera = False
        self.primaryCameraResolution = -1
        self.primaryCameraString = "N/A" 
        self.operatingSystem = "N/A"
        self.talktime_3g = -1   #-1 refers to details not available
        self.talktime_2g = -1
        self.dimensions = "N/A"
        self.is3GEnabled = False
        #-1 as the dimension indicates that it is currently not available
        self.isWifiEnabled = False
        self.height = -1
        self.width = -1
        self.length = -1
        request = Request(url)
        response = urlopen(request)
        src = response.read()
        self.page = BeautifulSoup(src)     
    def findOperatingSystem(self):#completed
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == "os" or (i.td.a.string.lower() == "operating system") :
                    self.operatingSystem = str(i.findAll('td')[1].string)
                    break        
            except Exception:
                pass
    def findModel(self):#completed
        try:
            self.model = str(self.page.h1.string)
        except Exception as e:
            print e
    def findPrimaryCamera(self):#completed
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == "primary" or (i.td.a.string.lower() == "primary camera") :
                    self.primaryCameraString = str(i.findAll('td')[1]).lower()
                    k = re.findall('("none")|("no")', self.primaryCameraString)
                    if k == []:
                        self.primaryCamera = True
                        l = re.findall('vga',self.primaryCameraString)
                        if l != []:
                            self.primaryCameraResolution = 0.5
                        else:
                            l = re.findall('((\d+(\.\d+)*)\s(mp|megapixel|mega pixel))', self.primaryCameraString)
                            if l != []:
                                self.primaryCameraResolution = float(l[0][1])
                    break                  
            except Exception as e:
                pass
   

        
    def findSecondaryCamera(self):#completed
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == "secondary" or (i.td.a.string.lower() == "secondary camera") :
                    self.secondaryCameraString = i.findAll('td')[1].string.lower()
                    k = re.findall('("none")|("no")', self.secondaryCameraString)
                    if k == []:
                        self.secondaryCamera = True
                        l = re.findall('vga',self.secondaryCameraString)
                        if l != []:
                            self.secondaryCameraResolution = 0.5
                        else:
                            l = re.findall('((\d+(\.\d+)*)\s(mp|megapixel|mega pixel))', self.secondaryCameraString)
                            if l != []:
                                self.secondaryCameraResolution = float(l[0][1])
                    break                  
            except Exception:
                pass
    def is3GEnabledf(self):
        if self.talktime_3g != -1:
            self.is3GEnabled = True   
            
   
    def isWifiEnabledf(self):
        tr = self.page.findAll('tr')
        for i in tr:
            try:                
                if i.td.a.string.lower() == "wlan" or (i.td.a.string.lower() == "w-lan"):
                    self.wifiString =  i.findAll('td')[1].string.lower()
                    k = re.findall('(wifi|wi-fi)',self.wifiString)
                    if k != []:
                        self.isWifiEnabled = True          
            except Exception as e:
                pass
   
    def isTouchEnabledf(self):
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == 'type':
                    self.touchString = str(i.findAll('td')[1]).lower()
                    k = re.findall('touch',self.touchString)
                    if k != []:
                        self.isTouchEnabled = True
                        break
            except Exception:
                pass   
               
    def isNFCEnabledf(self):
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == 'nfc':
                    if re.findall('yes',i.findAll('td')[1].string.lower()) != []:
                        self.isNFCEnabled = True
                        break
                    break
            except Exception:
                pass   
        
    def isMultiTouchEnabledf(self):
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == 'multitouch':
                    self.multiTouchString = str(i.findAll('td')[1].string).lower()
                    k = re.findall('yes',self.multiTouchString)
                    if k != []:
                        self.isMultiTouchEnabled = True
                        break
            except Exception:
                pass    
    def findAll(self):
        try:
            self.findModel()
            self.findDimensions()
            self.findOperatingSystem()
            self.findTalkTime()
            self.is3GEnabledf()
            self.isTouchEnabledf()
            self.findPrimaryCamera()   
            self.findSecondaryCamera()     
            self.isWifiEnabledf()
            self.findPrice()
            self.isMultiTouchEnabledf()
            self.findDisplaySize()
            self.findDisplayDensity()
            self.isNFCEnabledf()   
        except Exception as e:
            print e    
    def printAll(self):
        try:
            print "model = ", self.model
            print "wifi description =", self.wifiString 
            print "isWIFIEnabled = ", self.isWifiEnabled
            print "touchString = ", self.touchString
            print "isTouchEnabled = ", self.isTouchEnabled
            print "multiTouchString = ", self.multiTouchString 
            print "isMultiTouchEnabled = ", self.isMultiTouchEnabled
            print "isNFCEnabled = ", self.isNFCEnabled

            print "displaySizeString = ", self.displaySizeString
            print "display density in ppi = ", self.displayDensity
            print "displaySize in inches = ", self.displaySize
            print "approximate price in euros = ", self.price
            print "secondaryCameraString = ", self.secondaryCameraString
            print "Secondary camera = ",self.secondaryCamera
            print "secondary camera resolution in megapixel = ", self.secondaryCameraResolution
            print "isPrimaryCamera enabled = ", self.primaryCamera
            print "primary camera resolution in megapixel = ", self.primaryCameraResolution
            print "primaryCameraString = ", self.primaryCameraString 
            print "operatingSystem = ", self.operatingSystem
            print "is3GEnabled = ", self.is3GEnabled
            print "talktime_3g = ", self.talktime_3g
            print "talktime_2g = ", self.talktime_2g
            print "dimensions string = ", self.dimensions
            print "height = ", self.height
            print "width = ", self.width
            print "length = ", self.length
              
        except Exception as e:
            print e
    def findPrice(self):
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == 'price group' or (i.td.a.string.lower() == 'price'):
                    ls = i.findAll('td')[1].img['title']
                    k = re.findall('\d+',ls)
                    self.price = int(k[0])
            except Exception:
                pass   
    def findDisplaySize(self):
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == "size":
                    self.displaySizeString = str(i.findAll('td')[1].string).lower()
                    k = re.findall('(\d+(\.\d+)*) inches',self.displaySizeString)
                    if k != []:
                        self.displaySize = float(k[0][0])
                        break
            except Exception:
                pass           
    def findDisplayDensity(self):
        try:
            k = re.findall('(\d+(\.\d+)*)\sppi',self.displaySizeString)
            if len(k) != 0:
                self.displayDensity = float(k[0][0])
        except Exception as e:
            print e
    def findTalkTime(self):#completed
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == "talk time" or (i.td.a.string.lower() == "tt"):
                    ls = i.findAll('td')[1].string
                    self.talktimeString = ls
                    if ls != None:
                        ll = re.findall('(\d+\s[h])',ls)
                        if ll != []:
                            try:
                                k = re.findall('(\d+)',ll[0])
                                self.talktime_2g = int(k[0])
                                k = re.findall('(\d+)',ll[1])
                                self.talktime_3g = int(k[0])
                                break
                            except Exception:
                                break
                    else:
                        break
            except Exception:
                pass   
        
    def findDimensions(self):   #completed
        tr = self.page.findAll('tr')
        for i in tr:
            try:
                if i.td.a.string.lower() == "dimensions":
                    self.dimensions = i.findAll('td')[1].string
                    break                  
            except Exception:
                pass
        pattern = "(\d+(\.\d+)*)"
        dimList= re.findall(pattern, self.dimensions)
        if dimList != []:
            try:
                self.length = float(dimList[0][0])
                self.width = float(dimList[1][0])
                self.height = float(dimList[2][0])
            except Exception:
                pass    #Maybe the dimension string is not of the specified format
        else:
            self.dimensions = "N/A"

        
if __name__ == "__main__":
    try:
        url = "http://www.gsmarena.com/apple_iphone_4s-4212.php"    #to be accepted later from the command line
        phone = PhoneDetails(url)
        phone.findAll()
        phone.printAll()
    except URLError as e:
        print "Network unreachable or URL invalid, please check and try again"