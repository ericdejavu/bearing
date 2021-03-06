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

    def dcopy(self, vec):
        self.x,self.y,self.z = vec.x,vec.y,vec.z

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
    def __init__(self, tail, head, name="default-arrow"):
        self.head = head
        self.tail = tail
        self.name = name
        self.update()

    def __str__(self):
        return self.name + ': {head-> ' + str(self.head) + ', tail-> ' + str(self.tail) + '}'

    def rebuild(self, tail, head):
        self.head = head
        self.tail = tail
        self.update()

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
    def __init__(self, axis, anchor, effect_vec, effect_axis, name='default-axis'):
        self.scopes = effect_vec + effect_axis
        if self.scopes == None:
            raise ValueError('scopes cant be None')
        for scope in self.scopes:
            correct_type = isinstance(scope, Arrow) or isinstance(scope, Vec)
            if not correct_type:
                raise ValueError(str(scope) + ' is not a arrow')
        self.axis = axis
        self.anchor = anchor
        self.effect_vec = effect_vec
        self.effect_axis = effect_axis
        self.name = name
        self.edges = [Arrow(anchor, vec, self.edge_name(vec)) for vec in effect_vec]

    def rebuild(self):
        for i, edge in enumerate(self.edges):
            edge.rebuild(self.anchor, self.effect_vec[i])

    def edge_name(self, vec):
        return self.name + '-' + vec.name

    def update(self):
        for i, edge in enumerate(self.edges):
             self.effect_vec[i].dcopy(edge.head)

    def __str__(self):
        return self.name + '|' + str(self.axis) + str([str(scope) for scope in self.scopes])

    def arotate(self, theta):
        self.rebuild()
        for edge in self.edges:
            edge.arotate(self.axis, theta)
        self.update()
        for axis in self.effect_axis:
            axis.arotate(self.axis, theta)
        return self
    


class Joint:
    def __init__(self, axis_nodes, vec_nodes, name='default-joint'):
        self.axis_list = axis_nodes
        self.name = name
        self.vec_nodes = vec_nodes
        self.edges = []
        self.build()

    def __str__(self):
        return self.name + str([str(axis_node) for axis_node in self.axis_list])

    def build(self):
        self.axis_map = {}
        for axis_node in self.axis_list:
            self.axis_map[axis_node.name] = axis_node
        for i, vec_node in enumerate(self.vec_nodes):
            if i == 0:
                continue
            self.edges.append(Arrow(self.vec_nodes[i-1], vec_node, self.vec_name(vec_node)))

    def vec_name(self, vec):
        return self.name + '<->' + vec.name
    
    def arotate(self, axis_name, theta):
        if axis_name in self.axis_map.keys():
            self.axis_map[axis_name].arotate(theta)
        return self

    def coordinate(self, linspace=1000):
        coo = {'x': np.array([]), 'y': np.array([]), 'z': np.array([])}
        for edge in self.edges:
            edge.update()
            tmp = edge.line(linspace)
            coo['x'] = np.append(coo['x'], tmp['x'])
            coo['y'] = np.append(coo['y'], tmp['y'])
            coo['z'] = np.append(coo['z'], tmp['z'])
        return coo
        

