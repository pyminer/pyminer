import re

from pyminer2.workspace.datamanager.variable import Variable
from pyminer2.workspace.datamanager.exceptions import ConflictError


class VarSet(dict):

    def insert_builtin_types(self, builtin_types: dict):
        self.update(builtin_types)

    def get_var(self, varname: str):
        return self[varname]

    def set_var(self, varname: str, variable):
        assert re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', varname)
        if varname in self and isinstance(
                self[varname], Variable) and self[varname].type == 'Type':
            raise ConflictError(f'{varname} is a builtin type')
        else:
            self[varname] = variable
