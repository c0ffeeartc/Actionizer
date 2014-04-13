from Argument import Argument

__author__ = 'cfe'

# str can be compared with str
# bool comparison with others is not decided yet
# Note: doesn't work yet
class Condition(object):
    """
    if statement specifier for conditinal execution of stepCollections
    a, b intended to be either string, number, bool or one of these from PS parameter
    """

    def __init__(
            self,
            a=Argument(),
            op="do",
            b=Argument(),
    ):
        self.type_name = "condition"
        self.stepA = None
        self.stepB = None
        self.a = a  # Arguments
        self.b = b  # Arguments
        self.op = op
        #self.compareFlags = {
        #    "quantity": True,
        #    "value": True,
        #    "name": False,
        #    "type_name": True,
        #    }
        self.resultFlags = {
            "quantity": None,
            "value": None,
            "name": None,
            "type_name": None,
        }

    def __initResultFlags(self):
        for key in self.checkFlags.keys():
            if self.checkFlags[key] is False:
                self.resultFlags[key] = True
            else:
                self.resultFlags[key] = False

    def __checkResultFlags(self):
        for value in self.resultFlags.values():
            if value is False:
                return False
        return True

    # TODO: add typeMatch(a,b) quantityMatch(a, b)
    def evaluate(self):
        return True
        ## Getting returns from steps
        #if self.stepA:
        #    self.a = self.stepA.play()

        #if self.stepB:
        #    self.b = self.stepB.play()

        ## check A to B validity
        #if self.a.type_name != self.b.type_name:
        #    print ("Quantity mismatch in condition.")
        #    return None
        #else:
        #    for i, type_nameA in enumerate(self.a[2]):
        #        if type_nameA != self.b[2][i]:
        #            print ("Type mismatch in condition.")
        #            return None

        # skip check
        if self.op == "do":
            return True

        # ======= comparision operations ===============
        if self.op == "eq":
            if self.a == self.b:
                return True

        if self.op == "le":  # less  equal
            if self.a <= self.b:
                return True

        if self.op == "be":  # bigger or equal
            if self.a >= self.b:
                return True

        if self.op == "ne":  # not equal
            if self.a != self.b:
                return True

        if self.op == "b":  # bigger
            if self.a > self.b:
                return True

        if self.op == "l":  # less
            if self.a < self.b:
                return True
        # END of :===== comparision operations ===============

        ## Not result
        #if self.n:
        #    if result:
        #        result = False
        #    else:
        #        result = True
        print ("Wrong conditional operation.")
        return None
