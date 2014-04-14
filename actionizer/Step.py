from ArgumentCollection import ArgumentCollection
import json

__author__ = 'cfe'


class Step(object):
    """
    Step is script that mimics function - has changeable argument_collection,
    pre_conditions, may return result.etc.
    """

    def __init__(self):
        self.__make_empty()

    def __make_empty(self):
        self.type_name = "step"
        self.uid = ""
        self.arg_dict = {"hasReturn": False}
        self.pre_conditions = [None]
        self.script = ";"
        # =================================================================
        self.unpack_args_script = """
        var num_args = arguments[0];
        var num_arg_parts = 2; //(arguments.length-1)/num_args;
        args = {}
        for (var i = 0; i < arguments.length - num_arg_parts; i +=  num_arg_parts ){
            var key = arguments[i+1];
            var value = arguments[i+2];
            args[key] = value;
        }
        """
        # =================================================================
        self.return_script = """
            //alert(activeDocument.layers[0].name)
            if(args.hasReturn){
                returnStr = result.toSource() + "%"
                activeDocument.layers[0].name = returnStr + activeDocument.layers[0].name;
                alert(activeDocument.layers[0].name)
            }
        """
        # ==================

    def from_builtin(self, stepDict):
        """
        Clears step and Copies stepDict's values to self
        """
        self.__make_empty()
        for key, value in stepDict.items():
            if hasattr(self, key):
                if key == "argument_collection" or key == "result":
                    attr_value = ArgumentCollection()
                    attr_value.from_list(value)
                    setattr(self, key, attr_value)
                else:
                    setattr(self, key, value)
            else:
                print("Wrong argument '" +
                      key + "' in step '" + stepDict["uid"] + "'")

    def set_arg(self, key, value):
        if key in self.arg_dict.keys():
            self.arg_dict[key] = value
            return
        print("No such argument: " + key)

    def get_arg(self, key):
        if key in self.arg_dict.keys:
            return self.arg_dict[key]
        print("No such argument: " + key)

    def arg_dict_to_ps_args(self):
        ps_args = [len(self.arg_dict)]
        for key, value in self.arg_dict.items():
            ps_args.append(key)
            ps_args.append(value)
        return ps_args

    def play(self, ps_app):
        ps_app.DoJavaScript(
            self.unpack_args_script + self.script + self.return_script,
            self.arg_dict_to_ps_args()
        )
        if self.arg_dict["hasReturn"]:
            # print(ps_app.activeDocument.layers[0].name)
            obj_str = ps_app.activeDocument.layers[0].name.split("%", 1)[0]
            layer_name = ps_app.activeDocument.layers[0].name.split("%", 1)[1]
            ps_app.activeDocument.layers[0].name = layer_name
            print(obj_str)
        return 0

    def __return_str_to_result(self, return_str):
        """
        move to argument_collection as def fromPsReturnStr(self, returnStr):
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
