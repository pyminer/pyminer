import re
# from pyminer2.workspace.datamanager.exceptions import ConflictError


class DataSet(dict):
    def __init__(self):
        super().__init__()
        self.__insert_builtin_type__(
            'Type', {
                'type': 'Type', 'structure': {
                    'structure': 'dict'}})
        self.__insert_builtin_type__(
            'Complex', {
                'type': 'Type', 'structure': {
                    'real': 'float', 'imag': 'float'}})
        self.__insert_builtin_type__(
            'Matrix', {
                'type': 'Type', 'structure': {
                    'value': [
                        ['float|int|Complex']]}})
        self.__insert_builtin_type__(
            'Vector', {
                'type': 'Type', 'structure': {
                    'value': ['float|int|Complex']}})
        self.__insert_builtin_type__(
            'TimeSeries', {
                'type': 'Type', 'structure': {
                    'time': ['float|int'], 'data': ['float|int']}})
        self.__insert_builtin_type__(
            'StateSpace', {
                'type': 'Type',
                'structure': {'A': 'Matrix',
                            'B': 'Matrix',
                            'C': 'Matrix',
                            'D': 'Matrix',
                            'x': ['str'],
                            'y': ['str'],
                            'u': ['str'],
                            'sys': 'str'}})
        self.__insert_builtin_type__(
            'DataFrame', {
                'type': 'Type',
                'structure': {'table': [['float|int|Complex|str']],
                            'columns': ['str'],}})
        self.__insert_builtin_type__(
            'Series', {
                'type': 'Type',
                'structure': {'value': [['float|int|Complex|str']]}})
        self.builtin_types = self.select_type('Type')

    def __insert_builtin_type__(self, key: str, obj: dict):
        self[key] = obj

    def write(self, key: str, obj: dict):
        assert re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', key)
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

    def compare(self, obj, req):
        if isinstance(req, dict):
            for key in req:
                req_val = req[key]
                obj_val = obj[key]
                self.compare(obj_val, req_val)
        elif isinstance(req, list):
            req_type = req[0]
            for item in obj:
                self.compare(item, req_type)
        else:
            assert isinstance(req, str)
            if '|' in req:
                valid = False
                for sub_req in req.split('|'):
                    try:
                        self.compare(obj, sub_req)
                        valid = True
                    except AssertionError:
                        pass
                assert valid
            elif req in ('list', 'dict', 'float', 'int', 'str'):
                assert type(obj).__name__ == req
            else:
                assert isinstance(obj, dict) and obj.get('type', '') == req
                type_def = self[req]
                structure = type_def['structure']
                self.compare(obj, structure)

    def select_type(self, type_name: str):
        dct = {}
        for varname, variable in self.items():
            if variable['type'] == type_name:
                dct[varname] = variable
        return dct


def main():
    dataSet = DataSet()
    mat = {'type': 'Matrix', 'value': [[1, 2, 3], [3, 2, 1]]}
    nonmat = {'type': 'Matrix', 'value': [1, 2, 3, 3, 2, 1]}
    ts = {'type': 'TimeSeries', 'time': [1, 2, 3], 'data': [3, 2, 1]}
    nonts = {'type': 'TimeSeries', 'time': [1, 2, 3], 'mdata': [3, 2, 1]}
    ss = {'type': 'statespace',
          'A': {'type': 'Matrix', 'value': [[1, 2], [2, 1]], },
          'B': {'type': 'Matrix', 'value': [[2], [1]], },
          'C': {'type': 'Matrix', 'value': [[1, 2]], },
          'D': {'type': 'Matrix', 'value': [[0]], },
          'x': ['x1', 'x2'], 'y': ['column'], 'u': ['u'], 'sys': 'str'}
    nonss = {'type': 'StateSpace',
             'A': {'type': 'TimeSeries', 'time': [1, 2, 3], 'mdata': [3, 2, 1]},
             'B': {'type': 'Matrix', 'value': [[2], [1]], },
             'C': {'type': 'Matrix', 'value': [[1, 2]], },
             'D': {'type': 'Matrix', 'value': [[0]], },
             'x': ['x1', 'x2'], 'y': ['y'], 'u': ['u'], 'sys': 'str'}
    # print(dataSet.is_valid(mat))
    # print(dataSet.is_valid(nonmat))
    # print(dataSet.is_valid(ts))
    # print(dataSet.is_valid(nonts))
    # print(dataSet.is_valid(ss))
    # print(dataSet.is_valid(nonss))
    # print(dataSet.is_valid(dataSet['Matrix']))
    # print(dataSet.is_valid(dataSet['Type']))

    import variable
    matvar = variable.Variable('Matrix', mat)
    print(matvar, matvar.__dict__)
    print(matvar.dump())
    # noinspection PyBroadException
    try:
        dataSet.write('mat', matvar.dump())
    except BaseException:
        print('error')
    else:
        print('valid')


if __name__ == "__main__":
    main()
