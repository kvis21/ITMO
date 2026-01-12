package org.security.auth.exception;

import org.security.auth.exception.base.AuthException;

import jakarta.ws.rs.core.Response;

public class InvalidCredentialsException extends AuthException {
    public InvalidCredentialsException() {
        super("неверный логин или пароль", Response.Status.UNAUTHORIZED);
    }
}