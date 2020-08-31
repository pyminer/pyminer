import json, re
from exceptions import ConflictError

class DataSet(dict):
    def __init__(self):
        self.__insert_builtin_type__('type', {'type':'type', 'structure':{'structure':'dict'}})
        self.__insert_builtin_type__('complex', {'type':'type', 'structure':{'real':'float', 'imag':'float'}})
        self.__insert_builtin_type__('matrix', {'type':'type', 'structure':{'value':[['float']]}})
        self.__insert_builtin_type__('cmatrix', {'type':'type', 'structure':{'value':[['complex']]}})
        self.__insert_builtin_type__('timeseries', {'type':'type', 'structure':{'time':['float'],'data':['float']}})
        self.__insert_builtin_type__('statespace',{'type':'type', 'structure':{'A':'matrix','B':'matrix','C':'matrix','D':'matrix', 'x':['str'], 'y':['str'], 'u':['str'], 'sys':'str'}})
        self.builtin_types = self.select_type('type')

    def __insert_builtin_type__(self, key:str, obj:dict):
        self[key] = obj

    def write(self, key:str, value:str):
        assert re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', key)
        if key in self.builtin_types:
            raise ConflictError('conflict variable name')
        obj = json.loads(value)
        assert self.is_valid(obj)
        self[key] = obj

    def read(self, key:str)->str:
        return json.dumps(self[key])

    def synchronise(self, key:str, obj:dict):
        self[key] = obj

    def is_valid(self, obj:dict)->bool:
        try:
            obj_type = obj['type']
            type_def = self[obj_type]
            structure = type_def['structure']
            self.compare(obj, structure)
        except Exception as e:
            return False
        else:
            return True

    def compare(self, obj, req):
        if type(req) is dict:
            for key in req:
                req_val = req[key]
                obj_val = obj[key]
                self.compare(obj_val, req_val)
        elif type(req) is list:
            req_type = req[0]
            for item in obj:
                self.compare(item, req_type)
        elif req in ('list', 'dict', 'float', 'int', 'str'):
            assert type(obj).__name__==req or (type(obj) is int and req=='float')
        else:
            assert obj['type']==req
            type_def = self[req]
            structure = type_def['structure']
            self.compare(obj, structure)
            
    def select_type(self, type_name:str):
        dct = {}
        for varname, variable in self.items():
            if variable['type']==type_name:
                dct[varname] = variable
        return dct

def main():
    dataSet = DataSet()
    mat = {'type':'matrix', 'value':[[1,2,3],[3,2,1]]}
    nonmat = {'type':'matrix', 'value':[1,2,3,3,2,1]}
    ts = {'type':'timeseries', 'time':[1,2,3], 'data':[3,2,1]}
    nonts = {'type':'timeseries', 'time':[1,2,3], 'mdata':[3,2,1]}
    ss = {'type':'statespace', 
        'A':{'type':'matrix','value':[[1,2],[2,1]],},
        'B':{'type':'matrix','value':[[2],[1]],},
        'C':{'type':'matrix','value':[[1,2]],},
        'D':{'type':'matrix','value':[[0]],}, 
        'x':['x1','x2'], 'y':['y'], 'u':['u'], 'sys':'str'}
    nonss = {'type':'statespace', 
        'A':{'type':'timeseries','time':[1,2,3], 'mdata':[3,2,1]},
        'B':{'type':'matrix','value':[[2],[1]],},
        'C':{'type':'matrix','value':[[1,2]],},
        'D':{'type':'matrix','value':[[0]],}, 
        'x':['x1','x2'], 'y':['y'], 'u':['u'], 'sys':'str'}
    print(dataSet.is_valid(mat))
    print(dataSet.is_valid(nonmat))
    print(dataSet.is_valid(ts))
    print(dataSet.is_valid(nonts))
    print(dataSet.is_valid(ss))
    print(dataSet.is_valid(nonss))
    print(dataSet.is_valid(dataSet['matrix']))
    print(dataSet.is_valid(dataSet['type']))

    import variable
    v = variable.Variable()
    matvar = v.loads(json.dumps(mat))
    print(matvar, matvar.__dict__)
    print(matvar.dumps())
    try:
        dataSet.write('mat', matvar.dumps())
    except:
        print('error')
    else:
        print('valid')

if __name__ == "__main__":
    main()