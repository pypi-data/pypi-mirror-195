#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
from collections.abc import Iterable
from itertools import combinations

# Other imports
from FiberFusing import buffer
from MPSPlots.Render2D import Scene2D, Axis
from shapely.ops import unary_union
from shapely.ops import nearest_points
import shapely.geometry as geo


def NearestPoints(Object0, Object1):
    if hasattr(Object0, '_shapely_object'):
        Object0 = Object0._shapely_object

    if hasattr(Object0, '_shapely_object'):
        Object1 = Object1._shapely_object

    P = nearest_points(Object0.exterior, Object1.exterior)

    return buffer.Point(position=(P[0].x, P[0].y))


def Union(*Objects):
    if len(Objects) == 0:
        return buffer.Polygon(instance=geo.Polygon())

    Objects = [o._shapely_object if hasattr(o, '_shapely_object') else o for o in Objects]
    output = unary_union(Objects)

    return buffer.Polygon(instance=output)


def Intersection(*Objects):
    if len(Objects) == 0:
        return buffer.Polygon(instance=geo.Polygon())

    Objects = [o._shapely_object if hasattr(o, '_shapely_object') else o for o in Objects]

    intersection = unary_union(
        [a.intersection(b) for a, b in combinations(Objects, 2)]
    )

    return buffer.Polygon(instance=intersection)


# 4th order accurate gradient function based on 2nd order version from http://projects.scipy.org/scipy/numpy/browser/trunk/numpy/lib/function_base.py
def gradientO4(f, *varargs):
    """Calculate the fourth-order-accurate gradient of an N-dimensional scalar function.
    Uses central differences on the interior and first differences on boundaries
    to give the same shape.
    Inputs:
      f -- An N-dimensional array giving samples of a scalar function
      varargs -- 0, 1, or N scalars giving the sample distances in each direction
    Outputs:
      N arrays of the same shape as f giving the derivative of f with respect
       to each dimension.
    """
    N = len(f.shape)  # number of dimensions
    n = len(varargs)
    dx = list(varargs)

    # use central differences on interior and first differences on endpoints

    outvals = []

    # create slice objects --- initially all are [:, :, ..., :]
    slice0 = [slice(None)] * N
    slice1 = [slice(None)] * N
    slice2 = [slice(None)] * N
    slice3 = [slice(None)] * N
    slice4 = [slice(None)] * N

    otype = f.dtype.char
    if otype not in ['f', 'd', 'F', 'D']:
        otype = 'd'

    for axis in range(N):
        # select out appropriate parts for this dimension
        out = numpy.zeros(f.shape, f.dtype.char)

        slice0[axis] = slice(2, -2)
        slice1[axis] = slice(None, -4)
        slice2[axis] = slice(1, -3)
        slice3[axis] = slice(3, -1)
        slice4[axis] = slice(4, None)
        # 1D equivalent -- out[2:-2] = (f[:4] - 8*f[1:-3] + 8*f[3:-1] - f[4:])/12.0
        out[tuple(slice0)] = (f[tuple(slice1)] - 8.0 * f[tuple(slice2)] + 8.0 * f[tuple(slice3)] - f[tuple(slice4)]) / 12.0

        slice0[axis] = slice(None, 2)
        slice1[axis] = slice(1, 3)
        slice2[axis] = slice(None, 2)
        # 1D equivalent -- out[0:2] = (f[1:3] - f[0:2])
        out[tuple(slice0)] = (f[tuple(slice1)] - f[tuple(slice2)])

        slice0[axis] = slice(-2, None)
        slice1[axis] = slice(-2, None)
        slice2[axis] = slice(-3, -1)
        # 1D equivalent -- out[-2:] = (f[-2:] - f[-3:-1])
        out[tuple(slice0)] = (f[tuple(slice1)] - f[tuple(slice2)])

        # divide by step size
        outvals.append(out / dx[axis])

        # reset the slice object in this dimension to ":"
        slice0[axis] = slice(None)
        slice1[axis] = slice(None)
        slice2[axis] = slice(None)
        slice3[axis] = slice(None)
        slice4[axis] = slice(None)

    if N == 1:
        return outvals[0]
    else:
        return outvals


def interpret_to_tuple(*args):
    args = tuple(arg if isinstance(arg, Iterable) else tuple(arg.x, arg.y) for arg in args)

    if len(args) == 1:
        return args[0]
    return args


def interpret_to_point(*args):
    args = tuple(arg if isinstance(arg, buffer.Point) else buffer.Point(position=arg) for arg in args)

    if len(args) == 1:
        return args[0]
    return args


def multi_plot(*geometry, title=''):
    figure = Scene2D(unit_size=(6, 6), title=title)
    ax = Axis(row=0, col=0, x_label='x', y_label='y', colorbar=False, equal=True)
    figure.add_axes(ax)

    figure._generate_axis_()
    for poly in geometry:
        poly._render_(ax)

    figure.show()

# -
