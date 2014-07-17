# -*- coding: utf-8 -*-
# translateByDict4UI.py
'''
Created on 2011-3-16
Modified on 2012-11-16, create untranslated files in key=value format
@author: cnxc8360
'''

import os
# import re
import codecs
from subprocess import call
import time

class TranslateByDict(object):
    '''
    classdocs
    '''
    pass

    def __init__(self, enFile2Trans = None, enZhDictFile = None, targetZhFileName = None, native2ascii_exe = None):
        '''
        Initiate enFile name and enZhDictFile name. enFile and enZhDictFile should be
        full file names with directory. Blank lines and comment lines
        (starts with "#") in dict file are ignored. 
        enFile2Trans is a .properties (I18N ASCII) file and 
        enZhDictFile is a .txt (Unicode) or .properties (I18N ASCII) file 
        '''
        #        print "I'm here!"
        self.enFile2Trans = enFile2Trans
        self.enZhDictFile = enZhDictFile
        self.targetZhFileName = targetZhFileName
        self.native2ascii_exe = native2ascii_exe
        self.fNameTransedI18N = None
        self.fNameUntransedI18N = None

        
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
    
    def openAndReadDictFile(self,fName):
        '''
        Read "key1 = value1 \n, ...\n, keyN = valueN \n" format 
        dictionary(properties) file. fName should be
        full file names with directory.
        Parse the contents of properties file (i.e. enFile
        and zhFile) to form a list. Blank lines and comment lines
        (starts with "#") are ignored. 
        Return a dict of {"key1":"value1",...,"keyi":"valuei"}
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
            fDict = dict([(k[0].strip(),k[1].strip()) for k in fList])
            return fDict
        except IOError:
            pass
        
    def openAndReadFile2Trans(self,fName):
        '''
        Read "key1 = value1 \n, ...\n, keyN = valueN \n" format 
        English(properties) file. fName should be
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
            return fLns
        except IOError:
            pass
    
    
    def translateByDictAndWrite(self):
        
        if self.enFile2Trans == None or self.enZhDictFile == None: 
            return "English file to be translated and dict file to be used are needed."
        if os.path.isfile(self.enFile2Trans) == False: return "self.enFile2Trans is not a file name!"
        enLns = self.openAndReadFile2Trans(self.enFile2Trans)
        enZhDict = self.openAndReadDictFile(self.enZhDictFile)


#       parse absolute filename to path, name trunk and extension
#        form result file names
        pathName,fileName = os.path.split(self.enFile2Trans)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        fNameTransedI18N = os.path.join(pathName,fileNameTrunk+"_Transed.properties")
        fNameUntransedI18N = os.path.join(pathName,fileNameTrunk+"_Untransed.properties")
        fNameUntransedDummyI18N = os.path.join(pathName,fileNameTrunk+"_UntransedDummy.properties")
        targetZhFileName = self.targetZhFileName
        # # open properties file to write traslation result
        fTransed = codecs.open(fNameTransedI18N,mode="w")
        fUntransed = codecs.open(fNameUntransedI18N,mode="w")
        fUntransedDummy = codecs.open(fNameUntransedDummyI18N,mode="w")
        if self.targetZhFileName != None:
            fTargetZhFile = codecs.open(targetZhFileName,mode="w")
#        translation infomation
        transInfoLn1 = "#This file is create by translateByDict.py.\n"
        transInfoLn2 = "#Date of translation is %s. Dict file used is %s.\n" % \
                        (time.strftime("%Y%m%d"), self.enZhDictFile)
        fTransed.write(transInfoLn1)
        fTransed.write(transInfoLn2)
        if self.targetZhFileName != None:
            fTargetZhFile.write(transInfoLn1)
            fTargetZhFile.write(transInfoLn2)
        lineUntransed = []
        lineUntransedDummy = []
        for line in enLns:
            if line.isspace() or line.startswith("#"):
        #        print "line is:" + line
                fTransed.write(line)
                if self.targetZhFileName != None:
                    fTargetZhFile.write(line)
            else: # line.find("=") != -1:
        #         split line by "="
        #        print "line is: " + line
                lineList = line.split("=")
#                print "lineList is: \n"
#                print lineList
                tryKey = lineList[1].strip()
                lineNew = line
                if enZhDict.has_key(tryKey):
        #            dicts has key, translate 
                    lineListNew = [lineList[0],lineList[1].replace(tryKey,enZhDict[tryKey])]
                    lineNew = "=".join(lineListNew)
                else:
        #            key can not be find in dicts, write to untranslated file
                    lineUntransed.append(tryKey+"\t=\t\n")
                    lineUntransedDummy.append(tryKey + "\t=\t" + tryKey + "\n")
                fTransed.write("#:-#" + line)
                fTransed.write(lineNew)
                if self.targetZhFileName != None:
                    #fTargetZhFile.write("#:-#" + line)
                    fTargetZhFile.write(lineNew)
        #            print "line is:" + line
        #            print "new line is:" + lineNew
        
        fTransed.close()
        if self.targetZhFileName != None:
                    fTargetZhFile.close()
        # remove duplicates from the list
        lineUntransed = list(set(lineUntransed))
        lineUntransed.sort()
        for i in lineUntransed: fUntransed.write(i)
        
        # remove duplicates from dummy untranslated En-to-En pairs
        lineUntransedDummy = list(set(lineUntransedDummy))
        lineUntransedDummy.sort()
        for i in lineUntransedDummy: fUntransedDummy.write(i)
        
        fUntransed.close()
        fUntransedDummy.close()
        
        self.ascii2Unicode(fNameTransedI18N)
        
        if self.targetZhFileName != None:
            return targetZhFileName
        else:
            return fNameTransedI18N
        
def test(enFile2Trans = None, enZhDictFile = None):
    translateByDict = TranslateByDict(enFile2Trans,enZhDictFile)
    translateByDict.translateByDictAndWrite()
        
if __name__ == "__main__":
    # #file and directories to be deal with
#    print "I'm here!"
    fPath = "D:\\workspace\\Python27\\myfirstpython\\files\\TranslateByDict"
    # English and Chinese properties file used to prepare for extracting dictionary
    fEnFile2Trans = os.path.join(fPath,"Messages_zh_Phase1.properties")
    fEnZhDictFile = os.path.join(fPath,"Base_Dict_WordsInMsgAndAppRes_20110318Rev3.txt")
    test(fEnFile2Trans,fEnZhDictFile)
    
        
        