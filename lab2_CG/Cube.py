import time
from numpy import *
from graphics import *
from math import *

height = 600
width = 800
scale = 300

d = 1
RO = 800
THETA = pi / 3
FI = pi / 6

window = GraphWin("Cube filled & carcass", width, height)


def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()
    return


# повороты вокруг осей координат
def rotateOZ(alpha):
    return array([[cos(alpha), sin(alpha), 0, 0], [-sin(alpha), cos(alpha), 0, 0],
                     [0, 0, 1, 0], [0, 0, 0, 1]])


def rotateOX(alpha):
    return array([[1, 0, 0, 0], [0, cos(alpha), sin(alpha), 0],
                     [0, -sin(alpha), cos(alpha), 0], [0, 0, 0, 1]])


def rotateOY(alpha):
    return array([[cos(alpha), 0, sin(alpha), 0], [0, 1, 0, 0],
                     [-sin(alpha), 0, cos(alpha), 0], [0, 0, 0, 1]])


# переход из мировой в видовую систему координат
def worldintoview(ro, theta, fi):
    return array([[-sin(theta), -cos(fi) * cos(theta), -sin(fi) * cos(theta), 0],
                     [cos(theta), -cos(fi) * sin(theta), -sin(fi) * sin(theta), 0],
                     [0, sin(fi), -cos(fi), 0],
                     [0, 0, ro, 1]])


def drawfigure(verses, edges):
    clear(window)
    for i, j in edges:
        l = Line(Point(verses[i][0], verses[i][1]), Point(verses[j][0], verses[j][1]))
        if (not (window.closed)):
            l.draw(window)
    return


