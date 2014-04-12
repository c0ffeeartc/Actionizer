__author__ = 'cfe'


class Container(object):
    # Class is Not used yet
    def __init__(self):
        self.nodes = []
        pass

    def add(self, node):
        self.nodes.append(node)

    def remove(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
