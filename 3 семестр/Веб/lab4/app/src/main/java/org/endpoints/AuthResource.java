package org.endpoints;

import jakarta.ejb.EJB;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.model.User;
import org.repository.UserRepository;
import org.security.PasswordHasher;
import org.security.auth.exception.InvalidCredentialsException;
import org.security.auth.exception.UserAlreadyExistsException;
import org.security.jwt.JwtService;

import java.util.Map;

@Path("/auth")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AuthResource {

    @EJB
    private UserRepository userRepository;

    @Inject
    private PasswordHasher passwordHasher;

    @Inject
    private JwtService jwtService;

    @POST
    @Path("/register")
    public Response register(User user) {
        if (userRepository.existsByUsername(user.getUsername())) {
            throw new UserAlreadyExistsException(user.getUsername());
        }
        
        user.setPasswordHash(passwordHasher.hash(user.getPasswordHash()));
        userRepository.save(user);
        
        String token = jwtService.generateToken(user.getUsername());
        return Response.ok(Map.of("token", token, "username", user.getUsername())).build();
    }

    @POST
    @Path("/login")
    public Response login(User loginData) {
        User user = userRepository.findByUsername(loginData.getUsername())
                .orElseThrow(InvalidCredentialsException::new);

        if (!passwordHasher.check(loginData.getPasswordHash(), user.getPasswordHash())) {
            throw new InvalidCredentialsException();
        }

        String token = jwtService.generateToken(user.getUsername());
        return Response.ok(Map.of("token", token, "username", user.getUsername())).build();
    }
}