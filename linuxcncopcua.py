import inspect
import linuxcnc
import types

from functionmanager import *
from functions.cnchoming import *
from functions.createfilefunction import *
from functions.movecnctorobotremove import *
from functions.selectandstartprogram import *

from main import variableMap, server, startSelectedProgramm, pauseSelectedProgramm, resumeSelectedProgramm, setModeMDI, \
    setModeAuto, setModeManual, setMoveRobotRemovePos

pythonMethodMembers = ["clear",
                        "copy",
                        "fromkeys",
                        "get",
                        "items",
                        "keys",
                        "pop",
                        "popitem",
                        "setdefault",
                        "setdefault",
                        "update",
                        "values",
                        "count",
                        "index",
                        "has_key",
                        "iteritems",
                        "iterkeys",
                        "itervalues",
                        "viewitems",
                        "viewkeys",
                        "viewvalues",
                        "poll"]


def add_entry_to_model(ns, newKey, opcname, opcobject, value):
    print "func", inspect.isfunction(value), "meth", inspect.ismethod(
        value), "methDesc", inspect.ismethoddescriptor(
        value), "dataDesc", inspect.isdatadescriptor(value), "frame", inspect.isframe(
        value), "abstract", inspect.isabstract(
        value), "gen", inspect.isgenerator(value), "class", inspect.isclass(value), \
        "buildIn", inspect.isbuiltin(value), "code", inspect.iscode(
        value), "memberDesc", inspect.ismemberdescriptor(value), \
        "getset", inspect.isgetsetdescriptor(value), "routine", inspect.isroutine(
        value), "trace", inspect.istraceback(value), \
        "module", inspect.ismodule(value)
    if isinstance(value, (dict, types.TypeType, types.ClassType)):
        print "addDictionary:", newKey, value
        variableMap[newKey] = opcobject.add_object(ns, opcname)
        print dir(value)
        for dicKey in value.keys():
            if not dicKey.startswith('_') and dicKey not in pythonMethodMembers and not inspect.isroutine(
                    value[dicKey]) and not inspect.isbuiltin(value[dicKey]):
                add_entry_to_model(ns, str(dicKey) + "-" + newKey, dicKey, variableMap[newKey], value[dicKey])
    elif isinstance(value, list):
        print "addList:", newKey, value
        if len(value) > 0:
            if isinstance(value[0], (dict, tuple)):
                variableMap[newKey] = opcobject.add_object(ns, opcname)
                for listElement in value:
                    add_layer_to_model(ns, newKey, variableMap[newKey], listElement)
            else:
                variableMap[newKey] = opcobject.add_variable(ns, opcname, value)
    elif isinstance(value, (tuple)):
        print "addTuple:", newKey, value
        variableMap[newKey] = opcobject.add_object(ns, opcname)
        add_layer_to_model(ns, newKey, variableMap[newKey], value)

    else:
        print "addSimpleTo", ns, opcobject
        print "addSimpleValue", newKey, value
        if "tool_result" in str(value):
            print "tool_result has to be skipped/only displayed as string for now", str(value)
            variableMap[newKey] = opcobject.add_variable(ns, opcname, str(value))
        else:
            variableMap[newKey] = opcobject.add_variable(ns, opcname, value)


def add_object_layer_to_model(ns, key, opcobject, layerobject):
    for x in dir(layerobject):
        newKey = x + "-" + key
        value = getattr(layerobject, x)
        if not x.startswith('_') and x not in pythonMethodMembers and not inspect.isroutine(value) and not inspect.isbuiltin(value):
            add_entry_to_model(ns, newKey, str(x), opcobject, value)


def add_layer_to_model(ns, key, opcobject, layerobject):
    if isinstance(layerobject, (tuple)):
        print "TupleValues", len(layerobject), layerobject
        counter = 0
        newKey = str(counter) + "-" + key
        for entry in layerobject:
            add_entry_to_model(ns, newKey, str(counter), opcobject, entry)
            counter = counter + 1
    else:
        add_object_layer_to_model(ns, key, opcobject, layerobject)


