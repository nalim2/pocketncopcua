import os

from main import path
from functionmanager import customFeatures

createfilefunction_defaultparams = {"FileContent": "Testdigga", "ProgrammName": "/home"}

def startCreateFileFunc(hal, funcName):
    print("Start CreateFile function")
    featureParams = customFeatures[funcName]["params"]
    filename = featureParams["ProgrammName"].get_value() + '.ngc'
    with open(os.path.join(path, filename), 'wb') as temp_file:
        temp_file.write(featureParams["FileContent"].get_value())


def checkFinisedCreateFile(hal, funcName):
    print("Check Finished CreateFile")
    return True


def checkErrorCreateFile(hal, funcName):
    print("Check CreateFile")
    return False