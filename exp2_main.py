from Lexer import DFA
from Parser import Parser

"""
G[E]:
        E  →TE'
        E'→+TE'|ε
        T  →FT'
        T'→*FT'|ε
        F  →(E)|i
"""

start_state = 'START'
accept_state = 'ACCEPT'


with open("exp2_tests/test8.txt", "r") as file:
    input_string = file.read()

dfa = DFA(start_state, accept_state)

token_list = []

print("\033[31m-- Original --\033[0m")
print(input_string)

print("\033[32m-- Lexer part --\033[0m")

i = 0
while i < len(input_string):
    dfa.run(input_string[i])
    if dfa.current_state == accept_state:
        token_list.append(dfa.conclude())
        dfa.refresh()
    else:
        i += 1
        if i == len(input_string):
            dfa.run(input_string[i-1])
            token_list.append(dfa.conclude())
            dfa.refresh()
token_list.pop()
token_list.append((-1, "EOF"))
print('(-1,"EOF")')

# ========================================================#

print()
print("\033[33m-- Parser part--\033[0m")

parser = Parser(token_list)
parser.run()
