export class GraphRenderer {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private readonly BASE_R: number = 100;
  private centerX: number;
  private centerY: number;
  private activeAnimations: Map<number, { opacity: number; points: Array<{x: number, y: number, result: boolean}> }> = new Map();
  private animationFrameId: number | null = null;
  private animationTimeout: number = 3000;

  constructor(canvasId: string) {
    const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
    if (!canvas) {
      throw new Error(`Canvas with id ${canvasId} not found`);
    }
    const computedStyle = getComputedStyle(canvas);
    canvas.width = parseInt(computedStyle.width) + 150;
    canvas.height = parseInt(computedStyle.height) + 150;

    this.canvas = canvas;
    const context = this.canvas.getContext('2d');
    if (!context) {
      throw new Error('Could not get 2D context');
    }

    this.ctx = context;
    this.centerX = this.canvas.width / 2;
    this.centerY = this.canvas.height / 2;

    this.startAnimationLoop();
    this.drawGraph();
  }

  private startAnimationLoop(): void {
    const animate = () => {
      this.drawGraph();
      this.animationFrameId = requestAnimationFrame(animate);
    };
    animate();
  }

  public showFigure(r: number): void {
    if (this.activeAnimations.size >= 5) {
      const oldestR = this.activeAnimations.keys().next().value;
      if (oldestR !== undefined) {
        this.activeAnimations.delete(oldestR);
      }
    }
    
    // Добавляем фигуру с пустым массивом точек
    this.activeAnimations.set(r, { 
      opacity: 0, 
      points: [] 
    });
    
    const fadeIn = () => {
      const animation = this.activeAnimations.get(r);
      if (!animation) return;

      if (animation.opacity < 1) {
        animation.opacity += 0.05;
        setTimeout(fadeIn, 50);
      } else {
        setTimeout(() => this.hideFigure(r), this.animationTimeout);
      }
    };
    fadeIn();
  }

  public hideFigure(r: number): void {
    const fadeOut = () => {
      const animation = this.activeAnimations.get(r);
      if (!animation) return;

      if (animation.opacity > 0) {
        animation.opacity -= 0.05;
        setTimeout(fadeOut, 50);
      } else {
        this.activeAnimations.delete(r);
      }
    };
    fadeOut();
  }

  public drawGraph(): void {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Рисуем только анимированные фигуры (без основной)
    this.activeAnimations.forEach((animation, r) => {
      this.drawFigure(this.BASE_R * r, animation.opacity, animation.points);
    });

    // Оси и подписи
    this.drawAxes();
    this.drawLabels();
  }

  private drawFigure(radius: number, opacity: number, points: Array<{x: number, y: number, result: boolean}>): void {
    this.ctx.save();
    
    this.ctx.globalAlpha = opacity;
    this.ctx.fillStyle = `rgba(61, 211, 248, ${0.79 * opacity})`;
    this.ctx.strokeStyle = `rgba(0, 100, 200, ${opacity})`;
    this.ctx.lineWidth = 2;

    this.ctx.beginPath();
    this.ctx.rect(
      this.centerX - radius, 
      this.centerY - radius / 2, 
      radius, 
      radius / 2
    );
    this.ctx.fill();
    this.ctx.stroke();

    this.ctx.beginPath();
    this.ctx.moveTo(this.centerX, this.centerY);
    this.ctx.arc(this.centerX, this.centerY, radius, 0, Math.PI / 2, false);
    this.ctx.lineTo(this.centerX, this.centerY);
    this.ctx.fill();
    this.ctx.stroke();

    this.ctx.beginPath();
    this.ctx.moveTo(this.centerX, this.centerY);
    this.ctx.lineTo(this.centerX - radius / 2, this.centerY);
    this.ctx.lineTo(this.centerX, this.centerY + radius / 2);
    this.ctx.closePath();
    this.ctx.fill();
    this.ctx.stroke();

    this.ctx.globalAlpha = 1;
    points.forEach(point => {
      const scale = this.BASE_R;
      const canvasX = this.centerX + point.x * scale;
      const canvasY = this.centerY - point.y * scale;
      
      this.ctx.beginPath();
      this.ctx.arc(canvasX, canvasY, 4, 0, 2 * Math.PI);
      this.ctx.fillStyle = point.result ? 'green' : 'red';
      this.ctx.fill();
      this.ctx.strokeStyle = 'black';
      this.ctx.lineWidth = 1;
      this.ctx.stroke();
    });

    this.drawFigureLabels(radius, opacity);

    this.ctx.restore();
  }

