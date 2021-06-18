# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from bmath.vec import *


#定义坐标轴
plt.ion()
fig = plt.figure()
ax1 = plt.axes(projection='3d')

a = Vec(0,0,0, 'zero')
b = Vec(10,10,10, 'mid')
c = Vec(15,15,15, 'top')

vaxis = Vec(0,0,1, 'vaxis')
h1axis = Vec(1,-1,0, 'h1axis')
h2axis = Vec(1,-1,0, 'h2axis')
raxis = Vec(1,0,0, 'raxis')

axis_group = [vaxis, h1axis, h2axis, raxis]
for axis in axis_group:
    axis.normalize()
# vaxis -> [b, c, h1axis, h2axis, raxis] raxis -> [b, c, h1axis, h2axis] h1axis -> [b, c] h2axis -> [c]

van = AxisNode(vaxis, a, [b, c], [h1axis, h2axis, raxis], name='v-axis')
ran = AxisNode(raxis, a, [b, c], [h1axis, h2axis], name='r-axis')
h1an = AxisNode(h1axis, a, [b, c], [], name='h1-axis')
h2an = AxisNode(h2axis, b, [c], [], name='h2-axis')

leg = Joint([van, ran, h1an, h2an], [a, b, c], name='leg0')
line = leg.coordinate(2)

z = line['z']
x = line['x']
y = line['y']
ax1.scatter3D(x,y,z, cmap='Blues')


for i in range(2):
    leg.arotate('h2-axis', 30)
    line = leg.coordinate(2)

    z = line['z']
    x = line['x']
    y = line['y']
    ax1.scatter3D(x,y,z, cmap='Reds')  #绘制散点图
    ax1.plot3D(x,y,z,'gray')     #绘制空间曲线
    plt.pause(1)

for i in range(2):
    leg.arotate('v-axis', 30)
    line = leg.coordinate(2)

    z = line['z']
    x = line['x']
    y = line['y']
    ax1.scatter3D(x,y,z, cmap='Reds')  #绘制散点图
    ax1.plot3D(x,y,z,'gray')     #绘制空间曲线
    plt.pause(1)

for i in range(2):
    leg.arotate('h2-axis', 30)
    line = leg.coordinate(2)

    z = line['z']
    x = line['x']
    y = line['y']
    ax1.scatter3D(x,y,z, cmap='Reds')  #绘制散点图
    ax1.plot3D(x,y,z,'gray')     #绘制空间曲线
    plt.pause(1)

for i in range(2):
    leg.arotate('h1-axis', 30)
    line = leg.coordinate(2)

    z = line['z']
    x = line['x']
    y = line['y']
    ax1.scatter3D(x,y,z, cmap='Reds')  #绘制散点图
    ax1.plot3D(x,y,z,'gray')     #绘制空间曲线
    plt.pause(1)


plt.ioff()
plt.show()
