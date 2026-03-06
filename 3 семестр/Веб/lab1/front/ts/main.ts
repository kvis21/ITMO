import { PointsDB } from './db';
import { PointValidator } from './validation';
import { GraphRenderer } from './graph';
import { ApiResponse, TableResult } from './types';

class Application {
  private validator: PointValidator;
  private graph: GraphRenderer;
  private resultTable: HTMLTableElement;
  private pointsDB: PointsDB;
  //private clearBtn: HTMLButtonElement;

  constructor() {
    const submitBtn = document.querySelector('.submit-btn') as HTMLButtonElement;
    if (!submitBtn) {
      throw new Error('Submit button not found');
    }

    this.validator = new PointValidator(submitBtn);
    this.graph = new GraphRenderer('graphCanvas');
    this.resultTable = document.getElementById('resultsTable') as HTMLTableElement;
    this.pointsDB = new PointsDB();

    // this.clearBtn = document.getElementById('clearData') as HTMLButtonElement;
    // if (!this.clearBtn) {
    //   throw new Error('Clear button not found');
    // }

    this.initializeEventListeners();
    this.loadStoredResults();
  }

  private initializeEventListeners(): void {
    const form = document.getElementById('pointForm') as HTMLFormElement;
    form?.addEventListener('submit', this.handleFormSubmit.bind(this));
    //this.clearBtn.addEventListener('click', () => this.handleClearData());
  }

  
  private async handleFormSubmit(ev: Event): Promise<void> {
    ev.preventDefault();

    const formData = this.validator.getFormData();
    if (!formData) return;

    const params = new URLSearchParams({
      x: formData.x.toString(),
      y: formData.y.toString(),
      listR: formData.r.join(',')
    });

    console.log("Sending request with params:", params.toString());

    try {
      const response = await fetch(`/fcgi-bin/FastCGIApp.jar/calculate?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });

      await this.handleResponse(response, formData);
    } catch (error) {
      console.error('Request failed:', error);
      this.addErrorToTable('Network error');
    }
  }

  private async handleResponse(response: Response, formData: { x: number; y: number; r: number[] }): Promise<void> {
    const baseResult: Omit<TableResult, 'r' | 'result' | 'execTime'> = {
      x: formData.x,
      y: formData.y,
      time: ''
    };

    if (response.ok) {
      const result: ApiResponse = await response.json();
      
      this.graph.drawGraph();
      
      for (let i = 0; i < formData.r.length; i++) {
        const tableResult: TableResult = {
          ...baseResult,
          r: formData.r[i].toString(),
          result: result.results[i].toString(),
          time: new Date(result.now).toLocaleString(),
          execTime: `${result.time} ns`
        };

        // Показываем анимированную фигуру и сразу рисуем на ней точку
        this.graph.showFigure(formData.r[i]);
        this.graph.drawPoint(formData.x, formData.y, result.results[i], formData.r[i]);
        
        this.addResultToTable(tableResult);
        await this.pointsDB.addPoint(tableResult);

        if (i < formData.r.length - 1) {
          await new Promise(resolve => setTimeout(resolve, this.graph.get_animationTimeout() + 2000));
        }
      } 
    } else {
      if (response.status === 400) {
        const result: ApiResponse = await response.json();
        const errorResult: TableResult = {
          ...baseResult,
          r: 'N/A',
          result: `error: ${result.message}`,
          time: new Date(result.now).toLocaleString(),
          execTime: 'N/A'
        };
        this.addResultToTable(errorResult);
      } else {
        const errorResult: TableResult = {
          ...baseResult,
          r: 'N/A',
          result: 'error',
          time: 'N/A',
          execTime: 'N/A'
        };
        this.addResultToTable(errorResult);
      }
    }
  }

  private addResultToTable(result: TableResult): void {
    const newRow = this.resultTable.insertRow(-1);
    
    const rowX = newRow.insertCell(0);
    const rowY = newRow.insertCell(1);
    const rowR = newRow.insertCell(2);
    const rowResult = newRow.insertCell(3);
    const rowTime = newRow.insertCell(4);
    const rowExecTime = newRow.insertCell(5);

    rowX.textContent = result.x.toString();
    rowY.textContent = result.y.toString();
    rowR.textContent = result.r;
    rowTime.textContent = result.time;
    rowExecTime.textContent = result.execTime;
    
    if (result.result.includes('error')) {
      rowResult.textContent = result.result;
      rowResult.className = 'result-error';
    } else {
      // УНИФИЦИРУЕМ ПРОВЕРКУ
      const isHit = result.result === 'true' || result.result === 'Попадание';
      rowResult.textContent = isHit ? 'Попадание' : 'Непопадание';
      rowResult.className = isHit ? 'result-hit' : 'result-miss';
    }

    newRow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  private addErrorToTable(message: string): void {
    const errorResult: TableResult = {
      x: 0,
      y: 0,
      r: 'N/A',
      result: message,
      time: 'N/A',
      execTime: 'N/A'
    };
    this.addResultToTable(errorResult);
  }

  private async loadStoredResults(): Promise<void> {
    try {
      await this.pointsDB.init();
      const storedPoints = await this.pointsDB.getAllPoints();
      
      storedPoints.sort((a, b) => a.timestamp - b.timestamp);
      
      storedPoints.forEach(point => {
        this.addResultToTable(point);
      });
    } catch (error) {
      console.error('Failed to load stored results:', error);
    }
  }
  async clearAllData(): Promise<void> {
    try {
      // Очищаем базу данных
      await this.pointsDB.clearPoints();

      // Очищаем график
      this.graph.clearPoints();

      // Полностью пересоздаем тело таблицы
      const tbody = this.resultTable.querySelector('tbody');
      if (tbody) {
        // Удаляем старый tbody
        tbody.remove();
        
        // Создаем новый пустой tbody
        const newTbody = document.createElement('tbody');
        this.resultTable.appendChild(newTbody);
      }
      
      console.log('All data cleared successfully');
      
    } catch (error) {
      console.error('Failed to clear data:', error);
      throw error;
    }
  }
}



// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
  try {
    new Application();
  } catch (error) {
    console.error('Failed to initialize application:', error);
  }
});