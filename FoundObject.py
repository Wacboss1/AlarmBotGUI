class FoundObject:

    def __init__(self, angle, distance, width):
        self.angle = angle
        self.distance = distance
        self.width = width
        self.color = self.setColor(width)

    def setColor(self, width):
        color = ''
        if width > 8:
            color = 'r'
        else:
            color = 'g'
        return color

    def toDict(self):
        return {
            'angle': self.angle,
            'distance': self.distance,
            'width':self.width,
            'color': self.color
        }
