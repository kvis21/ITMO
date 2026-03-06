package org.markdown;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import lombok.Getter;
import lombok.Setter;

@Named
@SessionScoped
public class MarkdownBean implements Serializable {
    @Getter @Setter
    private String orientation = "vertical";

    @Getter @Setter
    private String codeTheme = "light";

    @Getter @Setter
    private boolean openLinksInNewTab = false;

    @Getter @Setter
    private String content;

    @Getter @Setter
    private String lastUpdateTime;

    @Setter
    private int contentLength = 0;

    public MarkdownBean() {
        restoreExample();
    }
    
    public void updatePreview() {
        this.lastUpdateTime = LocalDateTime.now()
            .format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        this.contentLength = (content != null) ? content.length() : 0;
        
        System.out.println("Preview updated at: " + lastUpdateTime);
        System.out.println("Content length: " + contentLength);
    }
    
    public void clearContent() {
        this.content = "";
        updatePreview();
    }
    
    public void restoreExample() {
        this.content = "# Заголовок статьи\n\n" +
                      "Это **жирный текст** и *курсив*.\n\n" +
                      "## Список возможностей:\n" +
                      "- Поддержка списков\n" +
                      "- Поддержка `inline кода`\n" +
                      "- Поддержка [ссылок](https://example.com)\n\n" +
                      "### Вложенный список:\n" +
                      "1. Первый пункт\n" +
                      "2. Второй пункт\n" +
                      "   - Подпункт A\n" +
                      "   - Подпункт B\n\n" +
                      "```java\n" +
                      "// Пример кода\n" +
                      "public class HelloWorld {\n" +
                      "    public static void main(String[] args) {\n" +
                      "        System.out.println(\"Hello Markdown!\");\n" +
                      "    }\n" +
                      "}\n" +
                      "```\n\n" +
                      "> Это блок цитаты\n" +
                      "> который поддерживается в markdown\n\n";
        updatePreview();
    }

    public int getContentLength() {
        return (content != null) ? content.length() : 0;
    }
}