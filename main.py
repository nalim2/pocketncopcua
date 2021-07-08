# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import multiprocessing
import sys
import linuxcnc
import types

from opcua import ua, Server
import logging
import time
from multiprocessing import Pool


variableMap = {}
server = Server()
c = linuxcnc.command()


def startSelectedProgramm(parent):
    c.wait_complete()
    c.auto(linuxcnc.AUTO_RUN, 0)
    c.wait_complete()
    print("STAARRTT!!")

def pauseSelectedProgramm(parent):
    c.wait_complete()
    c.auto(linuxcnc.AUTO_PAUSE)
    c.wait_complete()
    print("Paused!!")

def resumeSelectedProgramm(parent):
    c.wait_complete()
    c.auto(linuxcnc.AUTO_RESUME)
    c.wait_complete()
    print("Resume!!")

def homeAllAxis(parent):
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

def init_variables_start_server():
    # now setup our server
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/")
    server.set_server_name("FreeOpcUa Example Server")

    # setup our own namespace
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    myfolder = objects.add_folder(idx, "pocketnc")
    myobj = myfolder.add_object(idx, "PocketNC")
    # Use a breakpoint in the code line below to debug your script.
    try:
        s = linuxcnc.stat()  # create a connection to the status channel
        s.poll()  # get current values

        for x in dir(s):
            if not x.startswith('_') and not isinstance(getattr(s, x), (types.TypeType, types.ClassType, dict, tuple)):
                value = getattr(s, x)
                if isinstance(value, list) and len(value) > 0:
                    if isinstance(value[0], (types.TypeType, types.ClassType, dict, tuple)):
                        continue
                if x == 'poll':
                    continue
                variableMap[x] = myobj.add_variable(idx, x, value)
        startRunMethod = myobj.add_method(idx, "startSelectedProgramm", startSelectedProgramm)
        pauseRunMethod = myobj.add_method(idx, "pauseSelectedProgramm", pauseSelectedProgramm)
        resumeRunMethod = myobj.add_method(idx, "resumeSelectedProgramm", resumeSelectedProgramm)
        homeAll = myobj.add_method(idx, "homeAllAxis", homeAllAxis)
    except linuxcnc.error, detail:
        print "error", detail



def start_server():
    # starting!
    server.start()



def update_function():
    s = linuxcnc.stat()  # create a connection to the status channel
    s.poll()  # get current values

    for x in dir(s):
        if not x.startswith('_') and not isinstance(getattr(s, x), (types.TypeType, types.ClassType, dict, tuple)):
            value = getattr(s, x)
            if isinstance(value, list) and len(value) > 0:
                if isinstance(value[0], (types.TypeType, types.ClassType, dict, tuple)):
                    continue
            if x == 'poll':
                continue
            variableMap[x].set_value(value)

def update_loop():
    while True:
        update_function()
        time.sleep(1)
        print("Update")

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    print("Configure OPC Server")
    init_variables_start_server()
    print("Start OPC UA Server")
    start_server()
    print("Beginn update loop!")
    update_loop()

