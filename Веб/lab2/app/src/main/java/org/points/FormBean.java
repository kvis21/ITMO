package org.points;

import java.io.Serializable;

public class FormBean implements Serializable {
    private String x;
    private String y;
    private String[] r;

    public FormBean() {
    }

    public String getX() {
        return x;
    }

    public void setX(String x) {
        this.x = x;
    }

    public String getY() {
        return y;
    }

    public void setY(String y) {
        this.y = y;
    }

    public String[] getR() {
        return r;
    }

    public void setR(String[] r) {
        this.r = r;
    }

    public void clear() {
        this.x = null;
        this.y = null;
        this.r = null;
    }
}