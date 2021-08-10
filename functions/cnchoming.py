from main import c, setModeManual


def homeAllAxis(parent):
    c.wait_complete()
    c.home(0)
    c.wait_complete()
    c.home(1)
    c.wait_complete()
    c.home(2)
    c.wait_complete()
    c.home(3)
    c.wait_complete()
    c.home(4)
    c.wait_complete()
    c.home(5)
    c.wait_complete()
    print("Homeing!!")


def startHomingFunc(hal, funcName):
    print("Start Home function")
    print("Set mode manual")

    setModeManual(None)
    print("Start homing")
    homeAllAxis(None)


def checkFinishedHomed(hal, funcName):
    print("Check Finished Homed")
    homedInfo = hal.homed
    result = True
    for index in range(0, hal.axes):
        result = result and homedInfo[index]
    return result


def checkErrorHomed(hal, funcName):
    print("Check Error Homed")
    return False