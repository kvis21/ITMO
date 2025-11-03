<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="org.points.Point" %>
<%@ page import="java.util.List" %>
<%@ page import="java.util.Map" %>
<%
    String currentX = (String) session.getAttribute("currentX");
    String currentY = (String) session.getAttribute("currentY");
    
    if (currentX == null) {
        Map<String, Object> formState = (Map<String, Object>) session.getAttribute("formState");
        if (formState != null) {
            currentX = (String) formState.get("x");
            currentY = (String) formState.get("y");
        }
    }
    
    List<Point> currentPoints = (List<Point>) session.getAttribute("currentPoints");
%>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Результат проверки - Лаба №1</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/result.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <table class="header-table">
                <tr class="header-fio">
                    <td>ФИО: </td>
                    <td>Панченко Антон Дмитриевич</td>
                </tr> 
                <tr class="header-group">
                    <td>Группа:</td>
                    <td>P3115</td>
                </tr> 
                <tr class="header-var">
                    <td>Вариант: </td>
                    <td>№467018</td>      
                </tr> 
            </table>
        </header>

        <main class="result-content">
            <% if (currentPoints != null && !currentPoints.isEmpty()) { %>
                <div class="multi-results">
                    <div class="result-summary">
                        <h2>Результаты проверки</h2>
                        <% if (currentX != null && currentY != null) { %>
                            <p>Использованы значения: <strong>X=<%= currentX %>, Y=<%= currentY %></strong></p>
                        <% } else { %>
                            <p>Использованы значения: <strong>X=неизвестно, Y=неизвестно</strong></p>
                        <% } %>
                        <%
                            long hitCount = currentPoints.stream().filter(Point::result).count();
                        %>
                        <p>Попаданий: <strong><%= hitCount %></strong> из <strong><%= currentPoints.size() %></strong></p>
                    </div>

                    <div class="radius-results">
                        <% for (Point point : currentPoints) { %>
                            <div class="radius-card <%= point.result() ? "hit" : "miss" %>">
                                <div class="radius-value">Радиус R = <%= point.r() %></div>
                                <div class="result-details">
                                    <span class="result-badge <%= point.getResultColor() %>">
                                        <%= point.getResultText().toUpperCase() %>
                                    </span>
                                    <div>Время выполнения: <%= point.executionTime() %> мкс</div>
                                </div>
                            </div>
                        <% } %>
                    </div>
                </div>
            <% } else { %>
                <div class="error-message">
                    <h2>Ошибка</h2>
                    <p>Данные точки недоступны.</p>
                </div>
            <% } %>

            <div class="navigation-actions">
                    <form method="POST" action="controller" id="backForm">
                        <button type="submit" class="btn btn-primary">Вернуться к форме</button>
                    </form>
            </div>

            <section class="recent-results">
                <h3>Последние проверки</h3>
                <div class="table-container">
                    <table class="results-table">
                        <thead>
                            <tr class="column-name">
                                <th>X</th>
                                <th>Y</th>
                                <th>R</th>
                                <th>Результат</th>
                                <th>Время выполнения</th>
                                <th>Время запроса</th>
                            </tr>
                        </thead>
                        <tbody>
                            <%
                                List<Point> allResults = (List<Point>) session.getAttribute("results");
                                if (allResults != null && !allResults.isEmpty()) {
                                    int count = Math.min(allResults.size(), 5);
                                    for (int i = 0; i < count; i++) {
                                        Point point = allResults.get(i);
                            %>
                                <tr class="<%= point.getResultColor() %>">
                                    <td><%= point.x() %></td>
                                    <td><%= point.y() %></td>
                                    <td><%= point.r() %></td>
                                    <td><%= point.getResultText() %></td>
                                    <td><%= point.executionTime() %> мкс</td>
                                    <td><%= point.getFormattedTimestamp() %></td>
                                </tr>
                            <%
                                    }
                                } else {
                            %>
                                <tr>
                                    <td colspan="6" class="no-results">Нет результатов</td>
                                </tr>
                            <%
                                }
                            %>
                        </tbody>
                    </table>
                </div>
            </section>
        </main>
    </div>
    <script src="${pageContext.request.contextPath}/js/validation.js"></script>
</body>
</html>