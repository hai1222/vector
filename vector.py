#-*- coding: utf-8 -*-
from math import sqrt,acos,pi
from decimal import Decimal

class Vector(object):

	CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalized the zero vector'

	def __init__(self, coordinates):
		try:
			if not coordinates:
				raise ValueError
			self.coordinates = tuple(coordinates)
			self.dimension = len(coordinates)
			self.idx = 0

		except ValueError:
			raise ValueError('The coordinates must be nonempty')

		except TypeError:
			raise TypeError('The coordinates must be an iterable')

	def times_scalar(self, c):
		new_coordinates = [Decimal(c)*Decimal(x) for x in self.coordinates]
		return Vector(new_coordinates)

	def magnitude(self):
		coordinates_squared = [Decimal(x)**2 for x in self.coordinates]
		return sqrt(sum(coordinates_squared))

	def normalized(self):
		try:
			magnitude = self.magnitude()
			return self.times_scalar(1./magnitude)
		except ZeroDivisionError:
			raise Exception('Cannot normalize the zero vector')

	def dot(self, v):
		return sum([Decimal(x)*Decimal(y) for x,y in zip(self.coordinates, v.coordinates)])

	def minus(self, v):
		new_coordinates = [Decimal(x)-Decimal(y) for x,y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)

	def is_parallel_to(self, v):
		return (self.is_zero() or
			v.is_zero() or
			self.angle_with(v) == 0 or 
			self.angle_with(v) == pi)

	def angle_with(self, v, in_degrees = False):
		try:
			u1 = self.normalized()
			u2 = v.normalized()
			angle_in_radians = acos(round(u1.dot(u2), 3))

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

	def is_zero(self, tolerance=1e-10):
		return self.magnitude() < tolerance

	def is_orthogonal_to(self, v, tolerance=1e-10):
		return abs(self.dot(v)) < tolerance

	def plus(self, v):
		new_coordinates = [Decimal(x)+Decimal(y) for x,y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)

	def __iter__(self):
		return self

	def next(self):
	   self.idx += 1
	   try:
		   return Decimal(self.coordinates[self.idx-1])
	   except IndexError:
		   self.idx = 0
		   raise StopIteration  # Done iterating.

	def __getitem__(self,index):
		return Decimal(self.coordinates[index])

	def __str__(self):
		return 'Vector: {}'.format(self.coordinates)


	def __eq__(self, v):
		return self.coordinates == v.coordinates
