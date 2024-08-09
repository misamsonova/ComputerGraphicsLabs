from numpy import *
from graphics import *
from math import *


height = 600
width = 800
scale = 250

RO = 800
THETA = pi / 3
FI = pi / 6

window = GraphWin("CubeCarcas", width, height)


def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()
    return


# поворот вокруг осей координат
def rotateOZ(alpha):
    return array([[cos(alpha), sin(alpha), 0, 0], [-sin(alpha), cos(alpha), 0, 0],
                     [0, 0, 1, 0], [0, 0, 0, 1]])


def rotateOX(alpha):
    return array([[1, 0, 0, 0], [0, cos(alpha), sin(alpha), 0],
                     [0, -sin(alpha), cos(alpha), 0], [0, 0, 0, 1]])


def rotateOY(alpha):
    return array([[cos(alpha), 0, sin(alpha), 0], [0, 1, 0, 0],
                     [-sin(alpha), 0, cos(alpha), 0], [0, 0, 0, 1]])


# сдвиг на a, b, c
def move(a, b, c):
    return array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [a, b, c, 1]])


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
    verses = array([[1, 0, 0, 1], [0, 0, 0, 1],
                       [0, 1, 0, 1], [1, 1, 0, 1],  # [0.5, 0.5, 1, 1]])
                       [1, 0, 1, 1], [0, 0, 1, 1],
                       [0, 1, 1, 1], [1, 1, 1, 1]])

    edges = array([[0, 1], [1, 2], [2, 3], [3, 0],
                      # [0, 4], [1, 4], [2, 4], [3, 4]])
                      [4, 5], [5, 6], [6, 7], [7, 4],
                      [0, 4], [1, 5], [2, 6], [3, 7]])

    # center=np.array([0, 0, 0, 1])

    def __init__(self):
        a = list()
        for i in self.verses:
            a.append([(i[0] - 1 / 2) * scale, (i[1] - 1 / 2) * scale, (i[2] - 1 / 2) * scale, 1])
        self.verses = array(a)
        self.perspectiveprojection(RO, THETA, FI)

    def movecube(self, alpha=0, betha=0, gamma=0, a=0, b=0, c=0):
        for i in range(len(self.verses)):
            self.verses[i] = dot(self.verses[i], rotateOZ(alpha))
            self.verses[i] = dot(self.verses[i], rotateOX(betha))
            self.verses[i] = dot(self.verses[i], rotateOY(gamma))
            self.verses[i] = dot(self.verses[i], move(a, b, c))

    # параллельная проекция
    def parallelprojection(self):
        a = list()
        for i in self.verses:
            a.append([i[0] + width / 2, i[1] + height / 2])
        return (a, self.edges)

    # перспективная проекция
    def perspectiveprojection(self, ro, theta, fi):
        b = list()
        for i in range(len(self.verses)):
            a = dot(self.verses[i], worldintoview(ro, theta, fi))
            b.append([a[0] * ro / (2 * a[2]) + width / 2, a[1] * ro / (2 * a[2]) + height / 2])
        return (b, self.edges)


cube = Cube()

while (not (window.closed)):
    cube.movecube(alpha=pi / 300, betha=pi / 600, gamma=pi / 600)
    # THETA += pi / 60
    da = cube.perspectiveprojection(RO, THETA, FI)
    # cube.drawfillcube()
    drawfigure(da[0], da[1])
    time.sleep(1 / 24)

window.close()