def update_entry_to_model( newKey, value):
    if isinstance(value, (dict, types.TypeType, types.ClassType)):
        for dicKey in value.keys():
            if not dicKey.startswith('_') and dicKey not in pythonMethodMembers and not inspect.isroutine(
                    value[dicKey]) and not inspect.isbuiltin(value[dicKey]):
                update_entry_to_model(str(dicKey) + "-" + newKey, value[dicKey])
    elif isinstance(value, list):
        if len(value) > 0:
            if isinstance(value[0], (dict, tuple)):
                for listElement in value:
                    update_layer_to_model( newKey, listElement)
            else:
                variableMap[newKey].set_value(value)
    elif isinstance(value, (tuple)):
        update_layer_to_model( newKey, value)

    else:
        if "tool_result" in str(value):
            variableMap[newKey].set_value(str(value))
        else:
            variableMap[newKey].set_value(value)


def update_object_layer_to_model( key, layerobject):
    for x in dir(layerobject):
        newKey = x + "-" + key
        value = getattr(layerobject, x)
        if not x.startswith('_') and x not in pythonMethodMembers and not inspect.isroutine(value) and not inspect.isbuiltin(value):
            update_entry_to_model( newKey,  value)


def update_layer_to_model( key, layerobject):
    if isinstance(layerobject, (tuple)):
        counter = 0
        newKey = str(counter) + "-" + key
        for entry in layerobject:
            update_entry_to_model( newKey, entry)
            counter = counter + 1
    else:
        update_object_layer_to_model( key, layerobject)


def update_layer( key, layerobject):
    update_object_layer_to_model(key, layerobject)


def start_server():
    # starting!
    server.start()


def init_variables_start_server():
    s = linuxcnc.stat()  # create a connection to the status channel
    s.poll()  # get current values
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
    variableMap["counter"] = myobj.add_variable(idx, "counter", 0)
    # Use a breakpoint in the code line below to debug your script.
    try:
        s = linuxcnc.stat()  # create a connection to the status channel
        s.poll()  # get current values
        add_object_layer_to_model(idx, "", myobj, s)
        customFunc = myfolder.add_object(idx, "CustomFunc")
        startRunMethod = customFunc.add_method(idx, "startSelectedProgramm", startSelectedProgramm)
        pauseRunMethod = customFunc.add_method(idx, "pauseSelectedProgramm", pauseSelectedProgramm)
        resumeRunMethod = customFunc.add_method(idx, "resumeSelectedProgramm", resumeSelectedProgramm)
        homeAll = customFunc.add_method(idx, "homeAllAxis", homeAllAxis)
        setModeMDIF = customFunc.add_method(idx, "setModeMDI", setModeMDI)
        setModeAutoF = customFunc.add_method(idx, "setModeAuto", setModeAuto)
        setModeMANUALF = customFunc.add_method(idx, "setModeManual", setModeManual)
        moveRobotRemovePos = customFunc.add_method(idx, "setMoveRobotRemovePos", setMoveRobotRemovePos)
        createFunction(customFunc, idx, startHomingFunc, checkFinishedHomed, checkErrorHomed, {}, "Home")
        createFunction(customFunc, idx, startGoToRobotRemovePositionFunc, checkFinishedGoToRobotRemovePosition,
                       checkErrorGoToRobotRemovePosition, {}, "RobotRemovePos")

        createFunction(customFunc, idx, startCreateFileFunc, checkFinisedCreateFile, checkErrorCreateFile, {"FileContent": "Testdigga", "ProgrammName": "/home"}, "WriteNCFile")
        createFunction(customFunc, idx, startNCProgrammFunc, checkFinisedNCProgramm, checkErrorNCProgramm,
                       {"ProgrammName": ""}, "startProgram")

    except linuxcnc.error, detail:
        print "error", detail


def update_function():
    variableMap["counter"].set_value(variableMap["counter"].get_value() + 1)

    s = linuxcnc.stat()  # create a connection to the status channel
    s.poll()  # get current values
    update_function_lifecycle(s)
    update_layer("", s)


