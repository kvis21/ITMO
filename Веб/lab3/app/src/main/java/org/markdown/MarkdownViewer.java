package org.markdown;

import com.vladsch.flexmark.html.HtmlRenderer;
import com.vladsch.flexmark.parser.Parser;
import com.vladsch.flexmark.util.ast.Node;
import jakarta.faces.component.FacesComponent;
import jakarta.faces.component.UIComponentBase;
import jakarta.faces.context.FacesContext;
import jakarta.faces.context.ResponseWriter;
import java.io.IOException;

@FacesComponent(createTag = true, namespace = "http://markdown.org/ui", tagName = "markdownViewer")
public class MarkdownViewer extends UIComponentBase {
    
    @Override
    public String getFamily() {
        return "org.markdown";
    }
    
    @Override
    public void encodeBegin(FacesContext context) throws IOException {
        ResponseWriter writer = context.getResponseWriter();
        
        String value = (String) getAttributes().get("value");
        String codeTheme = (String) getAttributes().get("codeTheme");
        Boolean openLinksInNewTab = (Boolean) getAttributes().get("openLinksInNewTab");
        
        if (value == null || value.trim().isEmpty()) {
            return;
        }
        
        String html = convertMarkdownToHtml(value, 
                codeTheme != null ? codeTheme : "light",
                openLinksInNewTab != null ? openLinksInNewTab : false);
        
        writer.startElement("div", this);
        writer.writeAttribute("class", "markdown-viewer " + getClientId(), null);
        
        writer.write(html);
        
        writer.endElement("div");
    }
    
    private String convertMarkdownToHtml(String markdown, String theme, boolean openInNewTab) {
        Parser parser = Parser.builder().build();
        HtmlRenderer renderer = HtmlRenderer.builder().build();
        
        Node document = parser.parse(markdown);
        String html = renderer.render(document);
        
        if (openInNewTab) {
            html = html.replace("<a href=", "<a target=\"_blank\" rel=\"noopener noreferrer\" href=");
        }
        
        if ("dark".equals(theme)) {
            html = "<div class=\"markdown-theme-dark\">" + html + "</div>";
        } else {
            html = "<div class=\"markdown-theme-light\">" + html + "</div>";
        }
        
        return html;
    }
}