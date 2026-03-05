import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class HarterHeighwayDragon:
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.max_iterations = 12
        
        # Начальные параметры дракона
        self.start_point = np.array([0, 0])
        self.initial_segment = np.array([1, 0])
        
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.25)
        
    def dragon_iteration(self, points):
        """Одна итерация построения дракона"""
        new_points = [points[0]]  # Начинаем с первой точки
        
        for i in range(len(points) - 1):
            # Текущий отрезок
            p1 = points[i]
            p2 = points[i + 1]
            
            # Вектор отрезка
            v = p2 - p1
            
            # Поворот на 90 градусов для создания "излома"
            # Чередуем повороты: +90, -90, +90, -90, ...
            if i % 2 == 0:
                # Поворот на +90 градусов
                v_rotated = np.array([-v[1], v[0]])
            else:
                # Поворот на -90 градусов
                v_rotated = np.array([v[1], -v[0]])
            
            # Новая точка - середина + повернутый вектор/2
            new_point = p1 + v/2 + v_rotated/2
            new_points.extend([new_point, p2])
        
        return new_points
    
    def generate_dragon(self, iterations=None):
        """Генерирует точки дракона Хартера-Хейтуэя"""
        if iterations is None:
            iterations = self.max_iterations
            
        # Начальный отрезок [0,0] -> [1,0]
        points = [self.start_point, self.start_point + self.initial_segment]
        
        for _ in range(iterations):
            points = self.dragon_iteration(points)
        
        return np.array(points)
    
    def plot_dragon(self, iterations=None):
        """Строит график дракона Хартера-Хейтуэя"""
        if iterations is not None:
            self.max_iterations = iterations
            
        dragon_points = self.generate_dragon(self.max_iterations)
        
        self.ax.clear()
        
        # Рисуем дракона
        self.ax.plot(dragon_points[:, 0], dragon_points[:, 1], 
                    'b-', linewidth=0.8, alpha=0.8)
        self.ax.fill(dragon_points[:, 0], dragon_points[:, 1], 
                    'lightblue', alpha=0.3)
        
        self.ax.set_title(f'Дракон Хартера-Хейтуэя (итераций: {self.max_iterations})')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.axis('equal')
        self.ax.grid(True, alpha=0.3)
        
        # Добавляем информацию о количестве сегментов
        num_segments = len(dragon_points) - 1
        self.ax.text(0.02, 0.98, f'Сегментов: {num_segments}', 
                    transform=self.ax.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Обновляем рисунок
        self.fig.canvas.draw_idle()
        
    def transform_dragon(self, scale=1.0, rotation=0, translation=(0, 0)):
        """Применяет преобразования к дракону"""
        points = self.generate_dragon(self.max_iterations)
        
        # Поворот
        theta = np.radians(rotation)
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        
        # Масштабирование и поворот
        transformed_points = (points * scale) @ rotation_matrix.T
        
        # Сдвиг
        transformed_points += translation
        
        return transformed_points
    
    def plot_transformed_dragon(self, scale=1.0, rotation=0, translation=(0, 0)):
        """Строит преобразованный дракон"""
        transformed_points = self.transform_dragon(scale, rotation, translation)
        
        self.ax.clear()
        
        # Рисуем преобразованного дракона
        self.ax.plot(transformed_points[:, 0], transformed_points[:, 1], 
                    'r-', linewidth=0.8, alpha=0.8)
        self.ax.fill(transformed_points[:, 0], transformed_points[:, 1], 
                    'lightcoral', alpha=0.3)
        
        self.ax.set_title(f'Дракон Хартера-Хейтуэя (итераций: {self.max_iterations})\n'
                         f'Масштаб: {scale}, Поворот: {rotation}°, Сдвиг: {translation}')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.axis('equal')
        self.ax.grid(True, alpha=0.3)
        
        self.fig.canvas.draw_idle()
    
    def interactive_plot(self):
        """Создает интерактивный график с возможностью изменения параметров"""
        self.plot_dragon()
        
        # Создаем слайдеры для изменения параметров
        ax_iter = plt.axes([0.25, 0.15, 0.65, 0.03])
        ax_scale = plt.axes([0.25, 0.10, 0.65, 0.03])
        ax_rotation = plt.axes([0.25, 0.05, 0.65, 0.03])
        
        slider_iter = Slider(ax_iter, 'Итерации', 1, 20, valinit=self.max_iterations, valstep=1)
        slider_scale = Slider(ax_scale, 'Масштаб', 0.1, 3.0, valinit=1.0)
        slider_rotation = Slider(ax_rotation, 'Поворот (°)', 0, 360, valinit=0)
        
        # Кнопки для предустановленных значений
        ax_button1 = plt.axes([0.05, 0.15, 0.15, 0.04])
        ax_button2 = plt.axes([0.05, 0.10, 0.15, 0.04])
        ax_button3 = plt.axes([0.05, 0.05, 0.15, 0.04])
        ax_button4 = plt.axes([0.05, 0.20, 0.15, 0.04])
        
        button1 = Button(ax_button1, 'Базовый')
        button2 = Button(ax_button2, 'Высок. деталь')
        button3 = Button(ax_button3, 'Двойной')
        button4 = Button(ax_button4, 'Трансформация')
        
        # Переменная для отслеживания режима
        self.transform_mode = False
        
        def update(val=None):
            if self.transform_mode:
                self.plot_transformed_dragon(
                    scale=slider_scale.val,
                    rotation=slider_rotation.val,
                    translation=(0, 0)
                )
            else:
                self.max_iterations = int(slider_iter.val)
                self.plot_dragon()
        
        def set_basic(event):
            self.transform_mode = False
            slider_iter.set_val(8)
            slider_scale.set_val(1.0)
            slider_rotation.set_val(0)
            update()
        
        def set_high_detail(event):
            self.transform_mode = False
            slider_iter.set_val(15)
            update()
        
        def set_double(event):
            self.transform_mode = False
            slider_iter.set_val(16)
            update()
        
        def toggle_transform(event):
            self.transform_mode = not self.transform_mode
            if self.transform_mode:
                button4.label.set_text('Обычный')
                self.plot_transformed_dragon(
                    scale=slider_scale.val,
                    rotation=slider_rotation.val
                )
            else:
                button4.label.set_text('Трансформация')
                self.plot_dragon()
        
        slider_iter.on_changed(update)
        slider_scale.on_changed(update)
        slider_rotation.on_changed(update)
        
        button1.on_clicked(set_basic)
        button2.on_clicked(set_high_detail)
        button3.on_clicked(set_double)
        button4.on_clicked(toggle_transform)
        
        plt.show()
    
    def multiple_dragons_plot(self):
        """Показывает несколько драконов с разными параметрами"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        iterations_list = [5, 8, 10, 12, 14, 16]
        
        for i, iterations in enumerate(iterations_list):
            points = self.generate_dragon(iterations)
            
            axes[i].plot(points[:, 0], points[:, 1], 'b-', linewidth=0.8)
            axes[i].set_title(f'Итераций: {iterations}\nСегментов: {len(points)-1}')
            axes[i].axis('equal')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


def main():
    # Создаем экземпляр класса
    dragon = HarterHeighwayDragon()
    
    print("Интерактивное исследование дракона Хартера-Хейтуэя")
    print("Используйте слайдеры для изменения параметров:")
    print("- Итерации - количество итераций построения")
    print("- Масштаб - масштабирование фигуры")
    print("- Поворот - вращение фигуры в градусах")
    print("\nКнопки для быстрого выбора:")
    print("- Базовый: 8 итераций, стандартный вид")
    print("- Высок. деталь: 15 итераций, высокая детализация")
    print("- Двойной: 16 итераций, очень детализированный")
    print("- Трансформация: переключение в режим трансформаций")
    
    # Выберите один из вариантов:
    
    # 1. Интерактивный режим
    dragon.interactive_plot()
    
    # 2. Множественное отображение
    # dragon.multiple_dragons_plot()


if __name__ == "__main__":
    main()