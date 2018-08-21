'''		Name: 	Bryan Pennington
		Course: COSC 4315
		Assignment #3
        
        Description: This program prompts the user for three variables. First is
        the location of the comparison documents. Second is the location of a
        query document to determine which of our comparison documents are
        the closest match. Third is an integer value that returns the
        specified number of documents, ranked in order from most similar to
        least similar.
'''


import os			# used for reading filenames
import codecs		# used for getting past unknown characters
import re 			# used for splitting up text using multiple delimiters
from math import log

class search:

	def buildinvertedmatrix(file_loc):
		'''Builds an inverted index matrix of all of the .txt files in a folder
		Returns the file list, the inverted index matrix and a list of words
		that should be ignored when comparing because they're too common.

		Args:
		    file_loc (str): file location of the documents being parsed
		'''
		file_list = [file for file in os.listdir(file_loc)]						# gets our list of file names
		final_list = []
		ignore_list = []
		for i,file in enumerate(file_list):
			doc_word_list = []
			f = codecs.open(file_loc + file, "r", "utf-8", errors = "ignore")	# stops any errors should the file contain unknown characters
			delims = r'[\[;:+"=(&/,.-<>!@#$%*\s)\]]\s*'
			for line in f:
				split_line = re.split(delims, line)								# breaks the line up based on our delimiters
				for word in split_line:
					word = PorterStemmer().stem(word.lower(), 0, len(word) - 1)	# stems the word
					if not word.isnumeric() and len(word) > 2:					# removes any strings that are all numbers and length less than 3
						doc_word_list.append(word)
			reduced_list = list(set(doc_word_list))								# removes any repeat elements
			file_list[i] = (file_list[i], len(doc_word_list))					# adds the length of a document along with filename
			for word in reduced_list:
				final_list.append([str(word), int(0), tuple((i, doc_word_list.count(word)))])	# adds the stemmed word, an int 0 for placeholder and the tuple
			f.close()																			# containing the document index and word count
		final_list.sort()
		for i in range(len(final_list) - 2, -1, -1):							# compares the string with the one next in the list, if they're equal, it'll combine
			if final_list[i][0] == final_list[i + 1][0]:						# the two words
				final_list[i].extend(final_list[i + 1][2:])
				del final_list[i + 1]											# removes the extra list that got combined above
		for i in range(len(final_list) - 1, -1, -1):							# iterates through the list backwards to avoid list index out of range error
			final_list[i][1] = len(final_list[i]) - 2							# that comes from removing items below
			if final_list[i][1] > 32:											# if the word is contained in 30 or more of the documents then it's too common
				ignore_list.append(final_list[i][0])							# and we should ignore it. Adds to an ignore list, so we can remove the same
				del final_list[i]												# words from our query document
		return file_list, final_list, ignore_list

	def getquerydoc(file_loc):
		'''Returns a list of all the words (stemmed) contained in the query
		document

		Args:
		    file_loc (str): file location of the query document to be parsed
		'''
		f = codecs.open(file_loc, "r", "utf-8", errors = "ignore")	# stops any errors should the file contain unknown characters
		delims = r'[\[;:+"=(&/,.-<>!@#$%*\s)\]]\s*'
		temp_list = []
		for line in f:
			split_line = re.split(delims, line)
			for word in split_line:
				if len(word) > 2 and word != "":
					temp_list.append(PorterStemmer().stem(word.lower(), 0, len(word) - 1))
		return temp_list

	def tfidf(x1, x2, x3, x4):
		'''Calculates TF-IDF value for a set of values.
		
		Args:
		    x1 (float/int): number of occurence of a term
		    x2 (float/int): number of terms in a document
		    x3 (float/int): number of documents in the collection
		    x4 (float/int): number of documents containing the term
		'''
		return log(1 + x1 / x2) * log(x3 / x4)

	def mag(vector):
		'''Calculates the magnitude of a vector.
		
		Args:
		    vector (list): any list of floats or ints
		'''
		return search.dotproduct(vector, vector) ** 0.5

	def dotproduct(list1, list2):
		'''Calculates the dot product of two vectors.
		
		Args:
		    list1 (list): any list of floats or ints
		    list2 (list): any list of floats or ints
		'''
		return_value = (0)
		for i in range(len(list1)):
			return_value += list1[i] * list2[i]
		return return_value


	def compare(file_loc, query_loc, num_docs):
		'''Parses each document, calculates the TF-IDF score for each word and
		stores that value in a list. Then calculates how close each document is
		to the query document using the formula dotp(q, d_n) / mag(q) * mag(d_n)
		where 0 <= n < len(file_list). It then sorts the list with greatest
		values at top and returns the top k documents based on the int num_docs.

		Args:
		    file_loc (str): file location of the documents to be parsed
		    query_loc (str): file location of the query document to be parsed
		    num_docs (int): total number of results to be returned
		'''
		file_list, final_list, ignore_list = search.buildinvertedmatrix(file_loc)	# gets the list of files, the inverted index matrix and a list of words ignored
																					# because they were too common and likely irrelevant
		query_list = search.getquerydoc(query_loc)								# gets the list of words contained in the query document
		word_list = [item[0] for item in final_list]							# gives us the list of words, built from the inverted index matrix
		query_vector = {}														# defines a dictionary in Python
		doc_vector_list = [{} for i in range(len(file_list))]					# creates a list of dictionaries for each document in our file
		for word in query_list:
			if word not in word_list and word not in ignore_list:				# if our query document contains a word that isn't part of our inverted index matrix,
																				# we need to handle these separately
				query_vector[word] = log(1 + query_list.count(word) / len(query_list))	# calculates the term frequency. The IDF for these would be
																						# log(1/1) = log(1) = 0, and we don't want to multiply by 0.
				for i in range(len(doc_vector_list)):							# adds the word to each of the vector for the documents with a TF-IDF score of 0
					doc_vector_list[i][word] = 0
			elif word not in ignore_list:										# the word is already in our word list, add the TF-IDF score for it
				query_vector[word] = search.tfidf(query_list.count(word), len(query_list), len(file_list), final_list[word_list.index(word)][1])
		for i,word in enumerate(word_list):										# iterates through each word in the word_list where 'word' is the string and 'i'
																				# is the respesctive index position
			if word not in query_vector.keys():									# if the word is not already in our queries list, add a TF-IDF score of 0
				query_vector[word] = 0
			for toople in final_list[i][2:]:									# iterates through our list of tuples
				doc_index, word_count = toople   								# stores the document index position and word count in two variables
				doc_word_count = final_list[i][1]								# gets the total number of words in a document
				doc_vector_list[doc_index][word] = search.tfidf(word_count, file_list[doc_index][1], len(file_list), doc_word_count)	#calculates TF-IDF
		for word in word_list:													# iterates through each word again
			for i,item in enumerate(doc_vector_list):							# iterates through each item in our list of vectors
				if word not in item.keys():										# if the word doesn't already have a value, then the TF-IDF score should be 0
					doc_vector_list[i][word] = 0
		ranked_list = [0 for i in range(len(doc_vector_list))]					# creates a list that is the same length as the number of documents we're comparing
		for i,item in enumerate(doc_vector_list):								# iterates through each vector in our list
			num_list1 = [query_vector[word] for word in word_list]				# gets the float values for each word we've computed the TF-IDF score for
			num_list2 = [doc_vector_list[i][word] for word in word_list]		# same thing but for each document
			dotp = search.dotproduct(num_list1, num_list2)						# calculates dot product between the query vector and the document vector
			ranked_list[i] = [dotp / (search.mag(num_list1) * search.mag(num_list2)), i]	# stores the dotp(v1,v2) / mag(v1) * mag(v2) for each document
		ranked_list.sort(reverse = True)										# sorts in descending order
		return [file_list[ranked_list[i][1]][0] for i in range(num_docs)]		# returns the first k number of documents


