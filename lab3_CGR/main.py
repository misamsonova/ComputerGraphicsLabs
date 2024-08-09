import matplotlib.pyplot as plt
from math import cos, sin, radians
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

class Cube:
    def __init__(self):
        self.vertices = [
            (-0, 1, 1),
            (-0, -0, 1),
            (-0, -0, -0),
            (-0, 1, -0),
            (1, 1, 1),
            (1, -0, 1),
            (1, -0, -0),
            (1, 1, -0)
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
        #self.ax.set_axis_off()

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
                vertex[0] * rotation_matrix[0][0] + vertex[1] * rotation_matrix[0][1] + vertex[2] * rotation_matrix[0][
                    2],
                vertex[0] * rotation_matrix[1][0] + vertex[1] * rotation_matrix[1][1] + vertex[2] * rotation_matrix[1][
                    2],
                vertex[0] * rotation_matrix[2][0] + vertex[1] * rotation_matrix[2][1] + vertex[2] * rotation_matrix[2][
                    2]
            ]
            rotated_vertices.append(rotated_vertex)

        rotated_faces = []
        for face in self.faces:
            rotated_face = [
                [
                    vertex[0] * rotation_matrix[0][0] + vertex[1] * rotation_matrix[0][1] + vertex[2] *
                    rotation_matrix[0][2],
                    vertex[0] * rotation_matrix[1][0] + vertex[1] * rotation_matrix[1][1] + vertex[2] *
                    rotation_matrix[1][2],
                    vertex[0] * rotation_matrix[2][0] + vertex[1] * rotation_matrix[2][1] + vertex[2] *
                    rotation_matrix[2][2]
                ]
                for vertex in face
            ]
            rotated_faces.append(rotated_face)

        # Отображаем грани куба
        self.ax.add_collection3d(Poly3DCollection(rotated_faces, facecolors='cyan', linewidths=1, edgecolors='black', alpha=0.5))

        for edge in self.edges:
            x = [rotated_vertices[edge[0]][0], rotated_vertices[edge[1]][0]]
            y = [rotated_vertices[edge[0]][1], rotated_vertices[edge[1]][1]]
            z = [rotated_vertices[edge[0]][2], rotated_vertices[edge[1]][2]]
            self.ax.plot(x, y, z, color="black")

        def koch_curve_3d(p1, p2, order, g):
            if order == 0:
                return [p1, p2]

            # Calculate intermediate points
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dz = p2[2] - p1[2]

            # Calculate one-third and two-thirds points
            one_third = [p1[0] + dx / 3, p1[1] + dy / 3, p1[2] + dz / 3]
            two_thirds = [p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3, p1[2] + 2 * dz / 3]

            ux = two_thirds[0] - one_third[0]
            uy = two_thirds[1] - one_third[1]
            uz = two_thirds[2] - one_third[2]

            angle = np.pi / 2
            if g == g2 or g == g3:
                vx = ux
                vy = np.cos(angle) * uy + np.sin(angle) * uz
                vz = -np.sin(angle) * uy + np.cos(angle) * uz
                mid_point = [(one_third[0] + two_thirds[0]) / 2, (one_third[1] + two_thirds[1]) / 2,
                             (one_third[2] + two_thirds[2]) / 2]
                mid_point = [mid_point[0] + vx, mid_point[1] + vy, mid_point[2] + vz]
                apex = [
                    mid_point[0],
                    mid_point[1],
                    mid_point[2]
                ]
            elif g == g0 or g == g1:
                # Calculate equilateral triangle point
                vx = np.cos(angle) * ux + np.sin(angle) * uy
                vy = - np.sin(angle) * ux + np.cos(angle) * uy
                vz = uz
                mid_point = [(one_third[0] + two_thirds[0]) / 2, (one_third[1] + two_thirds[1]) / 2,
                             (one_third[2] + two_thirds[2]) / 2]
                mid_point = [mid_point[0] + vx, mid_point[1] + vy, mid_point[2] + vz]
                apex = [
                    mid_point[0],
                    mid_point[1],
                    mid_point[2]
                ]
            elif g == g4 or g == g5:
                vx = np.cos(angle) * ux + np.sin(angle) * uz
                vy = uy
                vz = - np.sin(angle) * ux + np.cos(angle) * uz
                mid_point = [(one_third[0] + two_thirds[0]) / 2, (one_third[1] + two_thirds[1]) / 2,
                             (one_third[2] + two_thirds[2]) / 2]
                mid_point = [mid_point[0] + vx, mid_point[1] + vy, mid_point[2] + vz]
                apex = [
                    mid_point[0],
                    mid_point[1],
                    mid_point[2]
                ]

            # Recursively get points for sub-curves
            points = koch_curve_3d(p1, one_third, order - 1, g)
            points.extend(koch_curve_3d(one_third, apex, order - 1, g))
            points.extend(koch_curve_3d(apex, two_thirds, order - 1, g))
            points.extend(koch_curve_3d(two_thirds, p2, order - 1, g))

            return points

        def draw_koch_snowflake_3d(ax, order, size, p1, p2, p3, g):
            # Draw three Koch curves to form the snowflake
            snowflake_points = []
            snowflake_points.extend(koch_curve_3d(p1, p2, order, g))
            snowflake_points.extend(koch_curve_3d(p2, p3, order, g))
            snowflake_points.extend(koch_curve_3d(p3, p1, order, g))

            # Close the snowflake
            snowflake_points.append(snowflake_points[0])

            # Convert points to numpy array for plotting
            snowflake_points = np.array(snowflake_points)

            # Set z-coordinate to zero (place on the XY plane)

            # Plot the snowflake
            ax.plot3D(snowflake_points[:, 0], snowflake_points[:, 1], snowflake_points[:, 2], color='blue')

        order = 4
        size = 0.9
        # Define the three starting points of the snowflake
        p10 = [0.1, size / 4, 0]
        p20 = [size-0.1, size / 4, 0]
        p30 = [size / 2, size * np.sqrt(3) / 2 + size / 4, 0]
        g0 = 0
        p1 = [0.1, size / 4, 1]
        p2 = [size-0.1, size / 4, 1]
        p3 = [size / 2, size * np.sqrt(3) / 2 + size / 4, 1]
        g1 = 1

        p12 = [0, 0, size / 4]
        p22 = [0, size, size / 4]
        p32 = [0, size / 2, size * np.sqrt(3) / 2 + size / 4]
        g2 = 2

        p13 = [1, 0, size / 4]
        p23 = [1, size, size / 4]
        p33 = [1, size / 2, size * np.sqrt(3) / 2 + size / 4]
        g3 = 3

        p14 = [0, 0, size / 4]
        p24 = [size, 0, size / 4]
        p34 = [size / 2, 0, size * np.sqrt(3) / 2 + size / 4]
        g4 = 4

        p15 = [0, 1, size / 4]
        p25 = [size, 1, size / 4]
        p35 = [size / 2, 1, size * np.sqrt(3) / 2 + size / 4]
        g5 = 5
        # Draw the 3D Koch Snowflake
        draw_koch_snowflake_3d(self.ax, order, size, p10, p20, p30, g0)
        draw_koch_snowflake_3d(self.ax, order, size, p1, p2, p3, g1)
        draw_koch_snowflake_3d(self.ax, order, size, p12, p22, p32, g2)
        draw_koch_snowflake_3d(self.ax, order, size, p13, p23, p33, g3)
        draw_koch_snowflake_3d(self.ax, order, size, p14, p24, p34, g4)
        draw_koch_snowflake_3d(self.ax, order, size, p15, p25, p35, g5)

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
