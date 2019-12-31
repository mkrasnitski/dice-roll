import itertools
import pandas as pd

data = pd.DataFrame()
data['outcome'] = list(itertools.product(range(1, 7), range(1, 7), (0, 0, 0, 1, 2, 3)))

triple = data['outcome'].apply(lambda s: s[0] == s[1] == s[2]).copy()

sum_data = data[~triple].copy()
double = sum_data['outcome'].apply(lambda s: s[0] == s[1])
sum_data['sum'] = sum_data['outcome'].apply(sum)

misc = pd.Series(index=['odd', 'even', 'odd_doubles', 'even_doubles', 'triples'], dtype=int)
odd = sum_data['sum'] % 2 == 1
misc['odd'] = len(sum_data[odd])
misc['even'] = len(sum_data[~odd])
misc['odd_doubles'] = len(sum_data[odd & double])
misc['even_doubles'] = len(sum_data[~odd & double])
misc['triples'] = len(data[triple])

sum_counts = pd.DataFrame(index=range(2, 16), dtype='object', columns=('=', '<', '>', '<=', '>='))
sum_counts['='] = sum_data['sum'].value_counts()
for s in range(2, 16):
	sum_counts.loc[s, '<'] = len(sum_data[sum_data['sum'] < s])
	sum_counts.loc[s, '>'] = len(sum_data[sum_data['sum'] > s])
sum_counts['<='] = sum_counts['<'] + sum_counts['=']
sum_counts['>='] = sum_counts['>'] + sum_counts['=']

misc_percents = 100*misc/len(data)
sum_percents = 100*sum_counts/len(data)

fstr = '{:.1f}%'.format

def t(*, raw=False):
	if raw:
		print(misc.to_string())
		print(sum_counts)
	print(misc_percents.apply(fstr).to_string())
	print()
	print(sum_percents.applymap(fstr))

def r(low, high=None, /, *, raw=False):
	if not high:
		high = low
		low = 2
	num = len(sum_data[(low <= sum_data['sum']) & (sum_data['sum'] < high)])
	if raw:
		print(num)
	print(fstr(100*num / len(data)))
