# -*- coding: utf-8 -*-
"""micrograd.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sPI7BD8WRRO-ffsX4q2aeKLk7yqmPuHy
"""

# Commented out IPython magic to ensure Python compatibility.
import math
import numpy as np
import matplotlib.pyplot as plt
import math
# %matplotlib inline
from graphviz import Digraph

def f(x):
  return 3*x**2-4*x+5

f(3.0)

xs = np.arange(-5,5,0.25)
ys = f(xs)
plt.plot(xs,ys)

class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op='',label=""):
        self.data = data
        self.grad = 0.0
        self._prev = set(_children)
        self._op = _op # the op that produced this node, for graphviz / debugging / etc
        self.label = label
        self._backward = lambda:None

    def __repr__(self):
      return f"Value(data={self.data})"

    def __add__(self, other):
        other = other if isinstance(other,Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
          self.grad += 1*out.grad
          other.grad += 1.0*out.grad
        out._backward =_backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
          self.grad += (out.grad)*other.data
          other.grad += (out.grad)*self.data
        out._backward = _backward
        return out

    """non linear squasing function """

    def __rmul__(self,other):
      return self*other

    def __radd__(self,other):
      return self+other


    def __truediv__(self,other):
      return self*other**-1

    def __pow__(self,other):
      assert  isinstance(other,(int,float))
      out = Value(self.data**other,(self,),f'**{other}')

      def _backward():
        self.grad += other*(self.data**(other-1))*out.grad

      out._backward =_backward
      return out

    def __neg__(self):
      return self*-1

    def __sub__(self,other):
      return self+(-other)


    def tanh(self):
      x = self.data
      t = (np.exp(2**x)-1)/(np.exp(2**x)+1)
      out = Value(t,(self,),'tanh')

      def _backward():
         self.grad += (1 - (out.data)**2)*out.grad
      out._backward = _backward
      return out

    def backward(self):
      topo = []
      visited = set()
      def build_topo(v):
        if v not in visited:
          visited.add(v)
          for child in v._prev:
            build_topo(child)
          topo.append(v)

      build_topo(self)
      self.grad = 1
      for el in reversed(topo):
        el._backward()

      def __radd__(self, other): # other + self
        return self + other


    def exp(self):
      x = self.data
      out  = Value(np.exp(x),(self,),"exp")
      def _backward():
        self.grad += (out.data)*out.grad
      out._backward = _backward
      return out

a = (Value(5)-Value(10))**2
1+a

k = Value(10)
l = Value(5)

def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root, format='svg', rankdir='LR'):
    """
    format: png | svg | ...
    rankdir: TB (top to bottom graph) | LR (left to right)
    """
    assert rankdir in ['LR', 'TB']
    nodes, edges = trace(root)
    dot = Digraph(format=format, graph_attr={'rankdir': rankdir}) #, node_attr={'rankdir': 'TB'})

    for n in nodes:
        dot.node(name=str(id(n)), label = "{ %s | data %.4f | grad %.4f }" % (n.label,n.data, n.grad), shape='record')
        if n._op:
            dot.node(name=str(id(n)) + n._op, label=n._op)
            dot.edge(str(id(n)) + n._op, str(id(n)))

    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)

    return dot

x1 = Value(2.0,label="x1")
x2 = Value(0.0,label="x2")
w1 = Value(-3.0,label="w1")
w2 = Value(1.0,label = "w2")
b = Value(6.881373587019543,label="b")
x1w1 = x1*w1;x1w1.label="x1w1"
x2w2 = x2*w2;x2w2.label = "x2w2"
x1w1x2w2 = x1w1+x2w2;x1w1x2w2.label="x1w1 + x2w2"
n = x1w1x2w2+b;n.label = "n"
e = (2*n).exp()
o = (e-1)/(e+1);o.label = "o"
o.backward()

# # derivatives
# #o = tanh(n)
# #do/dl*do/dn = 1*(1-o**2)
# # o.grad = 1
# # n.grad  = 1-(o.data)**2
# # x1w1x2w2.grad = 0.4723
# # b.grad  = 0.4723
# # x2w2.grad = 0.4723
# # x1w1.grad  = 0.4723
# # w1.grad = 0.4723 * x1.data
# # w2.grad = 0.4723 * x2.data
# # x1.grad = 0.4723 * w1.data
# # x2.grad = 0.4723 * w2.data
# # time node is also here
# #w2.grad =  dx2w2/dl*dw2/dx2w2 = 0.4723 *(x2.data)
# #x2.grad  = 0.4723 *w2.data
# # x2w2 = x2*w2
# #c = a*b
# #dc/da = b
# o.grad = 1
# o._backward()
# n._backward()
# x1w1x2w2._backward()
# # b._backward()
# x1w1._backward()
# x2w2._backward()
# 1 =d(n^k)/do
#dn/do*do/dl = e^n*out.grad

draw_dot(o)

import random
class Neuron:
  def __init__(self,nin):
    self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
    self.b = Value(random.uniform(-1,1))

  def __call__(self,x):
   act = sum((wi*xi for wi,xi in zip(self.w,x)),self.b)
   out  = act.tanh()
   return out

  def parameters(self):
    return self.w+[self.b]

class Layer:
  def __init__(self,nin,nout):
    self.neurons = [Neuron(nin) for _ in range(nout)]

  def __call__(self,x):
    outs = [n(x) for n in self.neurons]
    return outs[0] if len(outs)==1 else outs

  def parameters(self):
    params = []
    for neuron in self.neurons:
      ps = neuron.parameters()
      params.extend(ps)
    return params

class MLP:
  def __init__(self,nin,nouts):
     sz = [nin]+nouts
     self.layers = [Layer(sz[i],sz[i+1]) for i in range(len(nouts))]
  def __call__(self,x):
    for layer in self.layers:
      x = layer(x)
    return x

  def parameters(self):
    return [p for layer in self.layers for p in layer.parameters()]
n = MLP(3,[4,4,1])



xs = [[2.0,3.0,-1.0],[3.0,-1.0,0.5],[0.5,1.0,1.0],[1.0,1.0,-1.0]]
ys = [1.0,-1.0,-1.0,1.0]
ypred = [n(x) for x in xs]
ypred

for k in range(20):
    ypred = [n(x) for x in xs]
    loss = sum(((yout-ygt)**2) for  ygt,yout in zip(ys,ypred))
    for p in n.parameters():
      p.grad = 0
    loss.backward()

    for p in n.parameters():
      p.data+=-0.1*(p.grad)
    print(loss,k)







