'''
Created on 2011-3-10
Update base dict file using a new dict file.
Both dict files are in the form of "key1 = value1 \n, ...\n, keyN = valueN \n".
Value in base dict will be replaced if the two dict files have the same key. 
All key-values appear in both base dict and new dict will be saved and sorted
in a file with "_Updated" as suffix in the name.
Both I18N ASCII file and Unicode file will be created, with an extension of
.properties and . txt respectively.
@author: cnxc8360
'''

import os
# import re
import codecs
from subprocess import call

class UpdateDict:
    '''
    classdocs
    '''
    pass

    def __init__(self,baseDictFile = None, newDictFile = None, updatedDictFile = None, native2ascii_exe = None):
        '''
        Initiate baseDictFile name and newDictFile name.
        baseDictFile and newDictFile should be
        full file names with directory. Blank lines and comment lines
        (starts with "#") are ignored. 
        '''
#        print "I'm here!"
        self.baseDictFile = baseDictFile
        self.newDictFile = newDictFile
        self.updatedDictFile = updatedDictFile
        self.native2ascii_exe = native2ascii_exe
        self.updatedDict = None
        self.sortedListOfUpdatedDict = None
        self.sortedListOfCleanedDict = None

    def openAndRead(self,fName):
        '''
        Read "key1 = value1 \n, ...\n, keyN = valueN \n" format 
        dictionary(properties) file. fName should be
        full file names with directory.
        Parse the contents of dict file (i.e. baseDictFile file
        and newDictFile) to form a list. Blank lines and comment lines
        (starts with "#") are ignored. 
        Return a list of [["key1","value1"],...,["keyi","valuei"]
        '''
        if os.path.isfile(fName) == False: return "Not a file name!"
#       parse absolute filename to path, name trunk and extension
        pathName,fileName = os.path.split(fName)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
#        if fName is not a .properties file, i.e. it is not I18N ASCII file
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
    def updateDict(self):
        if self.baseDictFile == None or self.newDictFile == None: 
            return "Two dict files needed."
        baseDictList = self.openAndRead(self.baseDictFile)
        newDictList = self.openAndRead(self.newDictFile)
        # strip blanks and "\t\r\n" in all keys and values
        # and use keys and values to form dictionary
        baseDict = dict([(k[0].strip(),k[1].strip()) for k in baseDictList])
        newDict = dict([(k[0].strip(),k[1].strip()) for k in newDictList])
        self.updatedDict = baseDict.copy()
        self.updatedDict.update(newDict)
        # sort dictionary by keys
        self.sortedListOfUpdatedDict = sorted(self.updatedDict.items(),\
                                              key = lambda x:x[0])
#        print "I'm here!"
    def writeUpdatedDict(self,fName=None, fName4UI=None):
        if fName == None: fName = self.baseDictFile
        if os.path.isfile(fName) == False: return "Not a file name!"
        if fName4UI == None: fName4UI = self.updatedDictFile
#       parse absolute filename to path, name trunk and extension
        pathName,fileName = os.path.split(fName)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        updatedDictFileName = os.path.join(pathName,fileNameTrunk+"_Updated.properties")
#       if sorted list of updated dict is exist, write it in "keyi = valuei" format  
        if self.sortedListOfUpdatedDict != None:
            f = codecs.open(updatedDictFileName,mode="w")
            if fName4UI != None:
                f4UI = codecs.open(fName4UI,mode="w")
            for i in self.sortedListOfUpdatedDict:
                f.write(i[0]+'\t = \t'+i[1]+'\n')
                if fName4UI != None:
                    f4UI.write(i[0]+'\t = \t'+i[1]+'\n')
            f.close() 
            if fName4UI != None:
                f4UI.close()      
        self.ascii2Unicode(updatedDictFileName)
        if fName4UI != None:
            return fName4UI
        else:
            return updatedDictFileName
    
    def cleanDictFile(self,fName):
        '''
        Open a dict file and clean nonsense pairs in it.
        Then write the cleaned dict in to a new file.
        fName should be a file name with its absolute directory
        '''
#        print fName
        if os.path.isfile(fName) == False: return "Not a file name!"
#       parse absolute filename to path, name trunk and extension
        pathName,fileName = os.path.split(fName)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
#        generate new file name with a suffix of "_Cleaned"s
        cleanedDictFileName = os.path.join(pathName,fileNameTrunk+"_Cleaned.properties")
#        print cleanedDictFileName
#        Read dict file in to a list
        fList = self.openAndRead(fName)
        # Clean nonsense pairs in list, i.e. keep only translated pairs
        dictValueEnZhCleaned = dict([k for k in fList if k[0].strip()!=k[1].strip()])
        self.sortedListOfCleanedDict = sorted(dictValueEnZhCleaned.items(), key = lambda x:x[0])
#       if sorted list of updated dict is exist, write it in "keyi = valuei" format  
        if self.sortedListOfCleanedDict != None:
            f = codecs.open(cleanedDictFileName,mode="w")
            for i in self.sortedListOfCleanedDict:
                f.write(i[0]+'\t = \t'+i[1]+'\n')
            f.close()   
        self.ascii2Unicode(cleanedDictFileName)
        

def test(baseDictFile=None,newDictFile=None):
    updateBaseDict = UpdateDict(baseDictFile,newDictFile)
    updateBaseDict.updateDict()
    updateBaseDict.writeUpdatedDict()
     
if __name__ == "__main__":
    # #file and directories to be deal with
#    print "I'm here!"
    fPath = "D:\\workspace\\Python27\\myfirstpython\\files\\UpdateDict"
    # base dict file used to prepare replacement pairs for translation
#    fBaseDict = os.path.join(fPath,"Base_Dict_Updated_Cleaned_Updated.txt")
#    fNewDict = os.path.join(fPath,"ApplicationResources_NewDict.txt")
#    test(fBaseDict,fNewDict)
    
#    convert .txt unicode file to .properties I18N ASCII file
    convertDict = UpdateDict()
    fName2I18N = os.path.join("D:\\workspace\\Python27\\myfirstpython\\files\\TranslateByDict","Messages_zh_Phase1_Transed_RevName.txt")
    convertDict.unicode2Ascii(fName2I18N)
#    fName2Convert = os.path.join("D:\\workspace\\Python27\\myfirstpython\\files\\TranslateByDict","Messages_zh_Phase1_Transed_RevName.properties")
#    convertDict.ascii2Unicode(fName2Convert)
        
        
        
        