__author__ = 'cfe'


class RemapList(object):
    CTRL = "^"
    ALT = "%"
    SHIFT = "+"

    def __init__(self):
        self.remap_list = {}
        self.remap_list["Alt+1"] = "%["
        self.remap_list["Alt+2"] = "%]"
        self.remap_list["Alt+Shift+1"] = "%+["
        self.remap_list["Alt+Shift+2"] = "%+]"
        self.remap_list["A"] = "%{[}"
        self.remap_list["S"] = "%{]}"
        self.remap_list["Ctrl+1"] = "^["
        self.remap_list["Ctrl+2"] = "^]"

    def add_remap(self, from_key, to_key):
        self.remove_remap(from_key)
        self.remap_list[from_key] = to_key

    def remove_remap(self, from_key):
        if from_key in self.remap_list[from_key]:
            del self.remap_list[from_key]
