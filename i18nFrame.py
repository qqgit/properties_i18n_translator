
""" Test wxPython
2011.12.21 Xueqi

"""

import wx
import wx.lib.filebrowsebutton as filebrowse
import os
import codecs
from subprocess import call
import time
import translateByDict4UI
import extractDict4UI
import updateDict4UI

class i18nFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "I18N Translator")
        panel = wx.Panel(self)
        
        # First create the controls
        #     native <--->ascii controls
        nativeANDasciiLbl = wx.StaticText(panel, -1, "Native <---> ASCII")
        nativeANDasciiLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        #         native2ascii.exe control
        nat2ascfbb = filebrowse.FileBrowseButton(
                                                    panel, 
                                                    -1, 
                                                    size=(450, -1), 
                                                    labelText="native2ascii.exe:",
                                                    )
        if os.getenv("JAVA_HOME") != None:
            native2ascii_exe = os.getenv("JAVA_HOME") + os.sep + "bin" + os.sep + "native2ascii.exe"
        else:
            native2ascii_exe = os.getcwd() + os.sep + "native2ascii.exe"
            if os.path.isfile(native2ascii_exe) == False:
                native2ascii_exe = "JAVA_HOME environment variable is NOT set!!!!Please select native2ascii.exe file."
        nat2ascfbb.SetValue( native2ascii_exe )
        #         native -->ascii controls
        natsrcfbb = filebrowse.FileBrowseButton(
                                                panel, 
                                                -1, 
                                                size=(450, -1), 
                                                labelText="Native Source File:", 
                                                changeCallback = self.natsrcfbbCallback 
                                                )
        asctgtLbl = wx.StaticText(panel, -1, "Target ASCII File:")
        asctgtTxt = wx.TextCtrl(panel, -1, "")
        native2asciiBtn = wx.Button(panel, -1, "Native 2 Ascii")
        self.Bind(wx.EVT_BUTTON, self.OnNative2AsciiBtnClick, native2asciiBtn)
        #        ascii -->native controls
        ascsrcfbb = filebrowse.FileBrowseButton(
                                                panel, 
                                                -1, 
                                                size=(450, -1), 
                                                labelText="Ascii Source File:", 
                                                changeCallback = self.ascsrcfbbCallback 
                                                )
        nattgtLbl = wx.StaticText(panel, -1, "Target Native File:")
        nattgtTxt = wx.TextCtrl(panel, -1, "")
        ascii2nativeBtn = wx.Button(panel, -1, "Ascii 2 Native")
        self.Bind(wx.EVT_BUTTON, self.OnAscii2NativeBtnClick, ascii2nativeBtn)
        
        # Update dictionary controls, Base Dict + New Dict ----> Updated Dict
        updateDictLbl = wx.StaticText(panel, -1, "Base Dict + New Dict ---> Updated Dict")
        updateDictLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        baseDictfbb = filebrowse.FileBrowseButton(
                                                panel, 
                                                -1, 
                                                size=(450, -1), 
                                                labelText="Base Dict File:", 
                                                )
        newDictfbb = filebrowse.FileBrowseButton(
                                                panel, 
                                                -1, 
                                                size=(450, -1), 
                                                labelText="New Dict File:", 
                                                changeCallback = self.newDictfbbCallback
                                                )
        updatedDictLbl = wx.StaticText(panel, -1, "Updated Dict File:")
        updatedDictTxt = wx.TextCtrl(panel, -1, "")
        updateDictBtn = wx.Button(panel, -1, "Update Dictionary")
        self.Bind(wx.EVT_BUTTON, self.OnUpdateDictBtnClick, updateDictBtn)
        #updateDictBtn.Disable()
        
        # En properties file to Zh properties file translation controls
        transEn2ZhLbl = wx.StaticText(panel, -1, "En Prop File --(Dict)--> Zh Prop File")
        transEn2ZhLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        dictfbb = filebrowse.FileBrowseButton(
                                                panel, 
                                                -1, 
                                                size=(450, -1), 
                                                labelText="Dictionary File:", 
                                                )
        en2transfbb = filebrowse.FileBrowseButton(
                                                    panel, 
                                                    -1, 
                                                    size=(450, -1), 
                                                    labelText="En Properties File:", 
                                                    changeCallback = self.en2transfbbCallback
                                                    )
        zhTransedLbl = wx.StaticText(panel, -1, "Target Zh File:")
        zhTransedTxt = wx.TextCtrl(panel, -1, "")
        transBtn = wx.Button(panel, -1, "Translate")
        self.Bind(wx.EVT_BUTTON, self.OnTransBtnClick, transBtn)
        
        # Controls for extracting dictionary form En and Zh properties files
        extractDictLbl = wx.StaticText(panel, -1, "En && Zh properties files --> Dictionary")
        extractDictLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        en2extractfbb = filebrowse.FileBrowseButton(
                                                    panel, 
                                                    -1, 
                                                    size=(450, -1), 
                                                    labelText="En properties File:", 
                                                    )
        zh2extractfbb = filebrowse.FileBrowseButton(
                                                    panel, 
                                                    -1, 
                                                    size=(450, -1), 
                                                    labelText="Zh Properties File:", 
                                                    changeCallback = self.zh2extractfbbCallback
                                                    )
        dicttgtLbl = wx.StaticText(panel, -1, "Target Dictionary File:")
        dicttgtTxt = wx.TextCtrl(panel, -1, "")
        extractBtn = wx.Button(panel, -1, "Extract")
        self.Bind(wx.EVT_BUTTON, self.OnExtractBtnClick, extractBtn)
        
        # 
        self.nat2ascfbb = nat2ascfbb
        self.natsrcfbb = natsrcfbb
        self.asctgtTxt = asctgtTxt
        self.native2asciiBtn = native2asciiBtn
        self.ascsrcfbb = ascsrcfbb
        self.nattgtTxt = nattgtTxt
        self.ascii2nativeBtn = ascii2nativeBtn
        self.baseDictfbb = baseDictfbb
        self.newDictfbb = newDictfbb
        self.updatedDictTxt = updatedDictTxt
        self.updateDictBtn = updateDictBtn
        self.dictfbb = dictfbb
        self.en2transfbb = en2transfbb
        self.zhTransedTxt = zhTransedTxt
        self.transBtn = transBtn
        self.en2extractfbb = en2extractfbb
        self.zh2extractfbb = zh2extractfbb
        self.dicttgtTxt = dicttgtTxt
        self.extractBtn = extractBtn

        

        # Now do the layout.
        
        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rithtSizer = wx.BoxSizer(wx.VERTICAL)
        leftTopSizer = wx.BoxSizer(wx.VERTICAL)
        leftBottomSizer = wx.BoxSizer(wx.VERTICAL)
        rightTopSizer = wx.BoxSizer(wx.VERTICAL)
        rightBottomSizer = wx.BoxSizer(wx.VERTICAL)
        
        #    leftTopSizer is the sizer for native <---> ascii controls
        leftTopSizer.Add(nativeANDasciiLbl, 0, wx.ALL, 5)
        leftTopSizer.Add(wx.StaticLine(panel), 0,
                      wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        leftTopSizer.Add(nat2ascfbb, 0, wx.EXPAND)
        leftTopSizer.Add(wx.StaticLine(panel), 0,
                      wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        leftTopSizer.Add(natsrcfbb, 0, wx.EXPAND)
        
        asctgtSizer = wx.BoxSizer(wx.HORIZONTAL)
        asctgtSizer.Add(asctgtLbl, 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        asctgtSizer.Add(asctgtTxt, 1, wx.EXPAND|wx.ALL)
        
        leftTopSizer.Add(asctgtSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        native2asciiBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        native2asciiBtnSizer.Add((50,50))
        native2asciiBtnSizer.Add(native2asciiBtn, 1, wx.EXPAND)
        native2asciiBtnSizer.Add((50,50))
        leftTopSizer.Add(native2asciiBtnSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        leftTopSizer.Add(ascsrcfbb, 0, wx.EXPAND)
        
        nattgtSizer = wx.BoxSizer(wx.HORIZONTAL)
        nattgtSizer.Add(nattgtLbl, 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        nattgtSizer.Add(nattgtTxt, 1, wx.EXPAND)
        
        leftTopSizer.Add(nattgtSizer, 0, wx.EXPAND|wx.ALL, 10)
        ascii2nativeBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        ascii2nativeBtnSizer.Add((50,50))
        ascii2nativeBtnSizer.Add(ascii2nativeBtn, 1, wx.EXPAND)
        ascii2nativeBtnSizer.Add((50,50))
        leftTopSizer.Add(ascii2nativeBtnSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        leftBottomSizer.Add(updateDictLbl, 0, wx.ALL, 5)
        leftBottomSizer.Add(wx.StaticLine(panel), 0,
                          wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        leftBottomSizer.Add(baseDictfbb, 0, wx.EXPAND)
        leftBottomSizer.Add(newDictfbb, 0, wx.EXPAND)
        
        updatedDictSizer = wx.BoxSizer(wx.HORIZONTAL)
        updatedDictSizer.Add(updatedDictLbl, 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        updatedDictSizer.Add(updatedDictTxt, 1, wx.EXPAND)
        
        leftBottomSizer.Add(updatedDictSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        updateDictBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        updateDictBtnSizer.Add((50,50))
        updateDictBtnSizer.Add(updateDictBtn, 1, wx.EXPAND)
        updateDictBtnSizer.Add((50,50))
        leftBottomSizer.Add(updateDictBtnSizer, 0, wx.EXPAND|wx.ALL, 10)

        #    rightTopSizer is the sizer for translate en prop file to zh prop file
        rightTopSizer.Add(transEn2ZhLbl, 0, wx.ALL, 5)
        rightTopSizer.Add(wx.StaticLine(panel), 0,
                          wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        rightTopSizer.Add(dictfbb, 0, wx.EXPAND)
        rightTopSizer.Add(en2transfbb, 0, wx.EXPAND)
        
        zhTransedSizer = wx.BoxSizer(wx.HORIZONTAL)
        zhTransedSizer.Add(zhTransedLbl, 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        zhTransedSizer.Add(zhTransedTxt, 1, wx.EXPAND)
        
        rightTopSizer.Add(zhTransedSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        transBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        transBtnSizer.Add((50,50))
        transBtnSizer.Add(transBtn, 1, wx.EXPAND)
        transBtnSizer.Add((50,50))
        rightTopSizer.Add(transBtnSizer, 0, wx.EXPAND|wx.ALL, 10)

        
        #    rightBottomSizer is the sizer for extract dictionary from en and zh prop file
        rightBottomSizer.Add(extractDictLbl, 0, wx.ALL, 5)
        rightBottomSizer.Add(wx.StaticLine(panel), 0,
                          wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        rightBottomSizer.Add(en2extractfbb, 0, wx.EXPAND)
        rightBottomSizer.Add(zh2extractfbb, 0, wx.EXPAND)
        
        dicttgtSizer = wx.BoxSizer(wx.HORIZONTAL)
        dicttgtSizer.Add(dicttgtLbl, 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        dicttgtSizer.Add(dicttgtTxt, 1, wx.EXPAND)
        
        rightBottomSizer.Add(dicttgtSizer, 0, wx.EXPAND|wx.ALL, 10)
        extractBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        extractBtnSizer.Add((50,50))
        extractBtnSizer.Add(extractBtn, 1, wx.EXPAND)
        extractBtnSizer.Add((50,50))
        rightBottomSizer.Add(extractBtnSizer, 0, wx.EXPAND|wx.ALL, 10)

        
        # add all sub sizers together
        leftSizer.Add(leftTopSizer, 0, wx.EXPAND|wx.ALL, 10)
        leftSizer.Add(leftBottomSizer, 0, wx.EXPAND|wx.ALL, 10)
        rithtSizer.Add(rightTopSizer, 0, wx.EXPAND|wx.ALL, 10)
        rithtSizer.Add(rightBottomSizer, 0, wx.EXPAND|wx.ALL, 10)
        mainSizer.Add(leftSizer, 0, wx.EXPAND, 5)
        mainSizer.Add(wx.StaticLine(panel), 0,
                          wx.EXPAND|wx.ALL, 10)
        mainSizer.Add(rithtSizer, 0, wx.EXPAND, 5)

        panel.SetSizer(mainSizer)
        
        # Fit the frame to the needs of the sizer. The frame will
        # automatically resize the panel as needed. Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)
    
    def OnNative2AsciiBtnClick(self, evt):
        native2ascii_exe = self.nat2ascfbb.GetValue()
        nativeFileName = self.natsrcfbb.GetValue()
        asciiFileName = self.asctgtTxt.GetValue()
        #check exe file name
        if os.path.isfile(native2ascii_exe) == False: 
            self.nat2ascfbb.SetValue(native2ascii_exe + " is NOT a file!!!")
            return "Not a file name!"
        #self.asctgtTxt.SetValue(native2ascii_exe)
        targetFileName = self.native2Ascii(native2ascii_exe, nativeFileName, asciiFileName)
        #check target filename
        if os.path.isfile(targetFileName) == False: 
            self.asctgtTxt.SetValue(targetFileName + "is NOT generated!!!")
            return "File not generated!"
        try:
            call(["notepad.exe", targetFileName])
        except IOError:
            self.asctgtTxt.SetValue("Error occured when open " + targetFileName)
            return "Error open target file"
        
    def OnAscii2NativeBtnClick(self, evt):
        native2ascii_exe = self.nat2ascfbb.GetValue()
        asciiFileName = self.ascsrcfbb.GetValue()
        nativeFileName = self.nattgtTxt.GetValue()
        #check exe file name
        if os.path.isfile(native2ascii_exe) == False: 
            self.nat2ascfbb.SetValue(native2ascii_exe + " is NOT a file!!!")
            return "Not a file name!"
        #self.asctgtTxt.SetValue(native2ascii_exe)
        targetFileName = self.ascii2Native(native2ascii_exe, asciiFileName, nativeFileName)
        #check target filename
        if os.path.isfile(targetFileName) == False: 
            self.nattgtTxt.SetValue(targetFileName + "is NOT generated!!!")
            return "File not generated!"
        call(["notepad.exe", targetFileName])
        
    def OnUpdateDictBtnClick(self, evt):
        baseDictFileName = self.baseDictfbb.GetValue()
        newDictFileName = self.newDictfbb.GetValue()
        updatedDictFileName = self.updatedDictTxt.GetValue()
        
        updateBaseDict = updateDict4UI.UpdateDict(
                                                  baseDictFileName,
                                                  newDictFileName,
                                                  updatedDictFileName
                                                  )
        updateBaseDict.updateDict()
        targetFileName = updateBaseDict.writeUpdatedDict()
        #check target filename
        if os.path.isfile(targetFileName) == False: 
            self.updatedDictTxt.SetValue(targetFileName + "is NOT generated!!!")
            return "File not generated!"
        call(["notepad.exe", targetFileName])
        
    def OnTransBtnClick(self, evt):
        dictFileName = self.dictfbb.GetValue()
        enPropFileName = self.en2transfbb.GetValue()
        zhTargetFileName = self.zhTransedTxt.GetValue()
        
        translateByDict = translateByDict4UI.TranslateByDict(enPropFileName,
                                                             dictFileName,
                                                             zhTargetFileName)
        targetFileName = translateByDict.translateByDictAndWrite()
        #check target filename
        if os.path.isfile(targetFileName) == False: 
            self.zhTransedTxt.SetValue(targetFileName + "is NOT generated!!!")
            return "File not generated!"
        call(["notepad.exe", targetFileName])
    
    def OnExtractBtnClick(self, evt):
        enPropFileName = self.en2extractfbb.GetValue()
        zhPropFileName = self.zh2extractfbb.GetValue()
        targetDictFileName = self.dicttgtTxt.GetValue()
        
        extractDict = extractDict4UI.ExtractDict(enPropFileName,
                                                 zhPropFileName,
                                                 targetDictFileName)
        extractDict.extractDict()
        targetFileName = extractDict.writeExtractedDict()
        #check target filename
        if os.path.isfile(targetFileName) == False: 
            self.dicttgtTxt.SetValue(targetFileName + "is NOT generated!!!")
            return "File not generated!"
        call(["notepad.exe", targetFileName])
    
    def natsrcfbbCallback(self, evt):
        srcFileStr = evt.GetString()
        # parse source file name and generate default target file name, 
        # then set it to target control 
        pathName,fileName = os.path.split(srcFileStr)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        tgtFileStr = os.path.join(pathName,fileNameTrunk+"_ascii.properties")
        
        #tgtFileStr = srcFileStr
        self.asctgtTxt.SetValue(tgtFileStr)
        
    def ascsrcfbbCallback(self, evt):
        srcFileStr = evt.GetString()
        # parse source file name and generate default target file name, 
        # then set it to target control 
        pathName,fileName = os.path.split(srcFileStr)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        tgtFileStr = os.path.join(pathName,fileNameTrunk+"_native.properties")
        
        #tgtFileStr = srcFileStr
        self.nattgtTxt.SetValue(tgtFileStr)
        
    def newDictfbbCallback(self, evt):
        srcFileStr = evt.GetString()
        # parse source file name and generate default target file name, 
        # then set it to target control 
        pathName,fileName = os.path.split(srcFileStr)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        tgtFileStr = os.path.join(pathName,fileNameTrunk+"_UpdatedDict.properties")
        self.updatedDictTxt.SetValue(tgtFileStr)
        
    def en2transfbbCallback(self, evt):
        srcFileStr = evt.GetString()
        # parse source file name and generate default target file name, 
        # then set it to target control 
        pathName,fileName = os.path.split(srcFileStr)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        tgtFileStr = os.path.join(pathName,fileNameTrunk+"_zh.properties")
        
        #tgtFileStr = srcFileStr
        self.zhTransedTxt.SetValue(tgtFileStr)
        
    def zh2extractfbbCallback(self, evt):
        srcFileStr = evt.GetString()
        # parse source file name and generate default target file name, 
        # then set it to target control 
        pathName,fileName = os.path.split(srcFileStr)
        fileNameTrunk, fileNameExt = os.path.splitext(fileName)
        tgtFileStr = os.path.join(pathName,fileNameTrunk+"_EnZhDict.properties")
        
        #tgtFileStr = srcFileStr
        self.dicttgtTxt.SetValue(tgtFileStr)
        
        
    def native2Ascii(self,native2ascii_exe, nativeFileName, asciiFileName):
        """
        Convert a file from native to I18N ASCII file 
        """
        try:
            call([native2ascii_exe,nativeFileName,asciiFileName])
            return asciiFileName
        except IOError:
            return "Error in native2Ascii."
        
    
    def ascii2Native(self, native2ascii_exe, asciiFileName, nativeFileName):
        """
        Convert a file from I18N ASCII to  native file 
        """
        call([native2ascii_exe,"-reverse",asciiFileName,nativeFileName])
        return nativeFileName

if __name__ == '__main__':        
    app = wx.PySimpleApp()
    i18nFrame().Show()
    app.MainLoop()
            