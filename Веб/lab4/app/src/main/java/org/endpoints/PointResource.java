package org.endpoints;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.SecurityContext;

import org.model.Point;
import org.model.User;
import org.repository.PointRepository;
import org.repository.UserRepository;
import org.security.annotation.Secured;
import org.utils.AreaChecker;
import java.util.List;

@Path("/points")
@Secured
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class PointResource {

    @Inject
    private PointRepository pointRepository;

    @Inject
    private UserRepository userRepository;

    @GET
    public Response getUserPoints(@Context SecurityContext context) {
        String username = context.getUserPrincipal().getName();
        List<Point> points = pointRepository.findAllByUser(username);
        return Response.ok(points).build();
    }

    @POST
    public Response addPoint(Point point, @Context SecurityContext context) {
        if (point.getY() <= -3 || point.getY() >= 5) {
            return Response.status(400).entity("Y должен быть от -3 до 5").build();
        }

        String username = (String) context.getUserPrincipal().getName();
        User user = userRepository.findByUsername(username).orElseThrow();

        point.setResult(AreaChecker.checkArea(point.getX(), point.getY(), point.getR()));
        point.setUser(user);

        pointRepository.save(point);
        return Response.ok(point).build();
    }

    
}