"""
FastAPI web interface for HubSpot Landing Page Builder.
Run: uvicorn main:app --reload
"""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from config import config
from services.hubspot import HubSpotService, HubSpotError
from services.ai_content import AIContentService
from services.template_engine import TemplateEngine
from services.themes import list_themes, DEFAULT_THEME

app = FastAPI(
    title="HubSpot Landing Page Builder",
    description="AI-powered landing page generator for HubSpot CMS",
    version="1.0.0",
)


# ââââââââââââââââââââââââââââââââââââââââââ
#  Request models
# ââââââââââââââââââââââââââââââââââââââââââ
class GenerateRequest(BaseModel):
    page_type: str  # lead_gen, service, event
    business_name: str
    business_description: str
    target_audience: str
    key_offering: str
    tone: str = "professional"
    theme: str = DEFAULT_THEME
    extra_instructions: str = ""
    event_date: Optional[str] = None
    event_time: Optional[str] = None
    event_location: Optional[str] = None


class PublishRequest(BaseModel):
    html_body: str
    page_title: str
    business_name: str
    meta_description: str = ""
    slug: Optional[str] = None
    publish: bool = False


# ââââââââââââââââââââââââââââââââââââââââââ
#  Routes
# ââââââââââââââââââââââââââââââââââââââââââ
@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the web UI."""
    ui_path = Path(__file__).parent / "web_templates" / "index.html"
    if ui_path.exists():
        return HTMLResponse(content=ui_path.read_text())
    return HTMLResponse(content="<h1>HubSpot LP Builder - Web UI not found</h1>")


@app.get("/api/status")
async def status():
    """Check API status and configuration."""
    errors = config.validate()
    return {
        "status": "ok" if not errors else "config_error",
        "errors": errors,
        "hubspot_configured": bool(config.hubspot_access_token),
        "ai_configured": bool(config.anthropic_api_key),
    }


@app.get("/api/themes")
async def get_themes():
    """List all available themes."""
    return {"themes": list_themes(), "default": DEFAULT_THEME}


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    """Generate AI content and render HTML."""
    errors = config.validate()
    if errors:
        raise HTTPException(status_code=500, detail="Config errors: " + ", ".join(errors))

    if req.page_type not in ("lead_gen", "service", "event"):
        raise HTTPException(status_code=400, detail=f"Invalid page_type: {req.page_type}")

    try:
        ai = AIContentService(config.anthropic_api_key, config.anthropic_model)
        content = ai.generate_content(
            page_type=req.page_type,
            business_name=req.business_name,
            business_description=req.business_description,
            target_audience=req.target_audience,
            key_offering=req.key_offering,
            tone=req.tone,
            extra_instructions=req.extra_instructions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

    try:
        engine = TemplateEngine(config.template_dir)
        html = engine.render(
            page_type=req.page_type,
            content=content,
            business_name=req.business_name,
            theme_slug=req.theme,
            event_date=req.event_date or "",
            event_time=req.event_time or "",
            event_location=req.event_location or "",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template rendering failed: {str(e)}")

    return {
        "html": html,
        "content": {
            "headline": content.headline,
            "subheadline": content.subheadline,
            "cta_text": content.cta_text,
            "page_title": content.page_title,
            "meta_description": content.meta_description,
        },
    }


@app.post("/api/publish")
async def publish(req: PublishRequest):
    """Publish generated HTML to HubSpot."""
    errors = config.validate()
    if errors:
        raise HTTPException(status_code=500, detail="Config errors: " + ", ".join(errors))

    try:
        hs = HubSpotService(config.hubspot_access_token)
        page = hs.create_landing_page(
            name=f"{req.business_name} â {req.page_title}",
            html_body=req.html_body,
            slug=req.slug,
            meta_description=req.meta_description,
            page_title=req.page_title,
            publish=req.publish,
        )
    except HubSpotError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "success": True,
        "page_id": page.get("id"),
        "slug": page.get("slug"),
        "state": page.get("state"),
    }


@app.get("/api/pages")
async def get_pages(limit: int = 20):
    """List existing HubSpot landing pages."""
    try:
        hs = HubSpotService(config.hubspot_access_token)
        result = hs.list_landing_pages(limit=limit)
        return result
    except HubSpotError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.app_host,
        port=config.app_port,
        reload=config.debug,
    )
