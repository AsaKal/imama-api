package com.yourpackage.app;

public class Message {
    public static final int TYPE_BOT = 0;
    public static final int TYPE_USER = 1;

    private final String text;
    private final String time;
    private final int type;

    public Message(String text, String time, int type) {
        this.text = text;
        this.time = time;
        this.type = type;
    }

    public String getText() {
        return text;
    }

    public String getTime() {
        return time;
    }

    public int getType() {
        return type;
    }
}