loc = str(input("Enter location of files >>"))
Q = str(input("Enter location of the query file >>"))
k = int(input("Number of items to return >>"))

l = search.compare(loc, Q, k)
for item in l:
	print(item)








# PortStemmer code was not written by me.


#!/usr/bin/env python

"""Porter Stemming Algorithm
This is the Porter stemming algorithm, ported to Python from the
version coded up in ANSI C by the author. It may be be regarded
as canonical, in that it follows the algorithm presented in

Porter, 1980, An algorithm for suffix stripping, Program, Vol. 14,
no. 3, pp 130-137,

only differing from it at the points maked --DEPARTURE-- below.

See also http://www.tartarus.org/~martin/PorterStemmer

The algorithm as described in the paper could be exactly replicated
by adjusting the points of DEPARTURE, but this is barely necessary,
because (a) the points of DEPARTURE are definitely improvements, and
(b) no encoding of the Porter stemmer I have seen is anything like
as exact as this version, even with the points of DEPARTURE!

Vivake Gupta (v@nano.com)

Release 1: January 2001

Further adjustments by Santiago Bruno (bananabruno@gmail.com)
to allow word input not restricted to one word per line, leading
to:

release 2: July 2008
"""

import sys

class PorterStemmer:

    def __init__(self):
        """The main part of the stemming algorithm starts here.
        b is a buffer holding a word to be stemmed. The letters are in b[k0],
        b[k0+1] ... ending at b[k]. In fact k0 = 0 in this demo program. k is
        readjusted downwards as the stemming progresses. Zero termination is
        not in fact used in the algorithm.

        Note that only lower case sequences are stemmed. Forcing to lower case
        should be done before stem(...) is called.
        """

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0   # j is a general offset into the string

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        """m() measures the number of consonant sequences between k0 and j.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        """doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        """step1c() turns terminal y to i when there is another vowel in the stem."""
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i' + self.b[self.k+1:]

    def step2(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1

    def stem(self, p, i, j):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]


if __name__ == '__main__':
    p = PorterStemmer()
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            infile = open(f, 'r')
            while 1:
                output = ''
                word = ''
                line = infile.readline()
                if line == '':
                    break
                for c in line:
                    if c.isalpha():
                        word += c.lower()
                    else:
                        if word:
                            output += p.stem(word, 0,len(word)-1)
                            word = ''
                        output += c.lower()
                print (output)
            infile.close()