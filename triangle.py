from pygame import Vector2

class Triangle:

    def __init__(self, edges:tuple = ((0, 0), (0, 0), (0, 0))):
        self.edges = [Vector2(edge) for edge in edges]
        self.line = self.edges[2] - self.edges[1]
        self.slope = self.line.y / self.line.x

    def is_inside_triangle(self, point:Vector2):
        c = self.edges[1][1] - self.slope * self.edges[1][0]

        return point.y >= self.slope * point.x + c * 0.95
