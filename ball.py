from pygame import Vector2


class Ball:
    """ Implements a game ball, a circle like object with the following attributes"""
    def __init__(self, radius:float=30, mass:float=0, charge:float=0, position:tuple[float, float]=(100, 100), velocity:tuple[float, float]=(0,0)):
        self.radius = radius
        self.mass = mass
        self.charge = charge
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)

class Electron(Ball):
    pass

class Neutron(Ball):
    pass

class Proton(Ball):
    pass

