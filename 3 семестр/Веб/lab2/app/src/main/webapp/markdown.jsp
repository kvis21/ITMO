<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="content" uri="http://JSPApp.com/content-tags" %>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/markdown.css">
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/main.css">
</head>
<body>
    <div class="container">
        
        
        <content:markdown id="article" enableFeatures="headers,bold,italic,links,lists" codeTheme="light">
            # Заголовок статьи

            Это **жирный текст** и *курсив*.

            ## Список возможностей:
            - Поддержка списков
            - Поддержка `inline кода`
            - Поддержка [ссылок](https://example.com)

            ### Вложенный список:
            1. Первый пункт
            2. Второй пункт
            - Подпункт A
            - Подпункт B
        </content:markdown>

    </div>
</body>
</html>