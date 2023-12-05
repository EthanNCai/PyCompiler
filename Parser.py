class Parser:
    def __init__(self, token_list, debug):
        self.token_list = token_list
        self.token_list_iterator = iter(token_list)
        self.current_token = next(self.token_list_iterator)
        self.position = 0
        self.debug = debug

    def report_error(self, expected):
        print(f"Error in position {self.position}: Unexpected token {self.current_token}, expected {expected}")
        exit(1)

    def run(self):
        if self.E() and self.current_token is None:
            print("Accepted")
        else:
            self.report_error('+ or *')
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
            else:
                return False
        else:
            self.report_error("i or (")
            return False

    def E_(self):
        if self.debug:
            print('E_', end='->')
        elif self.current_token and self.current_token[0] == 3:  # '+' token
            self.advance()  # Consume '+'
            if self.T():
                if self.E_():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True
            # ε production

    def T(self):
        if self.debug:
            print('T', end='->')
        if self.F():
            if self.T_():
                return True
            else:
                return False
        else:
            return False

    def T_(self):
        if self.debug:
            print('T_', end='->')
        if self.current_token and self.current_token[0] == 5:  # '*' token
            self.advance()  # Consume '*'
            if self.F():
                if self.T_():
                    return True
            return False
        else:
            # ε production
            return True

    def F(self):
        if self.debug:
            print('F', end='->')
        if self.current_token and self.current_token[0] == 13:  # '(' token
            self.advance()  # Consume '('
            if self.E():
                if self.current_token and self.current_token[0] == 14:  # ')' token
                    self.advance()  # Consume ')'
                    return True
                else:
                    self.report_error(")")
            else:
                self.report_error("expression")
        elif self.current_token and self.current_token[0] == 1:  # 'i' token
            self.advance()  # Consume 'i'
            return True
        else:
            self.report_error("'(' or id")
