from Arguments import Arguments

__author__ = 'cfe'


class Step(object):
    """
    Step is script that mimics function - has changeable arguments,
    preRequisites, may return result.etc.
    """

    def __init__(self):
        self.__makeEmpty()

    def __makeEmpty(self):
        self.typename = "step"
        self.Uid = ""
        self.returns = False  # returns value
        self.arguments = Arguments()
        self.result = Arguments()
        self.preConditions = [None]
        self.script = ";"
        # ==================
        self.argScript = """
            args = arguments[1];
            result = arguments[2];
        """
        # ==================
        self.returnScript = """
            //var returnStr = result[0].toString() + ";";  // quantity;
            var returnStr = "";
            //index, value, name, typename; i times, ending with '%'
            for (i = 0; i<result[0] ;i++){
                returnStr = returnStr.concat(
                    result[1][i].toString() + "," +
                    result[2][i].toString() + "," +
                    result[3][i].toString() + ";";
                )
            }
            returnStr = returnStr + "%"
            activeDocument.layers[0].name = returnStr + activeDocument.layers[0].name;
            alert(activeDocument.layers[0].name)
        """
        # ==================

    def fromDict(self, stepDict):
        """
        Clears step and Copies stepDict's values to self
        """
        self.__makeEmpty()
        for key, value in stepDict.items():
            if hasattr(self, key):
                if key != "arguments" or \
                                key != "result":
                    setattr(self, key, value)
                else:
                    setattr(self, key, Arguments().fromList(value))
            else:
                print ("Wrong argument '" +
                       key + "' in step '" + stepDict["Uid"] + "'")

    def setArg(self, searchName, value):
        for arg in self.arguments:
            if arg.name == searchName:
                arg.value = value
                return
        print ("No such argument: " + searchName)

    def getArg(self, searchName):
        for arg in self.arguments:
            if arg.name == searchName:
                return arg.value
        print ("No such argument: " + searchName)


    def play(self, psApp):
        arguments = self.__prepareArguments()

        if self.returns:  # returns value
            # play action with return value
            psApp.DoJavaScript(
                self.argScript + self.script + self.returnScript,
                arguments
            )

            # get returnStr and restore temp string
            returnStr, newName = psApp.activeDocument.layers[0].name.split('%', 1)
            psApp.activeDocument.layers[0].name = newName

            result = self.__returnStrToResult(returnStr)
            return result

        else:  # play action without return value
            psApp.DoJavaScript(
                self.argScript + self.script,
                [self.returns, self.arguments.asList(), self.result.asList()]
            )
            return 0

    # move to Arguments as def fromPsReturnStr(self, returnStr):
    def __returnStrToResult(self, returnStr):
        b = returnStr.split(";")
        c = [int(b[0]), [], [], []]
        for i in xrange(c[0]):
            if (b[i + 1].split(",")[2] == "string"):
                c[1].append(b[i + 1].split(",")[0])
            elif (b[i + 1].split(",")[2] == "number"):
                c[1].append(float(b[i + 1].split(",")[0]))
            c[2].append(b[i + 1].split(",")[1])
            c[3].append(b[i + 1].split(",")[2])
        return c

    def __repr__(self):
        return self.Uid
