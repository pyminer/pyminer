import threading
import subprocess
import time
import re
from typing import List
import logging

logger = logging.getLogger(__name__)

class Module(object):
    '''
    Notation:
    ---
    name: name
    version: 1.2.3
    ver_num: [1, 2, 3]
    relation: ==|>=|<=
    module_str: name==1.2.3
    requirement: name(==|>=|<=)1.2.3
    '''
    def __init__(self, module_str: str):
        if module_str.count('==') != 1:
            self.valid = False
            return
        module_str = module_str.strip()
        self.name, self.version = module_str.split('==')
        try:
            assert re.match('^[a-zA-Z][-_a-zA-Z0-9]*', self.name) is not None
            self.ver_num = self.parse(self.version)
        except ValueError:
            self.valid = False
            return
        self.requirements = []
        self.valid = True

    def meet_requirement_str(self, requirement: str) -> bool:
        requirement = requirement.strip()
        match = re.search(r'==|<=|>=', requirement)
        if match:
            relation = match.group(0)
            name, version = re.split(r'==|<=|>=', requirement)
            assert self.name == name
            return self.meet_requirement(relation, version)
        else:
            assert self.name == requirement
            return True

    def meet_requirement(self, relation: str, version: str):
        met = self._meet_requirement(relation, version)
        self.requirements.append((relation, version))  # in case error do not record
        return met

    def _meet_requirement(self, relation: str, version: str) -> bool:
        if version == self.version:
            return True
        elif relation == '==':
            return False
        else:
            cmp = self.version_compare(self.ver_num, self.parse(version))
            if relation == '>=':
                return cmp >= 0
            elif relation == '<=':
                return cmp <= 0
            else:
                raise ValueError(f'{relation} is not a valid relation')

    def is_conflict(self):
        for relation, version in self.requirements:
            if not self._meet_requirement(relation, version):  # do not record again
                return True
        else:
            return False

    def update(self, version: str):
        self.version, version = version, self.version
        self.ver_num, ver_num = self.parse(self.version), self.ver_num
        if self.is_conflict():
            self.version = version
            self.ver_num = ver_num
            raise Exception('Conflict with requirements')
        else:
            logger.error(f'{self.name} should be updated to {self.version}')
        
    def parse(self, version: str) -> List[int]:
        ver_match = re.search(r'\d+(\.\d+)*', version)
        if ver_match is None:
            raise ValueError(f'unsupported version {version}')
        ver = ver_match.group(0)
        try:
            return [int(i) for i in ver.split('.')]
        except:
            raise ValueError(f'invalid version {ver}')

    def version_compare(self, ver_num1: str, ver_num2: str) -> int:
        for v1, v2 in zip(ver_num1, ver_num2):
            if v1 > v2: 
                return 1
            elif v1 < v2:
                return -1
            else:
                continue
        return 0

    def __str__(self):
        if not self.valid:
            return 'invalid version'
        return f'{self.name}=={self.version}'
        
    __repr__ = __str__

class VersionsManager(object):
    def __init__(self):
        self.current_modules = {}
    
    def set_current_modules(self, current_modules_lst: List[str]):
        current_modules = [Module(module_str) for module_str in current_modules_lst if module_str]
        self.current_modules.update({module.name: module for module in current_modules if module.valid})

    def check_requirements(self, requirements: List[str]) -> set:
        solvable = set()  # requirements
        conflict = set()  # module names
        for requirement in requirements:
            name_version_tuple = re.split(r'==|<=|>=', requirement)
            name = name_version_tuple[0]
            if name not in self.current_modules:
                logger.error(f'No version {name} was found')
                solvable.add(requirement)
                continue
            module = self.current_modules[name]
            if not module.meet_requirement_str(requirement):
                try:
                    version = name_version_tuple[1]  # if not met, there must be version requirement
                    module.update(version)
                    solvable.add(requirement)
                except:
                    logger.error(f'Unsolved conflict in version {name}')
                    conflict.add(name)
        return solvable, conflict
