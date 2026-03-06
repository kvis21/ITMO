import {CoordinateX} from './types';

export class PointValidator {
  private static readonly POSSIBLE_VALUES_X: Set<number> = new Set([-3, -2, -1, 0, 1, 2, 3, 4, 5]);
  private static readonly POSSIBLE_VALUES_R: Set<number> = new Set([1, 1.5, 2.0, 2.5, 3.0]);
  
  private x: CoordinateX | null = null;
  private y: number | null = null;
  private r: number[] = [];
  private isFormValid: boolean = false;

  constructor(private submitBtn: HTMLButtonElement) {
    this.initializeEventListeners();
    this.updateSubmitButton();
  }

  private initializeEventListeners(): void {
    const xElement = document.getElementById("x") as HTMLSelectElement;
    const yElement = document.getElementById("y") as HTMLInputElement;
    const rCheckboxes = document.getElementsByName("r") as NodeListOf<HTMLInputElement>;
    const form = document.getElementById("pointForm") as HTMLFormElement;

    xElement?.addEventListener("change", this.handleXChange.bind(this));
    yElement?.addEventListener("input", this.handleYChange.bind(this));
    
    rCheckboxes.forEach(checkbox => {
      checkbox.addEventListener("change", this.handleRChange.bind(this));
    });

    form?.addEventListener("submit", this.handleFormSubmit.bind(this));
  }

  private handleXChange(ev: Event): void {
    const target = ev.target as HTMLSelectElement;
    try {
      const xValue = parseInt(target.value);
      this.validateX(xValue);
      target.classList.remove('error');
    } catch (error) {
      this.x = null;
      target.classList.add('error');
    }
    this.validateForm();
  }

  private handleYChange(ev: Event): void {
    const target = ev.target as HTMLInputElement;
    try {
      const yValue = parseFloat(target.value);
      this.validateY(yValue);
      target.classList.remove('error');
    } catch (error) {
      this.y = null;
      target.classList.add('error');
    }
    this.validateForm();
  }

  private handleRChange(): void {
    this.r = Array.from(document.getElementsByName("r") as NodeListOf<HTMLInputElement>)
      .filter(input => input.checked)
      .map(input => parseFloat(input.value));
    
    document.querySelectorAll('.checkbox-label').forEach(label => {
      label.classList.remove('error');
    });
    
    if (this.r.length === 0) {
      document.querySelectorAll('.checkbox-label').forEach(label => {
        label.classList.add('error');
      });
    }
    
    this.validateForm();
  }

  private handleFormSubmit(ev: Event): void {
    if (!this.isFormValid) {
      ev.preventDefault();
      alert("Пожалуйста, заполните все поля корректно перед отправкой");
    }
  }

  public validateX(x: number): CoordinateX {
    if (!PointValidator.POSSIBLE_VALUES_X.has(x)) {
      throw new Error("Invalid X: X must be one of [-3, -2, -1, 0, 1, 2, 3, 4, 5]");
    }
    this.x = x as CoordinateX;
    return this.x;
  }

  public validateY(y: number): number {
    if (y < -5 || y > 3 || isNaN(y)) {
      throw new Error("Invalid Y: Y must be in range [-5, 3]");
    }
    this.y = y;
    return this.y;
  }

  private validateForm(): void {
    const isXValid = this.x !== null && PointValidator.POSSIBLE_VALUES_X.has(this.x);
    const isYValid = this.y !== null && this.y >= -5 && this.y <= 3;
    const isRValid = this.r.length > 0 && this.r.every(r => PointValidator.POSSIBLE_VALUES_R.has(r));
    
    this.isFormValid = isXValid && isYValid && isRValid;
    this.updateSubmitButton();
  }

  private updateSubmitButton(): void {
    if (this.isFormValid) {
      this.submitBtn.disabled = false;
      this.submitBtn.classList.remove('disabled');
    } else {
      this.submitBtn.disabled = true;
      this.submitBtn.classList.add('disabled');
    }
  }

  public getFormData(): { x: number; y: number; r: number[] } | null {
    if (!this.isFormValid) return null;
    
    return {
      x: this.x!,
      y: this.y!,
      r: this.r
    };
  }

  public get isValid(): boolean {
    return this.isFormValid;
  }
}