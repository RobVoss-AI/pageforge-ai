"""
Visual theme definitions for PageForge AI landing pages.
Each theme provides CSS custom properties for colors, typography, and styling.
"""

from dataclasses import dataclass


@dataclass
class Theme:
    slug: str
    name: str
    description: str
    best_for: str
    font_heading: str
    font_body: str
    primary: str
    primary_dark: str
    accent: str
    accent_hover: str
    text_dark: str
    text_light: str
    text_muted: str
    surface: str
    border: str
    hero_gradient: str = ""

    def to_css(self) -> str:
        """Generate a <style> block with CSS custom properties for this theme."""
        gradient = self.hero_gradient or self.primary
        return f"""<style>
  :root {{
    --font-heading: {self.font_heading};
    --font-body: {self.font_body};
    --theme-primary: {self.primary};
    --theme-primary-dark: {self.primary_dark};
    --theme-accent: {self.accent};
    --theme-accent-hover: {self.accent_hover};
    --theme-text-dark: {self.text_dark};
    --theme-text-light: {self.text_light};
    --theme-text-muted: {self.text_muted};
    --theme-surface: {self.surface};
    --theme-border: {self.border};
    --theme-hero-gradient: {gradient};
  }}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Merriweather:wght@400;700&family=Outfit:wght@400;500;600;700;800&family=Lora:wght@400;500;600;700&family=Sora:wght@400;500;600;700;800&family=Crimson+Pro:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">"""


