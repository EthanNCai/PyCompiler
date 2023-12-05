from Lexer import DFA

start_state = 'START'
accept_state = 'ACCEPT'

with open("exp1_tests/code1_e.txt", "r") as file:
    input_string = file.read()

dfa = DFA(start_state, accept_state)

i = 0

while i < len(input_string):
    # print(input_string[i], dfa.current_state)
    dfa.run(input_string[i])
    if dfa.current_state == accept_state:
        dfa.conclude()
        dfa.refresh()
    else:
        i += 1
        if i == len(input_string):
            dfa.run(input_string[i-1])
            dfa.conclude()
            dfa.refresh()
