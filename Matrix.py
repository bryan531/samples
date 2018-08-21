from random import *
from fractions import *





class matrix:
	'''A matrix class
	'''
	def __init__(self, grid):
		input_err = '\n\nMatrix class requires rectangular grid of numbers as input.\n\n'
		try:
			self._coldim = len(grid[0])
			if self._coldim == 0:
				raise ValueError(input_err)
			self._data = []
			for row in grid:
				if (len(row) != self._coldim) or not all([type(x) in [float,int,ComplexNumber,Fraction] for x in row]):
					raise ValueError(input_err[2:-2])
				else:
					self._data.append(tuple(row))
		except:
			print(input_err)
			raise
		self._data = tuple(self._data)
		self._rowdim = len(grid)


	def __repr__(self):
		return str(self._data)

	def __getitem__(self, coords):
		if type(coords) != type( (1,1) ):
			raise TypeError('Matrices require a tuple for indexing.')
		i,j = coords
		return self._data[i][j]


	def __mul__(self, other):
		mult_err = 'Matrices may only be multiplied by scalars, or by matrices of appropriate dimensions.'
		if type(other) is vector and self._coldim == other.dims():
			other = other.col()
		if type(self) == type(other): # matrix multiplication
			m,n = self.dims()
			p,q = other.dims()
			if n != p:
				raise ValueError(mult_err)
			new_grid = [[sum([self[i,k] * other[k,j] for k in range(n)]) for j in range(q)] for i in range(m)]
			return matrix(new_grid)
		elif type(other) in [type(1), type(0.1), ComplexNumber]: # scalar multiplication
			m,n = self.dims()
			new_grid = [[self[i,j] * other for j in range(n)] for i in range(m)]
			return matrix(new_grid)
		else:
			raise TypeError(mult_err)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __str__(self):
		return_string = ""
		m, n = self.dims()
		matrix_list = [[self[i,j] for j in range (n)] for i in range(m)]
		for item in matrix_list:
			return_string += "|"
			for thing in item:
				if type(thing) is float:
					thing = float(str(thing)[:9])
				return_string += " " * (12 - len(str(thing))) + str(thing)
			return_string += "  |\n"
		return return_string

	def __add__(self, other):
		if type(self) == type(other):
			m, n = self.dims()
			if self.dims() != other.dims():
				raise ValueError('Cannot add matrices of different dimensions.')
			new_grid = [[self[i,j] + other[i,j] for j in range(n)] for i in range(m)]
			return matrix(new_grid)

	def __radd__(self, other):
		return self.__add__(other)

	def __sub__(self, other):
		if type(self) == type(other):
			if self.dims() != other.dims():
				raise ValueError('Cannot subtract matrices of different dimensions.')
			else:
				return self + -1 * other

	def swap(self,i,j):
		'''matrix.swap(i, j) where 'i' and 'j' are the indices of the rows to be
		swapped
		'''
		try:
			return_matrix = list(self._data)
			return_matrix[i], return_matrix[j] = return_matrix[j], return_matrix[i]
		except:
			print("Can't do that.")
			raise

		return matrix(return_matrix)

	def transpose(self):
		'''Returns the transpose of a matrix
		'''
		m, n = self.dims()
		return matrix([[self[j,i] for j in range(m)] for i in range(n)])

	def scalerow(self, i, s):
		'''matrix.(scalerow(i, s)) where 'i' is the index of the row being scaled,
		and 's' is the scalar for the row
		'''
		return_matrix = list(self._data)
		matrix_row = [item * s for item in return_matrix[i]]
		return_matrix[i] = tuple(matrix_row)
		return matrix(return_matrix)

	def scaleandadd(self, i, j, s):
		'''matrix.scaleandadd(i, j, s) where 'i' is the index of the row being
		scaled, 'j' is the index of the row that the scaled 'i' is being added
		to and 's' is the scalar for row 'i'
		'''
		return_matrix = list(self._data)
		try:
			scaled_row = [item * s for item in return_matrix[i]]
			new_row = [scaled_row[m] + return_matrix[j][m] for m in range(len(scaled_row))]
			return_matrix[j] = new_row
		except:
			print("That's not happening.")
			raise
		return matrix(return_matrix)

	def dims(self):
		return tuple([self._rowdim, self._coldim])

	def genrand(m, n):
		'''Generates an m x n matrix of integers and ComplexNumbers(floats and
		fractions excluded)
		'''
		return_list = [[0 for j in range(n)] for i in range(m)]
		for i in range(m):
			for j in range(n):
				rand_int = randint(0,3)
				if rand_int == 10:
					return_list[i][j] = ComplexNumber(randint(-9,9),randint(-9,9))
				else:
					return_list[i][j] = randint(-9,9)
		return matrix(return_list)

	def ref(self):
		'''Reduces a matrix to row echelon form.
		'''
		m, n = self.dims()
		for i in range(m):
			largest_row = self.findlargest(i)
			if largest_row != i:
				self = self.swap(largest_row, i)
			for x in range(i + 1, m):
				self = self.scaleandadd(i, x, -1 * Fraction(self[x,i], self[i,i]))
		return self
					
	def findlargest(self, col):
		'''Returns the index of the row with the largest absolute value in a
		specific column.
		'''
		m, n = self.dims()
		largest = col
		for x in range(col + 1, m):
			if abs(self[x, col]) > abs(self[largest, col]):
				largest = x
		return largest

	def augment(self, other):
		'''Augments a vector or matrix to another matrix
		'''
		return_matrix = []
		if type(other) not in [matrix, vector]:
			raise TypeError("Must be either a matrix or vector to augment.")
		else:
			if type(other) is vector:
				other = other.col()
			m1, n1 = self.dims()
			m2, n2 = other.dims()
			if m1 != m2:
				raise ValueError("Rows must be equal dimensions.")
			else:
				for i in range(m1):
					return_matrix.append(self._data[i] + other._data[i])
			return matrix(return_matrix)

	def idmatrix(size):
		'''Generates an n x n identity matrix.
		'''
		return matrix([[1 if i == j else 0 for j in range(size)] for i in range(size)])

	def inverse(self):
		'''Computes the inverse of a square matrix.
		'''
		return_matrix = []

		if type(self) not in [matrix]:
			raise TypeError("Must be a matrix to find an inverse")

		elif self.isinvertible():
			m, n = self.dims()
			self = self.augment(matrix.idmatrix(m)).ref()
			for i in range(m):
				largest_row = self.findlargest(i)
				if largest_row != i:
					self = self.swap(largest_row, i)

				self = self.scalerow(i, Fraction(1, self[i,i]))

				for j in range(i - 1, -1, -1):
					self = self.scaleandadd(i, j, Fraction(self[j,i], -1))

			for i in range(m):
				return_matrix.append(self._data[i][m:])
		else:
			raise ValueError("Matrix is not invertible.")

		return matrix(return_matrix)

	def isinvertible(self):
		'''Determines if a matrix is invertible.
		'''
		return_value = True
		m, n = self.dims()
		if m != n:
			return_value = False
		else:
			self = self.ref().transpose().ref()
			for i in range(m):
				if self[i,i] == 0:
					return_value = False
		return return_value

	def backsub(self, loading_vector):
		'''Accepts an upper triangular matrix and solves the system of equations
		with 'loading_vector' as the solution set.
		'''
		temp_list = [list(item) for item in self._data]
		answers = []
		if type(loading_vector) is not vector:
			raise TypeError("Must be a vector to find solution.")
		m, n = self.dims()
		if not self.triangular():
			raise ValueError("Not upper triangular.")
		for i in range(m - 1, -1, -1):
			answers.append(Fraction((loading_vector[i] - sum(temp_list[i][i + 1:])), temp_list[i][i]))
			for j in range(i, -1, -1):
				temp_list[j][i] *= answers[-1]
		return vector(answers[::-1])

	def forwardsub(self, loading_vector):
		'''Accepts a lower triangular matrix and solves the system of equations
		with 'loading_vector' as the solution set.
		'''
		temp = []
		if type(loading_vector) is not vector:
			raise TypeError("Must be a vector to find solution.")
		m, n = self.dims()
		if not self.transpose().triangular():
			raise ValueError("Not lower triangular.")
		for i in range(m - 1, -1, -1):
			temp.append(self._data[i][::-1])
		self = matrix(temp)
		loading_vector = vector(loading_vector._data[::-1])
		return_vector = self.backsub(loading_vector)
		return vector(return_vector[::-1])

	def triangular(self):
		'''Determines if the matrix is upper triangular.
		'''
		return_value = True
		m, n = self.dims()
		if m != n:
			raise ValueError("Must be a square matrix.")
		for i in range(n):
			for j in range(i + 1, m):
				if self[j,i] != 0:
					return_value = False
		return return_value

	def gramschmidt(self):
		'''Orthonormalizes column vectors of a matrix using the Gram-Schmidt algorithm.
		'''
		if type(self) is not matrix:
			raise TypeError("Must be a matrix to orthonormalize")
		temp = []
		qlist = []
		m, n = self.dims()
		self = self.transpose()
		for x in self._data:
			temp.append(vector(x))
		qlist.append(temp[0] * (1 / temp[0].mag()))
		for vect in temp:
			total = vector([0] * m)
			for j in range(1, len(qlist)):
				total += (qlist[j].proj(vect))
			w = (vect + total * -1)
			w *= 1 / w.mag()
			qlist.append(w)
		qlist = qlist[1:]
		ret_matrix = qlist[0].col()
		for x in range(1,len(qlist)):
			ret_matrix = ret_matrix.augment(qlist[x])

		return ret_matrix

	def palu(self):
		m, n = self.dims()
		if m != n:
			raise ValueError('Nonsquare matrix.')

		elif not self.isinvertible():
			raise ValueError('Singular matrix.')

		else:
			P = [[1 if i==j else 0 for j in range(n)] for i in range(m)]
			mat = [[self[i,j] for j in range(n)] for i in range(m)]
			for j in range(m):
				maxv = abs(mat[j][j])
				piv = j
				for i in range(j + 1, m):
					if abs(mat[i][j]) > maxv:
						maxv = mat[i][j]
						piv = i
				if piv != j:
					mat = mat[:j] + [mat[piv]] + mat[j + 1:piv] + [mat[j]] + mat[piv + 1:]
					P = P[:j] + [P[piv]] + P[j + 1:piv] + [P[j]] + P[piv + 1:]
				for i in range(j + 1, m):
					mult = Fraction(mat[i][j], mat[j][j])
					mat[i][j] = mult
					for c in range(j + 1, n):
						mat[i][c] += -mult * mat[j][c]
			L = matrix([[1 if i == j else (0 if j > i else mat[i][j]) for j in range(n)] for i in range(m)])
			U = matrix([[mat[i][j] if j >= i else 0 for j in range(n)] for i in range(m)])
			return (matrix(P),L,U)




