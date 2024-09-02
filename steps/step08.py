import numpy as np

class Variable:
    def __init__(self,data):
        self.data = data
        self.grad = None
        self.creator= None

    def set_creator(self,func):
        self.creator = func

    def backward(self):
        funcs = [self.creator]
        while funcs:
            f = funcs.pop()
            x,y = f.input,f.output
            x.grad = f.backward(y.grad)

            if x.creator is not None:
                funcs.append(x.creator)

class Function:
    def __call__(self,input):
        x = input.data
        y = self.forward(x)
        output = Variable(y)
        output.set_creator(self)
        self.input = input
        self.output = output
        return output

    def forward(self,x):
        raise NotImplementedError()

    def backward(self,gy):
        raise NotImplementedError()

class Square(Function):
    def forward(self, x):
        return x**2

    def backward(self,gy):
        x = self.input.data
        gx = 2 * x * gy
        return gx

class Exp(Function):
    def forward(self,x):
        return np.exp(x)

    def backward(self,gy):
        x = self.input.data
        gx = np.exp(x) * gy
        return gx

# old
A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)
print(y.data)

assert y.creator == C
assert y.creator.input == b
assert y.creator.input.creator == B
assert y.creator.input.creator.input == a
assert y.creator.input.creator.input.creator == A
assert y.creator.input.creator.input.creator.input == x

y.grad = np.array(1.0)

C = y.creator
b = C.input
b.grad = C.backward(y.grad)

B = b.creator
a = B.input
a.grad = B.backward(b.grad)

A = a.creator
x = A.input
x.grad = A.backward(a.grad)
print(x.grad)

#   new
A0 = Square()
B0 = Exp()
C0 = Square()

x0 = Variable(np.array(0.5))
a0 = A0(x0)
b0 = B0(a0)
y0 = C0(b0)

y0.grad = np.array(1.0)
y0.backward()
print(x0.grad)