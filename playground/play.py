
class calc:
    def __init__(self) -> None:
        self.yo = 11
        pass

    def __call__(self, a, b):
        return future(self, a, b)

class abs_future:
    def __init__(self, calc: calc, a, b):
        self.calc = calc
        self.a = a
        self.b = b

class future(abs_future):
    pass


x = calc()
f = x(1,2)
print(type(f))
print(f, f.b)