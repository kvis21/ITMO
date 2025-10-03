package org;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import com.fastcgi.FCGIInterface;

public class FastCGIApp {
    public static void main(String[] args) {
        FCGIInterface fcgi = new FCGIInterface();
                
        while (fcgi.FCGIaccept() >= 0) {
            try {
                String queryParams = System.getProperties().getProperty("QUERY_STRING");
                Params params = new Params(queryParams);

                validateParams(params);
                
                Instant startTime = Instant.now();
                List<Boolean> result = calculate(params.getX(), params.getY(), params.getListR());
                Instant endTime = Instant.now();

                String resultJson = String.format(Responses.RESULT_JSON.getResponse(), String.valueOf(ChronoUnit.NANOS.between(startTime, endTime)), LocalDateTime.now(), result);
                String resultHTTP = String.format(Responses.RESULT_HTTP.getResponse(), resultJson.getBytes().length, resultJson);
                System.out.println(resultHTTP);
            } catch (Exception e) {
                String errorJson = String.format(Responses.ERROR_JSON.getResponse(), LocalDateTime.now(), e.getMessage());
                String errorHTTP = String.format(Responses.ERROR_HTTP.getResponse(), errorJson.getBytes().length, errorJson);
                System.out.println(errorHTTP);
            }
        }
    }

    private static void validateParams(Params params) throws ValidateException {
        if (!Set.of(-3f, -2f, -1f, 0f, 1f, 2f, 3f, 4f, 5f).contains(params.getX())) {
            throw new ValidateException("X must be one of: [-3, -2, -1, 0, 1, 2, 3, 4, 5]");
        }
  
        if (params.getY() < -5 || params.getY() > 3) {
            throw new ValidateException("Y must be between -5 and 3");
        }
   
        if (params.getListR().isEmpty()) {
            throw new ValidateException("ListR must not be empty");
        }
        
        Set<Float> validRValues = Set.of(1.0f, 1.5f, 2.0f, 2.5f, 3.0f);
        for (Float r : params.getListR()) {
            if (!validRValues.contains(r)) {
                throw new ValidateException("R must be one of: [1, 1.5, 2, 2.5, 3]");
            }
        }
    }

    private static List<Boolean> calculate(float x, float y, List<Float> listR) {
        List<Boolean> results = new ArrayList<>();
        for (Float r : listR) {
            boolean pointResult = checkPointInArea(x, y, r);
            results.add(pointResult);
        }
        return results;
    }

    private static boolean checkPointInArea(float x, float y, float r) {
     
        boolean inRectangle = (x >= -r && x <= 0) && (y >= 0 && y <= r/2);
   
        boolean inCircle = (x >= 0 && y <= 0) && (x*x + y*y <= r*r);
        
        boolean inTriangle = (x <= 0 && y <= 0) && (y >= -x - r/2) && (x >= -r/2) && (y >= -r/2);
        
        return inRectangle || inCircle || inTriangle;
    }
}