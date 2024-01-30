import math
from pygame import Vector2
import helpers


class Flipper:

    def __init__(self, base:tuple=(0,0), end:tuple=(0, 0), width=1, angular_velocity=0, is_rotating=False, is_flipped=False):
        self.line = None
        self.slope = None
        self.base = Vector2(base)
        self.end = Vector2(end)
        self.width = width
        self.length = self.base.distance_to(self.end)
        self.angular_velocity = angular_velocity
        self.is_rotating = is_rotating
        self.is_flipped = is_flipped

        self.set_line()

    def set_line(self):
        self.line = self.end - self.base
        self.slope = self.line.y / self.line.x

    def rotate_around_base(self, angle=0):
        self.end -= self.base
        self.end.rotate_ip_rad(angle)
        self.end += self.base
        self.set_line()

    def is_inside_line(self, point:Vector2):
        c = self.base.y - self.slope * self.base.x
        return (point.y >= self.slope * point.x + c * 0.95
                and min(self.base.x, self.end.x) < point.x < max(self.base.x, self.end.x))