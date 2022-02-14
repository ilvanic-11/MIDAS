import math
import numpy
import numpy as np
import sympy
import itertools

def get_All_Possible_Addends(a, b, c):
    """
    A is the number for which we are looking for addends based on constraint b, values we don't want, and c, the number
    of possible values to add together(i.e. if c is 3, then we would need 3 addends in each solutions in our output list
    of possible solutions.
    :param a:
    :param b:
    :param d:
    :return: List of possible solutions
    """
    list_1 = [i for i in range(1, a, 1)]
    #itertools.permutations
    result = itertools.combinations(list_1, c)



