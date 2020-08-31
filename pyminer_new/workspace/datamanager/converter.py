import numpy as np
from variable import Variable

class ConverterError(Exception):
    pass

class Converter:
    def __init__(self):
        self.convertible_var = {
            'ndarray': self.convert_ndarray_to_matrix,
        }
        self.convertible_data = {
            'matrix': self.convert_matrix_to_ndarray,
        }
        self.v = Variable()

    def convert_to_data(self, var)->dict:
        typename = type(var).__name__
        if typename in self.convertible_var:
            return self.convertible_var[typename](var)
        elif isinstance(var, Variable):
            return var.dump()
        else:
            raise ConverterError(f'{var} is inconvertible')

    def convert_to_var(self, data:dict):
        # firstly check if it is valid
        # this requires datamanager
        # assume it is valid
        var = self.v.create_var(data['type'], data)
        if data['type'] in self.convertible_data:
            return self.convertible_data[data['type']](var)
        else:
            # no valid converter
            return var

    def convert_ndarray_to_matrix(self, arr:np.ndarray)->dict:
        if arr.dtype in (np.int, np.float) and len(arr.shape)==2:
            return self.v.create_var('matrix', {'value':arr.tolist()}).dump()
        else:
            raise ConverterError(f'{arr} is inconvertible')

    def convert_matrix_to_ndarray(self, mat:Variable):
        assert type(mat).__name__=='matrix'
        return np.array(mat.value)

def main():
    c = Converter()
    arr = np.array([[1,2,3],[3,2,1]])
    mat = c.convert_to_data(arr)
    print(mat)

    arr1 = c.convert_to_var(mat)
    print(arr1, type(arr1))

if __name__ == "__main__":
    main()
