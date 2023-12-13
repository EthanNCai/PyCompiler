from Lexer import TOKEN_DICT


class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.token_list_iterator = iter(token_list)
        self.current_token = next(self.token_list_iterator)
        self.position = 0
        self.isError = False

    def print_error(self, expected):
        self.isError = True
        print(
            f"Error in position {self.position}: Unexpected token {self.current_token}, expected {expected}")

    def run(self):
        self.S()
        if not self.isError:
            print('Accepted!')

    def match(self, token):

        if token == self.current_token[1]:

            self.current_token = next(self.token_list_iterator, None)
            self.position += 1
            return True
        else:
            return False

    def drop_input(self):
        self.current_token = next(self.token_list_iterator, None)

    def S(self):
        EXPECT = "EOF"
        while True:
            if self.E():
                self.match('EOF')
                return True
            else:
                self.print_error(EXPECT)
                # Error Recovery
                self.drop_input()

    def E(self):
        FOLLOW = [')', 'EOF']
        SYNCH = [')', 'EOF']
        EXPECT = 'EOF'
        if self.T():
            if self.E_():
                return True

    def E_(self):

        FOLLOW = [')', 'EOF']
        SYNCH = []
        EXPECT = "'+' or ')' or 'EOF'"

        while True:
            # +TE':
            if self.match('+'):
                if self.T():
                    if self.E_():
                        return True
            # ε
            elif self.current_token[1] in FOLLOW:
                return True
            # Error Recovery
            else:
                self.print_error(EXPECT)
                if self.current_token[1] in SYNCH:
                    return True
                else:
                    self.drop_input()

    def T(self):
        FOLLOW = ['+', ')', 'EOF']
        SYNCH = ['+', ')', 'EOF']

        # FT':
        if self.F():
            if self.T_():
                return True

    def T_(self):
        FOLLOW = ['+', ')', 'EOF']
        SYNCH = []
        EXPECT = "'*' or '+' or ')' or 'EOF'"
        while True:
            # *FT':
            if self.match('*'):
                if self.F():
                    if self.T_():
                        return True
            # ε
            elif self.current_token[1] in FOLLOW:
                return True
            # Error Recovery
            else:
                self.print_error(EXPECT)
                # Error Recovery
                if self.current_token[1] in SYNCH:
                    return True
                else:
                    self.drop_input()

    def F(self):
        FOLLOW = ['+', '*', ')', 'EOF']  # unused
        SYNCH = ['+', '*', ')', 'EOF']
        EXPECT = "'(' or 'id'"
        while True:
            # (E) :
            if self.match('('):
                if self.E():
                    if self.match(')'):
                        return True
            # i :
            elif self.match('id'):
                return True
            # Error Recovery
            else:
                self.print_error(EXPECT)
                # Error Recovery
                if self.current_token[1] in SYNCH:
                    return True
                else:
                    self.drop_input()
