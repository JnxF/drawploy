
class Square:
    box = []
    tipo = 0
    i = ''
    disk = ''

    def __init__(self, i, tipo, box):
        self.i = i
        self.box = box
        self.tipo = tipo
    
    def __lt__(self, other):
        self.minX() < other.minX()
    
    def set_disk(self, disk):
        self.disk = disk

    def minX(self):
        return self.box[0]
    
    def maxX(self):
        return self.box[2]
    
    def minY(self):
        return self.box[1]
 
    @classmethod
    def solapaX(cls, a, b):
        return a.maxX() >= b.minX() and b.maxX() >= a.minX()
        # return ( (b.minX() >= a.minX() and b.minX() <= a.maxX()) or (a.minX() >= b.minX() and a.minX() <= b.maxX()) )