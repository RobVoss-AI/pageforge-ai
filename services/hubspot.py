"""
HubSpot CMS API service for creating and managing landing pages.
Uses HubSpot's CMS Pages API (v3).
"""

import httpx
from typing import Any

BASE_URL = "https://api.hubapi.com"


class HubSpotError(Exception):
    """Custom exception for HubSpot API errors."""

    def __init__(self, status_code: int, message: str, details: Any = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(f"HubSpot API error ({status_code}): {message}")


class HubSpotService:
    """Service for interacting with HubSpot's CMS API."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def _handle_response(self, response: httpx.Response) -> dict:
        """Parse response and raise on errors."""
        if response.status_code >= 400:
            try:
                body = response.json()
                message = body.get("message", response.text)
                details = body.get("errors", None)
            except Exception:
                message = response.text
                details = None
            raise HubSpotError(response.status_code, message, details)
        return response.json() if response.text else {}

    # ââ Landing Pages ââââââââââââââââââââââââââââââââââââââââââââââââ

    def create_landing_page(
        self,
        name: str,
        html_body: str,
        slug: str | None = None,
        meta_description: str = "",
        page_title: str = "",
        head_html: str = "",
        footer_html: str = "",
        publish: bool = False,
    ) -> dict:
        """
        Create a new landing page in HubSpot.

        Args:
            name: Internal name for the page.
            html_body: Full HTML content of the page body.
            slug: URL slug (e.g., 'my-landing-page'). Auto-generated if omitted.
            meta_description: SEO meta description.
            page_title: Browser tab title.
            head_html: Extra HTML injected into <head>.
            footer_html: Extra HTML injected before </body>.
            publish: If True, publish immediately; otherwise save as draft.

        Returns:
            HubSpot page object dict.
        """
        payload: dict[str, Any] = {
            "name": name,
            "htmlTitle": page_title or name,
            "layoutSections": {},
            "templatePath": "",  # blank = custom HTML
            "htmlBody": html_body,
            "metaDescription": meta_description,
        }
        if slug:
            payload["slug"] = slug
        if head_html:
            payload["headHtml"] = head_html
        if footer_html:
            payload["footerHtml"] = footer_html

        # Create the page as draft first
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{BASE_URL}/cms/v3/pages/landing-pages",
                headers=self.headers,
                json=payload,
            )
            page = self._handle_response(resp)

            # Optionally publish
            if publish and page.get("id"):
                self.publish_page(page["id"])
                page["state"] = "PUBLISHED"

            return page

    def publish_page(self, page_id: str) -> dict:
        """Publish a draft landing page."""
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{BASE_URL}/cms/v3/pages/landing-pages/{page_id}/publish",
                headers=self.headers,
                json={"id": page_id},
            )
            return self._handle_response(resp)

    def update_landing_page(self, page_id: str, updates: dict) -> dict:
        """Update an existing landing page."""
        with httpx.Client(timeout=30) as client:
            resp = client.patch(
                f"{BASE_URL}/cms/v3/pages/landing-pages/{page_id}",
                headers=self.headers,
                json=updates,
            )
            return self._handle_response(resp)

    def list_landing_pages(self, limit: int = 20, offset: int = 0) -> dict:
        """List existing landing pages."""
        with httpx.Client(timeout=30) as client:
            resp = client.get(
                f"{BASE_URL}/cms/v3/pages/landing-pages",
                headers=self.headers,
                params={"limit": limit, "offset": offset},
            )
            return self._handle_response(resp)

    def get_landing_page(self, page_id: str) -> dict:
        """Retrieve a single landing page by ID."""
        with httpx.Client(timeout=30) as client:
            resp = client.get(
                f"{BASE_URL}/cms/v3/pages/landing-pages/{page_id}",
                headers=self.headers,
            )
            return self._handle_response(resp)

    def delete_landing_page(self, page_id: str) -> None:
        """Delete a landing page."""
        with httpx.Client(timeout=30) as client:
            resp = client.delete(
                f"{BASE_URL}/cms/v3/pages/landing-pages/{page_id}",
                headers=self.headers,
            )
            if resp.status_code >= 400:
                self._handle_response(resp)

    # ââ Utility ââââââââââââââââââââââââââââââââââââââââââââââââââââââ

    def test_connection(self) -> bool:
        """Verify the access token works."""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    f"{BASE_URL}/cms/v3/pages/landing-pages",
                    headers=self.headers,
                    params={"limit": 1},
                )
                return resp.status_code == 200
        except Exception:
            return False
