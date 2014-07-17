# -*- coding: utf-8 -*-
# extractDict4UI.py
'''
Created on 2011-3-15

@author: cnxc8360
'''

import os
# import re
import codecs
from subprocess import call
class ExtractDict(object):
    '''
    classdocs
    '''
    pass

    def __init__(self, enFile = None, zhFile = None, extractedFile = None, native2ascii_exe = None):
        '''
        Initiate enFile name and zhFile name. enFile and zhFile should be
        full file names with directory. Blank lines and comment lines
        (starts with "#") are ignored. 
        '''
        #        print "I'm here!"
        self.enFile = enFile
        self.zhFile = zhFile
        self.extractedFile = extractedFile
        self.native2ascii_exe = native2ascii_exe
        self.sortedListOfKeyValueEnZhDict = None
        self.sortedListOfExtractedDict = None
        self.sortedListOfEnDiffZhDict = None
        self.sortedListOfZhDiffEnDict = None
        
    def openAndRead(self,fName):
        '''
        Read "key1 = value1 \n, ...\n, keyN = valueN \n" format 
        dictionary(properties) file. fName should be
        full file names with directory.
        Parse the contents of properties file (i.e. enFile
        and zhFile) to form a list. Blank lines and comment lines
        (starts with "#") are ignored. 
        Return a list of [["key1","value1"],...,["keyi","valuei"]
        if fName is not a .properties file, i.e. it is not I18N ASCII file,
        translate it using Java native2ascii.exe 
        '''
        if os.path.isfile(fName) == False: return "Not a file name!"
#       parse absolute filename to path, name trunk and extension
        pathName,fileName = os.path.split(fName)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
#        if fName is not a .properties file, i.e. it is not I18N ASCII file,
#        translate it using Java native2ascii.exe 
#        create a file with a name of os.path.join(pathName,fileNameTrunk+fileNameExt)
        if fileNameExt.upper() != ".properties".upper():
            fName = self.unicode2Ascii(fName)
        try:
            f = codecs.open(fName,mode="r")
            try:
                fLns = f.readlines()
            finally:    
                f.close() 
            # parse DictLns to Python dict
            # delete all the elements that represent blank lines from the list 
            fLnsClean = [i for i in fLns if i!=u'\r\n']
            fLnsNoComment = [i.rstrip() for i in fLnsClean if i[0]!='#']
            # split ["key1=value1",...,"keyi=valuei"] list to 
            # [["key1","value1"],...,["keyi","valuei"] format 
            fList = [k.split("=") for k in fLnsNoComment]
            fList = [k for k in fList if len(k)==2]# make sure only one "=" in each line

            return fList
        except IOError:
            pass
        
    def unicode2Ascii(self,unicodeFileName):
        """
        Convert a file from native to I18N ASCII file with the same file
         name and a extension of .properties
        """
        if self.native2ascii_exe != None:
            native2ascii_Fun = self.native2ascii_exe
        else:
            if os.getenv("JAVA_HOME") != None:
                native2ascii_Fun = os.getenv("JAVA_HOME") + os.sep + "bin" + os.sep + "native2ascii.exe"
            else:
                native2ascii_Fun = os.getcwd() + os.sep + "native2ascii.exe"
                if os.path.isfile(native2ascii_Fun) == False:
                    native2ascii_Fun = "Returned because native2ascii_Fun is Not set!"
        pathName,fileName = os.path.split(unicodeFileName)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        asciiFileName = os.path.join(pathName,fileNameTrunk+".properties")
        call([native2ascii_Fun,unicodeFileName,asciiFileName])
        return asciiFileName
    def ascii2Unicode(self,asciiFileName):
        """
        Convert a file from I18N ASCII to  native file with the same file
         name and a extension of .txt
        """
        if self.native2ascii_exe != None:
            native2ascii_Fun = self.native2ascii_exe
        else:
            if os.getenv("JAVA_HOME") != None:
                native2ascii_Fun = os.getenv("JAVA_HOME") + os.sep + "bin" + os.sep + "native2ascii.exe"
            else:
                native2ascii_Fun = os.getcwd() + os.sep + "native2ascii.exe"
                if os.path.isfile(native2ascii_Fun) == False:
                    native2ascii_Fun = "Returned because native2ascii_Fun is Not set!"
        pathName,fileName = os.path.split(asciiFileName)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        unicodeFileName = os.path.join(pathName,fileNameTrunk+".txt")
        call([native2ascii_Fun,"-reverse",asciiFileName,unicodeFileName])
        return unicodeFileName
    
    def extractDict(self):
        if self.enFile == None or self.zhFile == None: 
            return "Two .properties files needed."
        enList = self.openAndRead(self.enFile)
        zhList = self.openAndRead(self.zhFile)
        
        # strip blanks and "\t\r\n" in all keys and values
        # and use keys and values to form dictionary
        enDict = dict([(k[0].strip(),k[1].strip()) for k in enList])
        zhDict = dict([(k[0].strip(),k[1].strip()) for k in zhList])
        # merge two dictionaries, keep only the common keys
        # in the form of {key1:[enVaule1,zhValue1], ..., keyN:[enValueN,zhValueN]}
        dicts = enDict,zhDict
        commonKeySet = set(enDict.keys()) & set(zhDict.keys())
        enDiffZhKeySet = set(enDict.keys()) - set(zhDict.keys())
        zhDiffEnKeySet = set(zhDict.keys()) - set(enDict.keys())
        
        dictKeyValueEnZh = dict((k,[d.get(k) for d in dicts]) for k in commonKeySet)
        enDiffZhDict = dict((k,enDict[k]) for k in enDiffZhKeySet)
        zhDiffEnDict = dict((k,zhDict[k]) for k in zhDiffEnKeySet)
        # make a dictionary with only values use English words as keys
        # and eliminate duplicated keys
        listValueEnZh = dictKeyValueEnZh.values()
        dictValueEnZh = dict(listValueEnZh)
        # Clean nonsense pairs in dict, i.e. keep only translated pairs
        dictKeyValueEnZhCleaned = dict([[k,v] for k,v in \
                                   dictKeyValueEnZh.items() if v[0]!=v[1]])
        dictValueEnZhCleaned = dict([k for k in dictValueEnZh.items() if k[0]!=k[1]])
        # sort dictionaries by keys
        self.sortedListOfKeyValueEnZhDict = sorted(dictKeyValueEnZhCleaned.items(),key = lambda x:x[0])
        self.sortedListOfExtractedDict = sorted(dictValueEnZhCleaned.items(), key = lambda x:x[0])
        self.sortedListOfEnDiffZhDict = sorted(enDiffZhDict.items(), key = lambda x:x[0])
        self.sortedListOfZhDiffEnDict = sorted(zhDiffEnDict.items(), key = lambda x:x[0])
        
    def writeExtractedDict(self,fName=None, fName4UI=None):
        if fName == None: fName = self.enFile
        if os.path.isfile(fName) == False: return "Not a file name!"
        if fName4UI == None: fName4UI = self.extractedFile
