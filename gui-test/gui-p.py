# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
from bmath.vec import *


#定义坐标轴
fig = plt.figure()
ax = p3.Axes3D(fig)

o = Vec(0,0,0)
a = Vec(1,1,1)
axis = Vec(1,0,0)
arrow = Arrow(a,o)


def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
    return lines

lines = []
data = []
for i in range(5):
    arrow.arotate(axis, i)
    line = arrow.line(10)

    z = line['z']
    x = line['x']
    y = line['y']
    data.append([x,y,z])
    for dx, dy, dz in zip(x, y, z):
        lines.append(ax.plot(dx, dy, dz)[0])
data = np.array(data)


# Setting the axes properties
ax.set_xlim3d([-2.0, 2.0])
ax.set_xlabel('X')

ax.set_ylim3d([-2.0, 2.0])
ax.set_ylabel('Y')

ax.set_zlim3d([-2.0, 2.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, 100, fargs=(data, lines),
                                   interval=0, blit=True)

plt.show()