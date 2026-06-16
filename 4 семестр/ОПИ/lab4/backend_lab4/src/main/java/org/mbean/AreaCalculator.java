package org.mbean;

import jakarta.enterprise.context.ApplicationScoped;

import org.mbean.interfaces.AreaCalculatorMBean;

@ApplicationScoped
public class AreaCalculator implements AreaCalculatorMBean {
    private double r = 1.0; 

    @Override
    public double getR() {
        return r;
    }

    @Override
    public void setR(double r) {
        this.r = r;
    }

    @Override
    public double getArea() {
        return Math.pow(r, 2) * (Math.PI / 16.0 + 0.5 + 1.0);
    }
}