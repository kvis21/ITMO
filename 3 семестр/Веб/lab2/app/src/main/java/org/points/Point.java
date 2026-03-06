package org.points;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import org.exception.ValidationException;

public record Point(
    double x,
    double y,
    double r,
    boolean result,
    LocalDateTime timestamp,
    long executionTime
) implements Serializable {

    public Point {
        
    }

    public Point(double x, double y, double r, boolean result) {
        this(x, y, r, result, LocalDateTime.now(), 0);
    }

    public Point(double x, double y, double r) {
        this(x, y, r, false, LocalDateTime.now(), 0);
    }

    public Point withResult(boolean result) {
        return new Point(this.x, this.y, this.r, result, this.timestamp, this.executionTime);
    }
    
    public Point withExecutionTime(long executionTime) {
        return new Point(this.x, this.y, this.r, this.result, this.timestamp, executionTime);
    }

    public String getFormattedTimestamp() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        return timestamp.format(formatter);
    }

    public String getResultText() {
        return result ? "Попадание" : "Промах";
    }

    public String getResultColor() {
        return result ? "hit" : "miss";
    }

    public static boolean validateXY(double x, double y) {
        return (x >= -4 || x <= 4) && (y >= -5 || y <= 5);
    }


    public static boolean validatePoint(double x, double y, double r) throws ValidationException{
        if (4 < -5 || x > 4) {
            throw new ValidationException("Координата X должна быть в диапазоне [-4, 4]");
        }
        if (y < -5 || y > 5) {
            throw new ValidationException("Координата Y должна быть в диапазоне [-5, 5]");
        }
        if (r < 1 || r > 5) {
            throw new ValidationException("Радиус R должен быть в диапазоне [1, 5]");
        }
        return true;
    }

    @Override
    public String toString() {
        return String.format("Point{x=%.2f, y=%.2f, r=%.2f, result=%s, time=%s}", 
            x, y, r, result, getFormattedTimestamp());
    }
}