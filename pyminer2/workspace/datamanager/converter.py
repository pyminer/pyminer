import numpy as np
import pandas as pd
from pyminer2.workspace.datamanager.variable import Variable


class ConverterError(Exception):
    pass


class Converter:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def convert_to_data(self, var) -> dict:
        typename = type(var).__name__
        convert_func = f'convert_{typename.lower()}'
        if hasattr(self, convert_func):
            return getattr(self, convert_func)(var)
        elif isinstance(var, Variable):
            return var.dump()
        else:
            raise ConverterError(f'{var} is inconvertible')

    def convert_to_var(self, data: dict):
        assert self.data_manager.dataset.is_valid(data)
        var = Variable(data['type'], data)
        try:
            # in case any error which means unsupported type
            iconvert_func = f'iconvert_{data["type"].lower()}'
            return getattr(self, iconvert_func)(var)
        except BaseException:
            # no valid converter
            return var

    # convert to data, func format: convert_obj

    def convert_ndarray(self, arr: np.ndarray) -> dict:
        if arr.dtype in (np.int, np.float):
            if len(arr.shape) == 2:
                return Variable('Matrix', {'value': arr.tolist()}).dump()
            elif len(arr.shape) == 1:
                return Variable('Vector', {'value': arr.tolist()}).dump()
        else:
            raise ConverterError(f'{arr} is inconvertible')

    def convert_list(self, lst: list) -> dict:
        return self.convert_ndarray(np.array(lst))

    def convert_dataframe(self, dataframe: pd.DataFrame) -> dict:
        return Variable('DataFrame', {'table': dataframe.values.tolist(), 'columns': dataframe.columns})

    # convert to var, func format: iconvert_type

    def iconvert_matrix(self, mat: Variable) -> np.ndarray:
        assert mat.type == 'Matrix'
        return np.array(mat['value'])

    def iconvert_vector(self, vec: Variable) -> np.ndarray:
        assert vec.type == 'Vector'
        return np.array(vec['value'])

    def iconvert_dataframe(self, dataframe: Variable) -> pd.DataFrame:
        assert dataframe.type == 'DataFrame'
        return pd.DataFrame(dataframe['table'], columns=dataframe['columns'])


def main():
    c = Converter()
    arr = np.array([[1, 2, 3], [3, 2, 1]])
    mat = c.convert_to_data(arr)
    print(mat)

    arr1 = c.convert_to_var(mat)
    print(arr1, type(arr1))


if __name__ == "__main__":
    main()