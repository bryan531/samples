'''
		Bryan Pennington
		COSC 4315
		Assignment 5

		Description: This program will parse through a text file, finding all of
		the possible dates contained in the file. It will then compare which of
		the dates are actually the same and keep count of the total number of
		each occurence of the dates. It will then return the three highest
		ranked dates.
'''





import codecs
import re


def check_equality(a1, a2):
	'''
	Compares two lists of strings where the first element is the month, second
	element is the day and third is for the year. Determines if they're the same
	by comparing the first three letters of the month, the two days, and the
	last two digits of the year.

	Args:
	    a1 (str): First date to compare
	    a2 (str): Second date to compare
	'''
	return True if (a1[0][:3] == a2[0][:3] and int(a1[1]) == int(a2[1]) and str(a1[2])[-2:] == str(a2[2])[-2:]) else False


def expand_month(m1):
	'''
	Accepts any abbreviated month and returns the entire month string.

	Args:
	    m1 (str): any abbreviated month
	'''
	if m1[:3].lower() == "jan":
		return "January"
	elif m1[:3].lower() == "feb":
		return "February"
	elif m1[:3].lower() == "mar":
		return "March"
	elif m1[:3].lower() == "apr":
		return "April"
	elif m1[:3].lower() == "may":
		return "May"
	elif m1[:3].lower() == "jun":
		return "June"
	elif m1[:3].lower() == "jul":
		return "July"
	elif m1[:3].lower() == "aug":
		return "August"
	elif m1[:3].lower() == "sep":
		return "September"
	elif m1[:3].lower() == "oct":
		return "October"
	elif m1[:3].lower() == "nov":
		return "November"
	elif m1[:3].lower() == "dec":
		return "December"
	else:
		return "Unkown"


n1 = input("Enter Input Document Location >>")

f = codecs.open(n1, "r", "utf-8", errors = "ignore")	# opens the file, ignoring unknown characters

answer_list = []
month_list = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
month_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", \
			  8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

for line in f:									# iterates through each line in the file
	delims = r'[[;:+"=(&,.?<>!@#$%*\s)\]]\s*'	# list of delimiters
	line = re.split(delims, line)				# splits the line based on the delimiters
	for i,item in enumerate(line):				# iterates through each string
		if item.lower()[:3] in month_list:		# if the first three characters are in our list of abbreviated months
			month = item
			if line[i - 1].isnumeric() and (len(line[i - 1]) == 1 or len(line[i - 1]) == 2):	# checks if the string before the month is a day
				day = line[i - 1]
				if line[i + 1].isnumeric() and (len(line[i + 1]) == 2 or len(line[i + 1]) == 4):	# checks if the string after the month is a year
					year = line[i + 1]
					answer_list.append((month, day, year, 1))
			if line[i + 1].isnumeric() and (len(line[i + 1]) == 1 or len(line[i + 1]) == 2):	# checks if the string after the month is a day
				day = line[i + 1]
				if line[i + 2].isnumeric() and (len(line[i + 2]) == 2 or len(line[i + 2]) == 4):	# checks if the string after the day is a month
					year = line[i + 2]
					answer_list.append((month, day, year, 1))	# adds the answer to our list of answers
		elif "-" in item or "/" in item:	# if the string contains '-' or '/'
			delims = r'[[;:+"=(&-/,.?<>!@#$%*\s)\]]\s*'	# same list of delimiters but with '-/' added
			item = re.split(delims, item)	# splits the item
			if len(item) == 3 and item[0].isnumeric() and item[1].isnumeric() and item[2].isnumeric():		# checks if it has three numbers in it
				year = item[-1]				# assumes the last number is the year
				if int(item[0]) > 12:		# checks if the first item cannot possibly be a month
					month = item[1]
					day = item[0]
				else:						# default action - first item is month, second is day
					month = item[0]
					day = item[1]
				answer_list.append((month_dict[int(month)], day, year, 1))	# adds our answer to our list of answers
f.close()
answer_list.sort()

for i in range(len(answer_list) - 1, -1, -1):					# iterates backwards through the list, comparing if the dates are the same, if they are
	if check_equality(answer_list[i], answer_list[i - 1]):		# combine them, removing extras, and keeps track of the total number of occurences of each date
		year = max([int(answer_list[i][2]), int(answer_list[i - 1][2])])	# this will check to see which, if any, of the years are in the 4-digit
																			# form and stores that form in the answer list
		answer_list[i - 1] = (answer_list[i - 1][0], answer_list[i - 1][1], year, answer_list[i - 1][3] + answer_list[i][3])
		del answer_list[i]



for i in range(len(answer_list)):			# formats the list of days and restructures the list so that the number of occurences is the first item
											# so the program can use answer_list.sort() and automatically sort by occurences
	month = expand_month(answer_list[i][0])	# expands abbreviated months

	if len(answer_list[i][1]) == 1:			# appends a '0' character to a single digit integer day
		day = "0" + answer_list[i][1]
	else:
		day = answer_list[i][1]

	if len(str(answer_list[i][2])) == 2:	# checks if the length of the year is still in its 2-digit form
		if int(answer_list[i][2]) < 17:		# if it is, it'll check if the integer is less than 17 and assume that the year is supposed to be 20##
			year = "20" + answer_list[i][2]	# otherwise it assumes the year should be 19##
		else:
			year = "19" + answer_list[i][2]
	else:
		year = answer_list[i][2]
	answer_list[i] = (answer_list[i][3], month, day, year)	# stores list with number of occurences first
answer_list.sort(reverse = True)


# prints out the three highest ranked dates in a nicely formatted way
print("Rank  |Date                 |Occurence\n=======================================")
for i in range(3):
	occ, month, day, year = answer_list[i]
	print(str(i + 1) + ")    |" + month + " " + day + ", " + str(year) + " " * (10 - len(month) + len(day)) + "| " + str(occ))

