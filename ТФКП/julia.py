import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class JuliaSet:
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.max_iter = 50
        self.escape_radius = 2.0
        self.c = complex(-0.5251993, 0.5251993)
        
        # Создаем координатную сетку
        self.x = np.linspace(-2, 2, width)
        self.y = np.linspace(-2, 2, height)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.25)
        
        # Добавляем атрибут для хранения colorbar
        self.colorbar = None
        
    def julia_iteration(self, z, c):
        """Одна итерация отображения Жюлиа: z -> z² + c"""
        return z**2 + c
    
    def compute_julia_set(self, c=None, max_iter=None):
        """Вычисляет множество Жюлиа для заданного c"""
        if c is None:
            c = self.c
        if max_iter is None:
            max_iter = self.max_iter
            
        # Инициализируем массив для результатов
        julia_set = np.zeros((self.height, self.width), dtype=np.float32)
        
        # Преобразуем координаты в комплексные числа
        Z = self.X + 1j * self.Y
        
        # Векторизованное вычисление итераций
        for i in range(max_iter):
            # Применяем отображение Жюлиа
            Z = self.julia_iteration(Z, c)
            
            # Отмечаем точки, которые вышли за пределы радиуса схода
            mask = np.abs(Z) > self.escape_radius
            julia_set[mask & (julia_set == 0)] = i + 1
            
            # Обновляем только те точки, которые еще не вышли
            Z = np.where(np.abs(Z) > self.escape_radius, np.nan, Z)
        
        # Точки, которые никогда не вышли - принадлежат множеству Жюлиа
        julia_set[julia_set == 0] = max_iter
        
        return julia_set
    
    def plot_julia_set(self, c=None, max_iter=None):
        """Строит график множества Жюлиа"""
        if c is not None:
            self.c = c
            
        julia_set = self.compute_julia_set(c, max_iter)
        
        self.ax.clear()
        
        # Используем логарифмическую шкалу для лучшего отображения деталей
        im = self.ax.imshow(np.log(julia_set + 1), 
                           extent=[-2, 2, -2, 2],
                           cmap='hot',
                           origin='lower')
        
        self.ax.set_title(f'Множество Жюлиа для c = {self.c.real:.6f} + {self.c.imag:.6f}i\n'
                         f'Максимум итераций: {self.max_iter if max_iter is None else max_iter}')
        self.ax.set_xlabel('Re(z)')
        self.ax.set_ylabel('Im(z)')
        
        # Удаляем старый colorbar, если он существует
        if self.colorbar is not None:
            self.colorbar.remove()
        
        # Создаем новый colorbar
        self.colorbar = plt.colorbar(im, ax=self.ax, label='log(количество итераций)')
        
        # Обновляем рисунок
        self.fig.canvas.draw_idle()
        
    def interactive_plot(self):
        """Создает интерактивный график с возможностью изменения параметров"""
        self.plot_julia_set()
        
        # Создаем слайдеры для изменения параметров
        ax_real = plt.axes([0.25, 0.15, 0.65, 0.03])
        ax_imag = plt.axes([0.25, 0.10, 0.65, 0.03])
        ax_iter = plt.axes([0.25, 0.05, 0.65, 0.03])
        
        slider_real = Slider(ax_real, 'Re(c)', -2.0, 2.0, valinit=self.c.real)
        slider_imag = Slider(ax_imag, 'Im(c)', -2.0, 2.0, valinit=self.c.imag)
        slider_iter = Slider(ax_iter, 'Макс. итераций', 10, 500, valinit=self.max_iter, valstep=10)
        
        # Кнопки для предустановленных значений c
        ax_button1 = plt.axes([0.05, 0.15, 0.15, 0.04])
        ax_button2 = plt.axes([0.05, 0.10, 0.15, 0.04])
        ax_button3 = plt.axes([0.05, 0.05, 0.15, 0.04])
        
        button1 = Button(ax_button1, 'Красивое c')
        button2 = Button(ax_button2, 'Дендрит')
        button3 = Button(ax_button3, 'Кролик')
        
        def update(val=None):
            self.c = complex(slider_real.val, slider_imag.val)
            self.max_iter = int(slider_iter.val)
            self.plot_julia_set()
        
        def set_beautiful_c(event):
            slider_real.set_val(-0.5251993)
            slider_imag.set_val(0.5251993)
            update()
        
        def set_dendrite_c(event):
            slider_real.set_val(0)
            slider_imag.set_val(1)
            update()
        
        def set_rabbit_c(event):
            slider_real.set_val(-0.123)
            slider_imag.set_val(0.745)
            update()
        
        slider_real.on_changed(update)
        slider_imag.on_changed(update)
        slider_iter.on_changed(update)
        
        button1.on_clicked(set_beautiful_c)
        button2.on_clicked(set_dendrite_c)
        button3.on_clicked(set_rabbit_c)
        
        plt.show()


def main():
    # Создаем экземпляр класса
    julia = JuliaSet()
    
    print("Интерактивное исследование множества Жюлиа")
    print("Используйте слайдеры для изменения параметров:")
    print("- Re(c) и Im(c) - действительная и мнимая части константы c")
    print("- Макс. итераций - максимальное количество итераций")
    print("\nКнопки для быстрого выбора интересных значений c:")
    print("- Красивое c: c = -0.5251993 + 0.5251993i")
    print("- Дендрит: c = i")
    print("- Кролик: c = -0.123 + 0.745i")
    
    julia.interactive_plot()

if __name__ == "__main__":
    main()