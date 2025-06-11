# имплементация стэка, где последний элемент уходит в никуда
class Stack:
    def __init__(self, size: int):
        self.stack = [0 for i in range(size)]

    def get_T(self):
        return self.stack[-1]

    def get_S(self):
        return self.stack[-2]

    def push(self, val):
        self.stack.append(val)
        self.stack.pop(0)

    def pop(self):
        top = self.stack[-1]
        self.stack.pop(-1)
        self.stack[0:0] = [0]
        return top

    def over(self):
        tmp = self.stack[-1]
        self.stack[-1] = self.stack[-2]
        self.stack[-2] = tmp
