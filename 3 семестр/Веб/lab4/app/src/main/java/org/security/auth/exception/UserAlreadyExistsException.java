package org.security.auth.exception;

import org.security.auth.exception.base.AuthException;

import jakarta.ws.rs.core.Response;

public class UserAlreadyExistsException extends AuthException {
    public UserAlreadyExistsException(String username) {
        super("пользователь с именем '" + username + "' уже существует", Response.Status.CONFLICT);
    }
}