from dict import TOKEN_DICT, HINT_DICT


class DFA:
    def __init__(self, start_state, accept_states):
        self.transitions = {
            'START': self.state_start,
            'INID': self.state_inid,
            'INNUM': self.state_innum,
            'BEFASS': self.state_befass,
            'INCOMM': self.state_incomm,
            'COMMEND': self.state_commend,
            'INCHAR': self.state_inchar,
            'OTHER': self.state_other,
            'DONEA': self.state_donea,
            'DONEB': self.state_doneb,
            'INASS': self.state_inass,
            'BEFCUR': self.state_befcur,
            'BEFICUR': self.state_beficur
        }
        self.start_state = start_state
        self.current_state = start_state
        self.accept_states = accept_states
        self.state_changed = False
        self.buffer = []
        self.hint = ""

    def run(self, symbol_):
        if self.current_state == self.accept_states:
            return
        target_state = self.transitions[self.current_state](symbol_)
        self.state_changed = self.current_state != target_state
        self.current_state = target_state

    def conclude(self):
        string = ''.join(self.buffer)
        if string not in [" ", "\n", "\t"]:
            token = self.lookup_for_token(string)
            print(
                f'({"ERROR, " if self.hint == "ERROR" else ""}{token}, "{string}")')

    def refresh(self):
        self.buffer.clear()
        self.current_state = 'START'
        self.hint = ""

    def set_current_state(self, state):
        self.current_state = state

    def lookup_for_token(self, string_in):
        if self.hint:
            if self.hint == "ID" and string_in in TOKEN_DICT:
                return TOKEN_DICT[string_in]
            else:
                return HINT_DICT[self.hint]
        else:
            return TOKEN_DICT[string_in]

    # 以下都是 STATE METHOD
    # 实际意义是 DFA 的跳转逻辑

    def state_start(self, symbol_in):

        self.buffer.append(symbol_in)
        if symbol_in.isalpha():
            return 'INID'
        elif symbol_in.isdigit():
            return 'INNUM'
        elif symbol_in in ["+", "-", "*", "/", "(", ")", ";", "[", "]", "=", ","]:
            return 'DONEA'
        elif symbol_in == ":":
            return 'BEFASS'
        elif symbol_in == "{":
            return 'INCOMM'
        elif symbol_in == "\"":
            return 'INCHAR'
        elif symbol_in == "<":
            return 'BEFCUR'
        elif symbol_in == ">":
            return 'BEFICUR'
        else:
            return 'OTHER'

    def state_inid(self, symbol_in):
        self.hint = "ID"
        if symbol_in.isalnum():
            self.buffer.append(symbol_in)
            return 'INID'
        else:
            return 'ACCEPT'

    def state_innum(self, symbol_in):
        self.hint = "INT"
        if symbol_in.isdigit():
            self.buffer.append(symbol_in)
            return 'INNUM'
        else:
            return 'ACCEPT'

    def state_inchar(self, symbol_in):
        if symbol_in.isalnum():
            self.buffer.append(symbol_in)
            return 'INCHAR'
        elif symbol_in == "\"":
            self.buffer.append(symbol_in)
            return 'DONEB'
        else:
            self.hint = "ERROR"
            return 'ACCEPT'

    def state_donea(self, symbol_in):
        return 'ACCEPT'

    def state_doneb(self, symbol_in):
        self.hint = "STRING"
        return 'ACCEPT'

    def state_befass(self, symbol_in):
        if symbol_in == "=":
            self.buffer.append(symbol_in)
            return 'INASS'
        else:
            self.hint = "ERROR"
            return 'ACCEPT'

    def state_other(self, symbol_in):
        self.hint = "ERROR"
        return 'ACCEPT'

    def state_incomm(self, symbol_in):
        if symbol_in.isalnum():
            self.buffer.append(symbol_in)
            return 'INCOMM'
        elif symbol_in == "}":
            self.buffer.append(symbol_in)
            return 'COMMEND'

    def state_inass(self, symbol_in):
        return 'ACCEPT'

    def state_commend(self, symbol_in):
        self.hint = "COMMENT"
        return 'ACCEPT'

    def state_befcur(self, symbol_in):
        if symbol_in == ">":
            self.buffer.append(symbol_in)
            return 'ACCEPT'
        elif symbol_in == "=":
            self.buffer.append(symbol_in)
            return 'ACCEPT'
        else:
            return 'ACCEPT'

    def state_beficur(self, symbol_in):
        if symbol_in == "=":
            self.buffer.append(symbol_in)
            return 'ACCEPT'
        else:
            return 'ACCEPT'
