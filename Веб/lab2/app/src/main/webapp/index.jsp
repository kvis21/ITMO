<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List" %>
<%@ page import="org.points.Point" %>
<jsp:useBean id="formBean" class="org.points.FormBean" scope="session"/>
<jsp:setProperty name="formBean" property="*"/>

<%
    String currentX = formBean.getX();
    String currentY = formBean.getY();
    String[] currentR = formBean.getR();
%>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Лаба №1</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/main.css">
</head>
<body>
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

    <main>
        <section class="input-graph-section">
            <h2>Проверка попадания точки в область</h2>
            <div class="input-graph-container">
                <div class="form-container">
                    <form id="pointForm" class="point-form" action="controller" method="POST">
                        <table class="form-table">
                            <tr>
                                <td><label for="x">Координата X:</label></td>
                                <td>
                                    <div class="button-group" id="xButtons">
                                        <%
                                            String[] xValues = {"-4", "-3", "-2", "-1", "0", "1", "2", "3", "4"};
                                            for (String xVal : xValues) {
                                                String activeClass = xVal.equals(currentX) ? "active" : "";
                                        %>
                                        <button type="button" class="x-btn <%= activeClass %>" value="<%= xVal %>">
                                            <%= xVal %>
                                        </button>
                                        <% } %>
                                    </div>
                                    <input type="hidden" id="x" name="x" value="<%= currentX != null ? currentX : "" %>" required>
                                    <div id="xError" class="error-message"></div>
                                </td>
                            </tr>
                            <tr>
                                <td><label for="y">Координата Y:</label></td>
                                <td>
                                    <input type="text" id="y" name="y" 
                                        placeholder="Введите Y (-5 до 5)" 
                                        value="<%= currentY != null ? currentY : "" %>"
                                        required class="form-input">
                                    <div id="yError" class="error-message"></div>
                                </td>
                            </tr>
                            <tr>
                                <td><label>Радиус R:</label></td>
                                <td>
                                    <div class="checkbox-group">
                                        <%
                                            String[] rValues = {"1", "2", "3", "4", "5"};
                                            for (String rVal : rValues) {
                                                boolean isChecked = false;
                                                if (currentR != null) {
                                                    for (String selectedR : currentR) {
                                                        if (rVal.equals(selectedR)) {
                                                            isChecked = true;
                                                            break;
                                                        }
                                                    }
                                                }
                                        %>
                                        <label class="checkbox-label <%= isChecked ? "selected" : "" %>">
                                            <input type="checkbox" name="r" value="<%= rVal %>" 
                                                class="r-checkbox" <%= isChecked ? "checked" : "" %>> 
                                            <%= rVal %>
                                        </label>
                                        <% } %>
                                    </div>
                                    <div id="rError" class="error-message"></div>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2" class="form-buttons">
                                    <button type="submit" class="submit-btn">Проверить</button>
                                    <button type="button" class="clear-btn">Очистить результаты</button>
                                </td>
                            </tr>
                        </table>
                    </form>
                </div>
                
                <div class="graph-container">
                    <canvas id="graphCanvas"></canvas>
                    <div id="graphError" class="error-message"></div>
                    <div id="clickInfo" class="click-info"></div>
                </div>
            </div>
        </section>

        <section class="results-section">
            <h2>Результаты проверок</h2>
            <div class="table-container">
                <table class="results-table">
                    <thead>
                        <tr class="column-name">
                            <th>X</th>
                            <th>Y</th>
                            <th>R</th>
                            <th>Результат</th>
                            <th>Время запроса</th>
                            <th>Время работы (мкс)</th>
                        </tr>
                    </thead>
                    <tbody id="resultsBody">
                        <%
                            List<Point> results = (List<Point>) session.getAttribute("results");
                            if (results != null && !results.isEmpty()) {
                                for (Point point : results) {
                        %>
                                <tr class="<%= point.getResultColor() %>">
                                    <td><%= point.x() %></td>
                                    <td><%= point.y() %></td>
                                    <td><%= point.r() %></td>
                                    <td><%= point.getResultText() %></td>
                                    <td><%= point.getFormattedTimestamp() %></td>
                                    <td><%= point.executionTime() %></td>
                                </tr>
                        <%
                                }
                            } else {
                        %>
                            <tr>
                                <td colspan="6" class="no-results">Нет результатов проверок</td>
                            </tr>
                        <%
                            }
                        %>
                    </tbody>
                </table>
            </div>
        </section>
    </main>

    <script src="${pageContext.request.contextPath}/js/main.js"></script>
    <script src="${pageContext.request.contextPath}/js/validation.js"></script>
    <script src="${pageContext.request.contextPath}/js/graph.js"></script>
</body>
</html>