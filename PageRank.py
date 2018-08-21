"""
		Bryan Pennington
		COSC 4315
		Assignment 4

		Description: This program prompts the user for 4 inputs. First, the
		location of the .txt files to be parsed. Second, the file location for
		the output file. Third, the teleport probability as a float. Finally,
		the number of iterations to calculate the popularity rate. It then
		parses through each .txt file in the file location, reading each 4 digit
		number it finds as a reference to another document. Once all the
		documents are parsed, it'll create the probability matrix of the links
		and write it to the given output file.

		n1 = "C:/filelocation/documents/"
		n2 = "C:/filelocation/output.txt"

		Examples of formatting for input and output.

"""


import os			# used for reading filenames
import codecs		# used for getting past unknown characters
import re 			# used for splitting up text using multiple delimiters


def probability(file_loc, out_loc, tele_rate, iterations):
	'''
	Args:
	    file_loc (str): file location of .txt files to be parsed
	    out_loc (str): file location + name of output file
	    tele_rate (float): teleport rate used for probability calculation
	    iterations (int): number of iterations for probability algorithm
	'''
	file_list = [file for file in os.listdir(file_loc)]							# creates a list of filenames
	link_list = []		# empty list
	known_math = [doc_name[5:9] for doc_name in file_list if doc_name[3] == "H"]	# creates a list of all math course numbers
	known_cosc = [doc_name[5:9] for doc_name in file_list if doc_name[3] == "C"]	# creates a list of all cosc course numbers
	known_mted = [doc_name[5:9] for doc_name in file_list if doc_name[3] == "D"]	# creates a list of all mted course numbers
	known_dups = set(list(set(known_math).intersection(set(known_cosc))) + list(set(known_math).intersection(set(known_mted))) \
	                 + list(set(known_cosc).intersection(set(known_mted))))		# creates a list of all course numbers that are common between any of the three
	for file in file_list:		# iterates through the file list and
		if file[3] == "H":		# determines what the subject is based on the
			doc_type = "M"		# fourth letter and assigns a doc_type for it
		elif file[3] == "C":
			doc_type = "C"
		else:
			doc_type = "E"
		link_list.append([doc_type + file[5:9]])	# adds the doc_type + 4 digit number to a list
		f = codecs.open(file_loc + file, "r", "utf-8", errors = "ignore")	# opens the file, ignoring unknown characters
		file_str = f.read().replace('\n', '')		# reads the text and removes line breaks
		delims = r'[\[;:+"=(&/,-.<>!@#$%*\s)\]]\s*'	# list of delimiters
		file_str = re.split(delims, file_str)		# splits the line based on delims
		temp_list = []	# empty list
		for i,item in enumerate(file_str):			# iterates through each string in the file_str list
			if item.isnumeric() and len(item) == 4 and item != file[5:9]:		# checks if the string is a 4 digit number and not the file name
				if item not in known_math and item not in known_cosc and item not in known_mted: # if the number isn't in our list of known document names
					doc_type = determine_doc_type(i, file_str)	# determines doc_type
					if doc_type == "M":		# adds the document to one of the known lists
						known_math.append(item)
					elif doc_type == "C":
						known_cosc.append(item)
					else:
						known_mted.append(item)
					link_list.append([doc_type + item])	# and appends it to our link list
					continue
				elif item in known_dups:	# if the item is in our list of duplicates courses, the program determines which subject the number references
					doc_type = determine_doc_type(i, file_str)
				elif item in known_mted:	# adds the doc_type based on known course numbers
					doc_type = "E"
				elif item in known_math:
					doc_type = "M"
				else:
					doc_type = "C"
				temp_list.append(doc_type + item)	# appends the doc_type and number to a temp list
		link_list[-1].extend(list(set(temp_list)))	# appends the temp_list to our link list

	whole_list = sorted(["C" + item for item in known_cosc] + ["E" + item for item in known_mted] + ["M" + item for item in known_math])
	# creates a sorted list of all the course numbers each with their doc_type
	link_list.sort()
	prob_matrix = [[0 for x in range(len(whole_list))] for y in range(len(whole_list))]	# creates a 2-d array of 0's
	for i,item in enumerate(link_list):		# iterates through link list
		try:
			prob_rate = 1 / (len(link_list[i]) - 1)
		except ZeroDivisionError:	# makes prob_rate 0 if program tries to divide by 0
			prob_rate = 0
		for j in range(len(link_list[i]) - 1):
			prob_matrix[i][whole_list.index(link_list[i][j + 1])] = prob_rate 	# stores the probability rate where a 0 was previously

	prob_tele_rate = 1 / len(prob_matrix)
	chance_matrix = [[prob_tele_rate] for i in range(len(whole_list))]	# creates a 2-d array with one the probablity rate in the [*][0] position
	for t in range(1, iterations + 1):	# iterates from index position 1 to (iterations + 1)
		for i in range(len(chance_matrix)):	# iterates through each 'row' in the matrix
			chance_matrix[i].append(tele_rate * prob_tele_rate + (1-tele_rate) * sum([chance_matrix[k][-1] * prob_matrix[k][i] for k in range(len(chance_matrix))]))
			# calucluates the probability of each item and appends the new probability in to the list
	ranked_matrix = []
	for i,item in enumerate(chance_matrix):		# creates a list of text files and their respective popularity rank
		if whole_list[i][0] == "C":
			ranked_matrix.append([chance_matrix[i][-1], "COSC " + str(whole_list[i][1:]) + ".txt"])
		if whole_list[i][0] == "E":
			ranked_matrix.append([chance_matrix[i][-1], "MTED " + str(whole_list[i][1:]) + ".txt"])
		if whole_list[i][0] == "M":
			ranked_matrix.append([chance_matrix[i][-1], "MATH " + str(whole_list[i][1:]) + ".txt"])
	ranked_matrix.sort(reverse = True)			# sorts in descending order
	for i,item in enumerate(ranked_matrix):		# prints the rank, file name, and popularity rating of all of the popular files
		print(str(i + 1) + ")" + " " * (5 - len(str(i + 1))) + str(item[1]) + "   " + str(item[0])[:5])

	f = open(out_loc, "w")
	for i,item in enumerate(prob_matrix):
		f.write(str(link_list[i]) + "\n" + str(item) + "\n\n")
	f.close()





def determine_doc_type(index, file_str):
	'''Looks for the first appearance of COSC, MATH or MTED in the list of words
	'''
	for i in range(index, -1, -1):
		if len(file_str[i]) == 4:
			if file_str[i] == "COSC":
				return "C"
			elif file_str[i] == "MATH":
				return "M"
			elif file_str[i] == "MTED":
				return "E"



n1 = input("Enter location of files >> ")
n2 = input("Enter location of output >> ")
n3 = float(input("Enter teleport probability (in decimals) >> "))
n4 = int(input("Number of iterations for computing probability >> "))





probability(n1, n2, n3, n4)
