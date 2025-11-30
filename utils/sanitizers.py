"""Input sanitization for XSS prevention."""
import re
from html import escape


def sanitize_html(html):
    """Basic HTML sanitization - escapes HTML entities."""
    if not html:
        return ''
    return escape(html)


def sanitize_markdown(markdown):
    """Basic markdown sanitization."""
    if not markdown:
        return ''
    # Remove script tags and dangerous HTML
    markdown = re.sub(r'<script[^>]*>.*?</script>', '', markdown, flags=re.IGNORECASE | re.DOTALL)
    markdown = re.sub(r'javascript:', '', markdown, flags=re.IGNORECASE)
    return markdown


def clean_text(text):
    """Clean and sanitize text input."""
    if not text:
        return ''
    # Remove null bytes and control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return text.strip()


