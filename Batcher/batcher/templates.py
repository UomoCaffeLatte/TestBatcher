from dataclasses import dataclass, field
from typing import Callable

@dataclass
class TestFunction:
    callable:Callable
    inputs: dict = field(init=False, default=None)

    def __post_init__(self) -> None:
        # get algorithm arguments
        self.args =  self.callable.__code__.co_varnames[:self.callable.__code__.co_argcount]
        if(len(self.args) == 0): raise ValueError("Algorithm must have at least 1 input.")
        # check return type is dict
        typehints = self.callable.__annotations__
        if typehints["return"] != dict: raise TypeError("Function return must be a dict type.")

class TestBase:
    def __init__(self, function:Callable, ID:int, testName:str) -> None:
        self.name = testName
        self.ID = ID
        # create TestFunction
        self.func = TestFunction(function)
        # create empty run list
        self.tests = []
    
    def AddTest(self, *args):
        # not responsible to check types or number of inputs.
        self.tests.append(args)
        


 ### TESTING CODE       

def hello(a,b,c) -> dict:
    print(2)

if __name__ == "__main__":
    Tb = TestBase(hello, 12)
    Tb.AddTest(10,20,30)
    Tb.AddTest(20,20,20)
    print([ test[0] for test in Tb.tests])