'''	Source code of the program written for the 2017 REU.
'''



import pickle



class letter:

	def __init__(self, letter):
		self._letter = int(letter)

	def __str__(self):
		return str(chr(self._letter + 55)) if self._letter > 9 \
		else str(self._letter)

	def __int__(self):
		return self._letter

class word:
	'''A class for quasi-Stirling permutations.
	'''
	
	def __init__(self, num_list):
		self._word = [letter(l) for l in num_list]

	def __str__(self):
		return ''.join([str(letter(l)) for l in self.list_form()])

	def __lt__(self, other):
		return True if self.list_form() < other.list_form() else False

	def __eq__(self, other):
		return True if self.list_form() == other.list_form() else False

	def __le__(self, other):
		return True if self < other or self == other else False

	def list_form(self):
		return [int(l) for l in self._word]

	def is_valid(self):
		'''returns true if word is a valid quasi-stirling permutation
		'''
		checked_list = []
		check_word = self.list_form()
		for pos in range(len(check_word) - 1):
			if check_word[pos] in checked_list:
				continue
			else:
				checked_list.append(check_word[pos])
			try:
				next_pos = check_word[pos + 1:].index(check_word[pos])
			except ValueError:
				return False
			small_word = check_word[pos + 1:pos + next_pos + 1]
			if len(small_word) != len(set(small_word)) * 2:
				return False
		return True

	def next_words(self):
		'''generates list of valid quasi-stirling permutations from a given word
		'''
		return_list = []
		word_list = self.list_form()
		size = max(word_list)
		new_letter = letter(size + 1)
		for i in range(2 * size + 1):
			for j in range(i, 2 * size + 1, 2):
				if word(word_list[i:j]).is_valid():
					return_list.append(word(word_list[:i] + [new_letter] + \
						word_list[i:j] + [new_letter] + word_list[j:]))
		return_list.sort()
		return return_list

	def avoids(self, p1 = "", p2 = "", p3 = "", p4 = "", p5 = ""):
		'''returns true if a word avoids the given pattern(s)
		'''
		check_word = self.list_form()
		if p2 == "":
			if p1 == "123":
				return self.check_p123()
			elif p1 == "132":
				return self.check_p132()
			elif p1 == "213":
				return self.check_p213()
			elif p1 == "231":
				return self.reverse().check_p132()
			elif p1 == "312":
				return self.reverse().check_p213()
			elif p1 == "321":
				return self.reverse().check_p123()
			else:
				raise ValueError("Invalid pattern.")
		elif p3 == "":
			return self.avoids(p1) and self.avoids(p2)
		elif p4 == "":
			return self.avoids(p1) and self.avoids(p2) and self.avoids(p3)
		elif p5 == "":
			return self.avoids(p1) and self.avoids(p2) and self.avoids(p3) \
			and self.avoids(p4)
		else:
			return self.avoids(p1) and self.avoids(p2) and self.avoids(p3) \
			and self.avoids(p4) and self.avoids(p5)

	def contains(self, p1 = "", p2 = "", p3 = "", p4 = "", p5 = ""):
		'''returns true if a word contains the given pattern(s)
		'''
		return not self.avoids(p1, p2, p3, p4, p5)

	def reverse(self):
		'''returns the reverse of the given word
		'''
		return word(self.list_form()[::-1])

	def check_p123(self):
		check_word = self.list_form()
		for i in range(len(check_word)):
			for j in range(len(check_word) - 1, i, -1):
				if check_word[i] >= check_word[j]:
					continue
				for letter in check_word[i:j]:
					if int(check_word[i]) < int(letter) and \
					int(letter) < int(check_word[j]):
						return False
		return True

	def check_p132(self):
		check_word = self.list_form()
		for i in range(len(check_word)):
			for j in range(len(check_word) - 1, i, -1):
				if check_word[i] >= check_word[j]:
					continue
				for letter in check_word[i:j]:
					if int(letter) > int(check_word[j]):
						return False
		return True

	def check_p213(self):
		check_word = self.list_form()
		for i in range(len(check_word)):
			for j in range(len(check_word) - 1, i, -1):
				if check_word[i] >= check_word[j]:
					continue
				for letter in check_word[i:j]:
					if int(letter) < int(check_word[i]):
						return False
		return True

	def count_asc_desc_plat(self):
		w = self.list_form()
		asc_count = 0
		desc_count = 0
		plat_count = 0
		for i in range(len(w) - 1):
			if w[i + 1] > w[i]:
				asc_count += 1
			elif w[i + 1] < w[i]:
				desc_count += 1
			else:
				plat_count += 1

		return asc_count,desc_count,plat_count


	def create_dictionary(self, p1="", p2="", p3="", p4="", p5=""):
		'''generates dictionary with a list of words generated from the root
		word that avoid p1, p2, p3, p4, p5
		'''
		return_dictionary = {}
		return_dictionary.setdefault(str(self), [])
		for i in self.next_words():
			if i.avoids(p1, p2, p3, p4, p5):
				return_dictionary[str(self)].append(i)
		return return_dictionary


	def get_next_number(self, p1="", p2="", p3="", p4="", p5=""):
		'''counts the number of words generated from the root word that avoid
		p1, p2, p3, p4, p5
		'''
		count = 0
		for i in self.next_words():
			if i.avoids(p1, p2, p3, p4, p5):
				count += 1
		return count

	def root_word(self):
		'''returns the root word of a given word
		'''
		l = self.list_form()
		m = max(l)
		i = l.index(m)
		j = l[i + 1:].index(m) + i + 1
		return word(l[:i] + l[i + 1:j] + l[j + 1:])



