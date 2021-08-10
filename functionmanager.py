customFeatures = {}

def createNamespace(ns, identifier):
    return 'ns=' + str(ns) +';s=' + identifier +';'

def createFunction(opcparent, ns, func, checkFinished, checkError, addtionalparams, name):
    functionObj = opcparent.add_object(ns, name)
    customFeatures[name] = {
        "functionName": name,
        "finished" : functionObj.add_variable(createNamespace(ns, name + ".finished"), "finished", 0),
        "reset": functionObj.add_variable(createNamespace(ns, name + ".reset"), "reset", 0),
        "start" :functionObj.add_variable(createNamespace(ns, name + ".start"), "start", 0),
        "error": functionObj.add_variable(createNamespace(ns, name + ".error"), "error", 0),
        "running": functionObj.add_variable(createNamespace(ns, name + ".running"), "running", 0),
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
            functionMapObj["params"][key] = paramObj.add_variable(createNamespace(ns, name + ".params." + key), key, addtionalparams[key])
            functionMapObj["params"][key].set_writable()

def lifecycleFunction(hal_object, functionName):
    function = customFeatures[functionName]
    try:
        if function["running"].get_value() :
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
        elif function["reset"].get_value():
            function["reset"].set_value(False)
            function["start"].set_value(False)
            function["error"].set_value(False)
            function["running"].set_value(False)
            function["finished"].set_value(False)


    except Exception as e:
        print ("Error while Execution: (0)".format(e))
        function["reset"].set_value(False)
        function["running"].set_value(False)
        function["error"].set_value(True)
        function["finished"].set_value(False)




def update_function_lifecycle(s):
    for key in customFeatures.keys():

        lifecycleFunction(s, key)