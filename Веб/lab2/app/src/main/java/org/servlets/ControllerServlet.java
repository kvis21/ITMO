package org.servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import org.points.FormBean;

@WebServlet(name = "ControllerServlet", value = "/controller")
public class ControllerServlet extends HttpServlet {
    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        processRequest(request, response);
    }
    
    private void processRequest(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        String clear = request.getParameter("clear");
        if ("true".equals(clear)) {
            clearResults(request);
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }
        
        String xStr = request.getParameter("x");
        String yStr = request.getParameter("y");
        String[] rValues = request.getParameterValues("r");
        
        if (xStr != null && yStr != null && rValues != null) {
            saveFormState(request, xStr, yStr, rValues);
            request.getRequestDispatcher("/area-check").forward(request, response);
        } else {
            request.getRequestDispatcher("/index.jsp").forward(request, response);
        }
    }
    
    private void saveFormState(HttpServletRequest request, String xStr, String yStr, String[] rValues) {
        HttpSession session = request.getSession();
        FormBean formBean = (FormBean) session.getAttribute("formBean");
        
        if (formBean == null) {
            formBean = new FormBean();
            session.setAttribute("formBean", formBean);
        }
        
        formBean.setX(xStr);
        formBean.setY(yStr);
        formBean.setR(rValues);
        
        System.out.println("Saved form state to bean - X: " + xStr + ", Y: " + yStr);
    }
    
    private void clearResults(HttpServletRequest request) {
        HttpSession session = request.getSession();
        
        FormBean formBean = (FormBean) session.getAttribute("formBean");
        if (formBean != null) {
            formBean.clear();
        }
        
        session.removeAttribute("results");
        session.removeAttribute("currentPoints");
        session.removeAttribute("listPoints");
        session.removeAttribute("currentX");
        session.removeAttribute("currentY");
    }
}