class ComplexNumber:
	'''A complex number class.
	'''
	def __init__(self, a, b):
		if (type(a) in [type(1), type(1.1)]) and (type(b) in [type(1),type(1.1)]):
			self._real_part = a
			self._imag_part = b
		else:
			raise TyperError('Complex numbers must have real coordinates.')

	def __repr__(self):
		return "(" + str(self._real_part) + "," + str(self._imag_part) + ")"

	def __str__(self):
		return str(self._real_part) + " + " + str(self._imag_part) + "i"

	def re(self):
		return self._real_part

	def im(self):
		return self._imag_part

	def __add__(self, other):
		if type(self) == type(other):
			return ComplexNumber(self.re() + other.re(), self.im() + other.im())
		elif type(other) in [type(0.1), type(1)]:
			return ComplexNumber(self.re() + other, self.im())
		else:
			raise TypeError('Not valid.')

	def __radd__(self, other):
		return self.__add__(other)

	def __mul__(self, other):
		if type(self) == type(other):
			return ComplexNumber(self.re() * other.re() - self.im() * other.im(), self.im() * other.re() + self.re() * other.im())
		elif type(other) in [type(0.1), type(1)]:
			return ComplexNumber(self.re() * other, self.im() * other)
		else:
			raise TypeError('Not valid.')

	def __rmul__(self, other):
		return self.__mul__(other)

	def conj(self):
		return ComplexNumber(self.re(), -self.im())

	def norm(self):
		return sqrt(self.re() ** 2 + self.im() ** 2)

	def __sub__(self,other):
		if type(other) in [float, int, ComplexNumber]:
			return self + (-1) * other
		else:
			raise TypeError('Wrong input')

