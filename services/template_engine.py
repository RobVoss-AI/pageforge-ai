"""
Jinja2 template rendering engine for landing pages.
Loads HTML templates and renders them with AI-generated content and theme CSS.
"""

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from services.themes import get_theme_css
from services.ai_content import ContentResponse


class TemplateEngine:
    """Render landing page templates with content and themes."""

    def __init__(self, template_dir: Path):
        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
        )

    def render(
        self,
        page_type: str,
        content: ContentResponse,
        business_name: str,
        theme_slug: str = "tech-innovation",
        event_date: str = "",
        event_time: str = "",
        event_location: str = "",
    ) -> str:
        """Render a landing page template with content and theme."""
        template_file = f"{page_type}.html"
        template = self.env.get_template(template_file)

        theme_css = get_theme_css(theme_slug)

        context = {
            # Theme
            "theme_css": theme_css,
            # Content
            "headline": content.headline,
            "subheadline": content.subheadline,
            "cta_text": content.cta_text,
            "cta_subtext": content.cta_subtext,
            "page_title": content.page_title,
            "meta_description": content.meta_description,
            "body_sections": content.body_sections,
            "features": content.features,
            "testimonial_placeholder": content.testimonial_placeholder,
            # Meta
            "business_name": business_name,
            "year": datetime.now().year,
            # Event fields
            "event_date": event_date,
            "event_time": event_time,
            "event_location": event_location,
        }

        return template.render(**context)

    def list_templates(self) -> list[str]:
        """List available template slugs."""
        return [
            p.stem
            for p in self.template_dir.glob("*.html")
            if p.is_file()
        ]