def generate_perms(file):
	'''generates a file of valid quasi-stirling permutations from the given file
	'''
	num = int(file[0])
	infile = open(file, "r")
	outfile = open(str(num + 1) + "permutations.txt", "w")
	temp_list = []
	for line in infile:
		for x in word(line).next_words():
			temp_list.append(x)
	temp_list.sort()
	for x in temp_list:
		outfile.write(str(x.list_form()) + "\n")
	infile.close()
	outfile.close()

def generate_stats(file):
	'''generates a file with number of ascents, descents and plateaus 
	'''
	f = open(file, "r")
	output = open(file[0] + "stats.txt", "w")
	count_list = [[0 for x in range(3)] for y in range(7)]
	for line in f:
		a, d, p = word(line).count_asc_desc_plat()
		for j in range(7):
			if a == j:
				count_list[j][0] = count_list[j][0] + 1
			if d == j:
				count_list[j][1] = count_list[j][1] + 1
			if p == j:
				count_list[j][2] = count_list[j][2] + 1

	for k in count_list:
		output.write(str(k) + "\n")
	output.close()
	f.close()

def generate_sequence(p1="", p2="", p3="", p4="", p5=""):
	'''generates the sequence of numbers that avoid the given pattern(s)
	(runs really slowly)
	'''
	word_list = [word([1,1,2,2]), word([1,2,2,1]), word([2,1,1,2]), word([2,2,1,1])]
	c3 = []
	c4 = []
	c5 = []
	c6 = []
	c7 = []
	for w in word_list:
		for x in w.next_words():
			if x.avoids(p1, p2, p3, p4, p5):
				c3.append(x)
	for w in c3:
		for x in w.next_words():
			if x.avoids(p1, p2, p3, p4, p5):
				c4.append(x)
	for w in c4:
		for x in w.next_words():
			if x.avoids(p1, p2, p3, p4, p5):
				c5.append(x)
	for w in c5:
		for x in w.next_words():
			if x.avoids(p1, p2, p3, p4, p5):
				c6.append(x)
	for w in c6:
		for x in w.next_words():
			if x.avoids(p1, p2, p3, p4, p5):
				c7.append(x)

	return [1,4,len(c3),len(c4),len(c5),len(c6),len(c7)]

