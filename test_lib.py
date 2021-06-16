# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from bmath.vec import *



o = Vec(0,0,0)
a = Vec(1,1,1)
axis = Vec(1,1,0)
axis.normalize()
arrow = Arrow(a,o)

# for i in range(120):
#     arrow.arotate(axis, 30)
#     print(arrow.length())

for i in range(120):
    a.arotate(axis, 30)
    print(a.x**2 + a.y**2 + a.z**2)