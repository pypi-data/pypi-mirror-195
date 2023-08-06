import math
import numpy

def radius(volume):
    radius = numpy.cbrt(volume/(math.pi*(4/3)))
    return radius