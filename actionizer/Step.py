from ArgumentCollection import ArgumentCollection

__author__ = 'cfe'


class Step(object):
    """
    Step is script that mimics function - has changeable ArgumentCollection,
    pre_conditions, may return result.etc.
    """

    def __init__(self):
        self.__make_empty()

    def __make_empty(self):
        self.type_name = "step"
        self.uid = ""
        self.returns = False  # returns value
        self.ArgumentCollection = ArgumentCollection()
        self.result = ArgumentCollection()
        self.pre_conditions = [None]
        self.script = ";"
        # ==================
        self.unpack_args_script = """
            alert(arguments);
            args = arguments[0];
            result = arguments[1];
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
                if key != "ArgumentCollection" and \
                                key != "result":
                    setattr(self, key, value)
                else:
                    attr_value = ArgumentCollection()
                    attr_value.from_list(value)
                    setattr(self, key, attr_value)
            else:
                print("Wrong argument '" +
                      key + "' in step '" + stepDict["uid"] + "'")

    def setArg(self, searchName, value):
        for arg in self.ArgumentCollection:
            if arg.name == searchName:
                arg.value = value
                return
        print("No such argument: " + searchName)

    def getArg(self, searchName):
        for arg in self.ArgumentCollection:
            if arg.name == searchName:
                return arg.value
        print("No such argument: " + searchName)


    def play(self, ps_app):
        # ArgumentCollection = self.__prepareArguments()

        if self.returns:
            # play action with return value
            ps_args = []
            ps_args.extend(self.ArgumentCollection.to_ps_arguments())
            ps_args.extend(self.result.to_ps_arguments())
            ps_app.DoJavaScript(
                self.unpack_args_script + self.script + self.return_script,
                ps_args
            )

            # get return_str and restore temp string
            return_str, new_name = ps_app.activeDocument.layers[0].name.split('%', 1)
            ps_app.activeDocument.layers[0].name = new_name

            result = self.__return_str_to_result(return_str)
            return result

        else:  # play action without return value
            ps_app.DoJavaScript(
                self.unpack_args_script + self.script,
                [self.returns, self.ArgumentCollection.to_list(), self.result.to_list()]
            )
            return 0

    def __return_str_to_result(self, return_str):
        """
        move to ArgumentCollection as def fromPsReturnStr(self, returnStr):
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
