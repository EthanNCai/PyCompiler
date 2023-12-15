"""
G[E]:
        E  →TE'
        E' →+TE'|ε
        T  →FT'
        T' →*FT'|ε
        F  →(E)|i
"""


class Parser2:
    def __init__(self, token_list):
        self.analyse_stack = Stack(['EOF', 'E'])
        self.input_stack = Stack([i[1] for i in reversed(token_list)])
        self.analysis_table = {
            ('E', 'id'): ['T', 'E_'],
            ('E', '('): ['T', 'E_'],
            ('E_', '+'): ['+', 'E', 'T_'],
            ('E_', ')'): [],
            ('E_', 'EOF'): [],
            ('T', 'id'): ['F', 'T_'],
            ('T', '('): ['F', 'T_'],
            ('T_', '+'): [],
            ('T_', '*'): ['*', 'F', 'T_'],
            ('T_', ')'): [],
            ('T_', 'EOF'): [],
            ('F', 'id'): ['id'],
            ('F', '('): ['(', 'E', ')']
        }
        self.input_stack.print_stack()
        self.analyse_stack.print_stack()

    def run(self):
        while not self.analyse_stack.is_accept():
            left = self.analyse_stack.peek()
            right = self.input_stack.peek()
            result = self.analysis_table[(left, right)]

    @staticmethod
    def is_terminal(sym):
        return sym in ['(', ')', 'EOF', '+', '*', 'id']


class Stack:
    def __init__(self, initial_list):
        self.stack = initial_list

    def is_accept(self):
        return len(self.stack) == 1 and self.stack[0] == 'EOF'

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0:
            raise IndexError("Stack is empty")
        return self.stack.pop()

    def peek(self):
        if len(self.stack) == 0:
            raise IndexError("Stack is empty")
        return self.stack[-1]

    def print_stack(self):
        for ch in self.stack:
            print(ch, end='')
        print()
