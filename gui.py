# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from bmath.vec import *


#定义坐标轴
plt.ion()
fig = plt.figure()
ax1 = plt.axes(projection='3d')

o = Vec(1,0,0)
a = Vec(1,1,0)
axis = Vec(1,1,1)
axis.normalize()
arrow = Arrow(a,o)

line = arrow.line(10)

z = line['z']
x = line['x']
y = line['y']
ax1.scatter3D(x,y,z, cmap='Blues')

for i in range(72):
    arrow.arotate(axis, 5)
    line = arrow.line(2)

    z = line['z']
    x = line['x']
    y = line['y']
    ax1.scatter3D(x,y,z, cmap='Blues')  #绘制散点图
    ax1.plot3D(x,y,z,'gray')    #绘制空间曲线
    plt.pause(0.001)

plt.ioff()
plt.show()