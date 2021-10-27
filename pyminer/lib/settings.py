import os
import json

class Setting:
    """用于读写pyminer系统信息"""

    def __init__(self):
        self.setting_path = os.path.join(os.path.dirname(__file__), 'settings.json')
        assert os.path.exists(self.setting_path)
        with open(self.setting_path,'r',encoding='utf-8') as f:
            self.system_info=json.load(f)

    def get_system_info(self):
        return self.system_info

    def get_system_version(self):
        """获取系统版本"""
        return self.system_info['core']['version']

    def set_system_version(self,version:str):
        """设置系统版本"""
        self.system_info['core']['version']=version

    def save(self):
        with open(self.setting_path, 'w',encoding='utf-8') as f:
            json.dump(self.system_info, f,ensure_ascii=False,indent=4, separators=(',', ': ')) # 确保中文能正确显示，且不是只在一行


if __name__ == '__main__':
    setting=Setting()
    print(setting.get_system_version())
    setting.set_system_version('1.0.3')
    setting.save()


