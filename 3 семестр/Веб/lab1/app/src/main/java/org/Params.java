package org;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.List;

public class Params {
    float x, y;
    List<Float> listR;
    
    public Params(String query){
        if (query != null) {
            Map<String, String> params = splitQuery(query);
            x = Float.parseFloat(params.get("x"));
            y = Float.parseFloat(params.get("y"));
            listR = parseListQueryParams(params.get("listR"));
        }
    }


    private static Map<String, String> splitQuery(String query) {
        return Arrays.stream(query.split("&"))
            .map(pair -> pair.split("="))
            .collect(
                Collectors.toMap(
                    pairParts -> URLDecoder.decode(pairParts[0], StandardCharsets.UTF_8),
                    pairParts -> URLDecoder.decode(pairParts[1], StandardCharsets.UTF_8),
                    (a, b) -> b,
                    HashMap::new
                )
            );
    }

    private static List<Float> parseListQueryParams(String listParams) {
        return Arrays.stream(listParams.split(","))
            .map(Float::parseFloat)
            .collect(Collectors.toList());
    }

    public float getX() {return x;}
    public float getY() {return y;}
    public List<Float> getListR() {return listR;}
}
