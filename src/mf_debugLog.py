import sys

class debugObj():
    def __init__(self):
        self.debugOn = True
        self.debug_output = 'shell'
        self.debug = 'INFO'
        self.debugLevel = {'ERROR': 0, 'WARNING': 3, 'INFO': 5}

    def setDebug(self, value):
        self.debug = value
    def enableDebug(self):
         self.debugOn = True
    def disableDebug(self):
         self.debugOn = False
    def setDebugOutput(self, value):
         self.debug_output = value

    def debugLog(self, string, level = 'ERROR'):
        if(self.debugOn and self.debug_output == 'shell'):
            if(self.debugLevel[self.debug] <= self.debugLevel[level]):
                print string
        elif(self.debugOn and self.debug_output == 'file'):
            if(self.debugLevel[self.debug] <= self.debugLevel[level]):
                print "Log debug file not supported"
