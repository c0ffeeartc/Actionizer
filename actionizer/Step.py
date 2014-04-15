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
        self.pre_conditions = [None]
        self.arg_dict = {"hasReturn": False}
        self.script = ";"

    def set_arg(self, key, value):
        if key in self.arg_dict.keys():
            self.arg_dict[key] = value
            return
        print("No such argument: " + key)

    def get_arg(self, key):
        if key in self.arg_dict.keys:
            return self.arg_dict[key]
        print("No such argument: " + key)

    def play(self, ps_app):
        py_args_to_javascript_script = """
        var num_args = arguments[0];
        var num_arg_parts = (arguments.length-1)/num_args;
        args = {}
        for (var i = 0; i < arguments.length - num_arg_parts; i +=  num_arg_parts ){
            var key = arguments[i+1];
            var value = arguments[i+2];
            args[key] = value;
        }
        """
        return_script = """
            if(args.hasReturn)
            {
                if (step_result!=null && typeof (step_result) === 'object')
                {
                    returnStr = step_result.toSource() + "%";
                }
                else
                {
                    returnStr = {none:null}.toSource() + "%";
                }
                activeDocument.layers[0].name = returnStr + activeDocument.layers[0].name;
            }
        """
        # TODO: think how to suspend history into one history step ps_app.suspendHistory(self.uid, javascript_str)
        # ps_app.SuspendHistory(self.uid,
        #                       py_args_to_javascript_script +
        #                       ";app.DoJavaScript(" + self.script + return_script +
        #                       ", args);")
        ps_app.DoJavaScript(
            py_args_to_javascript_script + self.script + return_script,
            self.__ps_args_from_arg_dict()
        )
        if self.arg_dict["hasReturn"]:
            result_source_str = ps_app.activeDocument.layers[0].name.split("%", 1)[0]
            print(self.__py_dict_from_ps_source_str(result_source_str))
            layer_name = ps_app.activeDocument.layers[0].name.split("%", 1)[1]
            ps_app.activeDocument.layers[0].name = layer_name
        return 0

    def __ps_args_from_arg_dict(self):
        ps_args = [len(self.arg_dict)]
        for key, value in self.arg_dict.items():
            ps_args.append(key)
            ps_args.append(value)
        return ps_args

    @staticmethod
    def __py_dict_from_ps_source_str(ps_obj_to_source_str):
        """
        Returns python object converted from javascript object.toSource() result string
        """
        py_dict = {}
        keys_values_str = ps_obj_to_source_str[2:-2]
        key_semicolon_value_array = keys_values_str.split(',')

        for key_semicolon_value_str in key_semicolon_value_array:
            key_str_with_spaces, value_str = key_semicolon_value_str.split(':')
            key_str = str(key_str_with_spaces.replace(" ", ""))

            value = None
            if value_str[0] == '"':  # if starts with " then is str
                value = str(value_str[1:-1])
            elif value_str == "undefined" or value_str == "null":
                value = None
            elif value_str == "false":
                value = False
            elif value_str == "true":
                value = True
            elif '.' in value_str:  # if has decimal point then float
                value = float(value_str)
            elif value_str == str(int(value_str)):  # if converts to int without losses then int
                value = int(value_str)

            py_dict[key_str] = value
        return py_dict
