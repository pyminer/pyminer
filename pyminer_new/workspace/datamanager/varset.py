from variable import Variable
from exceptions import ConflictError

class VarSet(dict):

    def insert_builtin_types(self, builtin_types:dict):
        self.update(builtin_types)

    def get_var(self, varname:str):
        return self[varname]

    def set_var(self, varname:str, variable):
        if varname in self and isinstance(self[varname], Variable) and self[varname].type=='type':
            raise ConflictError(f'{varname} is a builtin type')
        else:
            self[varname] = variable
