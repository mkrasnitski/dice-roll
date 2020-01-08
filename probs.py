import re
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from utils import SpecialZero

def t():
	print('Misc: \n' + misc_percents.apply(fstr).to_string() + '\n')
	print('Sums: \n' + sum_percents.apply(fstr).to_string() + '\n')
	print('Special (% prob given sum occured): \n' + special_percents.applymap(fstr).to_string())

def r(low, high, raw=False):
	if low is None:
		low = 2
	num = len(sum_data[(low <= sum_data['sum']) & (sum_data['sum'] < high)])
	print(fstr(100*num / len(data)))

def g(raw=False):
	ax = sum_percents.plot.bar()
	ax.set_ylabel('Percent Chance')
	ax.set_xlabel('Sum')
	plt.show()

special_names = ['Bus', 'Mr. Monopoly']
specials = list(map(SpecialZero, special_names))
strange_dice = (specials[0], specials[1], specials[1], 1, 2, 3)

data = pd.DataFrame()
data['outcome'] = list(itertools.product(range(1, 7), range(1, 7), strange_dice))

triple = data['outcome'].apply(lambda s: s[0] == s[1] == s[2]).copy()

sum_data = data[~triple].copy()
sum_data['sum'] = sum_data['outcome'].apply(sum)
for special in special_names:
	sum_data[special] = sum_data['outcome'].apply(lambda t: isinstance(t[-1], SpecialZero) and t[-1].name == special)
double = sum_data['outcome'].apply(lambda s: s[0] == s[1])

misc = pd.Series(index=['odd', 'even', 'odd_doubles', 'even_doubles', 'triples'], dtype=int)
odd = sum_data['sum'] % 2 == 1
misc['odd'] = len(sum_data[odd])
misc['even'] = len(sum_data[~odd])
misc['odd_doubles'] = len(sum_data[odd & double])
misc['even_doubles'] = len(sum_data[~odd & double])
misc['triples'] = len(data[triple])

sums = sum_data['sum'].value_counts()
sums.sort_index(inplace=True)
special_groupby = sum_data.groupby('sum')

fstr = '{:.1f}%'.format
misc_percents = 100*misc/len(data)
sum_percents = 100*sums/len(data)
special_percents = 100*special_groupby.mean().rename_axis(None)

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