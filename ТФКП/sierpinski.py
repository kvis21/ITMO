import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation

class SierpinskiTriangle:
    def __init__(self, iterations=10000):
        self.iterations = iterations
        
        # Вершины равностороннего треугольника
        self.vertices = np.array([
            [0, 0],
            [1, 0],
            [0.5, np.sqrt(3)/2]
        ])
        
    def chaotic_game(self):
        """Алгоритм хаотической игры"""
        points = np.zeros((self.iterations, 2))
        
        # Начальная точка (случайная внутри треугольника)
        points[0] = [random.uniform(0, 1), random.uniform(0, 0.8)]
        
        for i in range(1, self.iterations):
            # Выбираем случайную вершину
            random_vertex = random.choice(self.vertices)
            
            # Новая точка - середина между текущей точкой и случайной вершиной
            points[i] = (points[i-1] + random_vertex) / 2
        
        return points
    
    def plot_triangle(self, points=None):
        """Визуализация треугольника"""
        if points is None:
            points = self.chaotic_game()
        
        plt.figure(figsize=(10, 8))
        plt.scatter(points[:, 0], points[:, 1], s=0.1, c='blue', alpha=0.6)
        plt.scatter(self.vertices[:, 0], self.vertices[:, 1], s=50, c='red')
        
        plt.title(f'Треугольник Серпинского ({self.iterations} точек)')
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
import numpy as np
import matplotlib.pyplot as plt

class AffineSierpinski:
    def __init__(self):
        # Аффинные преобразования для треугольника Серпинского
        self.transforms = [
            # Меньший треугольник в левом углу
            lambda x: np.array([0.5, 0]) + np.array([[0.5, 0], [0, 0.5]]) @ x,
            # Меньший треугольник в правом углу
            lambda x: np.array([0.5, 0.5]) + np.array([[0.5, 0], [0, 0.5]]) @ x,
            # Меньший треугольник в верхнем углу
            lambda x: np.array([0.25, 0.5]) + np.array([[0.5, 0], [0, 0.5]]) @ x
        ]
    
    def generate_points(self, iterations=100000):
        """Генерация точек с помощью ИСП"""
        points = np.zeros((iterations, 2))
        current_point = np.random.rand(2)
        
        for i in range(iterations):
            # Выбираем случайное преобразование
            transform = np.random.choice(self.transforms)
            current_point = transform(current_point)
            points[i] = current_point
        
        return points
    
    def plot_affine(self, iterations=50000):
        """Визуализация ИСП метода"""
        points = self.generate_points(iterations)
        
        plt.figure(figsize=(10, 8))
        plt.scatter(points[:, 0], points[:, 1], s=0.1, c='green', alpha=0.7)
        plt.title(f'Треугольник Серпинского (ИСП метод, {iterations} точек)')
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

# Демонстрация
# affine = AffineSierpinski()
# affine.plot_affine(100000)

# Демонстрация
triangle = SierpinskiTriangle(50000)
points = triangle.chaotic_game()
triangle.plot_triangle(points)
