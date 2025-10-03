export interface Point {
  x: number;
  y: number;
  r: number[];
}

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

export interface ApiResponse {
  results: boolean[];
  now: string;
  time: string;
  message?: string;
}

export interface TableResult {
  x: number;
  y: number;
  r: string;
  result: string;
  time: string;
  execTime: string;
}

export interface StoredPoint extends TableResult {
  id?: number;
  timestamp: number;
}

export type CoordinateX = -3 | -2 | -1 | 0 | 1 | 2 | 3 | 4 | 5;