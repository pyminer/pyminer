from pyminer2.workspace.datamanager.exceptions import ConflictError


class DataSet(dict):
    """
    这个类主要用于对变量进行管理，包括以下内容：
    * 添加内置类型，定义新的类型
    * 对变量根据类型进行校核，支持递归校核
    """

    def __init__(self):
        super().__init__()
        self.__insert_builtin_type__('Type', {'type': 'Type', 'structure': {
            'structure': 'dict',
        }})
        # TODO (panhaoyu) 把这种基本数据类型进行如此的定义，性能不会受影响吗？
        # TODO (panhaoyu) 内置数据类型是否过多？
        self.__insert_builtin_type__('Complex', {'type': 'Type', 'structure': {
            'real': 'float',
            'imag': 'float',
        }})
        self.__insert_builtin_type__('Matrix', {'type': 'Type', 'structure': {
            'value': [['float|int|Complex']],
        }})
        self.__insert_builtin_type__('Vector', {'type': 'Type', 'structure': {
            'value': ['float|int|Complex'],
        }})
        self.__insert_builtin_type__('TimeSeries', {'type': 'Type', 'structure': {
            'time': ['float|int'],
            'data': ['float|int'],
        }})
        self.__insert_builtin_type__('StateSpace', {'type': 'Type', 'structure': {
            'A': 'Matrix',
            'B': 'Matrix',
            'C': 'Matrix',
            'D': 'Matrix',
            'x': ['str'],
            'y': ['str'],
            'u': ['str'],
            'sys': 'str',
        }})
        self.__insert_builtin_type__('DataFrame', {'type': 'Type', 'structure': {
            'table': [['float|int|Complex|str']],
            'columns': ['str'],
        }})

        # TODO (panhaoyu) series与矩阵有什么区别呢？
        self.__insert_builtin_type__('Series', {'type': 'Type', 'structure': {
            'value': [['float|int|Complex|str']],
        }})
        self.builtin_types = self.select_type('Type')

    def __insert_builtin_type__(self, key: str, obj: dict):
        self[key] = obj

    def write(self, key: str, obj: dict):
        assert isinstance(key, str)
        assert key.isidentifier()
        if key in self.builtin_types:
            raise ConflictError('conflict variable name')
        assert self.is_valid(obj)
        self[key] = obj

    def read(self, key: str) -> dict:
        return self[key]

    def synchronise(self, key: str, obj: dict):
        self[key] = obj

    def is_valid(self, obj: dict) -> bool:
        # noinspection PyBroadException
        try:
            obj_type = obj['type']
            type_def = self[obj_type]
            structure = type_def['structure']
            self.compare(obj, structure)
        except Exception:
            return False
        else:
            return True

    def compare(self, obj, structure) -> None:
        """
        用于判断某个对象是否符合给定的结构。
        目标结构可以是以下内容：
            字典：递归检则每一个键是否符合要求
            列表：检测列表对象中的每一项是否都是给定的结构
            字符串：
                字符串内包含“|”分割符：表示可能是以下类型之一
                字符串是int,float,str,list,dict中的一种：检测对象是否是相应的Python类型
                其他字符串：从内置类型列表中查询该类型并进行检测
        :param obj: 待检测的对象
        :param structure: 目标结构
        :return: 无返回值，如果比较失败则报错
        """
        if isinstance(structure, dict):
            for key in structure:
                req_val = structure[key]
                obj_val = obj[key]
                self.compare(obj_val, req_val)
        elif isinstance(structure, list):
            req_type = structure[0]
            for item in obj:
                self.compare(item, req_type)
        else:
            assert isinstance(structure, str)
            if '|' in structure:
                valid = False
                for sub_structure in structure.split('|'):
                    try:
                        self.compare(obj, sub_structure)
                        valid = True
                    except AssertionError:
                        pass
                assert valid
            elif structure in ('list', 'dict', 'float', 'int', 'str'):
                assert type(obj).__name__ == structure
            else:
                assert isinstance(obj, dict) and obj.get('type', '') == structure
                type_def = self[structure]
                structure = type_def['structure']
                self.compare(obj, structure)

    def select_type(self, type_name: str):
        # TODO (panhaoyu) 这个函数的意义何在？请补充注释
        dct = {}
        for key, value in self.items():
            if value['type'] == type_name:
                dct[key] = value
        return dct
