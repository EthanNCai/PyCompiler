grammar1 = {
    'E': (['T', 'E_'],),
    'E_': (['+', 'T', 'E_'], ['ε'],),
    'T': (['F', 'T_'],),
    'T_': (['*', 'F', 'T_'], ['ε'],),
    'F': (['(', 'E', ')'], ['id'],)
}

LL1_ANALYSE_TABLE = dict()

first = {'E': {'(', 'id'}, 'E_': {'ε', '+'}, 'T': {'(', 'id'},
         'T_': {'ε', '*'}, 'F': {'(', 'id'}}

follow = {'E': {')', 'EOF'}, 'E_': {')', 'EOF'}, 'T': {
    '+', ')', 'EOF'}, 'T_': {'+', ')', 'EOF'}, 'F': {'+', '*', ')', 'EOF'}}

NON_TERMINATOR_LIST = ['E', 'E_', 'T', 'T_', 'F']
TERMINATORS_LIST = ['+', '*', '(', ')', 'id']
NULLABLE_NON_TERMINATORS = ['E_', 'T_']


def find_first(target_non_terminator, current_non_terminator):
    first = set()
    decisions = grammar1.get(current_non_terminator)
    for decision in decisions:
        first_sym = decision[0]
        if first_sym in NON_TERMINATOR_LIST:
            first.update(find_first(target_non_terminator, first_sym))
            # 递归寻找related的非终结符
        else:
            first.add(first_sym)
            # 在递归的途中收集见到的满足first集合的元素
    return first


def find_decision_first(decision):
    first_sym = decision[0]
    if first_sym in TERMINATORS_LIST:
        return set([first_sym])
    else:
        return find_first(first_sym, first_sym)


def insert_item(non_terminator, terminator, decision):
    LL1_ANALYSE_TABLE[(terminator, non_terminator)] = decision


def table_constructer():
    for non_terminator, decisions in grammar1.items():
        for decision in decisions:

            if decision == ['ε']:
                for terminator in follow[non_terminator]:
                    LL1_ANALYSE_TABLE[(non_terminator, terminator)] = []
                continue

            first = find_decision_first(decision)
            for terminator in first:
                LL1_ANALYSE_TABLE[(non_terminator, terminator)] = decision


table_constructer()

for key, value in LL1_ANALYSE_TABLE.items():
    print(key, value)
