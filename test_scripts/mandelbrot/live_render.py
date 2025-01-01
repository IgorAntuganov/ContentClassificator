import pygame

pygame.init()
# from numba import njit
from math import sqrt, log
from time import time


# @njit(fastmath=True)
def checkPoint(x, y, depth):
    z = c = x + 1j * y

    k = 0
    for k in range(depth):
        # z = z ** 2 + c
        # z = z ** 2 - z  AV: 5
        # z = z ** 3 + z ** 2 - c
        # z = z ** 4 - z
        # z = z ** 8 - z ** 4 + z ** 2 + z
        # z = z ** 4 - z ** 2 - c ** z * z ** c
        # z = (z + 1) ** 2
        # z = (z**c) ** 2  # !!!
        # z = (c**z) ** 2  # !!!
        # z = (z**c) ** 3  # Плавное усложнение предыдущего
        # z = (z**c) ** 20 #
        # z = z ** 4 - z ** 2 - c ** z * z ** c
        # z = z ** 4 - z ** 2 - c ** z * z ** (c**1/8)
        # z = z ** 8 - z ** 4 - z ** 2 - c ** z * z ** c
        # z = - z ** 4 + z ** 2 - c**z * z**c  # cool
        # z = z ** 37 - z ** 31 - c**z * z**c  # cool
        # z = z ** 4 - z ** 2 - (c ** z * z ** c) ** 2
        # z = z ** 4 - z ** 2 - (c ** z * z ** c) ** 1/2
        z = z ** 4 - z ** 2 - (c ** z * z ** c) * c

        if abs(z) > 4:
            break
    if k == depth - 1:
        k = -1

    return k

def chooseColor(n: int | None):
    if n is None:
        return 160, 200, 150
    color = [0, 0, 0]
    if n < 0:
        return color

    def quad(n):
        return sqrt(255 * 255 - n * n)

    if n > 4:
        k = log(n + 1, 1.0010)
    else:
        k = n * 20
    # k = (n**0.25)*250*1.3-130

    if 0 < k % 765 < 510:
        color[0] = quad(abs(255 - k % 765))
    if 255 < k % 765 < 765:
        color[1] = quad(abs(510 - k % 765))
    if 510 < k % 765 < 765:
        color[2] = quad(abs(765 - k % 765))
    if 0 <= k % 765 < 255 and k > 255:
        color[2] = quad(abs(0 - k % 765))

    return color


class Time:
    def __init__(self):
        self.last = time()

    def tick(self):
        if time() - self.last > 0.03:
            self.last = time()
            return True
        return False


class Info:
    x = 0
    y = 0
    scale = 1
    depth = 100
    surfaces = [0, 0, 0, 0]

    @property
    def zoom(self):
        return (2 ** self.scale) / 2

    @property
    def pix_offset(self):
        return (4 / self.zoom) / 384

    @property
    def left(self):
        return self.x - 192 * self.pix_offset

    @property
    def up(self):
        return self.y + 108 * self.pix_offset

    def move(self, x, y):
        if x > 0:
            self.x += 30 * self.pix_offset
        if x < 0:
            self.x -= 30 * self.pix_offset
        if y > 0:
            self.y += 30 * self.pix_offset
        if y < 0:
            self.y -= 30 * self.pix_offset
        self.littlesurface = False
        self.middlesurface = False
        self.normalsufrace = False

    def zooming(self, In):
        if In:
            self.scale += 0.5
        else:
            self.scale -= 0.5
        self.littlesurface = False
        self.middlesurface = False
        self.normalsufrace = False

    def changedepth(self, up):
        if up:
            self.depth *= 1.25
        else:
            self.depth /= 1.25
        self.depth = int(self.depth)
        self.littlesurface = False
        self.middlesurface = False
        self.normalsufrace = False

    def check_keys(self):
        changed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,
                                 pygame.K_z, pygame.K_x, pygame.K_e, pygame.K_q,
                                 pygame.K_r):
                    changed = True
                if event.key == pygame.K_w:
                    self.move(0, 1)
                if event.key == pygame.K_s:
                    self.move(0, -1)
                if event.key == pygame.K_a:
                    self.move(-1, 0)
                if event.key == pygame.K_d:
                    self.move(1, 0)
                if event.key == pygame.K_z:
                    self.changedepth(False)
                if event.key == pygame.K_x:
                    self.changedepth(True)
                if event.key == pygame.K_e:
                    self.zooming(True)
                if event.key == pygame.K_q:
                    self.zooming(False)
                if event.key == pygame.K_r:
                    self.scale = 1
                    self.depth = 100
                    self.x = 0
                    self.y = 0
        if changed:
            print('real:', I.x)
            print('imag:', I.y)
            print(f'zoom: 2^{I.scale}', 'or', I.zoom, 'times')
            print('iterations limit:', I.depth)
            print(' -------------------------------------------- ')
            return True
        return False


def draw_surf(I, rel):
    for i in range(int(384 / rel)):
        points = []
        for j in range(int(216 / rel)):
            x = I.left + I.pix_offset * rel * i
            y = I.up - I.pix_offset * rel * j
            try:
                k = checkPoint(x, y, I.depth)
                color = chooseColor(k)
            except ZeroDivisionError:
                color = (160, 210, 150)
            except OverflowError:
                color = (150, 155, 210)
            points.append(color)
        yield points, i


def draw(I):
    for rel in 24, 12, 4, 2, 1:
        for points, i in draw_surf(I, rel):
            for j, point in enumerate(points):
                pygame.draw.rect(sc, point, (2 * i * rel, 2 * j * rel, 2 * rel, 2 * rel))
            yield


sc = pygame.display.set_mode((384 * 2, 216 * 2), pygame.HWSURFACE)
pygame.display.set_caption('Live view')
font = pygame.font.Font('C:/Windows/Fonts/comic.ttf', 20)

I = Info()
T = Time()
surface = pygame.Surface((384, 216))

run = True
while run:
    for _ in draw(I):
        if T.tick():
            pygame.display.update()
        if I.check_keys():
            break
    else:
        while True:
            if I.check_keys():
                break