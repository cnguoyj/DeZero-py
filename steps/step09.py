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

def square(x):
    f = Square()
    return f(x)

def exp(x):
    f = Exp()
    return f(x)

x = Variable(np.array(0.5))
a = square(x)
b = exp(a)
y = square(b)

y.grad = np.array(1.0)
y.backward()
print(x.grad)
