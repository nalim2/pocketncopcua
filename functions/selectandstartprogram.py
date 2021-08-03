import os

from main import setModeAuto, c, path, startSelectedProgramm, resumeSelectedProgramm
from functionmanager import customFeatures


def startNCProgrammFunc(hal, funcName):
    print("Start NCProgramm function")
    featureParams = customFeatures[funcName]["params"]
    filename = featureParams["ProgrammName"].get_value() + '.ngc'
    setModeAuto(None)
    c.program_open(os.path.join(path, filename))
    startSelectedProgramm(None)
    resumeSelectedProgramm(None)


def checkFinisedNCProgramm(hal, funcName):
    print("Check Finished CreateFile")
    return hal.exec_state == 2 and hal.state == 1


def checkErrorNCProgramm(hal, funcName):
    print("Check CreateFile")
    return False