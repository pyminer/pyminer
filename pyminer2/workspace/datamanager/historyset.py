from pyminer2.workspace.datamanager.exceptions import NotFoundError


class HistoryError(Exception):
    pass


class DataHistory(list):
    def __init__(self, max_stack_num):
        super().__init__()
        self.max_stack_num = max_stack_num
        self.index = 0

    def push(self, var):
        for i in range(self.index):
            self.pop(0)
        self.index = 0
        self.insert(0, var)
        if len(self) > self.max_stack_num:
            self.pop(-1)

    def stepback(self, var):
        self.push(var)
        if self.index >= self.max_stack_num:
            raise HistoryError('stack bottom of history is reached')
        self.index += 1
        return self[self.index]

    def stepforward(self):
        if self.index <= 0:
            raise HistoryError('stack top of history is reached')
        self.index -= 1
        return self[self.index]


class HistorySet(dict):
    def __init__(self, max_stack_num=15):
        super().__init__()
        self.max_stack_num = max_stack_num

    def push(self, key: str, var):
        if key in self:
            history = self[key]
        else:
            history = DataHistory(self.max_stack_num)
            self[key] = history
        history.push(var)

    def stepback(self, key: str, var):
        if key not in self:
            raise NotFoundError(f'{key} not found in history')
        history = self[key]
        return history.stepback(var)

    def stepforward(self, key: str):
        if key not in self:
            raise NotFoundError(f'{key} not found in history')
        history = self[key]
        return history.stepforward()
