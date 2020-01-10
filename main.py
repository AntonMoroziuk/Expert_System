from Fact import Fact
from Rule import Rule
from sys import argv
from parser import parse_rule

facts = {}
queries = []

letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'

def get_rule_parts(rule):
	i, j, fact = 0, 0, True
	right = []
	left = []
	while (rule.operations[j] != '=>' and rule.operations[j] != '<=>') or fact:
		if fact:
			if j < len(rule.operations) and rule.operations[j] == '!':
				left += [rule.operations[j], rule.facts[i]]
				i += 1
				j += 1
			else:
				left.append(rule.facts[i])
				i += 1
			fact = False
		else:
			left.append(rule.operations[j])
			fact = True
			j += 1
	j += 1
	fact = True
	while j < len(rule.operations) or i < len(rule.facts):
		if fact:
			if j < len(rule.operations) and rule.operations[j] == '!':
				right += [rule.operations[j], rule.facts[i]]
				i += 1
				j += 1
			else:
				right.append(rule.facts[i])
				i += 1
			fact = False
		else:
			right.append(rule.operations[j])
			j += 1
	return left, right

def arr_to_rule(arr):
	rule = Rule()
	for i in arr:
		if i in letters:
			rule.facts.append(i)
		else:
			rule.operations.append(i)
	return rule

