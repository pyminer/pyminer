class QssTools(object):
    """
    定义一个读取样式的工具类
    """

    @classmethod
    def set_qss_to_obj(cls, file_path, obj):
        with open(file_path, 'r') as f:
            obj.setStyleSheet(f.read())
