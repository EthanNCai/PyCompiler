import itertools

# written by JunzhiCai in 2023, Dec. 17th.

"""
G[E]:
        E  →TE'
        E' →+TE'|ε
        T  →FT'
        T' →*FT'|ε
        F  →(E)|i
"""

grammar1 = {
    'E': (['T', 'E_'],),
    'E_': (['+', 'T', 'E_'], ['ε']),
    'T': (['F', 'T_'],),
    'T_': (['*', 'F', 'T_'], ['ε']),
    'F': (['(', 'E', ')'], ['i'])
}

NON_TERMINATOR_LIST = ['E', 'E_', 'T', 'T_', 'F']
TERMINATORS_LIST = ['+', '*', '(', ')', 'i']

first = {
    'E': set(),
    'E_': set(),
    'T': set(),
    'T_': set(),
    'F': set()
}

follow = {
    'E': set(),
    'E_': set(),
    'T': set(),
    'T_': set(),
    'F': set()
}

non_terminator_counts = len(NON_TERMINATOR_LIST)
nullable_non_terminator = ['E_', 'T_']


def find_first(target_non_terminator, current_non_terminator):
    decisions = grammar1.get(current_non_terminator)
    for decision in decisions:
        first_sym = decision[0]
        if first_sym in NON_TERMINATOR_LIST:
            find_first(target_non_terminator, first_sym)
        else:
            first[target_non_terminator].add(first_sym)


def find_follow(begin_non_terminator):
    follow[begin_non_terminator].add('EOF')

    search_list = list(itertools.product(NON_TERMINATOR_LIST, NON_TERMINATOR_LIST))
    # search_list 是全排列，形如: [('E', 'E'), ('E', 'E_'), ('E', 'T') ... ('T_', 'F'), ('F', 'E')]
    # 把查找和被查找的非终结符提前算出来，这是为了减少for循环的层数

    subset_relationships = set()
    for non_terminator_, non_terminator_to_search in search_list:
        decisions = grammar1.get(non_terminator_to_search)
        for decision in decisions:
            index = find_index(non_terminator_, decision)
            if index is None:
                # 找不到这个终结符
                continue
            if index == len(decision) - 1:
                # 如果这个终结符后面的其他非终结符是可以全部为Null的 或者 这个终结符在最后面，记录子集关系
                subset_relationships.add((non_terminator_, non_terminator_to_search))
                continue
            if backward_nullable(decision[index + 1:]):
                subset_relationships.add((non_terminator_, non_terminator_to_search))
            if index != len(decision) - 1:
                next_symbol = decision[index + 1]
                if next_symbol in TERMINATORS_LIST:
                    # 找到了一个直接的Follow元素啦！
                    follow[non_terminator_].add(next_symbol)
                elif next_symbol in NON_TERMINATOR_LIST:
                    follow[non_terminator_].update(first[next_symbol])
                    follow[non_terminator_].discard('ε')
                    # 如果是非终结符

    # Step2: 把互为子集的Follow集互相做并运算，喵！
    for i in range(non_terminator_counts):
        for subset_relationship in subset_relationships:
            _set_, subset = subset_relationship
            follow[_set_].update(set(follow[subset]))


def backward_nullable(backward_list):
    return set(backward_list).issubset(set(nullable_non_terminator))
    # 用集合运算，可读性极高，嘿嘿，从《Fluent Python》学到的


def find_index(target, _list):
    if target in _list:
        return _list.index(target)
    else:
        return None


for non_terminator in NON_TERMINATOR_LIST:
    find_first(non_terminator, non_terminator)

print('FIRST')
print(first)

find_follow('E')
print('FOLLOW')
print(follow)