def apply_rule(rule, value):
	changed = []
	rule = arr_to_rule(rule)
	if len(rule.operations) == 0 and len(rule.facts) == 1:
		if value == True:
			if facts[rule.facts[0]].value == False or facts[rule.facts[0]].value is None:
				 changed.append(rule.facts[0])
				 facts[rule.facts[0]].value = True
		elif value is None:
			if facts[rule.facts[0]].value == False:
				changed.append(rule.facts[0])
				facts[rule.facts[0]].value = None
		else:
			if facts[rule.facts[0]].value == True:
				print("Your rules are inconsistent")
				exit(1)
		return changed
	elif len(rule.operations) == 1 and rule.operations[0] == '!' and len(rule.facts) == 1:
		if value == False:
			if facts[rule.facts[0]].value == False or facts[rule.facts[0]].value is None:
				 changed.append(rule.facts[0])
				 facts[rule.facts[0]].value = True
		elif value == True:
			if facts[rule.facts[0]].value == True:
				print("Your rules are inconsistent")
				exit(1)
		return changed
	if rule.operations[0] == '!':
		left_value = not facts[rule.facts[0]].value if facts[rule.facts[0]].value else None
	else:
		left_value = facts[rule.facts[0]].value if facts[rule.facts[0]].value else None
	if (len(rule.operations) == 2 and rule.operations[0] == '!') or (len(rule.operations) == 3 and rule.operations[2] == '!'):
		right_value = not facts[rule.facts[1]].value if facts[rule.facts[1]].value else None
	else:
		right_value = facts[rule.facts[1]].value if facts[rule.facts[1]].value else None
	if '^' in rule.operations:
		if value == True:
			if right_value == True and left_value == True:
				if facts[rule.facts[0]].value == False and facts[rule.facts[1]].value == False:
					changed.append(rule.facts[0])
					changed.append(rule.facts[1])
					facts[rule.facts[0]].value = None
					facts[rule.facts[1]].value = None
				elif facts[rule.facts[0]].value == False:
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
				elif facts[rule.facts[1]].value == False:
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
				else:
					print("Your rules are inconsistent")
					exit(1)
			elif right_value == False and left_value == False:
				if facts[rule.facts[0]].value == False and facts[rule.facts[1]].value == False:
					changed.append(rule.facts[0])
					changed.append(rule.facts[1])
					facts[rule.facts[0]].value = None
					facts[rule.facts[1]].value = None
				elif facts[rule.facts[0]].value == False:
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
				elif facts[rule.facts[1]].value == False:
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
				else:
					print("Your rules are inconsistent")
					exit(1)
			elif right_value is None and left_value == False:
				if len(rule.operations) == 1 or (len(rule.operations) == 2 and rule.operations[0] == '!'):
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
			elif left_value is None and right_value == False:
				if len(rule.operations) == 1 or (len(rule.operations) == 2 and rule.operations[1] == '!'):
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
		elif value == False:
			if right_value == True and left_value == False:
				if facts[rule.facts[0]].value == False and facts[rule.facts[1]].value == False:
					changed.append(rule.facts[0])
					changed.append(rule.facts[1])
					facts[rule.facts[0]].value = None
					facts[rule.facts[1]].value = None
				elif facts[rule.facts[0]].value == False:
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
				elif facts[rule.facts[1]].value == False:
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
				else:
					print("Your rules are inconsistent")
					exit(1)
			elif right_value == False and left_value == False:
				if facts[rule.facts[0]].value == False and facts[rule.facts[1]].value == False:
					changed.append(rule.facts[0])
					changed.append(rule.facts[1])
					facts[rule.facts[0]].value = None
					facts[rule.facts[1]].value = None
				elif facts[rule.facts[0]].value == False:
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
				elif facts[rule.facts[1]].value == False:
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
				else:
					print("Your rules are inconsistent")
					exit(1)
			elif right_value is None and left_value == True:
				if len(rule.operations) == 1 or (len(rule.operations) == 2 and rule.operations[0] == '!'):
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
			elif left_value is None and right_value == True:
				if len(rule.operations) == 1 or (len(rule.operations) == 2 and rule.operations[1] == '!'):
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
		else:
			if facts[rule.facts[0]].value == False:
				changed.append(rule.facts[0])
				facts[rule.facts[0]].value = None
			if facts[rule.facts[1]].value == False:
				changed.append(rule.facts[1])
				facts[rule.facts[1]].value = None
	elif '+' in facts.operations:
		if value == True:
			if len(rule.operations) > 1:
				print("Your rules are inconsistent")
				exit(1)
			if facts[rule.facts[0].value] != True:
				changed.append(rule.facts[0])
				facts[rule.facts[0]].value = True
			if facts[rule.facts[1].value] != True:
				changed.append(rule.facts[1])
				facts[rule.facts[1]].value = True
		elif value == False:
			if right_value == True and left_value == True:
				if facts[rule.facts[0]].value == False and facts[rule.facts[1]].value == False:
					changed.append(rule.facts[0])
					changed.append(rule.facts[1])
					facts[rule.facts[0]].value = None
					facts[rule.facts[1]].value = None
				elif facts[rule.facts[0]].value == False:
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
				elif facts[rule.facts[1]].value == False:
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
				else:
					print("Your rules are inconsistent")
					exit(1)
			elif right_value is None and left_value == True:
				if (len(rule.operations) == 2 and rule.operations[1] == '!') or (len(rule.operations) == 3 and rule.operations[2] == '!'):
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
			elif left_value is None and right_value == True:
				if (len(rule.operations) == 2 and rule.operations[0] == '!') or (len(rule.operations) == 3 and rule.operations[0] == '!'):
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
		else:
			if facts[rule.facts[0]].value == False:
				changed.append(rule.facts[0])
				facts[rule.facts[0]].value = None
			if facts[rule.facts[1]].value == False:
				changed.append(rule.facts[1])
				facts[rule.facts[1]].value = None
	elif '|' in facts.operations:
		if value == True:
			if right_value == False and left_value == False:
				if facts[rule.facts[0]].value == False and facts[rule.facts[1]].value == False:
					changed.append(rule.facts[0])
					changed.append(rule.facts[1])
					facts[rule.facts[0]].value = None
					facts[rule.facts[1]].value = None
				elif facts[rule.facts[0]].value == False:
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
				elif facts[rule.facts[1]].value == False:
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
				else:
					print("Your rules are inconsistent")
					exit(1)
			elif right_value is None and left_value == False:
				if len(rule.operations) == 1 or (len(rule.operations) == 2 and rule.operations[0] == '!'):
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
			elif left_value is None and right_value == False:
				if len(rule.operations) == 1 or (len(rule.operations) == 2 and rule.operations[1] == '!'):
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
		elif value == False:
			if right_value == True and left_value == True:
				if facts[rule.facts[0]].value == False and facts[rule.facts[1]].value == False:
					changed.append(rule.facts[0])
					changed.append(rule.facts[1])
					facts[rule.facts[0]].value = None
					facts[rule.facts[1]].value = None
				else:
					print("Your rules are inconsistent")
					exit(1)
			elif right_value is None and left_value == False:
				if (len(rule.operations) == 2 and rule.operations[1] == '!') or (len(rule.operations) == 3 and rule.operations[2] == '!'):
					changed.append(rule.facts[1])
					facts[rule.facts[1]].value = True
			elif left_value is None and right_value == False:
				if (len(rule.operations) == 2 and rule.operations[0] == '!') or (len(rule.operations) == 3 and rule.operations[0] == '!'):
					changed.append(rule.facts[0])
					facts[rule.facts[0]].value = True
			elif right_value == False and left_value == True and facts[rule.facts[0]].value == False:
				changed.append(rule.facts[0])
				facts[rule.facts[0]].value = True
			elif left_value == False and right_value == True and facts[rule.facts[1]].value == False:
				changed.append(rule.facts[1])
				facts[rule.facts[1]].value = True
			elif left_value is None and right_value is None and len(rule.operations) == 3:
				changed.append(rule.facts[0])
				changed.append(rule.facts[1])
				facts[rule.facts[0]].value = True
				facts[rule.facts[1]].value = True
	else:
		print("Error")
		exit(1)
	return changed


