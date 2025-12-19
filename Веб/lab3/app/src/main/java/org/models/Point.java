package org.models;

import java.util.Date;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name="points")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Point {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false, unique = true)
    private int id;
    
    @Column(name = "x", nullable = false)
    private Double x;
    
    @Column(name = "y", nullable = false)
    private Double y;

    @Column(name = "r", nullable = false)
    private Double r;
    
    @Column(name = "execution_time", nullable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date executionTime;
    
    @Column(name = "result", nullable = false)
    private boolean result;

    public Point(Double x, Double y, Double r) {
        this.x = x;
        this.y = y;
        this.r = r;
    }
}
