package org;

public enum Responses {
        RESULT_HTTP("""
        HTTP/1.1 200 OK\r
        Content-Type: application/json\r
        Content-Length: %d\r\n
        %s\r
        """),

        ERROR_HTTP("""
        HTTP/1.1 400 Bad Request\r
        Content-Type: application/json\r
        Content-Length: %d\r\n
        %s\r
        """),

        RESULT_JSON("""
        {
            "time":"%s",
            "now":"%s",
            "results":%s
        }
        """),
        
        ERROR_JSON("""
        {
            "now":"%s",
            "message": "%s"
        }
        """);

    String response;

    Responses(String response) {
        this.response = response;
    }

    public String getResponse() {
    return response;
    }
}
