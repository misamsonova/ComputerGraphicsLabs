import matplotlib.pyplot as plt
from math import cos, sin, radians
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Cube:
    def __init__(self):
        self.vertices = [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (0, 1, 1)
        ]

        # Задаем ребра куба
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        self.faces = [
            [self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]],
            [self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]],
            [self.vertices[0], self.vertices[4], self.vertices[7], self.vertices[3]],
            [self.vertices[1], self.vertices[5], self.vertices[6], self.vertices[2]],
            [self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]],
            [self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]]
        ]

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.set_axis_off()

    def rotate(self):
        self.ax.cla()
        #self.ax.set_axis_off()

        # Матрица поворота по оси X
        rotation_x = [
            [1, 0, 0],
            [0, cos(radians(self.angle_x)), sin(radians(self.angle_x))],
            [0, -sin(radians(self.angle_x)), cos(radians(self.angle_x))]
        ]

        # Матрица поворота по оси Y
        rotation_y = [
            [cos(radians(self.angle_y)), 0, sin(radians(self.angle_y))],
            [0, 1, 0],
            [-sin(radians(self.angle_y)), 0, cos(radians(self.angle_y))]
        ]

        # Матрица поворота по оси Z
        rotation_z = [
            [cos(radians(self.angle_z)), sin(radians(self.angle_z)), 0],
            [-sin(radians(self.angle_z)), cos(radians(self.angle_z)), 0],
            [0, 0, 1]
        ]

        rotation_matrix = self.multiply_matrices(rotation_x, rotation_y)
        rotation_matrix = self.multiply_matrices(rotation_matrix, rotation_z)

        # Проходим по всем вершинам куба и применяем матрицу поворота
        rotated_vertices = []
        for vertex in self.vertices:
            rotated_vertex = [
                vertex[0] * rotation_matrix[0][0] + vertex[1] * rotation_matrix[0][1] + vertex[2] * rotation_matrix[0][2],
                vertex[0] * rotation_matrix[1][0] + vertex[1] * rotation_matrix[1][1] + vertex[2] * rotation_matrix[1][2],
                vertex[0] * rotation_matrix[2][0] + vertex[1] * rotation_matrix[2][1] + vertex[2] * rotation_matrix[2][2]
            ]
            rotated_vertices.append(rotated_vertex)

        def koch_snowflake(ax, order, size, vertices, base_tr):
            # В обеих функциях снежинка Коха рекурсивно строится путем разделения отрезков линии на три равные части
            # и замены средней части двумя сторонами равностороннего треугольника.
            # Рекурсия продолжается до тех пор, пока не будет достигнут указанный порядок.
            def koch_line(ax, order, size, p1, p2, face_vertices):
                if order == 0:
                    return [p1, p2]

                angle = np.pi / 3

                dx = (p2[0] - p1[0]) / 3
                dy = (p2[1] - p1[1]) / 3
                dz = (p2[2] - p1[2]) / 3
                s = [p1[0] + dx, p1[1] + dy, p1[2] + dz]
                t = [p1[0] + 2 * dx, p1[1] + 2 * dy, p1[2] + 2 * dz]

                ux = t[0] - s[0]
                uy = t[1] - s[1]
                uz = t[2] - s[2]

                if (face_vertices == self.faces[1]) or (face_vertices == self.faces[2]):
                    vx = ux
                    vy = np.cos(angle) * uy - np.sin(angle) * uz
                    vz = np.sin(angle) * uy + np.cos(angle) * uz

                if (face_vertices == self.faces[0]) or (face_vertices == self.faces[5]):
                    vx = np.cos(angle) * ux - np.sin(angle) * uy
                    vy = np.sin(angle) * ux + np.cos(angle) * uy
                    vz = uz

                if (face_vertices == self.faces[3]) or (face_vertices == self.faces[4]):
                    vx = np.cos(angle) * ux - np.sin(angle) * uz
                    vy = uy
                    vz = np.sin(angle) * ux + np.cos(angle) * uz

                w = [s[0] + vx, s[1] + vy, s[2] + vz]

                snowflake = koch_line(ax, order - 1, size, p1, s, face_vertices)
                snowflake.extend(koch_line(ax, order - 1, size, s, w, face_vertices))
                snowflake.extend(koch_line(ax, order - 1, size, w, t, face_vertices))
                snowflake.extend(koch_line(ax, order - 1, size, t, p2, face_vertices))

                return snowflake

            snowflake_texture = []

            for i in range(3):
                snowflake_texture.extend(koch_line(ax, order, size, base_tr[i], base_tr[i + 1], vertices))

            # Замкнутая снежинка Коха
            snowflake_texture.append(snowflake_texture[0])
            print(snowflake_texture)

            return Poly3DCollection([snowflake_texture], color='blue', alpha=0.3)

        # Отображаем снежинку Коха на боковой грани куба
        base_triangle_1 = np.array([
            [0, 0.5, 0],
            [0, 0, np.sqrt(2) / 2],
            [0, 1, np.sqrt(2) / 2],
            [0, 0.5, 0]
        ])

        base_triangle_2 = np.array([
            [1, 0.5, 0],
            [1, 0, np.sqrt(2) / 2],
            [1, 1, np.sqrt(2) / 2],
            [1, 0.5, 0]
        ])

        base_triangle_3 = np.array([
            [0.5, 0, 0],
            [0, 0, np.sqrt(2) / 2],
            [1, 0, np.sqrt(2) / 2],
            [0.5, 0, 0]
        ])

        base_triangle_4 = np.array([
            [0.5, 1, 0],
            [0, 1, np.sqrt(2) / 2],
            [1, 1, np.sqrt(2) / 2],
            [0.5, 1, 0]
        ])

        base_triangle_0 = np.array([
            [0.5, 0, 0],
            [0, np.sqrt(2) / 2, 0],
            [1, np.sqrt(2) / 2, 0],
            [0.5, 0, 0]
        ])

        base_triangle_5 = np.array([
            [0.5, 0, 1],
            [0, np.sqrt(2) / 2, 1],
            [1, np.sqrt(2) / 2, 1],
            [0.5, 0, 1]
        ])

        # Создаем замкнутую снежинку Коха и уменьшаем размер в два раза
        order = 4
        size = 1  # Длина ребра куба
        snowflake0 = koch_snowflake(self.ax, order, size, self.faces[0], base_triangle_0)
        snowflake1 = koch_snowflake(self.ax, order, size, self.faces[1], base_triangle_1)
        snowflake2 = koch_snowflake(self.ax, order, size, self.faces[2], base_triangle_2)
        snowflake3 = koch_snowflake(self.ax, order, size, self.faces[3], base_triangle_3)
        snowflake4 = koch_snowflake(self.ax, order, size, self.faces[4], base_triangle_4)
        snowflake5 = koch_snowflake(self.ax, order, size, self.faces[5], base_triangle_5)

        self.ax.add_collection3d(snowflake0)
        self.ax.add_collection3d(snowflake1)
        self.ax.add_collection3d(snowflake2)
        self.ax.add_collection3d(snowflake3)
        self.ax.add_collection3d(snowflake4)
        self.ax.add_collection3d(snowflake5)

        for edge in self.edges:
            x = [rotated_vertices[edge[0]][0], rotated_vertices[edge[1]][0]]
            y = [rotated_vertices[edge[0]][1], rotated_vertices[edge[1]][1]]
            z = [rotated_vertices[edge[0]][2], rotated_vertices[edge[1]][2]]
            self.ax.plot(x, y, z, color="black")

        plt.show()

    # Перемножаем матрицы поворота
    def multiply_matrices(self, mat1, mat2):
        result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += mat1[i][k] * mat2[k][j]
        return result

    # Функция обработки нажатий клавиш
    def on_key_press(self, event):
        key = event.key
        if key == "left":
            self.angle_y += 5
        elif key == "right":
            self.angle_y -= 5
        elif key == "up":
            self.angle_x += 5
        elif key == "down":
            self.angle_x -= 5
        elif key == "a":
            self.angle_z += 5
        elif key == "d":
            self.angle_z -= 5
        self.rotate()

    def run(self):
        self.rotate()

cube = Cube()
cube.run()
