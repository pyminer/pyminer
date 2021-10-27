import json
import os
import utils

class DataManager:
    instance=None
    def __init__(self):
        try:
            with open(os.path.join(utils.get_root_dir(),'configuration','settings.json'),encoding='utf-8') as f:
                self.data=json.load(f)
        except:
            self.data={}
    def set(self,key,value):
        self.data[key]=value
    def remove(self,key):
        del self.data[key]
    def get(self,key):
        return self.data[key]
    def __del__(self):
        with open(os.path.join(utils.get_root_dir(),'configuration','settings.json'),encoding='utf-8') as f:
            json.dump(self.data,f)

    def __new__(cls):
        if cls.instance:
            return cls.instance
        else:
            return object.__new__(DataManager)