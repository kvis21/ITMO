import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class MandelbrotSet:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.max_iter = 50
        self.escape_radius = 2.0
        
        # Параметры области просмотра
        self.center_x = -0.5
        self.center_y = 0.0
        self.zoom = 1.0
        
        # Создаем фигуру с фиксированным расположением
        self.fig = plt.figure(figsize=(10, 8))
        
        # Основная ось для графика
        self.ax = self.fig.add_axes([0.1, 0.3, 0.7, 0.6])  # [left, bottom, width, height]
        
        # Ось для colorbar
        self.cax = self.fig.add_axes([0.82, 0.3, 0.02, 0.6])
        
        self.image = None
        self.colorbar = None
        self.updating = False
        
        # Создаем элементы управления
        self.setup_controls()
        
    def get_limits(self):
        """Вычисляет границы области просмотра на основе центра и зума"""
        scale = 1.5 / self.zoom
        xmin = self.center_x - scale
        xmax = self.center_x + scale
        ymin = self.center_y - scale
        ymax = self.center_y + scale
        return [xmin, xmax, ymin, ymax]
    
    def mandelbrot_iteration(self, c, max_iter=None):
        """Вычисляет количество итераций для точки c"""
        if max_iter is None:
            max_iter = self.max_iter
            
        z = np.zeros_like(c, dtype=complex)
        mandelbrot_set = np.zeros(c.shape, dtype=np.float32)
        
        for i in range(max_iter):
            mask = np.abs(z) < self.escape_radius
            z[mask] = z[mask] * z[mask] + c[mask]
            mandelbrot_set[mask] = i
            
        mandelbrot_set[mandelbrot_set == max_iter - 1] = max_iter
        return mandelbrot_set
    
    def compute_mandelbrot(self, max_iter=None):
        """Вычисляет множество Мандельброта для текущей области"""
        if max_iter is None:
            max_iter = self.max_iter
            
        limits = self.get_limits()
        xmin, xmax, ymin, ymax = limits
        
        # Создаем координатную сетку
        x = np.linspace(xmin, xmax, self.width)
        y = np.linspace(ymin, ymax, self.height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        # Вычисляем множество Мандельброта
        mandelbrot_set = self.mandelbrot_iteration(C, max_iter)
        
        return mandelbrot_set, limits
    
    def plot_mandelbrot(self, update_sliders=False):
        """Строит график множества Мандельброта"""
        if self.updating:
            return
            
        self.updating = True
        
        try:
            mandelbrot_set, limits = self.compute_mandelbrot()
            xmin, xmax, ymin, ymax = limits
            
            # Если изображение еще не создано, создаем его
            if self.image is None:
                self.image = self.ax.imshow(np.log(mandelbrot_set + 1), 
                                          extent=limits,
                                          cmap='hot',
                                          origin='lower',
                                          aspect='auto')
                
                # Создаем colorbar один раз
                self.colorbar = self.fig.colorbar(self.image, cax=self.cax)
                self.colorbar.set_label('log(количество итераций)')
            else:
                # Обновляем данные существующего изображения
                self.image.set_data(np.log(mandelbrot_set + 1))
                self.image.set_extent(limits)
                # Обновляем limits colorbar
                self.image.set_clim(0, np.log(self.max_iter + 1))
            
            self.ax.set_title(f'Множество Мандельброта\n'
                             f'Центр: ({self.center_x:.4f}, {self.center_y:.4f}) | '
                             f'Зум: {self.zoom:.2f}x | '
                             f'Итераций: {self.max_iter}')
            self.ax.set_xlabel('Re(c)')
            self.ax.set_ylabel('Im(c)')
            
            # Обновляем слайдеры только если явно указано
            if update_sliders:
                self.center_x_slider.set_val(self.center_x)
                self.center_y_slider.set_val(self.center_y)
                self.zoom_slider.set_val(self.zoom)
                self.iter_slider.set_val(self.max_iter)
            
            # Обновляем рисунок
            self.fig.canvas.draw_idle()
            
        finally:
            self.updating = False
        
    def setup_controls(self):
        """Создает элементы управления"""
        # Слайдер для центра по X
        ax_center_x = plt.axes([0.25, 0.20, 0.65, 0.03])
        self.center_x_slider = Slider(ax_center_x, 'Центр X', -2.0, 1.0, 
                                     valinit=self.center_x)
        
        # Слайдер для центра по Y
        ax_center_y = plt.axes([0.25, 0.16, 0.65, 0.03])
        self.center_y_slider = Slider(ax_center_y, 'Центр Y', -1.5, 1.5, 
                                     valinit=self.center_y)
        
        # Слайдер для зума
        ax_zoom = plt.axes([0.25, 0.12, 0.65, 0.03])
        self.zoom_slider = Slider(ax_zoom, 'Зум', 0.1, 10.0, 
                                 valinit=self.zoom, valfmt='%.1f')
        
        # Слайдер для итераций
        ax_iter = plt.axes([0.25, 0.08, 0.65, 0.03])
        self.iter_slider = Slider(ax_iter, 'Макс. итераций', 10, 500, 
                                 valinit=self.max_iter, valstep=10)
        
        # Кнопки для интересных областей
        ax_button1 = plt.axes([0.05, 0.02, 0.18, 0.04])
        ax_button2 = plt.axes([0.24, 0.02, 0.18, 0.04])
        ax_button3 = plt.axes([0.43, 0.02, 0.18, 0.04])
        ax_button4 = plt.axes([0.62, 0.02, 0.18, 0.04])
        ax_reset = plt.axes([0.81, 0.02, 0.18, 0.04])
        
        self.button1 = Button(ax_button1, 'Спирали')
        self.button2 = Button(ax_button2, 'Морской конек')
        self.button3 = Button(ax_button3, 'Верхняя часть')
        self.button4 = Button(ax_button4, 'Детали')
        self.reset_button = Button(ax_reset, 'Сброс')
        
        # Подключаем обработчики
        self.center_x_slider.on_changed(self.update_center_x)
        self.center_y_slider.on_changed(self.update_center_y)
        self.zoom_slider.on_changed(self.update_zoom)
        self.iter_slider.on_changed(self.update_iterations)
        
        self.button1.on_clicked(self.show_spirals)
        self.button2.on_clicked(self.show_seahorse)
        self.button3.on_clicked(self.show_top)
        self.button4.on_clicked(self.show_details)
        self.reset_button.on_clicked(self.reset_view)
    
    def update_center_x(self, val):
        """Обновляет центр по X"""
        if self.updating:
            return
        self.center_x = val
        self.plot_mandelbrot()
    
    def update_center_y(self, val):
        """Обновляет центр по Y"""
        if self.updating:
            return
        self.center_y = val
        self.plot_mandelbrot()
    
    def update_zoom(self, val):
        """Обновляет зум"""
        if self.updating:
            return
        self.zoom = val
        self.plot_mandelbrot()
    
    def update_iterations(self, val):
        """Обновляет максимальное количество итераций"""
        if self.updating:
            return
        self.max_iter = int(val)
        self.plot_mandelbrot()
    
    def show_spirals(self, event):
        """Показывает область со спиралями"""
        self.center_x = -0.7
        self.center_y = 0.15
        self.zoom = 20.0
        self.max_iter = 200
        self.plot_mandelbrot(update_sliders=True)
    
    def show_seahorse(self, event):
        """Показывает область 'морской конек'"""
        self.center_x = -0.745
        self.center_y = 0.115
        self.zoom = 200.0
        self.max_iter = 300
        self.plot_mandelbrot(update_sliders=True)
    
    def show_top(self, event):
        """Показывает верхнюю часть множества"""
        self.center_x = 0.0
        self.center_y = 0.7
        self.zoom = 10.0
        self.max_iter = 150
        self.plot_mandelbrot(update_sliders=True)
    
    def show_details(self, event):
        """Показывает детальную структуру"""
        self.center_x = -0.75
        self.center_y = 0.05
        self.zoom = 100.0
        self.max_iter = 500
        self.plot_mandelbrot(update_sliders=True)
    
    def reset_view(self, event):
        """Сбрасывает вид к начальному состоянию"""
        self.center_x = -0.5
        self.center_y = 0.0
        self.zoom = 1.0
        self.max_iter = 50
        self.plot_mandelbrot(update_sliders=True)
    
    def interactive_plot(self):
        """Запускает интерактивную визуализацию"""
        self.plot_mandelbrot()
        plt.show()


def main():
    # Создаем экземпляр класса
    mandelbrot = MandelbrotSet()
    
    print("Интерактивное исследование множества Мандельброта")
    print("\nЭлементы управления:")
    print("- Центр X/Y: перемещение по плоскости")
    print("- Зум: увеличение/уменьшение (0.1-100x)")
    print("- Макс. итераций: детализация изображения")
    print("\nКнопки быстрого доступа:")
    print("  • Спирали: красивые спиральные структуры")
    print("  • Морской конек: знаменитая деталь")
    print("  • Верхняя часть: верхние ответвления")
    print("  • Детали: очень мелкие структуры")
    print("  • Сброс: возврат к полному виду")
    print("\nИзменяйте параметры и наблюдайте за обновлением графика в реальном времени!")
    
    mandelbrot.interactive_plot()


if __name__ == "__main__":
    main()