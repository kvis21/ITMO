package org.beans;

import jakarta.enterprise.context.SessionScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import lombok.Getter;
import lombok.Setter;

import org.models.Point;
import org.repositories.PointRepository;
import org.services.AreaCheckService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

@Named
@SessionScoped
public class PointBean implements Serializable {
    @Setter @Getter
    private Double x = 0.0;

    @Setter @Getter
    private Double y = 0.0;

    @Setter @Getter
    private Double r = 3.0;

    
    @Inject
    private PointRepository pointRepository;
    
    @Inject
    private AreaCheckService areaCheckService;
    
    public void addPoint() {
        Point point = areaCheckService.processPoint(x, y, r);
        pointRepository.save(point);
    }
    
    public void addPointFromGraph() {
        FacesContext context = FacesContext.getCurrentInstance();
        Map<String, String> params = context.getExternalContext().getRequestParameterMap();
        
        String xStr = params.get("x");
        String yStr = params.get("y");
        
        if (xStr != null && yStr != null) {
            try {
                double graphX = Double.parseDouble(xStr);
                double graphY = Double.parseDouble(yStr);
                
                Point point = areaCheckService.processPoint(graphX, graphY, r);
                pointRepository.save(point);
                
            } catch (NumberFormatException e) {
                FacesContext.getCurrentInstance().addMessage(null, 
                    new FacesMessage(FacesMessage.SEVERITY_ERROR, "Ошибка", "Неверные координаты"));
            }
        }
    }

    public List<Point> getPoints() {
        return pointRepository.findAll();
    }

    public String getPointsJson() {
        try {
            ObjectMapper mapper = new ObjectMapper();
            mapper.enable(SerializationFeature.INDENT_OUTPUT); 
            return mapper.writeValueAsString(getPoints());
        } catch (Exception e) {
            e.printStackTrace();
            return "[]";
        }
    }
    public void setPointsJson(String pointsJson) {
    }
    
    public void clearPoints() {
        pointRepository.clearAll();
    }
}