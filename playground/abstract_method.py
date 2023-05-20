import abc

class A:
    def __init__(self):
        self.a = 1

    @abc.abstractmethod
    def f(self):
        pass

    def resolve(self):
        return self.f()

class B(A):
    def f(self):
        return self.a

b = B()
print(b.resolve())