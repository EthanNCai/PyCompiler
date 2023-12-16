import sys

"""
G[E]:
        E  →TE'
        E' →+TE'|ε
        T  →FT'
        T' →*FT'|ε
        F  →(E)|i
"""

ANALYSE_TABLE = {
    ('E', 'id'):    ['T', 'E_'],
    ('E', '('):     ['T', 'E_'],
    ('E_', '+'):    ['+', 'T', 'E_'],
    ('E_', ')'):    [],
    ('E_', 'EOF'):  [],
    ('T', 'id'):    ['F', 'T_'],
    ('T', '('):     ['F', 'T_'],
    ('T_', '+'):    [],
    ('T_', '*'):    ['*', 'F', 'T_'],
    ('T_', ')'):    [],
    ('T_', 'EOF'):  [],
    ('F', 'id'):    ['id'],
    ('F', '('):     ['(', 'E', ')'],
    ('E', ')'):     ['synch'],
    ('E', 'EOF'):   ['synch'],
    ('T', '+'):     ['synch'],
    ('T', ')'):     ['synch'],
    ('T', 'EOF'):   ['synch'],
    ('F', '+'):     ['synch'],
    ('F', '*'):     ['synch'],
    ('F', ')'):     ['synch'],
    ('F', 'EOF'):   ['synch'],
}

EXPECT = {
    'E': "'id' or '('",
    'E_': "'+' or ')' or 'EOF'",
    'T': "'id' or '('",
    'T_': "'+' or '*' or ')' or 'EOF'",
    'F': "'id' or '('"
}


class Parser2:
    def __init__(self, token_list):
        print(token_list)
        self.analyse_stack = Stack(['EOF', 'E'])
        self.input_stack = Stack([i[1] for i in reversed(token_list)])
        self.analysis_table = ANALYSE_TABLE
        self.position = 0

    def run(self):

        while not self.analyse_stack.is_accept():
            self.print_step()
            left = self.analyse_stack.peek()
            right = self.input_stack.peek()
            result = self.analysis_table.get((left, right))

            if result is not None or self.is_terminal(left):

                if result == ['synch']:
                    passed_non_term = self.analyse_stack.pop()
                    self.print_error_synch(passed_non_term, self.position, right, EXPECT[passed_non_term])
                elif self.is_terminal(left):
                    # 左边是终结符
                    self.analyse_stack.pop()
                    match = self.input_stack.pop()
                    self.position += 1
                    self.print_output_event(match)
                else:
                    # 左边是非终结符
                    self.analyse_stack.pop()
                    self.analyse_stack.push([i for i in reversed(result)])
                    self.print_match_event(left, ''.join(result))

            else:
                passed_sym = self.input_stack.pop()
                self.position += 1
                self.print_error_pass(passed_sym, self.position, passed_sym, EXPECT[left])

        print('ACCEPTED')

    @staticmethod
    def is_terminal(sym):
        return sym in ['(', ')', 'EOF', '+', '*', 'id']

    @staticmethod
    def is_non_terminal(sym):
        return sym in ['E', 'E_', 'T', 'T_', 'F']

    def print_step(self):

        stack = ' '.join(self.analyse_stack.stack)
        input_stack = ' '.join(reversed(self.input_stack.stack))
        output = f'{stack:<28}\t{input_stack:>28}'
        print(output, end='\t\t')

    @staticmethod
    def print_match_event(left, result):
        print("\033[33m输出\033[0m", end='')
        if result:
            print(left, '->', result)
        else:
            print(left, '-> ε')

    @staticmethod
    def print_output_event(non_terminal):
        print("\033[32m匹配\033[0m", end='')
        print(non_terminal)

    @staticmethod
    def print_error_synch(pass_non_terminal, position, current_token, expected):
        print("\033[31m出错，跳过非终结符\033[0m", end='')
        print(pass_non_terminal, end='')
        print(
            f" <错误信息：Error in position {position}: Unexpected token {current_token}, expected {expected}>")

    @staticmethod
    def print_error_pass(pass_sym, position, current_token, expected):
        print("\033[31m出错，跳过\033[0m", end='')
        print(pass_sym, end='')
        print(
            f" <错误信息：Error in position {position}: Unexpected token {current_token}, expected {expected}>")


class Stack:
    def __init__(self, initial_list):
        self.stack = initial_list

    def is_accept(self):
        return len(self.stack) == 1 and self.stack[0] == 'EOF'

    def push(self, item):
        self.stack += item

    def pop(self):
        if len(self.stack) == 0:
            raise IndexError("Stack is empty")
        return self.stack.pop()

    def peek(self):
        if len(self.stack) == 0:
            raise IndexError("Stack is empty")
        return self.stack[-1]
