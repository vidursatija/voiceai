import re

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

f = open('10knews.txt', 'r')
f2 = open('newsfile.tsv', 'w')

for line in f:
	words = re.sub("[^\w]", " ",  line).split()
	for word in words:
		if is_number(word) == False:
			f2.write(word.strip())
			f2.write('\tO\n')
	f2.write('\n')

f2.close()
f.close()
