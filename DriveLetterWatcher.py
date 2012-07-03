import win32serviceutil
import string
from ctypes import windll
from sets import *
import os
import sys
import time
import subprocess
import json
from winservice import Service, instart

class DriveLetterWatcher(Service):
    # Function adapted from http://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-drive-letters-in-python
    def get_drives(self):
        drives = Set()
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.uppercase:
            if bitmask & 1:
                drives.add(letter)
            bitmask >>= 1

        return drives

    def on_connect(self, ltr, connectEvents):
        self.log( "Connected: " + ltr )
        if( connectEvents[ltr] != "" ):
            self.log( "Running: " + connectEvents[ltr] )
            os.startfile(connectEvents[ltr]);

    def on_disconnect(self, ltr, disconnectEvents):
        self.log( "Disconnected: " + ltr )
        if( disconnectEvents[ltr] != "" ):
            self.log( "Running: " + disconnectEvents[ltr] )
            os.startfile(disconnectEvents[ltr]);

    def parse_config(self):
        base = win32serviceutil.GetServiceCustomOption('DriveLetterWatcher', 'startIn')
        jsonFile = json.load(file(base + "config.json.txt"))
        return jsonFile["connectEvents"], jsonFile["disconnectEvents"]
        
    def start(self):
        self.runflag = True
        old = self.get_drives()
        connectEvents, disconnectEvents = self.parse_config()
        while self.runflag:
            new = self.get_drives()
            for ltr in new.difference(old):
                self.on_connect(ltr, connectEvents)
            for ltr in old.difference(new):
                self.on_disconnect(ltr, disconnectEvents)
            old = new
            time.sleep(5)
            
    def stop(self):
        self.runflag = False
        
instart(DriveLetterWatcher, 'DriveLetterWatcher', 'DriveLetterWatcher')

