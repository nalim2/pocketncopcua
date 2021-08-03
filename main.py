# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import linuxcnc
from opcua import Server
import logging
import time
import os

from linuxcncopcua import *

variableMap = {}

server = Server()
c = linuxcnc.command()
path = "/tmp/cncprogramm"


def setModeMDI(parent):
    c.wait_complete()
    c.mode(linuxcnc.MODE_MDI)
    c.wait_complete()
    print("NOW MACHINE IS MDI!!!")

def setModeManual(parent):
    c.wait_complete()
    c.mode(linuxcnc.MODE_MANUAL)
    c.wait_complete()
    print("NOW MACHINE IS MANUAL!!!")

def setModeAuto(parent):
    c.wait_complete()
    c.mode(linuxcnc.MODE_AUTO)
    c.wait_complete()
    print("NOW MACHINE IS AUTO!!!")

def setMoveRobotRemovePos(parent):
    c.wait_complete()
    xInch = 64.770 / 25.4
    c.mdi("G0 G21 G90 X63.5 Y0 Z0 A0 B15")# G21 for Units in MM
    c.wait_complete()
    print("MOVE THAT ROBOT!!")

def startSelectedProgramm(parent):
    c.wait_complete()
    c.auto(linuxcnc.AUTO_RUN, 0)
    c.wait_complete()
    print("STAARRTT!!")

def pauseSelectedProgramm(parent):
    c.wait_complete()
    c.auto(linuxcnc.AUTO_PAUSE)
    c.wait_complete()
    print("Paused!!")

def resumeSelectedProgramm(parent):
    c.wait_complete()
    c.auto(linuxcnc.AUTO_RESUME)
    c.wait_complete()
    print("Resume!!")

def startFileTransfer(hal, funcName):
    print("Check Transfer File ")

def checkFinishedTransferFile(hal, funcName):
    print("Start Transfer File function")
    return True
def checkErrorTransferFile(hal, funcName):
    print("Check Error Transfer File")
    return False


def update_loop():
    while True:
        update_function()
        time.sleep(0.1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)

    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)

    print("Configure OPC Server")
    init_variables_start_server()
    print("Start OPC UA Server")
    start_server()
    print("Beginn update loop!")
    update_loop()

