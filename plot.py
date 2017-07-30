
from slice import *

from shapely.geometry import box
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as spc
import matplotlib.patches as mp
import shapely.geometry as sg
import math
from matplotlib import animation
from tqdm import tqdm, trange


fig = plt.figure()
plt.axis([-1,1,-1,1])
ax = plt.gca()
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_aspect(1)

def slicing(poly, divisions):
    area = poly.area / divisions
    while True:
        result, poly = slice_poly(poly, area)
        yield result
        if poly.is_empty: break
        poly = rotate_coords(poly)

def init():
    return []

def animate(frame):
    n = frame
    items = []
    ax.clear()

    for sl, i in tqdm(zip(slicing(poly, n), range(math.ceil(n))), total=math.ceil(n)):
        # import IPython; IPython.embed()
        fill = mp.Polygon(np.array(sl.exterior.xy).T, closed=True, facecolor='C{}'.format(i%10), zorder=1)
        items.append(ax.add_patch(fill))
        line, = ax.plot(*sl.exterior.xy, 'k-', linewidth=linewidth, zorder=2)
        items.append(line)
            # ax.plot(*sl.centroid.coords[0], 'o')
            # ax.text(*sl.centroid.coords[0], "{}".format(i), ha='center', va='center')

        # import traceback; traceback.print_exc()
        # import IPython; IPython.embed()
    return items

shapes = {}
sides = list(range(3,9))+[10, 12, 15, 20, 50]
for x in sides:
    shapes["{}-gon".format(x)] = regular_polygon(x)
# shapes["golden-rect-wide"] = box(-spc.golden,-1,spc.golden,1)
# shapes["golden-rect-tall"] = box(-1,-spc.golden,1,spc.golden)
shapes["trunc-square"] = rotate_coords(sg.polygon.orient(box(-1,-1,0,0).union(box(-1,0,0,1)).union(box(0,-1,1,0)).convex_hull))

linewidth = 1.0

# selected = {k:shapes[k] for k in ["trunc-square"] if k in shapes}
selected = shapes

ipbar = tqdm(selected.items())
# ipbar = tqdm([3])
for name, polygon in ipbar:
    ipbar.set_description(name)
    poly = polygon

    cutcnt = list(range(2,21))+[30, 50, 200, 1000]
    cutlinewidth = [1]*len(range(2,21))+[.8,.5,.1,.05]
    jpbar = tqdm(zip(cutcnt, cutlinewidth), total=len(cutcnt))
    for j, lw in jpbar:
        linewidth = lw
        jpbar.set_description(str(j))
        animate(j)
        plt.savefig('images/{}-{}.png'.format(name,j), bbox_inches='tight')
    jpbar.close()

    linewidth=1.0
    frames = np.sort(np.concatenate([
        np.geomspace(1.,50.,1000),
        np.floor(np.geomspace(1.,50.,450)),
        np.repeat(50., 50)
        ]))

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=tqdm(frames), interval=20)
    anim.save('animations/{}.gif'.format(name), dpi=80, writer='imagemagick')

ipbar.close()

# plt.show()
