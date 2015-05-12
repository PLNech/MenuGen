import math

__author__ = 'PLNech'


def format_length_integer(max_value, margin=0):
    """
    Returns the appropriate length to fit numbers up to a maximum value

    :param max_value the higher value you could print
    :type max_value int
    :param margin a margin to add
    :type int
    :rtype int
    """
    return math.ceil(math.log10(max_value) + 1 + margin)
