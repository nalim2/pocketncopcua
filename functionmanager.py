customFeatures = {}


def createFunction(opcparent, ns, func, checkFinished, checkError, addtionalparams, name):
    functionObj = opcparent.add_object(ns, name)
    customFeatures[name] = {
        "functionName": name,
        "finished" : functionObj.add_variable(ns, "finished", 0),
        "start" :functionObj.add_variable(ns, "start", 0),
        "error": functionObj.add_variable(ns, "error", 0),
        "running": functionObj.add_variable(ns, "running", 0),
        "startFunc": func,
        "checkFinished": checkFinished,
        "checkError": checkError,
    }
    functionMapObj = customFeatures[name]
    functionMapObj["finished"].set_writable()
    functionMapObj["start"].set_writable()

    if addtionalparams:
        functionMapObj["params"] = {}
        paramObj = functionObj.add_object(ns, "params")
        for key in addtionalparams.keys():
            functionMapObj["params"][key] = paramObj.add_variable(ns, key, addtionalparams[key])
            functionMapObj["params"][key].set_writable()


def lifecycleFunction(hal_object, functionName):
    function = customFeatures[functionName]
    if function["running"].get_value():
        function["start"].set_value(False)
        function["finished"].set_value(False)
        if function["checkError"](hal_object, functionName):
            function["running"].set_value(False)
            function["error"].set_value(True)
        elif function["checkFinished"](hal_object, functionName):
            function["running"].set_value(False)
            function["finished"].set_value(True)
    elif function["start"].get_value() and not function["error"].get_value():
        function["start"].set_value(False)
        function["finished"].set_value(False)
        function["running"].set_value(True)
        function["startFunc"](hal_object, functionName)


def update_function_lifecycle(s):
    for key in customFeatures.keys():
        lifecycleFunction(s, key)