import json

class VariableError(Exception):
    pass

class Variable:
    def __init__(self, members:dict={}):
        if self.__class__=='Variable':
            pass
        self.type = self.__class__.__name__
        self.__dict__.update(members)

    def create_var(self, vartype:str, members:dict):
        return type(vartype, (Variable,), {})(members)

    def load(self, dct:dict):
        if 'type' not in dct:
            raise VariableError('invalid json object')
        return self.create_var(dct['type'], dct)

    def loads(self, jsonstr:str):
        dct = json.loads(jsonstr)
        return self.load(dct)

    def dump(self):
        return self.__dict__

    def dumps(self):
        return json.dumps(self.__dict__)
