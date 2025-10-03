package org;

public class ValidateException extends Exception{
    String message = "";
    ValidateException(){}
    ValidateException(String msg){
        message = msg;
    }

    @Override
    public String getMessage() {
        return message;
    }
}
