import linuxcnc
from opcua import Server
import logging
import time
import os
from os.path import expanduser
from linuxcncopcua import *
import threading

variableMap = {}

server = Server()
c = linuxcnc.command()
path = expanduser("~/opc-tmp/cncprogramm")


def setModeMDI(parent):
    c.mode(linuxcnc.MODE_MDI)
    c.wait_complete()
    print("NOW MACHINE IS MDI!!!")

def setModeManual(parent):
    c.mode(linuxcnc.MODE_MANUAL)
    c.wait_complete()
    print("NOW MACHINE IS MANUAL!!!")

def setModeAuto(parent):
    c.mode(linuxcnc.MODE_AUTO)
    c.wait_complete()
    print("NOW MACHINE IS AUTO!!!")

def setMoveRobotRemovePos(parent):
    xInch = 64.770 / 25.4
    c.mdi("G0 G21 G90 X63.5 Y0 Z0 A0 B15")# G21 for Units in MM
    print("MOVE THAT ROBOT!!")

def startSelectedProgramm(parent):
    c.auto(linuxcnc.AUTO_RUN, 0)
    c.wait_complete()
    print("STAARRTT!!")

def pauseSelectedProgramm(parent):
    c.auto(linuxcnc.AUTO_PAUSE)
    c.wait_complete()
    print("Paused!!")

def resumeSelectedProgramm(parent):
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
    print("Selected System path: ", path)
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
    thread = threading.Thread(target=update_loop, args=())
    thread.daemon = True
    thread.start()
    thread.join()

