from typing import Tuple, Union, Any, Type, Container

ERROR_INVALID_TYPE = 'Parameter or Variable'
TYPE_RANGE = Tuple[Union[int, float], Union[int, float]]


def iter_isinstance(iter, elem_cls) -> bool:
    """
    检查可迭代变量是否为iter_type指定的类型。
    :param iter: 
    :param elem_cls: 
    :return: 
    """
    for item in iter:
        if not isinstance(item, elem_cls):
            return False
    return True


def assert_in(elem: Any, container: Container):
    """
    判断元素elem是否在container中。
    Args:
        elem:
        container:

    Returns:

    """
    assert elem in container, 'Element {0} not in Container {1}'.format(elem, container)


def assert_not_in(elem, container: Container):
    """
    判断元素elem是否在container中。
    Args:
        elem:
        container:

    Returns:

    """
    assert elem not in container, 'Element {0} in Container {1}'.format(elem, container)


class ErrorReporter():
    @staticmethod
    def create_invalid_parameter_value_message(param_name: str, param_value: Any):
        return 'Parameter \'%s\' value %s is not allowed.' % (param_name, str(param_value))

    @staticmethod
    def create_invalid_parameter_type_message(param_name, param_type, expected_type) -> Any:
        return 'Parameter \'%s\' type %s is not allowed.Expected type is %s' % (
            param_name, str(param_type), str(expected_type))

    @staticmethod
    def create_invalid_variable_value_message(variable_name, variable_value):
        return 'Parameter \'%s\' value %s is not allowed.' % (variable_name, variable_value)

    @staticmethod
    def create_file_not_found_error(file: str):
        if file != '':
            return FileNotFoundError('File \'%s\' not found!' % file)
        else:
            return FileNotFoundError('File name is empty.')

    @staticmethod
    def create_type_error(name: str, value: Any, type_expected: Union[Type[Any], str]):
        typ = type(value)
        return TypeError(
            'Variable \'%s\' is expected to be an instance of %s, but actually it was an instance of %s' % (
                name, str(type_expected), str(typ)))
