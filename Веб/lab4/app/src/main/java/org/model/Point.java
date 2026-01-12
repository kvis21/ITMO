package org.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

import com.fasterxml.jackson.annotation.JsonIgnore;

@Entity
@Table(name = "points")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Point implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "point_seq")
    @SequenceGenerator(name = "point_seq", sequenceName = "POINT_ID_SEQ", allocationSize = 1)
    private Long id;

    @Column(nullable = false)
    private Double x;

    @Column(nullable = false)
    private Double y;

    @Column(nullable = false)
    private Double r;

    @Column(nullable = false)
    private Boolean result;

    @Column(name = "created_at")
    private String time;

    @PrePersist
    protected void onCreate() {
        java.time.format.DateTimeFormatter formatter = 
            java.time.format.DateTimeFormatter.ofPattern("HH:mm:ss");
        this.time = java.time.LocalDateTime.now().format(formatter);
    }

    @ManyToOne 
    @JoinColumn(name = "user_login") 
    @JsonIgnore
    private User user;
}