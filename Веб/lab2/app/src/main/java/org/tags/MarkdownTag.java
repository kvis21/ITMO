package org.tags;

import jakarta.servlet.jsp.JspException;
import jakarta.servlet.jsp.JspWriter;
import jakarta.servlet.jsp.tagext.BodyTagSupport;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;

public class MarkdownTag extends BodyTagSupport {
    private String orientation = "vertical";
    private String enableFeatures = "headers,bold,italic,links,lists,images";
    private String codeTheme = "light";
    private boolean openLinksInNewTab = false;
    private String id;

    public void setOrientation(String orientation) {
        this.orientation = orientation;
    }

    public void setEnableFeatures(String enableFeatures) {
        this.enableFeatures = enableFeatures;
    }

    public void setOpenLinksInNewTab(boolean openLinksInNewTab) {
        this.openLinksInNewTab = openLinksInNewTab;
    }
    public void setCodeTheme(String codeTheme) {
        this.codeTheme = codeTheme;
    }

    public void setId(String id) {
        this.id = id;
    }

    @Override
    public int doAfterBody() throws JspException {
        try {
            String bodyContent = getBodyContent().getString();
            String htmlContent = convertMarkdownToHtml(bodyContent);
            
            JspWriter out = getBodyContent().getEnclosingWriter();
            out.write(htmlContent);
            
        } catch (IOException e) {
            throw new JspException("Error processing markdown tag", e);
        }
        return SKIP_BODY;
    }

    private String convertMarkdownToHtml(String markdown) {
        if (markdown == null || markdown.trim().isEmpty()) {
            return "";
        }

        Set<String> features = parseFeatures();
        String[] lines = markdown.split("\n");
        StringBuilder html = new StringBuilder();
        
        html.append("<div class=\"markdown-content\"");
        if (id != null && !id.isEmpty()) {
            html.append(" id=\"").append(id).append("\"");
        }
        html.append(" data-orientation=\"").append(orientation).append("\"");
        
        if (codeTheme != null && !codeTheme.isEmpty()) {
            html.append(" codeTheme=\"").append(codeTheme).append("\"");
        }
        html.append(">\n");

        boolean inList = false;
        boolean inOrderedList = false;
        int listIndentLevel = 0;

        for (int i = 0; i < lines.length; i++) {
            String line = lines[i].trim();
            String processedLine = processLine(line, features);

            if (isListItem(line)) {
                int currentIndent = getIndentLevel(lines[i]);
                String listItem = processListItem(line, features);

                if (!inList || currentIndent != listIndentLevel) {
                    if (inList) {
                        html.append("</li>\n");
                        html.append(getListClosingTag(inOrderedList));
                    }
                    
                    inOrderedList = isOrderedListItem(line);
                    listIndentLevel = currentIndent;
                    html.append(getListOpeningTag(inOrderedList, currentIndent));
                    inList = true;
                } else if (i > 0 && isListItem(lines[i-1].trim())) {
                    html.append("</li>\n");
                }

                html.append("<li>").append(listItem);
                
                if (i == lines.length - 1 || !isListItem(lines[i + 1])) {
                    html.append("</li>\n");
                    html.append(getListClosingTag(inOrderedList));
                    inList = false;
                    listIndentLevel = 0;
                }
            } else {
                if (inList) {
                    html.append("</li>\n");
                    html.append(getListClosingTag(inOrderedList));
                    inList = false;
                    listIndentLevel = 0;
                }

                if (!line.isEmpty()) {
                    html.append(processedLine).append("\n");
                }
            }
        }

        html.append("</div>"); 
        return html.toString();
    }

    private String processLine(String line, Set<String> features) {
        String processed = line;

        if (features.contains("headers")) {
            processed = processHeaders(processed);
        }

        if (features.contains("bold")) {
            processed = processBold(processed);
        }

        if (features.contains("italic")) {
            processed = processItalic(processed);
        }

        if (features.contains("links")) {
            processed = processLinks(processed);
        }

        processed = processInlineCode(processed);

        return processed.isEmpty() ? "<br>" : "<p>" + processed + "</p>";
    }

    private String processHeaders(String line) {
        if (line.startsWith("### ")) {
            return "<h3>" + escapeHtml(line.substring(4)) + "</h3>";
        } else if (line.startsWith("## ")) {
            return "<h2>" + escapeHtml(line.substring(3)) + "</h2>";
        } else if (line.startsWith("# ")) {
            return "<h1>" + escapeHtml(line.substring(2)) + "</h1>";
        }
        return escapeHtml(line);
    }

    private String processBold(String line) {
        return line.replaceAll("\\*\\*(.*?)\\*\\*", "<strong>$1</strong>")
                   .replaceAll("__(.*?)__", "<strong>$1</strong>");
    }

    private String processItalic(String line) {
        return line.replaceAll("\\*(.*?)\\*", "<em>$1</em>")
                   .replaceAll("_(.*?)_", "<em>$1</em>");
    }

    private String processLinks(String line) {
        Pattern linkPattern = Pattern.compile("\\[(.*?)\\]\\((.*?)\\)");
        java.util.regex.Matcher matcher = linkPattern.matcher(line);
        
        StringBuffer result = new StringBuffer();
        while (matcher.find()) {
            String linkText = escapeHtml(matcher.group(1));
            String url = escapeHtml(matcher.group(2));
            String target = openLinksInNewTab ? " target=\"_blank\" rel=\"noopener noreferrer\"" : "";
            String replacement = "<a href=\"" + url + "\"" + target + ">" + linkText + "</a>";
            matcher.appendReplacement(result, replacement);
        }
        matcher.appendTail(result);
        
        return result.toString();
    }

    private String processInlineCode(String line) {
        String codeClass = "code-" + (codeTheme != null ? codeTheme : "light");
        return line.replaceAll("`(.*?)`", "<code class=\"" + codeClass + "\">$1</code>");
    }

    private String processListItem(String line, Set<String> features) {
        String content = line.replaceFirst("^\\s*[\\*\\-\\+]\\s+", "")
                           .replaceFirst("^\\s*\\d+\\.\\s+", "")
                           .trim();
        
        return processLine(content, features).replace("<p>", "").replace("</p>", "");
    }

    private boolean isListItem(String line) {
        return line.matches("^\\s*([\\*\\-\\+]|\\d+\\.)\\s+.*");
    }

    private boolean isOrderedListItem(String line) {
        return line.matches("^\\s*\\d+\\.\\s+.*");
    }

    private int getIndentLevel(String line) {
        int indent = 0;
        for (char c : line.toCharArray()) {
            if (c == ' ' || c == '\t') {
                indent++;
            } else {
                break;
            }
        }
        return indent / 2;
    }

    private String getListOpeningTag(boolean ordered, int indentLevel) {
        String tag = ordered ? "ol" : "ul";
        String style = indentLevel > 0 ? " style=\"margin-left: " + (indentLevel * 20) + "px\"" : "";
        return "<" + tag + style + ">\n";
    }

    private String getListClosingTag(boolean ordered) {
        return ordered ? "</ol>\n" : "</ul>\n";
    }

    private Set<String> parseFeatures() {
        Set<String> features = new HashSet<>();
        if (enableFeatures != null && !enableFeatures.isEmpty()) {
            String[] featureArray = enableFeatures.split(",");
            for (String feature : featureArray) {
                features.add(feature.trim().toLowerCase());
            }
        }
        return features;
    }

    private String escapeHtml(String text) {
        if (text == null) return "";
        return text.replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;")
                  .replace("\"", "&quot;")
                  .replace("'", "&#39;");
    }
}