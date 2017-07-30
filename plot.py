
from slice import *

from shapely.geometry import box
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mp
import shapely.geometry as sg
import math
from matplotlib import animation
from tqdm import tqdm, trange

# plt.subplots_adjust(bottom = 0.1)
# plt.axis('equal')
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

# poly = box(0,0,1,1)
# poly = regular_polygon(200)


def init():
    return []

def animate(frame):
    n = frame
    items = []
    ax.clear()

    for sl, i in zip(slicing(poly, n), range(math.ceil(n))):
        # import IPython; IPython.embed()
        fill = mp.Polygon(np.array(sl.exterior.xy).T, closed=True, facecolor='C{}'.format(i%10), zorder=1)
        items.append(ax.add_patch(fill))
        line, = ax.plot(*sl.exterior.xy, 'k-', linewidth=1, zorder=2)
        items.append(line)
            # ax.plot(*sl.centroid.coords[0], 'o')
            # ax.text(*sl.centroid.coords[0], "{}".format(i), ha='center', va='center')

        # import traceback; traceback.print_exc()
        # import IPython; IPython.embed()
    return items

ipbar = tqdm(list(range(4,9))+[10, 12, 15, 20, 50])
# ipbar = tqdm([3])
for i in ipbar:
    poly = regular_polygon(i)
    ipbar.set_description("{}-gon".format(i))

    # jpbar = tqdm(list(range(2,11))+[15, 20, 30, 50, 200])
    # for j in jpbar:
    #     jpbar.set_description("{} pieces".format(j))
    #     jpbar.update(0)
    #     animate(j)
    #     plt.savefig('images/{}-gon-{}.png'.format(i,j), bbox_inches='tight')
    # jpbar.close()

    frames = np.sort(np.concatenate([
        np.geomspace(1.,50.,1000),
        np.floor(np.geomspace(1.,50.,450)),
        np.repeat(50., 50)
        ]))


    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=tqdm(frames), interval=20)
    anim.save('animations/{}-gon.gif'.format(i, 30), dpi=80, writer='imagemagick')
ipbar.close()


# plt.show()
