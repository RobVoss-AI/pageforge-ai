"""
AI content generation service using Anthropic's Claude API.
Generates conversion-optimized landing page copy.
"""

import json
from dataclasses import dataclass, field

import anthropic


@dataclass
class ContentResponse:
    """Structured AI-generated content for a landing page."""
    headline: str = ""
    subheadline: str = ""
    cta_text: str = ""
    cta_subtext: str = ""
    page_title: str = ""
    meta_description: str = ""
    body_sections: list[dict] = field(default_factory=list)
    features: list[dict] = field(default_factory=list)
    testimonial_placeholder: str = ""


SYSTEM_PROMPT = """You are an expert landing page copywriter who creates conversion-optimized content.
You write compelling, benefit-driven copy that speaks directly to the target audience.
Your copy is clear, specific, and avoids generic marketing jargon.
Always respond with valid JSON matching the exact schema requested."""

PAGE_TYPE_GUIDANCE = {
    "lead_gen": """This is a LEAD GENERATION page. The goal is to capture contact information.
Focus on: the value proposition of what they'll receive, urgency, trust signals.
The CTA should encourage form submission (e.g., "Get Your Free Guide", "Download Now", "Claim Your Spot").""",

    "service": """This is a SERVICE SHOWCASE page. The goal is to present services and drive consultation/contact.
Focus on: expertise, process clarity, results/outcomes, professionalism.
The CTA should drive engagement (e.g., "Schedule a Consultation", "Get Started Today", "Book Your Call").""",

    "event": """This is an EVENT/WORKSHOP page. The goal is to drive registrations.
Focus on: what attendees will learn, speaker credibility, FOMO/urgency, tangible takeaways.
The CTA should drive registration (e.g., "Reserve Your Seat", "Register Now", "Save My Spot").""",
}


class AIContentService:
    """Generate landing page content using Claude AI."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate_content(
        self,
        page_type: str,
        business_name: str,
        business_description: str,
        target_audience: str,
        key_offering: str,
        tone: str = "professional",
        extra_instructions: str = "",
    ) -> ContentResponse:
        """Generate structured content for a landing page."""

        type_guidance = PAGE_TYPE_GUIDANCE.get(page_type, PAGE_TYPE_GUIDANCE["lead_gen"])

        prompt = f"""Create landing page copy for the following:

**Business:** {business_name}
**Description:** {business_description}
**Target Audience:** {target_audience}
**Key Offering:** {key_offering}
**Tone:** {tone}
**Page Type:** {page_type}

{type_guidance}

{f"**Additional Instructions:** {extra_instructions}" if extra_instructions else ""}

Respond with ONLY valid JSON in this exact format (no markdown, no code fences):
{{
  "headline": "A compelling, benefit-driven headline (8-12 words max)",
  "subheadline": "Supporting text that expands on the headline (15-25 words)",
  "cta_text": "Action-oriented button text (2-5 words)",
  "cta_subtext": "Brief reassurance text below the CTA (8-15 words)",
  "page_title": "SEO-optimized browser tab title (50-60 chars)",
  "meta_description": "SEO meta description (140-155 chars)",
  "body_sections": [
    {{"heading": "Section heading", "text": "1-2 paragraph section body text (40-60 words)"}},
    {{"heading": "Section heading", "text": "1-2 paragraph section body text (40-60 words)"}}
  ],
  "features": [
    {{"icon": "relevant emoji", "title": "Feature/benefit title", "description": "Brief description (15-25 words)"}},
    {{"icon": "relevant emoji", "title": "Feature/benefit title", "description": "Brief description (15-25 words)"}},
    {{"icon": "relevant emoji", "title": "Feature/benefit title", "description": "Brief description (15-25 words)"}}
  ],
  "testimonial_placeholder": "A realistic-sounding testimonial quote (20-35 words)"
}}

Important:
- Write for the "{tone}" tone
- Make the headline specific to {business_name} and {key_offering}
- Features should highlight tangible benefits, not vague promises
- The testimonial should sound authentic and specific
- All text should speak directly to {target_audience}"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        raw_text = message.content[0].text.strip()

        # Strip markdown code fences if present
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            raw_text = "\n".join(lines[1:])
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3].strip()

        data = json.loads(raw_text)

        return ContentResponse(
            headline=data.get("headline", ""),
            subheadline=data.get("subheadline", ""),
            cta_text=data.get("cta_text", ""),
            cta_subtext=data.get("cta_subtext", ""),
            page_title=data.get("page_title", ""),
            meta_description=data.get("meta_description", ""),
            body_sections=data.get("body_sections", []),
            features=data.get("features", []),
            testimonial_placeholder=data.get("testimonial_placeholder", ""),
        )
