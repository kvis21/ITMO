package org.points;

import java.io.Serializable;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.stream.Collectors;

public class ListPoints implements Serializable {
    private List<Point> listPoints = new CopyOnWriteArrayList<>();

    public ListPoints() {
    }

    public List<Point> getListPoints() {
        return listPoints; 
    }

    public void addPoint(Point point) {
        listPoints.add(0, point); 
    }

    public void addAllPoints(List<Point> points) {
        listPoints.addAll(0, points); 
    }

    public boolean isEmpty() {
        return listPoints.isEmpty();
    }
    
    public int size() {
        return listPoints.size();
    }

    public void clear() {
        listPoints.clear();
    }

    public List<Point> getRecentPoints(int count) {
        return listPoints.stream()
                .limit(count)
                .collect(Collectors.toList());
    }

    public long getHitCount() {
        return listPoints.stream()
                .filter(Point::result)
                .count();
    }

    public long getMissCount() {
        return listPoints.size() - getHitCount();
    }

    public Point getLastPoint() {
        return listPoints.isEmpty() ? null : listPoints.get(0);
    }

    public List<Point> getPointsByRadius(double radius) {
        return listPoints.stream()
                .filter(point -> point.r() == radius)
                .collect(Collectors.toList());
    }

    @Override
    public String toString() {
        return "ListPoints{size=" + listPoints.size() + "}";
    }
}