class Cube:
    # вершины
    verses = array([[1, 0, 0, 1], [0, 0, 0, 1],
                       [0, 1, 0, 1], [1, 1, 0, 1],
                       [1, 0, 1, 1], [0, 0, 1, 1],
                       [0, 1, 1, 1], [1, 1, 1, 1]])
    v = verses

    # ребра
    edges = array([[0, 1], [1, 2], [2, 3], [3, 0],
                      [4, 5], [5, 6], [6, 7], [7, 4],
                      [0, 4], [1, 5], [2, 6], [3, 7]])

    # грани
    faces = [[0, 1, 2, 3, 'pale turquoise'], [4, 5, 6, 7, 'light sky blue'],
             [0, 4, 7, 3, 'turquoise'], [0, 4, 5, 1, 'aquamarine'],
             [1, 5, 6, 2, 'light sea green'], [2, 6, 7, 3, 'SteelBlue1']]

    center = array([0, 0, 0, 1])
    centerv = center

    def __init__(self):
        a = list()
        for i in self.verses:
            a.append([(i[0] - 1 / 2) * scale, (i[1] - 1 / 2) * scale, (i[2] - 1 / 2) * scale, 1])
        self.verses = array(a)
        self.perspectiveprojection(RO, THETA, FI, d)

    def movecube(self, alpha=0, betha=0, gamma=0, a=0, b=0, c=0):
        for i in range(len(self.verses)):
            self.verses[i] = dot(self.verses[i], rotateOZ(alpha))
            self.verses[i] = dot(self.verses[i], rotateOX(betha))
            self.verses[i] = dot(self.verses[i], rotateOY(gamma))
            self.verses[i] = self.verses[i]
        self.center = dot(self.center, rotateOZ(alpha))
        self.center = dot(self.center, rotateOX(betha))
        self.center = dot(self.center, rotateOY(gamma))
        self.center = self.center

    # параллельная проекция
    def parallelprojection(self):
        a = list()
        for i in self.verses:
            a.append([i[0] + width / 2, i[1] + height / 2])
        return (a, self.edges)

    # перспективная проекция (переход в экранные координаты)
    def perspectiveprojection(self, ro, theta, fi, d):
        b = list()
        g = list()
        for i in range(len(self.verses)):
            a = dot(self.verses[i], worldintoview(ro, theta, fi))
            g.append([a[0], a[1], a[2]])
            b.append([d * a[0] * ro / (2 * a[2]) + width / 2, d * a[1] * ro / (2 * a[2]) + height / 2])
        self.v = g
        self.centerv = dot(self.center, worldintoview(ro, theta, fi))
        return (b, self.edges)

    # проверка, является ли грань лицевой, 1 способ
    def h(self, a, b, c):
        ch = self.v[a][0] * ((self.v[b][1] - self.v[a][1]) * (self.v[c][2] - self.v[a][2]) -
                             (self.v[b][2] - self.v[a][2]) * (self.v[c][1] - self.v[a][1])) + self.v[a][1] * (
                         (self.v[b][2] - self.v[a][2]) * (self.v[c][0] - self.v[a][0]) -
                         (self.v[b][0] - self.v[a][0]) * (self.v[c][2] - self.v[a][2])) + self.v[a][2] * (
                         (self.v[c][1] - self.v[a][1]) * (self.v[b][0] - self.v[a][0]) -
                         (self.v[c][0] - self.v[a][0]) * (self.v[b][1] - self.v[a][1]))
        if ch > 0:
            return True
        else:
            return False

    # проверка, является ли грань лицевой, 2 способ
    def l(self, a, b, c):
        ca = ((self.v[b][1] - self.v[a][1]) * (self.v[c][2] - self.v[a][2]) -
              (self.v[b][2] - self.v[a][2]) * (self.v[c][1] - self.v[a][1]))
        cb = ((self.v[b][2] - self.v[a][2]) * (self.v[c][0] - self.v[a][0]) -
              (self.v[b][0] - self.v[a][0]) * (self.v[c][2] - self.v[a][2]))
        cc = ((self.v[c][1] - self.v[a][1]) * (self.v[b][0] - self.v[a][0]) -
              (self.v[c][0] - self.v[a][0]) * (self.v[b][1] - self.v[a][1]))
        ch = self.v[a][0] * ca + self.v[a][1] * cb + self.v[a][2] * cc
        cl = ca * self.centerv[0] + cb * self.centerv[1] + cc * self.centerv[2] - ch
        sgn = cl / abs(cl)
        n = array([ca, cb, cc]) * sgn
        d = array([(self.v[a][0] + self.v[b][0] + self.v[c][0]) / 3,
                   (self.v[a][1] + self.v[b][1] + self.v[c][1]) / 3,
                   (self.v[a][2] + self.v[b][2] + self.v[c][2]) / 3])
        csa = dot(d, n) / linalg.norm(n) / linalg.norm(d)
        if 0 < csa < 1:
            return True
        else:
            return False

    def fillfaces(self):
        flat = self.perspectiveprojection(RO, THETA, FI, d)[0]
        show = list()
        for f in self.faces:
            if self.l(f[0], f[1], f[2]):
                show.append(f)
        clear(window)
        for k in show:
            shape = Polygon(Point(flat[k[0]][0], flat[k[0]][1]),
                            Point(flat[k[1]][0], flat[k[1]][1]),
                            Point(flat[k[2]][0], flat[k[2]][1]),
                            Point(flat[k[3]][0], flat[k[3]][1]))
            shape.setFill(k[4])
            if not (window.closed):
                shape.draw(window)


cube = Cube()

while (not (window.closed)):
    'вращение куба по трем осям'
    # cube.movecube(alpha=pi / 300, betha=pi / 600, gamma=pi / 600)

    'вращение камеры'
    # THETA += pi/150
    # FI -= pi/150

    'вращение куба и камеры'
    cube.movecube(alpha=pi / 300, betha=pi / 600, gamma=pi / 600)
    THETA += pi / 150
    FI -= pi / 150

    'вывод полной модели куба'
    cube.fillfaces()
    time.sleep(1 / 24)

    'вывод каркасной модели куба'
    # da = cube.perspectiveprojection(RO, THETA, FI, d)
    # drawfigure(da[0], da[1])
    # time.sleep(1 / 24)

window.close()