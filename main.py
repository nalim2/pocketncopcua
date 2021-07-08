# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import linuxcnc
import types

from opcua import ua, Server
import logging

variableMap = {}

def init_variables_start_server():
    # now setup our server
    server = Server()
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/")
    server.set_server_name("FreeOpcUa Example Server")

    # setup our own namespace
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    myfolder = objects.add_folder(idx, "myEmptyFolder")
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
    except linuxcnc.error, detail:
        print "error", detail

    # starting!
    server.start()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    init_variables_start_server()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
