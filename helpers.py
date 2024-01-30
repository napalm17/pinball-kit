from pygame import Vector2


def slope(a:Vector2, b:Vector2):
    return (a.y - b.y) / (a.x - b.x)