from Arguments import Arguments

__author__ = 'cfe'


class Step(object):
    """
    Step is script that mimics function - has changeable arguments,
    pre_conditions, may return result.etc.
    """

    def __init__(self):
        self.__make_empty()

    def __make_empty(self):
        self.type_name = "step"
        self.uid = ""
        self.returns = False  # returns value
        self.arguments = Arguments()
        self.result = Arguments()
        self.pre_conditions = [None]
        self.script = ";"
        # ==================
        self.arg_script = """
            alert(arguments[0]);
            args = arguments[1];
            result = arguments[0];
        """
        # ==================
        self.return_script = """
            //var returnStr = result[0].toString() + ";";  // quantity;
            var returnStr = "";
            //index, value, name, type_name; i times, ending with '%'
            for (i = 0; i<result[0] ;i++){
                returnStr = returnStr.concat(
                    result[1][i].toString() + "," +
                    result[2][i].toString() + "," +
                    result[3][i].toString()
                )
            }
            returnStr = returnStr + "%"
            activeDocument.layers[0].name = returnStr + activeDocument.layers[0].name;
            alert(activeDocument.layers[0].name)
        """
        # ==================

    def from_dict(self, stepDict):
        """
        Clears step and Copies stepDict's values to self
        """
        self.__make_empty()
        for key, value in stepDict.items():
            if hasattr(self, key):
                if key != "arguments" and \
                                key != "result":
                    setattr(self, key, value)
                else:
                    attr_value = Arguments()
                    attr_value.from_list(value)
                    setattr(self, key, attr_value)
            else:
                print("Wrong argument '" +
                      key + "' in step '" + stepDict["uid"] + "'")

    def setArg(self, searchName, value):
        for arg in self.arguments:
            if arg.name == searchName:
                arg.value = value
                return
        print("No such argument: " + searchName)

    def getArg(self, searchName):
        for arg in self.arguments:
            if arg.name == searchName:
                return arg.value
        print("No such argument: " + searchName)


    def play(self, psApp):
        # arguments = self.__prepareArguments()

        if self.returns:
            # play action with return value
            psApp.DoJavaScript(
                self.arg_script + self.script + self.return_script,
                self.arguments.as_ps_arguments()
            )

            # get return_str and restore temp string
            return_str, new_name = psApp.activeDocument.layers[0].name.split('%', 1)
            psApp.activeDocument.layers[0].name = new_name

            result = self.__return_str_to_result(return_str)
            return result

        else:  # play action without return value
            psApp.DoJavaScript(
                self.arg_script + self.script,
                [self.returns, self.arguments.as_list(), self.result.as_list()]
            )
            return 0

    def __return_str_to_result(self, return_str):
        """
        move to Arguments as def fromPsReturnStr(self, returnStr):
        """
        b = return_str.split(";")
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
        return self.uid
