__author__ = 'cfe'


class Step(object):
    """
    Step is script that mimics function - has changeable argument_collection,
    pre_conditions, may return result.etc.
    """

    type_name = ""
    uid = ""
    arg_dict = ""
    script = ""
    file_path_name = ""
    pre_conditions = []

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
        args = {};
        for (var i = 0; i < arguments.length - num_arg_parts; i +=  num_arg_parts ){
            var key = arguments[i+1];
            var value = arguments[i+2];
            args[key] = value;
        }
        """
        return_script = """
            if(typeof (step_result)!= "undefined" && typeof (step_result) === "object") {
                returnStr = step_result.toSource();
            } else {
                returnStr = {}.toSource();
            }
        """
        # convert strings to fix bug
        a = py_args_to_javascript_script.encode('string_escape')
        b = self.script.encode('string_escape')
        c = return_script.encode('string_escape')

        ps_source_str = "({})"
        try:

            ps_source_str = ps_app.DoJavaScript(
                "returnStr = {}.toSource();\nif(app.documents.length != 0)\n{app.activeDocument.suspendHistory(\n'" +
                self.uid + "', '" + a + b + c + "'),\n returnStr;}",
                self.__ps_args_array_from_arg_dict(),
                1  # PsJavaScriptExecutionMode: 1 (psNeverShowDebugger), 2 (psDebuggerOnError), 3 (psBeforeRunning)
            )

        # except pywintypes.com_error:
        #     ps_app.DoJavaScript("alert('Error in script:" + b + "');")
        finally:
            result_py_dict = Step.__py_dict_from_ps_source_str(ps_source_str)
            return result_py_dict

    def __ps_args_array_from_arg_dict(self):
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

        if not keys_values_str:
            return py_dict

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
