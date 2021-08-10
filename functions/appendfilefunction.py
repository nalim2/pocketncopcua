import os

from main import path
from functionmanager import customFeatures

appendfile_programname = "ProgrammName"
appendfile_filecontent = "FileContent"

appendfilefunction_defaultparams = {appendfile_filecontent: "", appendfile_programname: "test"}


def startappendFileFunc(hal, funcName):
    print("Start AppendFile function")
    featureParams = customFeatures[funcName]["params"]
    filename = featureParams[appendfile_programname].get_value() + '.ngc'
    if os.path.exists(path):
        with open(os.path.join(path, filename), 'a') as temp_file:
            temp_file.write(featureParams[appendfile_filecontent].get_value())


def checkFinisedAppendFile(hal, funcName):
    print("Check Finished AppendFile")
    return True


def checkErrorAppendFile(hal, funcName):
    print("Check AppendFile")
    return os.path.exists(path)