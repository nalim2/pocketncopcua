import os

from main import setModeAuto, c, path, startSelectedProgramm, resumeSelectedProgramm
from functionmanager import customFeatures
field_program_name="ProgrammName"

selectandstartprogram_defaultparams = {field_program_name: ""}

def startNCProgrammFunc(hal, funcName):
    print("Start NCProgramm function")
    featureParams = customFeatures[funcName]["params"]
    filename = featureParams[field_program_name].get_value() + '.ngc'
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