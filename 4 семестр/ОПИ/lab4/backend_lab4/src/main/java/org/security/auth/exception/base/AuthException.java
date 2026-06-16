package org.security.auth.exception.base;

import org.security.auth.exception.utils.ErrorMessage;

import jakarta.ws.rs.WebApplicationException;
import jakarta.ws.rs.core.Response;

public class AuthException extends WebApplicationException {
    public AuthException(String message, Response.Status status) {
        super(Response.status(status)
                .entity(new ErrorMessage(message))
                .build());
    }
}