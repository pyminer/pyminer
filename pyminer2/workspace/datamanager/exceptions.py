class ConflictError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ConvertError(Exception):
    """用于在数据类型无法转换时进行报错"""
    # TODO (panhaoyu) 建议改成ConvertError
    # 由于改动涉及其他模块，需要在合并后的一个绝对安全的情况下进行修改
    pass


class WouldBlockError(Exception):
    # TODO (panhaoyu) 建议改成DataBlockedError
    pass
