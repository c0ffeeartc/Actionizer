from Argument import Argument

__author__ = 'cfe'


class ArgumentCollection(object):
    """
    Container for Argument objects, with helpful functionality for convertion to
    plain lists and psArguments
    """

    def __init__(self):
        self.__make_empty()

    def __make_empty(self):
        self.arg_collection = []
        self.type_name = "ArgumentCollection"

    def add(self, *arg_objs):
        for arg_obj in arg_objs:
            if arg_obj.type_name == "number" or \
                    arg_obj.type_name == "string" or \
                    arg_obj.type_name == "bool":
                self.arg_collection.append(arg_obj)

    def from_list(self, arg_plain_list):
        self.__make_empty()
        for argPlain in arg_plain_list:
            arg_obj = Argument()
            arg_obj.from_list(argPlain)
            self.arg_collection.append(arg_obj)

    def to_list(self):
        if self.arg_collection:
            argument_list = [len(self.arg_collection)]
            for arg_object in self.arg_collection:
                argument_list.append(arg_object.value)
                argument_list.append(arg_object.type_name)
                argument_list.append(arg_object.name)
            return argument_list
        else:
            return []

    def to_ps_arguments(self):
        ps_args = [len(self.arg_collection)]
        ps_args.extend([argObj.to_list() for argObj in self.arg_collection])
        return ps_args
