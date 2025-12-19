package org.repositories;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.models.Point;

import java.util.List;

@ApplicationScoped
public class PointRepository {
    
    @PersistenceContext(unitName = "pointsPU")
    private EntityManager entityManager;
    
    @Transactional
    public void save(Point point) {
        entityManager.persist(point);
    }
  
    public List<Point> findAll() {
        return entityManager.createQuery("SELECT p FROM Point p ORDER BY p.executionTime DESC", Point.class)
                .getResultList();
    }
    
    @Transactional
    public void clearAll() {
        entityManager.createQuery("DELETE FROM Point").executeUpdate();
    }
}