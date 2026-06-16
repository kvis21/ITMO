package org.mbean;

import jakarta.enterprise.context.ApplicationScoped;

import javax.management.Notification;
import javax.management.NotificationBroadcasterSupport;
import org.model.Point;

import org.mbean.interfaces.PointsCounterMBean;;

@ApplicationScoped
public class PointsCounter extends NotificationBroadcasterSupport implements PointsCounterMBean {
    private long totalPoints = 0;
    private long hitPoints = 0;
    private long sequenceNumber = 1;

    @Override
    public long getTotalPoints() {
        return totalPoints;
    }

    @Override
    public long getHitPoints() {
        return hitPoints;
    }

    @Override
    public synchronized void reset() {
        this.totalPoints = 0;
        this.hitPoints = 0;
    }

    public synchronized void registerPoint(Point point) {
        totalPoints++;
        if (point.getResult() != null && point.getResult()) {
            hitPoints++;
        }

        double r = point.getR();
        if (Math.abs(point.getX()) > r || Math.abs(point.getY()) > r) {
            Notification notification = new Notification(
                "org.mbeans.point.out_of_bounds",
                "org.mbeans:type=PointsCounter",
                sequenceNumber++,
                System.currentTimeMillis(),
                String.format("Точка (%.2f, %.2f) вышла за пределы отображаемой области для R = %.2f", 
                    point.getX(), point.getY(), r)
            );
            sendNotification(notification);
        }
    }
}