#       parse absolute filename to path, name trunk and extension
        pathName,fileName = os.path.split(fName)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        extractedDictFileName = os.path.join(pathName,fileNameTrunk+"_ExtractedDict.properties")
        keyValueEnZhDictFileName = os.path.join(pathName,fileNameTrunk+"_KeyValueEnZhDict.properties")
        EnDiffZhFileName = os.path.join(pathName,fileNameTrunk+"_EnDiffZh.properties")
        ZhDiffEnFileName = os.path.join(pathName,fileNameTrunk+"_ZhDiffEn.properties")
            
#       if sorted list of updated dict is exist, write it in "keyi = valuei" format  
        if self.sortedListOfKeyValueEnZhDict != None:
            f = codecs.open(keyValueEnZhDictFileName,mode="w")
            for i in self.sortedListOfKeyValueEnZhDict:
                f.write(i[0]+'\t = \t'+i[1][0]+','+i[1][1]+'\n')
            f.close()       
        self.ascii2Unicode(keyValueEnZhDictFileName)
        
        if self.sortedListOfExtractedDict != None:
            f = codecs.open(extractedDictFileName,mode="w")
            if fName4UI != None:
                f4UI = codecs.open(fName4UI,mode="w")
            for i in self.sortedListOfExtractedDict:
                f.write(i[0]+'\t = \t'+i[1]+'\n')
                if fName4UI != None:
                    f4UI.write(i[0]+'\t = \t'+i[1]+'\n')
            f.close()       
            if fName4UI != None:
                f4UI.close()
        self.ascii2Unicode(extractedDictFileName)
        
        if self.sortedListOfEnDiffZhDict != None:
            f = codecs.open(EnDiffZhFileName,mode="w")
            for i in self.sortedListOfEnDiffZhDict:
                f.write(i[0]+'\t = \t'+i[1]+'\n')
            f.close()
        if self.sortedListOfZhDiffEnDict != None:
            f = codecs.open(ZhDiffEnFileName,mode="w")
            for i in self.sortedListOfZhDiffEnDict:
                f.write(i[0]+'\t = \t'+i[1]+'\n')
            f.close()
        self.ascii2Unicode(ZhDiffEnFileName)
        if fName4UI != None:
            return fName4UI
        else:
            return extractedDictFileName
        
def test(enFile = None, zhFile = None):
    extractDict = ExtractDict(enFile,zhFile)
    extractDict.extractDict()
    extractDict.writeExtractedDict()
    
if __name__ == "__main__":
    # #file and directories to be deal with
#    print "I'm here!"
    fPath = "D:\\workspace\\Python27\\myfirstpython\\files\\ApplicationResources"
    # English and Chinese properties file used to prepare for extracting dictionary
    fEnFile = os.path.join(fPath,"ApplicationResources.properties")
    fZhFile = os.path.join(fPath,"ApplicationResources_zh.properties")
    test(fEnFile,fZhFile)
    
    
    

        
        
        