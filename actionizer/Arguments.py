from Argument import Argument

__author__ = 'cfe'


class Arguments(object):
    """
    Container for Argument objects, with helpful functionality for convertion to
    plain lists and psArguments
    """

    def __init__(self):
        self.__make_empty()

    def __make_empty(self):
        self.arg_objs = []
        self.type_name = "arguments"

    def add(self, *arg_objs):
        for arg_obj in arg_objs:
            if arg_obj.type_name == "number" or \
                    arg_obj.type_name == "string" or \
                    arg_obj.type_name == "bool":
                self.arg_objs.append(arg_obj)

    def from_list(self, arg_plain_list):
        self.__make_empty()
        for argPlain in arg_plain_list:
            arg_obj = Argument()
            arg_obj.from_list(argPlain)
            self.arg_objs.append(arg_obj)

    def as_list(self):
        if self.arg_objs:
            arguments = [len(self.arg_objs)]
            for argObj in self.arg_objs:
                arguments.append(argObj.value)
                arguments.append(argObj.type_name)
                arguments.append(argObj.name)
            return arguments
        else:
            return []

    def as_ps_arguments(self):
        ps_args = [len(self.arg_objs)]
        ps_args.append([argObj.to_list() for argObj in self.arg_objs])
        return ps_args
