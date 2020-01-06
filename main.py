from Fact import Fact
from Rule import Rule
from sys import argv

facts = {}
queries = []

letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'

def parse_line(line):
	if line[0] == '=':
		for char in line[0:]:
			if char in letters:
				facts[char].value = True
				recalculate(facts[char])
			elif char == '#':
				break
	elif line[0] == '?'

def main():
	if len(argv) != 2:
		print('Usage: python main.py <filename>')
	else:
		try:
			f = open(argv[1], 'r')
			for line in f:
				temp = line.strip()
				if temp = '' or temp[0] == '#':
					continue
				if not parse_line(temp):
					print('Syntax error!')
					exit(1)
		except(Exception e):
			print("No such file")

if __name__ == '__main__':
	main()