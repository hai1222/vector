#-*- coding: utf-8 -*-
from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    def is_parallel_to(self, ell):
        '''
        判断两条直接是否平行
        '''
        n1 = Vector(self.normal_vector)
        n2 = Vector(ell.normal_vector)
        return n1.is_parallel_to(n2)

    def __eq__(self, ell):
        '''
        判断两个平面是否是同一个平面
        '''
        if Vector(self.normal_vector).is_zero():
            if not Vector(ell.normal_vector).is_zero():
                return False
            else:
                deff = self.constant_term - ell.constant_term
                return MyDecimal(diff).is_near_zero()
        elif Vector(ell.normal_vector).is_zero():
            return False

        if not self.is_parallel_to(ell):
            return False

        x0 = self.basepoint
        y0 = ell.basepoint
        basepoint_difference = x0.minus(y0)

        n = self.normal_vector
        return basepoint_difference.is_orthogonal_to(Vector(n))


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = Decimal(n[initial_index])

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

print '1#'
p1 = Plane([-0.412, 3.806, 0.728], -3.46)
p2 = Plane([1.03, -9.515, -1.82], 8.65)
print p1.is_parallel_to(p2)
print p1 == p2

print '2#'
p1 = Plane([2.611, 5.528, 0.283], 4.6)
p2 = Plane([7.715, 8.306, 5.342], 3.76)
print p1.is_parallel_to(p2)
print p1 == p2

print '3#'
p1 = Plane([-7.926, 8.625, -7.212], -7.95)
p2 = Plane([-2.692, 2.875, -2.404], -2.443)
print p1.is_parallel_to(p2)
print p1 == p2