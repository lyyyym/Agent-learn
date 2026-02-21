
from os import name


class Test(object):
    def __init__(self,name):
        self.name = name 
    
    def __or__(self, other):
        return MySequence(self,other)
    
    def __str__(self):
        return self.name

class MySequence(object):
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    
    def __or__(self, other):
        self.sequence.append(other)
        return self
    
    def run(self):
        for item in self.sequence:
            print(item)


if __name__ == "__main__":
    a = Test("a")
    b = Test("b")
    d = a | b
    d.run()
    print(d)
