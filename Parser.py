class Parser:
    def __init__(self, token_list, debug):
        self.token_list = token_list
        self.token_list_iterator = iter(token_list)
        self.current_token = next(self.token_list_iterator)
        self.position = 0
        self.debug = debug

    def report_error(self, expected):
        print(f"Error in position {self.position}: Unexpected token {self.current_token}, expected {expected}")
        exit(0)

    def run(self):

        if self.E() and self.current_token[0] == -1:
            print("Accepted")
        else:
            print("Rejected")

    def advance(self):

        self.current_token = next(self.token_list_iterator, None)
        self.position += 1

    def E(self):
        if self.debug:
            print('E', end='->')
        if self.T():
            if self.E_():
                return True
        return False

    def E_(self):

        follow_E_ = [14, -1]  # [), $]
        if self.debug:
            print('E_', end='->')

        # +TE':
        if self.current_token and self.current_token[0] == 3:  # '+' token
            self.advance()  # Consume '+'
            if self.T():
                if self.E_():
                    return True

        # ε
        elif self.current_token and self.current_token[0] in follow_E_:
            return True
        self.report_error("'+' <E_1>")
        return False

    def T(self):
        if self.debug:
            print('T', end='->')

        # FT':
        if self.F():
            if self.T_():
                return True
        return False

    def T_(self):
        follow_T_ = [3, 14, -1]  # [+, ), $]
        if self.debug:
            print('T_', end='->')

        # *FT':

        if self.current_token and self.current_token[0] == 5:  # '*' token
            self.advance()  # Consume '*'
            if self.F():
                if self.T_():
                    return True
            return False
        # ε
        elif self.current_token and self.current_token[0] in follow_T_:
            return True
        self.report_error("'*' <T_1>")
        return False

    def F(self):
        if self.debug:
            print('F', end='->')

        # (E) :
        if self.current_token and self.current_token[0] == 13:  # '(' token
            self.advance()  # Consume '('
            if self.E():
                if self.current_token and self.current_token[0] == 14:  # ')' token
                    self.advance()  # Consume ')'
                    return True
                else:
                    self.report_error(") <F1>")
                    return False
            else:
                return False
        # i :
        elif self.current_token and self.current_token[0] == 1:  # 'i' token
            self.advance()  # Consume 'i'
            return True
        else:
            self.report_error("( or i <F3>")
            return False
