def testfunc(string):
    print(string)
    print("Success!")

class TestClass:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def printobj(self):
        print(f"The value assigned is {self.value}")
