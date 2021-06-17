# -*- coding:utf8 -*-
import numpy as np
import quaternionic
import math

class Vec:
    def __init__(self, x=0, y=0, z=0, name='defalut'):
        self.update(x, y, z)
        self.name = name

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return self.name + ': [' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ']'

    def update(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotate(self, axis, theta):
        half_theta = theta * math.pi / 360.0
        sta = math.sin(half_theta)
        cta = math.cos(half_theta)
        qpos = quaternionic.array([0, self.x, self.y, self.z])
        qaxis = quaternionic.array([cta, axis.x * sta, axis.y * sta, axis.z * sta])
        aqaxis = quaternionic.array([cta, -axis.x * sta, -axis.y * sta, -axis.z * sta])
        return qaxis * qpos * aqaxis

    def arotate(self, axis, theta):
        q = self.rotate(axis, theta)
        self.update(q.x, q.y, q.z)
        return self

    def normalize(self):
        t = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        self.x /= t
        self.y /= t
        self.z /= t


class Arrow:
    def __init__(self, head, tail, name="default-arrow"):
        self.head = head
        self.tail = tail
        self.name = name
        self.update()

    def __str__(self):
        return self.name + ': {head-> ' + str(self.head) + ', tail-> ' + str(self.tail) + '}'

    def update(self):
        self.arrow = self.head - self.tail

    def arotate(self, axis, theta):
        self.arrow.arotate(axis, theta)
        self.head = self.arrow + self.tail
        return self

    def get_array(self, n, array):
        return np.array([n for i in range(len(array))])

    def equation(self, seqs, v1, v2, v3, v4, v5, v6):
        k = (seqs - self.get_array(v1, seqs)) / self.get_array(v2, seqs)
        out1 = k * self.get_array(v3, seqs) + self.get_array(v4, seqs)
        out2 = k * self.get_array(v5, seqs) + self.get_array(v6, seqs)
        return {'seqs': seqs, 'out1': out1, 'out2': out2}

    def calc(self, x=None, y=None, z=None):
        out = {}
        if type(x) != type(None):
            tmp = self.equation(x, self.tail.x, self.arrow.x, self.arrow.y, self.tail.y, self.arrow.z, self.tail.z)
            out = {'x': x, 'y': tmp['out1'], 'z': tmp['out2']}
        elif type(y) != type(None):
            tmp = self.equation(y, self.tail.y, self.arrow.y, self.arrow.x, self.tail.x, self.arrow.z, self.tail.z)
            out = {'x': tmp['out1'], 'y': y, 'z': tmp['out2']}
        elif type(z) != type(None):
            tmp = self.equation(z, self.tail.z, self.arrow.z, self.arrow.y, self.tail.y, self.arrow.x, self.tail.x)
            out = {'x': tmp['out2'], 'y': tmp['out1'], 'z': z}
        return out
        
    def length(self):
        return self.arrow.x**2 + self.arrow.y**2 + self.arrow.z**2

    def line(self, linspace=1000):
        if abs(self.arrow.x) > 1 / linspace:
            return self.calc(x=np.linspace(self.tail.x, self.head.x, linspace))
        elif abs(self.arrow.y) > 1 / linspace:
            return self.calc(y=np.linspace(self.tail.y, self.head.y, linspace))
        elif abs(self.arrow.z) > 1 / linspace:
            return self.calc(z=np.linspace(self.tail.z, self.head.z, linspace))


class AxisNode:
    def __init__(self, axis, scopes, name='default-axis'):
        if scopes == None:
            raise ValueError('scopes cant be None')
        for scope in scopes:
            correct_type = isinstance(scope, Arrow) or isinstance(scope, Vec)
            if not correct_type:
                raise ValueError(str(scope) + ' is not a arrow')
        self.axis = axis
        self.scopes = scopes

    def arotate(self, theta):
        for vec in self.scopes:
            vec.arotate(self.axis, theta)
        return self
    


class Joint:
    def __init__(self, axis_nodes, name='default-joint'):
        self.axis_list = axis_nodes
        self.build()

    def build(self):
        self.axis_map = {}
        for axis_node in self.axis_list:
            self.axis_map[axis_node.name] = axis_node
    
    def arotate(self, axis_name, theta):
        if axis_name in self.axis_map.keys:
            self.axis_map[axis_name].arotate(theta)
        return self

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

leg = Joint([van, ran, h1an, h2an], name='leg1')
leg.arotate('v-axis', 60)
