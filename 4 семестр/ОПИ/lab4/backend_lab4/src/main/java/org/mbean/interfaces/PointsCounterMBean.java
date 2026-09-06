package org.mbean.interfaces;

public interface PointsCounterMBean {
    long getTotalPoints();
    long getHitPoints();
    void reset();
}