"""
Configuration management for HubSpot Landing Page Builder.
Loads settings from environment variables or .env file.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration loaded from environment."""

    # HubSpot
    hubspot_access_token: str = field(
        default_factory=lambda: os.getenv("HUBSPOT_ACCESS_TOKEN", "")
    )
    hubspot_portal_id: str = field(
        default_factory=lambda: os.getenv("HUBSPOT_PORTAL_ID", "")
    )

    # Anthropic (Claude API for AI content generation)
    anthropic_api_key: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", "")
    )
    anthropic_model: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    )

    # App settings
    app_host: str = field(default_factory=lambda: os.getenv("APP_HOST", "0.0.0.0"))
    app_port: int = field(
        default_factory=lambda: int(os.getenv("APP_PORT", "8000"))
    )
    debug: bool = field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true"
    )

    # Template directory
    template_dir: Path = field(
        default_factory=lambda: Path(__file__).parent / "templates" / "landing_pages"
    )

    def validate(self) -> list[str]:
        """Return list of missing required config values."""
        errors = []
        if not self.hubspot_access_token:
            errors.append("HUBSPOT_ACCESS_TOKEN is required")
        if not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required")
        return errors


config = Config()
