from main import setModeMDI, setMoveRobotRemovePos


def startGoToRobotRemovePositionFunc(hal, funcObj):
    print("Start go to Robot remove position function")
    setModeMDI(None)
    setMoveRobotRemovePos(None)


def checkFinishedGoToRobotRemovePosition(hal, funcObj):
    print("Check Finished Robot remove position")
    print("Current state " + str(hal.state))
    return hal.state == 1


def checkErrorGoToRobotRemovePosition(hal, funcObj):
    print("Check Error Homed")
    return False