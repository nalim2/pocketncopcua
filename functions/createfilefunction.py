import os

from main import path
from functionmanager import customFeatures
createfile_programname = "ProgrammName"
createfile_filecontent = "FileContent"


createfile_default_file_content = """\n%\n(AXIS,stop)\n(1001)\n(GZ)\nN10 G21\nN15 G90 G94 G40 G17 G91.1\nN20 G53 G0 Z0.\n(FACE4)\nN25 G49\nN30 M5\nN35 G53 G0 X63.5 Y63.5\nN40 M0\nN45 T1 M6\nN50 S5000 M3\nN55 G54 G0\nN60 G53 G0 X63.5 Y63.5\nN65 A90. B0.\nN70 M8\nN75 G1 X8.39 Y-9.719 F10000.\nN80 G43 Z68.789 H1\nN85 G1 Z58.789\nN90 Z51.089 F1000.\nN95 G18 G3 X8.09 Z50.789 I-0.3 K0.\nN100 G1 X7.304\nN105 X-7.304\nN110 X-9.544\nN115 G17 G2 Y-6.967 I0. J1.376\nN120 G1 X9.544\nN125 X10.656\nN130 G3 Y-4.215 I0. J1.376\nN135 G1 X-10.656\nN140 X-11.\nN145 G2 Y-1.462 I0. J1.376\nN150 G1 X11.\nN155 G3 Y1.29 I0. J1.376\nN160 G1 X-11.\nN165 G2 Y4.042 I0. J1.376\nN170 G1 X-10.702\nN175 X10.702\nN180 G3 Y6.794 I0. J1.376\nN185 G1 X9.637\nN190 X-9.637\nN195 G2 Y9.547 I0. J1.376\nN200 G1 X-7.498\nN205 X7.498\nN210 G18 G2 X7.798 Z51.089 I0. K0.3\nN215 G1 Z68.789 F10000.\nN220 G17\nN225 M9\nN230 G49\nN235 G53 G0 Z0.\nN240 G53 G0 X63.5 Y63.5\nN245 A0. B0.\nN250 M30\n(AXIS,stop)\n%\n"""
createfilefunction_defaultparams = {createfile_filecontent: createfile_default_file_content, createfile_programname: "test"}

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