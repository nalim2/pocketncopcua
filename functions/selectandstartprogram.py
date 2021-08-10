import os

from main import setModeAuto, c, path, startSelectedProgramm, resumeSelectedProgramm
from functionmanager import customFeatures
field_programname_selectandstartprogram = "ProgrammName"

selectandstartprogram_defaultparams = {field_programname_selectandstartprogram: ""}

def startNCProgrammFunc(hal, funcName):
    print("Start NCProgramm function")
    featureParams = customFeatures[funcName]["params"]
    filename = featureParams[field_programname_selectandstartprogram].get_value() + '.ngc'
    setModeAuto(None)
    c.program_open(os.path.join(path, filename))
    startSelectedProgramm(None)
    resumeSelectedProgramm(None)


def checkFinisedNCProgramm(hal, funcName):
    print("Check Finished NCProgramm")
    result = hal.exec_state == 2 and hal.state == 1
    print("Result: " + str(result))
    return result


def checkErrorNCProgramm(hal, funcName):
    print("Check NCProgramm Error")
    return False