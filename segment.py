class Segment:
    def __init__(self, x, y, t=0, r=0):
        self.x = x
        self.y = y
        self.t = t
        self.r = r

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False