package org.points;

public class AreaChecker {
    
    public static boolean checkHit(Point point) {
        double x = point.x();
        double y = point.y();
        double r = point.r();

        if (x >= 0 && y >= 0 && (x * x + y * y) <= (0.5 * r) * (0.5 * r)) {
            return true;
        }

        if (x <= 0 && y <= 0 && x >= -r && y >= -r) {
            return true;
        }

        if (x >= 0 && y <= 0 && y >= -r && x <= 0.5 * r && y >= (2 * x - r)) {
            return true;
        }

        return false;
    }
}