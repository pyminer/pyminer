import copy
import json


class VariableError(Exception):
    pass


class Variable(dict):
    def __init__(self, vartype: str, members: dict):
        members['type'] = vartype
        self.type = vartype
        self.update(members)
        super(Variable, self).__init__()

    def load(self, dct: dict):
        if 'type' not in dct:
            raise VariableError('invalid json object')
        return Variable(dct['type'], dct)

    def loads(self, jsonstr: str):
        dct = json.loads(jsonstr)
        return self.load(dct)

    def dump(self):
        return copy.copy(self)

    def dumps(self):
        return json.dumps(self)
