from DFA import DFA

start_state = 'START'
accept_state = 'ACCEPT'

with open("code1.txt", "r") as file:
    input_string = file.read()

dfa = DFA(start_state, accept_state)


# input_string = 'func:=nicer;"hello",{nidcer}dwad'


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
            dfa.conclude()
