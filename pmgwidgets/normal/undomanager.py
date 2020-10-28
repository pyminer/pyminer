class Stack():
    def __init__(self, stack_size: int = 10):
        self.pointer: int = 0
        self.content = []
        self.stack_size = stack_size

    def push(self, obj):
        self.content.append(obj)

    def pop(self):
        self.content.pop()


class UndoManager():
    def __init__(self, stack_size: int = 10):
        self.pointer: int = 0
        self.content = []
        self.stack_size = stack_size

    def push(self, obj):
        """
        压栈时指向栈顶，这里就是撤销时候的逻辑。
        :param obj:
        :return:
        """
        self.content.append(obj)
        if len(self.content) > self.stack_size:
            self.content.pop(0)
        self.pointer = len(self.content) - 1

    def undo(self) -> object:
        if 0 < self.pointer <= len(self.content)-1:
            self.pointer -= 1
            return self.content[self.pointer]
        else:
            if len(self.content) > 0:
                self.pointer = 0
                return self.content[0]
            else:
                return None

    def redo(self) -> object:
        if 0 <= self.pointer < len(self.content)-1:
            self.pointer += 1
            return self.content[self.pointer]
        else:
            if len(self.content) > 0:
                self.pointer = len(self.content) - 1
                return self.content[self.pointer]
            else:
                return None
if __name__=='__main__':
    manager  = UndoManager()
    manager.push('a')
    manager.push('ab')
    manager.push('abc')
    manager.push('ab')
    manager.push('abd')
    manager.push('abde')
    manager.push('abdef')
    manager.push('abdefg')
    print(manager.undo())
    print(manager.undo())
    manager.push('abdefgh')
    print(manager.content)
    print(manager.undo())
    print(manager.undo())
    print(manager.redo())
    print(manager.redo())