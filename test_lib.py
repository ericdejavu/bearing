# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from bmath.vec import *


a = Vec(0,0,0, 'zero')
b = Vec(1,1,1, 'mid')
c = Vec(2,2,1.5, 'top')

vaxis = Vec(0,0,1, 'vaxis')
h1axis = Vec(0,1,0, 'h1axis')
h2axis = Vec(0,1,0, 'h2axis')
raxis = Vec(1,0,0, 'raxis')
# vaxis -> [b, c, h1axis, h2axis, raxis] raxis -> [b, c, h1axis, h2axis] h1axis -> [b, c] h2axis -> [c]
br = Arrow(b, a, 'mid-arrow')
cr = Arrow(c, b, 'top-arrow')

van = AxisNode(vaxis, [br, cr, h1axis, h2axis, raxis], name='v-axis')
ran = AxisNode(raxis, [br, cr, h1axis, h2axis], name='r-axis')
h1an = AxisNode(h1axis, [br, cr], name='h1-axis')
h2an = AxisNode(h2axis, [cr], name='h2-axis')

leg = Joint([van, ran, h1an, h2an], name='leg0')



for i in range(20):
    print (leg.arotate('v-axis', 60))