import os

from main import setModeAuto, c, path, startSelectedProgramm, resumeSelectedProgramm
from functionmanager import customFeatures


abort_defaultparams = {}

def startAbortFunc(hal, funcName):
    print("Start NCProgramm function")
    c.abort()


def checkFinisedAbort(hal, funcName):
    print("Check Finished CreateFile")
    return hal.exec_state == 2 and hal.state == 1


def checkErrorAbort(hal, funcName):
    print("Check CreateFile")
    return False