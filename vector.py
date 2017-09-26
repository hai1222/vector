from math import sqrt, acos, pi
from decimal import Decimal, getcontext

#getcontext().prec = 30

class Vector(object):

	CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'

	def __init__(self, coordinates):
		try:
			if not coordinates:
				raise ValueError
			self.coordinates = tuple([Decimal(x) for x in coordinates])
			self.dimension = len(coordinates)

		except ValueError:
			raise ValueError('The coordinates must be nonempty')

		except TypeError:
			raise TypeError('The coordinates must be an iterable')

	def dot(self, v):
		return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

	def angle_with(self, v, in_degrees=False):
		try:
			u1 = self.normalized()
			u2 = v.normalized()
			angle_in_radians = acos(u1.dot(u2))

			if in_degrees:
				degrees_per_radian = 180. / pi
				return angle_in_radians * degrees_per_radian
			else:
				return angle_in_radians

		except Exception as e:
			if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
				raise Exception('Cannot compute an angle with the zero vector')
			else:
				raise e

	def magnitude(self):
		coordinates_squared = [x**2 for x in self.coordinates]
		return sqrt(sum(coordinates_squared))

	def normalized(self):
		try:
			magnitude = self.magnitude()
			return self.times_scalar(1./magnitude)
		except ZeroDivisionError:
			raise Exception('Cannot normalize the zero vector')

	def plus(self, v):
		new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)

	def minus(self, v):
		new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)

	def times_scalar(self, c):
		new_coordinates = [Decimal(c)*x for x in self.coordinates]
		return Vector(new_coordinates)

	def __str__(self):
		return 'Vector: {}'.format(self.coordinates)

	def __eq__(self, v):
		return self.coordinates == v.coordinates

v = Vector([3.183, -7.627])
w = Vector([-2.668, 5.319])
print v.eighttwo(w)

v = Vector([7.35, 0.221, 5.188])
w = Vector([2.751, 8.259, 3.985])
print v.eighttwo(w) * 180 / math.pi