THEMES: dict[str, Theme] = {
    "tech-innovation": Theme(
        slug="tech-innovation",
        name="Tech Innovation",
        description="Bold, modern, high-contrast with electric accents",
        best_for="SaaS, startups, AI/ML, digital transformation",
        font_heading="'Space Grotesk', sans-serif",
        font_body="'Inter', sans-serif",
        primary="#0a0f1e",
        primary_dark="#060a14",
        accent="#6366f1",
        accent_hover="#4f46e5",
        text_dark="#0f172a",
        text_light="#f8fafc",
        text_muted="#64748b",
        surface="#f1f5f9",
        border="#e2e8f0",
        hero_gradient="linear-gradient(135deg, #0a0f1e 0%, #1e1b4b 50%, #0a0f1e 100%)",
    ),
    "ocean-depths": Theme(
        slug="ocean-depths",
        name="Ocean Depths",
        description="Professional maritime blues with calm authority",
        best_for="Finance, consulting, corporate, professional services",
        font_heading="'Plus Jakarta Sans', sans-serif",
        font_body="'DM Sans', sans-serif",
        primary="#0c2d48",
        primary_dark="#091f33",
        accent="#2196f3",
        accent_hover="#1976d2",
        text_dark="#0d1b2a",
        text_light="#f0f4f8",
        text_muted="#5a7184",
        surface="#eef4f9",
        border="#d0dce7",
        hero_gradient="linear-gradient(160deg, #0c2d48 0%, #145374 60%, #0c2d48 100%)",
    ),
    "midnight-galaxy": Theme(
        slug="midnight-galaxy",
        name="Midnight Galaxy",
        description="Dramatic cosmic purples with stellar energy",
        best_for="Entertainment, gaming, luxury brands, creative agencies",
        font_heading="'Sora', sans-serif",
        font_body="'Inter', sans-serif",
        primary="#13052e",
        primary_dark="#0a0219",
        accent="#a855f7",
        accent_hover="#9333ea",
        text_dark="#1a0536",
        text_light="#f5f0ff",
        text_muted="#8b7aa0",
        surface="#f3eef8",
        border="#ddd4e8",
        hero_gradient="linear-gradient(135deg, #13052e 0%, #2d1657 40%, #13052e 100%)",
    ),
    "sunset-boulevard": Theme(
        slug="sunset-boulevard",
        name="Sunset Boulevard",
        description="Warm, vibrant sunset tones with creative energy",
        best_for="Marketing, events, lifestyle brands, creative pitches",
        font_heading="'Outfit', sans-serif",
        font_body="'DM Sans', sans-serif",
        primary="#1a0a00",
        primary_dark="#0f0600",
        accent="#f97316",
        accent_hover="#ea580c",
        text_dark="#1c1210",
        text_light="#fff7ed",
        text_muted="#92643e",
        surface="#fef3e2",
        border="#fbd5a0",
        hero_gradient="linear-gradient(135deg, #7c2d12 0%, #c2410c 50%, #9a3412 100%)",
    ),
    "forest-canopy": Theme(
        slug="forest-canopy",
        name="Forest Canopy",
        description="Natural earth tones with grounded warmth",
        best_for="Sustainability, wellness, education, outdoor brands",
        font_heading="'Merriweather', serif",
        font_body="'DM Sans', sans-serif",
        primary="#1a2e1a",
        primary_dark="#0f1c0f",
        accent="#22c55e",
        accent_hover="#16a34a",
        text_dark="#14291a",
        text_light="#f0fdf4",
        text_muted="#5c7c5c",
        surface="#ecfdf0",
        border="#c6e7c6",
        hero_gradient="linear-gradient(135deg, #1a2e1a 0%, #2d5a2d 50%, #1a2e1a 100%)",
    ),
    "golden-hour": Theme(
        slug="golden-hour",
        name="Golden Hour",
        description="Rich autumnal warmth with luxurious depth",
        best_for="Hospitality, restaurants, artisan products, fall campaigns",
        font_heading="'Playfair Display', serif",
        font_body="'Lora', serif",
        primary="#2c1810",
        primary_dark="#1a0e09",
        accent="#d97706",
        accent_hover="#b45309",
        text_dark="#27190e",
        text_light="#fef9f0",
        text_muted="#8c6d4f",
        surface="#fdf6e3",
        border="#e8d5b5",
        hero_gradient="linear-gradient(135deg, #2c1810 0%, #78350f 50%, #2c1810 100%)",
    ),
    "arctic-frost": Theme(
        slug="arctic-frost",
        name="Arctic Frost",
        description="Cool, crisp precision with clinical clarity",
        best_for="Healthcare, pharma, clean tech, data-driven businesses",
        font_heading="'Plus Jakarta Sans', sans-serif",
        font_body="'Inter', sans-serif",
        primary="#0c1929",
        primary_dark="#070f1a",
        accent="#06b6d4",
        accent_hover="#0891b2",
        text_dark="#0f1729",
        text_light="#ecfeff",
        text_muted="#5e7a8a",
        surface="#f0f9ff",
        border="#bae6fd",
        hero_gradient="linear-gradient(160deg, #0c1929 0%, #164e63 50%, #0c1929 100%)",
    ),
    "desert-rose": Theme(
        slug="desert-rose",
        name="Desert Rose",
        description="Soft, sophisticated dusty tones with elegance",
        best_for="Fashion, beauty, interior design, boutique businesses",
        font_heading="'Crimson Pro', serif",
        font_body="'DM Sans', sans-serif",
        primary="#2e1a1e",
        primary_dark="#1c1012",
        accent="#e11d48",
        accent_hover="#be123c",
        text_dark="#2a1519",
        text_light="#fff1f2",
        text_muted="#9a6b73",
        surface="#fdf2f4",
        border="#f0c6cd",
        hero_gradient="linear-gradient(135deg, #2e1a1e 0%, #5c2434 50%, #2e1a1e 100%)",
    ),
    "botanical-garden": Theme(
        slug="botanical-garden",
        name="Botanical Garden",
        description="Fresh, vibrant greens with organic vitality",
        best_for="Food brands, farm-to-table, garden centers, natural products",
        font_heading="'Outfit', sans-serif",
        font_body="'DM Sans', sans-serif",
        primary="#052e16",
        primary_dark="#03200f",
        accent="#10b981",
        accent_hover="#059669",
        text_dark="#052e16",
        text_light="#ecfdf5",
        text_muted="#4d7c5f",
        surface="#ecfdf5",
        border="#a7f3d0",
        hero_gradient="linear-gradient(135deg, #052e16 0%, #166534 50%, #052e16 100%)",
    ),
    "modern-minimalist": Theme(
        slug="modern-minimalist",
        name="Modern Minimalist",
        description="Clean grayscale with purposeful simplicity",
        best_for="Architecture, design, tech, modern business proposals",
        font_heading="'Space Grotesk', sans-serif",
        font_body="'Inter', sans-serif",
        primary="#111111",
        primary_dark="#000000",
        accent="#171717",
        accent_hover="#333333",
        text_dark="#111111",
        text_light="#fafafa",
        text_muted="#737373",
        surface="#f5f5f5",
        border="#e5e5e5",
        hero_gradient="linear-gradient(180deg, #111111 0%, #262626 100%)",
    ),
}

DEFAULT_THEME = "tech-innovation"


def get_theme(slug: str) -> Theme:
    """Get a theme by slug, falling back to default."""
    return THEMES.get(slug, THEMES[DEFAULT_THEME])


def get_theme_css(slug: str) -> str:
    """Get the CSS custom properties block for a theme."""
    return get_theme(slug).to_css()


def list_themes() -> list[dict]:
    """Return theme metadata for API responses and CLI display."""
    return [
        {
            "slug": t.slug,
            "name": t.name,
            "description": t.description,
            "best_for": t.best_for,
            "primary": t.primary,
            "accent": t.accent,
        }
        for t in THEMES.values()
    ]
