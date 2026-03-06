package org.security.auth.exception;

import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.ext.ExceptionMapper;
import jakarta.ws.rs.ext.Provider;

import org.security.auth.exception.base.AuthException;

@Provider
public class AuthExceptionMapper implements ExceptionMapper<AuthException> {
    @Override
    public Response toResponse(AuthException exception) {
        return exception.getResponse(); 
    }
}