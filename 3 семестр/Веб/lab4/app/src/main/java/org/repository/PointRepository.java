package org.repository;

import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import org.model.Point;

import java.util.List;

@Stateless
public class PointRepository {

    @PersistenceContext(unitName = "pointsPU")
    private EntityManager em;


    public void save(Point point) {
        em.persist(point);
    }

    public List<Point> findAllByUser(String username) {
        return em.createQuery("SELECT p FROM Point p WHERE p.user.username = :username ORDER BY p.id DESC", Point.class)
                .setParameter("username", username)
                .getResultList();
    }

    public void deleteByUser(String username) {
        em.createQuery("DELETE FROM Point p WHERE p.user.username = :username")
                .setParameter("username", username)
                .executeUpdate();
    }
}