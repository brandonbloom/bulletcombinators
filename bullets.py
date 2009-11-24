# MIT Licensed
# Hastily hacked together by Brandon Bloom <snprbob86@gmail.com>

import sys, pygame, math
from pygame.time import Clock


pygame.init()

size = width, height = 800, 600
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0

screen = pygame.display.set_mode(size)

def rotate_point((x, y), amount):
    return (x * math.cos(amount) - y * math.sin(amount),
            x * math.sin(amount) + y * math.cos(amount))

class Bullet(object):
    def __init__(self, position, rotation=0, radius=10, color=white):
        self.position = position
        self.rotation = rotation
        self.radius = radius
        self.color = color

class World(object):
    def __init__(self, bullets):
        self.bullets = bullets

def idle(world, bullet):
    return None

def both(go0, go1):
    def go_both(world, bullet):
        sub = go0(world, bullet)
        if sub:
            return both(sub, go1)
        return go1(world, bullet)
    return go_both

def forever(go):
    def go_forever(world, bullet):
        sub = go(world, bullet)
        if sub:
            return both(sub, forever(go))
        return forever(go)
    return go_forever

def move(dX, dY):
    def go_move(world, bullet):
        x, y = bullet.position
        bullet.position = (x + dX, y + dY)
        return None
    return go_move

def forward(distance):
    def go_forward(world, bullet):
        x, y = rotate_point((distance,0), bullet.rotation)
        return move(x, y)
    return go_forward

def repeat(n, go):
    def go_repeat(world, bullet):
        if n == 0:
            return None
        sub = go(world, bullet)
        next = repeat(n - 1, go)
        if sub:
            return both(sub, next)
        return next
    return go_repeat

def rotate(dR):
    def go_rotate(world, bullet):
        bullet.rotation += dR
        return None
    return go_rotate

def sequence(*go_list):
    if len(go_list) == 0:
        return None
    go = go_list[0]
    remaining_gos = go_list[1:]
    def go_sequence(world, bullet):
        if len(remaining_gos) == 0:
            return go
        return both(go, sequence(*remaining_gos))
    return go_sequence

def spawn(go, *args, **kwargs):
    def go_spawn(world, bullet):
        world.bullets.append(
            (Bullet(bullet.position, bullet.rotation, *args, **kwargs), go))
        return None
    return go_spawn


def handle_input(world):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def in_bounds(b):
    x, y = b.position
    return x > 0 and y > 0 and x < width and y < height

def update(world):
    bullets = []
    for bullet, go in world.bullets:
        go = go(world, bullet)
        if in_bounds(bullet):
            if not go:
                go = forever(idle)
            bullets.append((bullet, go))
    world.bullets = bullets

def draw(world):
    screen.fill(black)
    for bullet, go in world.bullets:
        pygame.draw.circle(screen, bullet.color,
                           bullet.position, bullet.radius)
        x, y = bullet.position
        nose_x, nose_y = rotate_point((bullet.radius, 0), bullet.rotation)
        pygame.draw.line(screen, black, bullet.position,
                         (x + nose_x, y + nose_y))
    pygame.display.flip()



world = World([
    (Bullet((400, 300)),
        forever(
            sequence(
                repeat(8,
                    sequence(
                        repeat(25, forward(3)),
                        rotate(3.14/4),
                        spawn(forever(forward(2)), color=red))),
                rotate(3.14)))),
])

clock = Clock()
while 1:
    handle_input(world)
    update(world)
    draw(world)
    clock.tick(30)