class vector:
	'''a vector class
	'''
	def __init__(self, data):
		
		init_err = 'Vector expects one-dimensional list or tuple of numbers.'
		if type(data) not in [list, tuple]:
			raise TypeError(init_err)
		new_data = []

		try:
			for x in data:
				if type(x) in [float, int, ComplexNumber, Fraction]:
					new_data.append(x)
				else:
					new_data.append(float(x))
		
		except:
			raise TypeError(init_err)

		self._data = tuple(new_data)

	def __repr__(self):
		return str(self._data)

	def __str__(self):
		return_string = "<"
		for i, item in enumerate(self._data):
			return_string += str(item)
			if i != len(self._data) - 1:
				return_string += ", "
		return_string += ">"
		return return_string

	def dims(self):
		return len(self._data)

	def __getitem__(self,i):
		return self._data[i]

	def __add__(self, other):
		if self.dims() != other.dims():
			raise ValueError('Cannot add vectors of different dimensions.')
		else:
			try:
				return_vector = [self[i] + other[i] for i in range(self.dims())]
			except:
				raise
		return vector(return_vector)

	def __radd__(self, other):
		return self.__add__(other)

	def __mul__(self,other):
		if type(other) not in [float, int, ComplexNumber, Fraction, matrix]:
			raise TypeError('Vectors can only be multiplied by scalars.')
		if type(other) is matrix:
			m, n = other.dims()
			if m != self.dims():
				raise ValueError("Wrong dimensions")
			else:
				return_vector = [sum([self[k] * other[k,j] for k in range(m)]) for j in range(n)]
		else:
			return_vector = [self[i] * other for i in range(self.dims())]
		return vector(return_vector)

	def __rmul__(self,other):
		return self.__mul__(other)

	def col(self):
		'''Returns the vector as an n x 1 column matrix.
		'''
		return matrix([[self[i] for j in range(1)] for i in range(self.dims())])

	def dot(self, other):
		'''Computes the dot product of two vectors.
		'''
		if self.dims() != other.dims():
			raise ValueError('Dot product requires vectors of the same dimensions.')
		else:
			return_answer = sum(self[i] * other[i] for i in range(self.dims()))
		return return_answer

	def mag(self):
		'''Computes the magnitude of a vector
		'''
		return self.dot(self) ** (0.5)

	def proj(self, b):
		'''Computes projection of b onto self. (proj_self b)
		'''
		if type(self) is not vector or type(b) is not vector:
			raise TypeError("Must be vectors")
		return (self.dot(b) / self.mag() ** 2) * self





