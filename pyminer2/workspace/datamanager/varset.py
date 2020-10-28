from pyminer2.workspace.datamanager.variable import Variable
from pyminer2.workspace.datamanager.exceptions import ConflictError


class VarSet(dict):
    """
    这个类是对于字典进行的扩展。
    主要功能是添加了get_var和set_var两个函数。
    """

    def insert_builtin_types(self, builtin_types: dict):
        # TODO (panhaoyu) 基于pycharm的索引没能找到调用，是否说明该功能已弃用？
        self.update(builtin_types)

    def __getitem__(self, item: str):
        # TODO (panhaoyu) 这个类需要类型提示
        return super(VarSet, self).__getitem__(item)

    def __setitem__(self, key: str, value):
        assert isinstance(key, str)
        assert key.isidentifier()
        if key in self and isinstance(self[key], Variable) and self[key].type == 'Type':
            raise ConflictError(f'{key} is a builtin type')
        else:
            super(VarSet, self).__setitem__(key, value)

    def get_var(self, key: str):
        return self[key]

    def set_var(self, value: str, variable):
        self[value] = variable