  private drawFigureLabels(radius: number, opacity: number): void {
    this.ctx.save();
    this.ctx.globalAlpha = opacity;
    this.ctx.font = "10px monospace";
    this.ctx.fillStyle = "black";

    const rValue = radius / this.BASE_R; // Вычисляем значение R (1, 1.5, 2, 2.5, 3)

    this.ctx.restore();
  }

private drawAxes(): void {
    this.ctx.save();
    this.ctx.globalAlpha = 1;
    this.ctx.strokeStyle = "black";
    this.ctx.lineWidth = 1;
    
    // Основные оси
    this.ctx.beginPath();
    this.ctx.moveTo(this.centerX, 0);
    this.ctx.lineTo(this.centerX, this.canvas.height);
    this.ctx.moveTo(0, this.centerY);
    this.ctx.lineTo(this.canvas.width, this.centerY);
    this.ctx.stroke();

    const radii = [0.5, 1, 1.5, 2, 2.5, 3];
    const tickSize = 6; 

    radii.forEach(r => {
        const radius = this.BASE_R * r;
        
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX + radius, this.centerY - tickSize);
        this.ctx.lineTo(this.centerX + radius, this.centerY + tickSize);
        this.ctx.stroke();

        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX - radius, this.centerY - tickSize);
        this.ctx.lineTo(this.centerX - radius, this.centerY + tickSize);
        this.ctx.stroke();

        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX - tickSize, this.centerY - radius);
        this.ctx.lineTo(this.centerX + tickSize, this.centerY - radius);
        this.ctx.stroke();

        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX - tickSize, this.centerY + radius);
        this.ctx.lineTo(this.centerX + tickSize, this.centerY + radius);
        this.ctx.stroke();
    });

    this.ctx.restore();
}

private drawLabels(): void {
    this.ctx.save();
    this.ctx.globalAlpha = 1;
    this.ctx.font = "14px Arial";
    this.ctx.textAlign = "center";

    // Подписи осей
    this.ctx.fillStyle = "red";
    this.ctx.fillText("X", this.canvas.width - 15, this.centerY - 15);
    this.ctx.fillText("Y", this.centerX + 15, 15);
    this.ctx.fillText("0", this.centerX + 6, this.centerY - 6);

    this.ctx.fillStyle = "black";
    this.ctx.font = "10px Arial";
    // Все значения радиусов с разными цветами
    const radii = [0.5, 1, 1.5, 2, 2.5, 3];
    
    radii.forEach((r) => {
        const radius = this.BASE_R * r;

        this.ctx.fillText(`${r}R`, this.centerX + radius, this.centerY - 10);
        this.ctx.fillText(`-${r}R`, this.centerX - radius, this.centerY - 10);
        this.ctx.fillText(`${r}R`, this.centerX + 15, this.centerY - radius + 4);
        this.ctx.fillText(`-${r}R`, this.centerX + 20, this.centerY + radius + 4);
    });
    
    this.ctx.restore();
}

  public drawPoint(x: number, y: number, result: boolean, r: number): void {
    // Находим анимацию для этого радиуса и добавляем точку
    const animation = this.activeAnimations.get(r);
    if (animation) {
      animation.points.push({ x, y, result });
    } else {
      // Если анимации нет, создаем ее и добавляем точку
      this.showFigure(r);
      // Ждем немного чтобы анимация успела запуститься, затем добавляем точку
      setTimeout(() => {
        const newAnimation = this.activeAnimations.get(r);
        if (newAnimation) {
          newAnimation.points.push({ x, y, result });
        }
      }, 100);
    }
  }

  public clearPoints(): void {
    this.activeAnimations.clear();
    this.drawGraph();
  }

  public destroy(): void {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
  }

  public get_animationTimeout(): number {
    return this.animationTimeout;
  }
}