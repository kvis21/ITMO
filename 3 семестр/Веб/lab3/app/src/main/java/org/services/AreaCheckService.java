package org.services;

import jakarta.enterprise.context.ApplicationScoped;
import org.models.Point;

import java.util.Date;

@ApplicationScoped
public class AreaCheckService {
    
    public boolean checkHit(Point point) {
        double x = point.getX();
        double y = point.getY();
        double r = point.getR();
        
        if (x >= 0 && y >= 0 && x <= r && y <= r) {
            return true;
        }
        
        if (x >= 0 && y <= 0 && y >= x - r/2) {
            return true;
        }
    
        if (x <= 0 && y >= 0 && (x*x + y*y) <= (r*r)) {
            return true;
        }
        
        return false;
    }
    
    public Point processPoint(double x, double y, double r) {
        Point point = new Point(x, y, r);
        boolean result = checkHit(point);
        point.setExecutionTime(new Date());
        point.setResult(result);
        return point;
    }
}