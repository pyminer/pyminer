from pyminer2.workspace.datamanager.exceptions import NotFoundError


class RecycleBin(list):
    """
    回收站，数据类型为(key, value)。
    使用discard方法将对象移入回收站，再使用restore方法将对象移出回收站。
    """

    def __init__(self, max_size=1000):
        super().__init__()
        self.max_size = max_size

    def get_varname(self, index: int):
        if index >= len(self):
            raise NotFoundError(f'{index} out of limit')
        return self[index][0]

    def discard(self, varname: str, variable):
        self.append((varname, variable))
        if len(self) > self.max_size:
            self.pop(0)

    def restore(self, index: int, var_to_discard=None) -> tuple:
        # for the case where variables with same name
        # exist in workspace and recycle bin, if you
        # restore the variable in recycle bin, you have
        # to discard the variable in the workspace
        if index >= len(self):
            raise NotFoundError(f'{index} out of limit')
        varname, var_to_restore = self[index]
        self.pop(index)
        if var_to_discard is not None:
            self.discard(varname, var_to_discard)
        return varname, var_to_restore
