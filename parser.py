# if GOOD -> object else none
import re
operations = ['|', '+', '!', '^', '=>', '<=>']
letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'

from Rule import Rule
from Fact import Fact


def unique_letters(array, unique_arr=[]):
    for i in array:
        if i not in unique_arr and isinstance(i, str) and i in letters:
            unique_arr.append(i)
    for i in array:
        if isinstance(i, Rule) and i not in unique_arr:
            unique_arr.append(i)
            unique_letters(i.facts, unique_arr)
    res = []
    for i in unique_arr:
        if isinstance(i, str):
            res.append(i)
    return res


def update_facts(father_rule, dog_rule, facts):
    ulet = unique_letters(dog_rule.facts)
    for i in ulet:
        if i in facts and father_rule not in facts[i].rules:
            facts[i].rules.append(father_rule)
        elif i in letters:
            facts[i] = Fact(i)
            facts[i].rules.append(father_rule)
    for i in dog_rule.facts:
        if isinstance(i, Rule):
            update_facts(father_rule, i, facts)
    return facts


def write_in_rule(rules_string_arr):
    rule = Rule()
    scope = 0
    skip_idx = 0
#    print('ARR: ', rules_string_arr)
    if len(rules_string_arr[-1]) < 1 or rules_string_arr[-1][0] not in letters:
        print('Expression must and with letter!')
        return None
    for i in rules_string_arr:
        if skip_idx > 0:
            skip_idx -= 1
            continue
        if i in letters:
            rule.facts.append(i)
        elif i in operations:
            rule.operations.append(i)
        else:
            tmp_rule, skip_idx = new_group_str(rules_string_arr)
            if tmp_rule is None or skip_idx is None:
                return None
            scope += 1
            if tmp_rule is None:
                return None
            rule.facts.append(tmp_rule)
    return rule


def get_indexes(rules_arr):
    open_brax = []
    close_brax = []
    for i in range(len(rules_arr)):
        [open_brax.append((i, m.start())) for m in re.finditer('\(', rules_arr[i])]
        [close_brax.append((i, m.start())) for m in re.finditer('\)', rules_arr[i])]
    if len(open_brax) != len(close_brax):
        print('Incorect brackets amount!')
        return None, None
    skip = 0
    for i in range(len(open_brax)):
        if i != len(open_brax) - 1:
            if open_brax[0][0] < close_brax[i][0] < open_brax[i + 1][0]:
                return ((open_brax[0], close_brax[i]))
            else:
                skip += 1
    if close_brax[skip][0] > open_brax[0][0]:
        return ((open_brax[0], close_brax[skip]))
    print('Incorrect brackets')
    return None, None


def remove_brax(array, open_idx, close_idx):
    tmp = list(array[open_idx[0]])
    tmp[open_idx[1]] = ''
    array[open_idx[0]] = "".join(tmp)
    tmp = list(array[close_idx[0]])
    tmp[close_idx[1]] = ''
    array[close_idx[0]] = "".join(tmp)
    return (array)


def new_group_str(rules_arr):
    open_brax, close_brax = get_indexes(rules_arr)
    if open_brax is None:
        return None, None
    rules_arr = remove_brax(rules_arr, open_brax, close_brax)
    rule_slice = rules_arr[open_brax[0]:close_brax[0] + 1]
 #   print('slice: ', rule_slice)
    rule = write_in_rule(rule_slice)
    return rule, (close_brax[0] - open_brax[0])


def correct_input(arr):
    test_arr = []
    for i in range(len(arr)):
        if '(' in arr[i]:
            test_arr.append(arr[i][-1])
        elif ')' in arr[i]:
            test_arr.append(arr[i][0])
        else:
            test_arr.append(arr[i])

    for i in test_arr:
        if i not in letters or i not in operations:
            return False
    return True


def correct_operation_number(op):
    for i in range(len(op)):
        if op[i] == '=>' and len(op) - i - 2 > 0:
            print("Too many operations after '=>'")
            return False
        if op[i] == '<=>' and len(op) > 3:
            print("Just one operation on both sides is acceptable!")
            return False
    counter = 0
    for i in op:
        if i in ['=>', '<=>']:
            counter += 1
        if counter > 1:
            print('Too many implies symbols!')
            return False
    return True


def single_brackets(array):
    new_array = []
    for i in array:
        if i[0] == '(' and i[-1] == ')':
            new_array.append(i[1:-1])
        else:
            new_array.append(i)
    return new_array


def split_not(array):
    x = 0
    for i in range(len(array)):
        if '!' in array[i] and len(array[i]) >= 2:
            first = array[:i]
            second = [array[i][0], array[i][1:len(array[i])]]
            try:
                third = array[i + 1:]
            except:
                third = []
            array = first + second + third
            x = 1
    if x == 1:
        array = split_not(array)
    return array


def parse_rule(line, facts):
    input = split_not(single_brackets(line.split()))
    if correct_input(input) is None:
        print('Incorrect rule:[', line, ']')
        return None
  #  print(input)
    rule = write_in_rule(input)
    if rule is None:
        print('Incorrect rule:[', line, ']')
        return None
    if not correct_operation_number(rule.operations):
        return None
  #  print('Facts:', rule.facts)
  #  print('Operations:', rule.operations)
    facts = update_facts(rule, rule, facts)
  #  print(facts)
    return rule

# if => 1 operations after '=>' if '<=>' 1 operation on both sides