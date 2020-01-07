import re
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from utils import Zero

def t(raw=False):
	if raw:
		print(str(misc) + '\n')
		print(sums)
	else:
		print(str(misc_percents.apply(fstr)) + '\n')
		print(sum_percents.applymap(fstr))

def r(low, high, raw=False):
	if low is None:
		low = 2
	num = len(sum_data[(low <= sum_data['sum']) & (sum_data['sum'] < high)])
	if raw:
		print(num)
	else:
		print(fstr(100*num / len(data)))

def g(raw=False):
	ax = None
	if raw:
		ax = sums['='].plot.bar()
		ax.set_ylabel('Raw Count')
	else:
		ax = sum_percents['='].plot.bar()
		ax.set_ylabel('Percent Chance')
	ax.set_xlabel('Sum')
	plt.show()

data = pd.DataFrame()
strange_dice = (Zero('Bus'), Zero('Monopoly Man'), Zero('Monopoly Man'), 1, 2, 3)
data['outcome'] = list(itertools.product(range(1, 7), range(1, 7), strange_dice))

triple = data['outcome'].apply(lambda s: s[0] == s[1] == s[2]).copy()

sum_data = data[~triple].copy()
sum_data['sum'] = sum_data['outcome'].apply(sum)
double = sum_data['outcome'].apply(lambda s: s[0] == s[1])

misc = pd.Series(index=['odd', 'even', 'odd_doubles', 'even_doubles', 'triples'], dtype=int)
odd = sum_data['sum'] % 2 == 1
misc['odd'] = len(sum_data[odd])
misc['even'] = len(sum_data[~odd])
misc['odd_doubles'] = len(sum_data[odd & double])
misc['even_doubles'] = len(sum_data[~odd & double])
misc['triples'] = len(data[triple])

sums = pd.DataFrame(index=range(2, 16), dtype='object', columns=('=', '<', '>', '<=', '>='))
sums['='] = sum_data['sum'].value_counts()
for s in range(2, 16):
	sums.loc[s, '<'] = len(sum_data[sum_data['sum'] < s])
	sums.loc[s, '>'] = len(sum_data[sum_data['sum'] > s])
sums['<='] = sums['<'] + sums['=']
sums['>='] = sums['>'] + sums['=']

fstr = '{:.1f}%'.format
misc_percents = 100*misc/len(data)
sum_percents = 100*sums/len(data)

# start event loop
while True:
	command = input('command: ').strip()
	if command in ['q', 'quit', 'exit']:
		break
	elif command in ['t', 'table']:
		t()
	elif command in ['g', 'graph']:
		g()
	elif match := re.match(r'r(?:ange)?\((?:(\d+),)?\s*(\d+)\)', command):
		low, high = match.groups()
		if low:
			low = int(low)
		high = int(high)
		r(low, high)
	elif command in ['h', 'help']:
		s = "list of commands\n" \
		+ " - t[able]\t\t\tprint a table\n" \
		+ " - g[raph]\t\t\tshow a graph\n" \
		+ " - r[ange]([low,] high)\t\tpercent change of a sum in a range\n" \
		+ " - q[uit], exit\t\t\tquit the program\n" \
		+ " - h[elp]\t\t\tshow this help text\n"
		print(s)
	else:
		print('unknown command')