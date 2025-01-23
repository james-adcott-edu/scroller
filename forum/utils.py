import markdown
import bleach

def render_markdown(text):
    # Convert markdown to HTML
    html = markdown.markdown(text, extensions=['markdown.extensions.extra'])
    
    # Define allowed tags and attributes
    allowed_tags = [
        'p', 'br', 'strong', 'b', 'em', 'i', 'a', 'pre'
    ]
    allowed_attrs = {
        'a': ['href', 'title']
    }

    # Sanitize the HTML
    clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    
    return clean_html