def create_table(root_list, p1="", p2="", p3="", p4="", p5="", full_page=True):
	'''generates latex code for a list of words and the words they generate that
	avoid the given pattern(s). also prints out the list of words in
	[1,1,2,2,...,n,n] and writes it to a file.
	'''
	rstr = "r_list = ["
	return_str = ""
	if full_page:
		return_str += "\\documentclass{article}\n\\usepackage[margin=0.2in]" + \
			"{geometry}\n\\usepackage{multirow}\n\n\\begin{document}\n\n"
	return_str += "\\begin{tabular}{|c|c|c|}\\hline\n"

	for root in root_list:
		d = root.create_dictionary(p1, p2, p3, p4, p5)
		next_list = list(d.values())[0]
		if len(next_list) == 0:
			return_str = return_str + str(root) + " &\\\\\\hline\n"
		elif len(next_list) == 1:
			rstr = rstr + "word(" + str(next_list[0].list_form()) + "), "
			return_str = return_str + str(root) + " & " + str(next_list[0]) + \
			" & " + str(next_list[0].get_next_number(p1,p2,p3,p4,p5)) + "\\\\\\hline\n"
		else:
			return_str = return_str + "\\multirow{" + str(len(next_list)) + \
				"}{*}{" + str(root) + "}\n"
			for i,w in enumerate(next_list):
				r = w.get_next_number(p1,p2,p3,p4,p5)
				rstr = rstr + "word(" + str(w.list_form()) + "), "
				if i == len(next_list) - 1:
					return_str = return_str + "    & " + str(w) + " & " + \
					str(r) + "\\\\\\hline\n"
				else:
					return_str = return_str + "    & " + str(w) + " & " + \
					str(r) + "\\\\\\cline{2-3}\n"
	f = open("junk", "w")
	f.write(rstr[:-2] + "]")
	f.close()
	return return_str + "\n\\end{tabular}\n\n\\end{document}" if full_page else return_str + "\n\\end{tabular}"

def filter_out(root_list, p1="", p2="", p3="", p4="", p5=""):
	'''runs through the list of words and filters out ones that avoid the
	given pattern(s)
	'''
	temp_list = []
	for r in root_list:
		if r.avoids(p1, p2, p3, p4, p5):
			temp_list.append(r)
	# print(len(temp_list))
	return temp_list

def table(root_list, p1):
	'''generates latex code with the first column being words and the second
	column is the number of (n + 1) words that can be generated with that as a
	root word
	'''
	count = 0
	return_list = [0 for x in range(300)]
	return_str = "\n\n\\begin{tabular}{|c|c|}\hline\n"
	for root in root_list:
		count = count + 1
		if count % 60 == 0:
			return_str = return_str + "\end{tabular}\n\\begin{tabular}" + \
			"{|c|c|}\hline\n"
		d = root.create_dictionary(p1)
		next_list = list(d.values())[0]
		return_str = return_str + str(root) + " & " + str(len(next_list)) + \
		"\\\\\hline\n"
		return_list[len(next_list)] = return_list[len(next_list)] + 1
	return return_str + "\end{tabular}"


def create(root_list, p1):
	c_list = [0 for x in range(301)]
	string = ""
	for root in root_list:
		n = root.get_next_number(p1)
		c_list[n] = c_list[n] + 1
	f1 = open("table.tex", "r")
	for i,line in enumerate(f1):
		if i < 2:
			string = string + line
			continue
		string = string + line[:-1] + str(c_list[i - 2]) + " & \n"
	f1.close()
	f1 = open("table.tex", "w")
	f1.write(string)
	f1.close()
	return("Done.")




def table_nums(root_list):
	ret_dict = {}
	l = len(root_list)
	for i in range(l):
		w = root_list.pop(0).root_word()
		try:
			ret_dict[str(w)] = ret_dict[str(w)] + 1
		except KeyError:
			ret_dict[str(w)] = 1
		if w not in root_list:
			root_list.append(w)


	while root_list != [word([1,1])]:
		l = len(root_list)
		for i in range(l):
			w = root_list.pop(0)
			rw = w.root_word()
			try:
				ret_dict[str(rw)] = ret_dict[str(rw)] + ret_dict[str(w)]
			except KeyError:
				ret_dict[str(rw)] = ret_dict[str(w)]
			if rw not in root_list:
				root_list.append(rw)


	return ret_dict




def generate_different_sequence(root_list, p1, p2, p3, p4, p5):
	'''generates list of numbers that represent the number of permutations that
	each (n + 1) permutation can generate from a given root word....
	'''
	c_list = []
	for root in root_list:
		temp_list = []
		for r in root.next_words():
			if r.avoids(p1, p2, p3, p4, p5):
				temp_list.append(r.get_next_number(p1, p2, p3, p4, p5, p6))
		if temp_list in c_list:
			continue
		else:
			c_list.append(temp_list)
	return c_list


def count_sequence(root_list, p1):
	'''sorts through the sequence of numbers counting how many times each
	sequence appears
	'''
	s_list = generate_sequence(root_list, p1)
	check_list = []
	d = {}
	# t_list = [x[1:] for x in s_list]
	for x in s_list:
		if x in check_list:
			d[str(x)] += 1
		else:
			d[str(x)] = 1
			check_list.append(x)
	return [[m,d[m]] for m in d.keys()]