def evaluate_rule(rule):
	temp = rule[:]
	for i in range(len(temp)):
		if temp[i] in letters:
			temp[i] = facts[temp[i]].value
	'''temp = []
	i, j, fact = 0, 0, True
	while j < len(rule.operations) or i < len(rule.facts):
		if fact:
			if j < len(rule.operations) and rule.operations[j] == '!':
				if type(rule.facts[i]) is str:
					temp += [rule.operations[j], facts[rule.facts[i]].value]
				else:
					temp += [rule.operations[j], evaluate_rule(rule.facts[i])]
				i += 1
				j += 1
			else:
				temp.append(facts[rule.facts[i]].value)
				i += 1
			fact = False
		else:
			temp.append(rule.operations[j])
			j += 1'''
	while '!' in temp:
		i = temp.index('!')
		if temp[i + 1] == None:
			temp = temp[:i] + [None] + temp[i + 1:]
		else:
			temp = temp[:i] + [not temp[i + 1]] + temp[i + 1:]
	while '+' in temp:
		i = temp.index('+')
		if temp[i - 1] == None:
			if temp[i + 1] == False:
				temp = temp[:i - 1] + [False] + temp[i + 1:]
			else:
				temp = temp[:i - 1] + [None] + temp[i + 1:]
		elif temp[i + 1] == None:
			if temp[i - 1] == False:
				temp = temp[:i - 1] + [False] + temp[i + 1:]
			else:
				temp = temp[:i - 1] + [None] + temp[i + 1:]
		else:
			temp = temp[:i - 1] + [temp[i - 1] and temp[i + 1]] + temp[i + 1:]
	while '|' in temp:
		i = temp.index('|')
		if temp[i - 1] == None:
			if temp[i + 1] == True:
				temp = temp[:i - 1] + [True] + temp[i + 1:]
			else:
				temp = temp[:i - 1] + [None] + temp[i + 1:]
		elif temp[i + 1] == None:
			if temp[i - 1] == True:
				temp = temp[:i - 1] + [True] + temp[i + 1:]
			else:
				temp = temp[:i - 1] + [None] + temp[i + 1:]
		else:
			temp = temp[:i - 1] + [temp[i - 1] or temp[i + 1]] + temp[i + 1:]
	while '^' in temp:
		i = temp.index('^')
		if temp[i - 1] == None or temp[i + 1] == None:
			temp = temp[:i - 1] + [None] + temp[i + 1:]
		else:
			temp = temp[:i - 1] + [temp[i - 1] ^ temp[i + 1]] + temp[i + 1:]
	return temp[0]

def check_rule(rule):
	if (rule.operations.count('=>') + rule.operations.count('<=>')) != 1: 
		print('Rule syntax error!')
		exit(1)
	left, right = get_rule_parts(rule)
	if rule.operations.count('=>') == 1:
		return apply_rule(right, evaluate_rule(left))
	else:
		right_res = evaluate_rule(right)
		left_res = evaluate_rule(left)
		if (left_res == True and right_res == False) or (left_res == True and right_res == None):
			return apply_rule(right, True)
		elif right_res == True and left_res == False or (right_res == True and left_res == None):
			return apply_rule(left, True)
		elif left_res == None and right_res == False:
			return apply_rule(right, None)
		elif right_res == None and left_res == False:
			return apply_rule(left, None)
		return []

def evaluate(fact):
	changed_facts = []
	for rule in facts[fact].rules:
		changed_facts += check_rule(rule)
	for fact in changed_facts:
		evaluate(fact)
	return len(changed_facts) > 0

def parse_line(line):
	if line[0] == '=':
		for char in line[1:]:
			if char in letters:
				facts[char].value = True
			elif char == '#':
				break
			else:
				return False
	elif line[0] == '?':
		for char in line[1:]:
			if char in letters:
				queries.append(char)
			elif char == '#':
				break
			else:
				return False
	else:
		rule = parse_rule(line, facts)
		'''rule = Rule()
		a = Fact('A')
		b = Fact('B')
		rule.facts = ['A', 'B']
		rule.operations = ['=>']
		facts['A'] = a
		facts['B'] = b
		a.rules.append(rule)
		b.rules.append(rule)
		for fact in rule.facts:
			if type(fact) is str:
				facts[fact].rules.append(rule)'''
	return True

def main():
	if len(argv) != 2:
		print('Usage: python main.py <filename>')
	else:
		try:
			f = open(argv[1], 'r')
			for line in f:
				temp = line.strip()
				if temp == '' or temp[0] == '#':
					continue
				if parse_line(temp) is None:
					print('Syntax error!')
					exit(1)
			for key in facts:
				if facts[key].value == True:
					if evaluate(key):
						break
			for query in queries:
				if query in facts:
					print('{}: {}'.format(query, facts[query].value if facts[query].value is not None else 'undefined'))
				else:
					print('{}: False'.format(query))
		except IOError:
			print("File not found")
	#	except:
	#		print("Error")

if __name__ == '__main__':
	main()