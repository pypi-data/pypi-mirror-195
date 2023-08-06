
class Array:
    def __init__(self, size = 5):
        self.size = [0] * size

    def push(self, value):
        self.size.insert(0, value)
        return self.size
    
    def append(self, value):
        self.size.append(value)
        return self.size
    
    def pop(self):
        return self.size.pop()
    
    def sort(self, order=1):
        self.size.sort() if (order >= 1) else self.size.reverse()
        return self.size
    
    def show(self):
        # print(self.size)
        return self.size
    
if __name__ == '__main__':
    array = Array(10)
    array.push(5)
    array.append(10)
    # arr = [1, 0, 0, 5]
    # arr.reverse()
    print(array.show())
