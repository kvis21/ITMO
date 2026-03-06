package org.utils;

public class AreaChecker {
    static public boolean checkArea(double x, double y, double r) {
        
        if (x <= 0 && y >= 0) return (x*x + y*y) <= (r*r/4);
        if (x <= 0 && y <= 0) return y >= -x - r;
        if (x >= 0 && y <= 0) return x <= r && y >= -r;
        
        return false;
    }
}
