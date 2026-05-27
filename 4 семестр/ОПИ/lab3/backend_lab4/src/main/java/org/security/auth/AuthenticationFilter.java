package org.security.auth;

import jakarta.annotation.Priority;
import jakarta.inject.Inject;
import jakarta.ws.rs.Priorities;
import jakarta.ws.rs.container.ContainerRequestContext;
import jakarta.ws.rs.container.ContainerRequestFilter;
import jakarta.ws.rs.core.HttpHeaders;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.ext.Provider;
import java.io.IOException;
import org.security.jwt.JwtService;
import org.security.annotation.Secured;

@Secured
@Provider
@Priority(Priorities.AUTHENTICATION)
public class AuthenticationFilter implements ContainerRequestFilter {

    @Inject
    private JwtService jwtService;

    @Override
    public void filter(ContainerRequestContext requestContext) throws IOException {
        String authHeader = requestContext.getHeaderString(HttpHeaders.AUTHORIZATION);

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            requestContext.abortWith(Response.status(Response.Status.UNAUTHORIZED).build());
            return;
        }

        String token = authHeader.substring("Bearer ".length()).trim();
        String username = jwtService.validateTokenAndGetUsername(token);

        if (username == null) {
            requestContext.abortWith(Response.status(Response.Status.UNAUTHORIZED).build());
        } else {
            final String finalUsername = username;
            requestContext.setSecurityContext(new jakarta.ws.rs.core.SecurityContext() {
                @Override
                public java.security.Principal getUserPrincipal() {
                    return () -> finalUsername;
                }
                @Override public boolean isUserInRole(String role) { return true; }
                @Override public boolean isSecure() { return false; }
                @Override public String getAuthenticationScheme() { return "Bearer"; }
            });
        }
    }
}