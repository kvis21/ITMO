package org.security.cors;

import jakarta.ws.rs.container.ContainerRequestContext;
import jakarta.ws.rs.container.ContainerResponseContext;
import jakarta.ws.rs.container.ContainerResponseFilter;
import jakarta.ws.rs.ext.Provider;
import java.io.IOException;

@Provider
public class CorsFilter implements ContainerResponseFilter {

    @Override
    public void filter(ContainerRequestContext requestContext, 
                       ContainerResponseContext responseContext) throws IOException {
        
        // Разрешаем запросы с http://localhost:5173 
        responseContext.getHeaders().add("Access-Control-Allow-Origin", "*");
        
        // Разрешаем заголовки 
        responseContext.getHeaders().add("Access-Control-Allow-Headers", 
                "origin, content-type, accept, authorization");
        
        // Разрешаем методы
        responseContext.getHeaders().add("Access-Control-Allow-Methods", 
                "GET, POST, PUT, DELETE, OPTIONS, HEAD");
        
        // Позволяем браузеру кэшировать настройки CORS
        //responseContext.getHeaders().add("Access-Control-Max-Age", "1209600");
    }
}