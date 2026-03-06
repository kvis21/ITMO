package org.servlets;

import org.points.Point;
import org.points.ListPoints;
import org.exception.ValidationException;
import org.points.AreaChecker;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@WebServlet(name = "AreaCheckServlet", value = "/area-check")
public class AreaCheckServlet extends HttpServlet {
    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        long startTime = System.nanoTime();
        
        try {
            String xStr = request.getParameter("x");
            String yStr = request.getParameter("y");
            String[] rValues = request.getParameterValues("r");
            
            if (rValues == null || rValues.length == 0) {
                request.setAttribute("error", "Не выбран радиус R");
                request.getRequestDispatcher("/index.jsp").forward(request, response);
                return;
            }

            double x = Double.parseDouble(xStr);
            double y = Double.parseDouble(yStr);

            HttpSession session = request.getSession();

            session.setAttribute("currentX", xStr);
            session.setAttribute("currentY", yStr);

            ListPoints listPoints = (ListPoints) session.getAttribute("listPoints");
            if (listPoints == null) {
                listPoints = new ListPoints();
                session.setAttribute("listPoints", listPoints);
            }

            List<Point> currentPoints = new ArrayList<>();
            List<String> validationErrors = new ArrayList<>();
            
            for (String rValue : rValues) {
                try {
                    double r = Double.parseDouble(rValue);
                    Point.validatePoint(x, y, r);
                    
                    Point point = new Point(x, y, r);
                    boolean result = AreaChecker.checkHit(point);
                    
                    Point resultPoint = point.withResult(result)
                                        .withExecutionTime((System.nanoTime() - startTime) / 1000);
                    
                    listPoints.addPoint(resultPoint);
                    currentPoints.add(resultPoint);
                    
                } catch (ValidationException e) {
                    if (e.getMessage().contains("R")) {
                        validationErrors.add("радиус " + rValue + " пропущен - " + e.getMessage());
                    } else {
                        request.setAttribute("error", e.getMessage());
                        request.getRequestDispatcher("/index.jsp").forward(request, response);
                        return;
                    }
                }
            }

            session.setAttribute("warnings", validationErrors);
            session.setAttribute("currentPoints", currentPoints);
            session.setAttribute("results", listPoints.getListPoints());
            
            response.sendRedirect(request.getContextPath() + "/result.jsp");
            
        } catch (NumberFormatException e) {
            request.setAttribute("error", "Ошибка преобразования чисел: " + e.getMessage());
            request.getRequestDispatcher("/index.jsp").forward(request, response);
        } catch (Exception e) {
            request.setAttribute("error", "Внутренняя ошибка сервера: " + e.getMessage());
            request.getRequestDispatcher("/index.jsp").forward(request, response);
        }
    }
}