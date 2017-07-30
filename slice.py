
import numpy as np
import shapely.geometry as sg
import math

def slice_poly(poly, area):
    """
    Slices a piece of a given area off of a polygon.

    :param poly: the polygon to slice
    :param area: how large the removed area should be
    :returns: tuple (poly, remainder)
        WHERE
        poly is the section with the desired area
        remainder is the rest of the polygon
    """

    if poly.interiors:
        raise NotImplementedError("Only simple polygons are supported")

    if poly.area < area or math.isclose(poly.area, area):
        return poly, sg.Polygon()  # take the whole chunk

    # find a triangle thing
    u = np.array(poly.exterior.coords[0]) - np.array(poly.exterior.coords[1])
    v = np.array(poly.exterior.coords[2]) - np.array(poly.exterior.coords[1])
    a = 2*area/abs(np.cross(u, v)) # >1 means it extends beyond the original borders
    
    rpts = poly.exterior.coords[:]
    if math.isclose(a, 1.0):
        tri = sg.Polygon(rpts[0:3])
        remainder = sg.Polygon(rpts[:1]+rpts[2:])
    elif a > 1:
        tri = sg.Polygon(rpts[0:3])
        remainder = sg.Polygon(rpts[:1]+rpts[2:])
        tri, remainder = slice_poly(remainder, area-tri.area)
        tpts = tri.exterior.coords[:]
        tri = sg.Polygon(tpts[:1]+rpts[1:2]+tpts[1:])
    else:
        p = np.array(poly.exterior.coords[1]) + a*v
        tri = sg.Polygon([rpts[0], rpts[1], p])
        remainder = sg.Polygon(rpts[:1]+[p]+rpts[2:])

    return tri, remainder


def rotate_coords(poly, n=1):
    """
    Rotates the exterior coordinate list of a Polygon, making the nth point the root point

    :param poly: the polygon to rotate
    :param n: the amount to rotate by
    :returns: the rotated polygon
    """
    c = poly.exterior.coords[:]
    c = c[:-1]  # de-duplicate the root point
    c = c[n:]+c[:n]  # rotate by n
    c.append(c[0])  # re-duplicate the root point

    return sg.Polygon(shell=c, holes=poly.interiors)


def regular_polygon(sides, upright=True):
    """
    Returns a polygon inscribed in the unit circle
    """
    points = []
    if upright:
        off = math.pi/sides - math.pi/2
    else:
        off = 0

    for i in range(sides):
        ang = 2*math.pi*i/sides + off
        p = (math.cos(ang), math.sin(ang))
        points.append(p)

    return sg.Polygon(points)