#!/usr/bin/env python3
"""
CLI interface for HubSpot Landing Page Builder.
Usage: python cli.py create --type lead_gen --business "Acme Corp" ...
"""

import typer
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from config import config
from services.hubspot import HubSpotService, HubSpotError
from services.ai_content import AIContentService
from services.template_engine import TemplateEngine
from services.themes import list_themes, THEMES, DEFAULT_THEME

app = typer.Typer(
    name="hubspot-lp",
    help="ð HubSpot Landing Page Builder â AI-powered landing pages in minutes.",
    add_completion=False,
)
console = Console()


def check_config():
    """Validate config before running commands."""
    errors = config.validate()
    if errors:
        console.print("[bold red]Configuration errors:[/bold red]")
        for e in errors:
            console.print(f"  â {e}")
        console.print("\nCopy .env.example to .env and fill in your keys.")
        raise typer.Exit(1)


@app.command()
def create(
    page_type: str = typer.Option(
        ...,
        "--type",
        "-t",
        help="Page type: lead_gen, service, or event",
    ),
    business_name: str = typer.Option(
        ...,
        "--business",
        "-b",
        help="Business or brand name",
    ),
    business_description: str = typer.Option(
        ...,
        "--description",
        "-d",
        help="What the business does (1-2 sentences)",
    ),
    target_audience: str = typer.Option(
        ...,
        "--audience",
        "-a",
        help="Who this page targets",
    ),
    key_offering: str = typer.Option(
        ...,
        "--offering",
        "-o",
        help="The specific product/service/event being promoted",
    ),
    tone: str = typer.Option(
        "professional",
        "--tone",
        help="Writing tone: professional, warm, authoritative, casual",
    ),
    slug: str = typer.Option(
        None,
        "--slug",
        "-s",
        help="URL slug for the page (auto-generated if omitted)",
    ),
    publish: bool = typer.Option(
        False,
        "--publish",
        help="Publish immediately (default: save as draft)",
    ),
    preview_only: bool = typer.Option(
        False,
        "--preview",
        help="Generate HTML locally without pushing to HubSpot",
    ),
    output_file: str = typer.Option(
        None,
        "--output",
        help="Save rendered HTML to this file path",
    ),
    event_date: str = typer.Option(None, "--event-date", help="Event date (for event pages)"),
    event_time: str = typer.Option(None, "--event-time", help="Event time (for event pages)"),
    event_location: str = typer.Option(None, "--event-location", help="Event location (for event pages)"),
    theme: str = typer.Option(
        DEFAULT_THEME,
        "--theme",
        help="Visual theme: tech-innovation, ocean-depths, midnight-galaxy, sunset-boulevard, forest-canopy, golden-hour, arctic-frost, desert-rose, botanical-garden, modern-minimalist",
    ),
    extra_instructions: str = typer.Option(
        "",
        "--extra",
        help="Additional copywriting instructions",
    ),
):
    """Create a new AI-powered landing page and push it to HubSpot."""
    check_config()

    if page_type not in ("lead_gen", "service", "event"):
        console.print(f"[red]Invalid page type: {page_type}. Use lead_gen, service, or event.[/red]")
        raise typer.Exit(1)

    if theme not in THEMES:
        console.print(f"[red]Invalid theme: {theme}[/red]")
        console.print("Available themes: " + ", ".join(THEMES.keys()))
        raise typer.Exit(1)

    console.print(f"[dim]Theme:[/dim] [cyan]{THEMES[theme].name}[/cyan] â {THEMES[theme].description}")

    # ââ Step 1: Generate AI content âââââââââââââââââââââââââââââââââ
    console.print()
    with console.status("[bold cyan]Generating AI-powered copy with Claude...[/bold cyan]"):
        ai = AIContentService(config.anthropic_api_key, config.anthropic_model)
        content = ai.generate_content(
            page_type=page_type,
            business_name=business_name,
            business_description=business_description,
            target_audience=target_audience,
            key_offering=key_offering,
            tone=tone,
            extra_instructions=extra_instructions,
        )

    console.print(Panel(
        f"[bold]{content.headline}[/bold]\n{content.subheadline}\n\n"
        f"CTA: [green]{content.cta_text}[/green]\n"
        f"Meta: {content.meta_description}",
        title="â¨ Generated Content",
        border_style="cyan",
    ))

    # ââ Step 2: Render template âââââââââââââââââââââââââââââââââââââ
    with console.status("[bold cyan]Rendering HTML template...[/bold cyan]"):
        engine = TemplateEngine(config.template_dir)
        html = engine.render(
            page_type=page_type,
            content=content,
            business_name=business_name,
            theme_slug=theme,
            event_date=event_date or "",
            event_time=event_time or "",
            event_location=event_location or "",
        )

    console.print(f"[green]â[/green] HTML rendered ({len(html):,} characters)")

    # ââ Save locally if requested âââââââââââââââââââââââââââââââââââ
    if output_file:
        Path(output_file).write_text(html)
        console.print(f"[green]â[/green] Saved to {output_file}")

    if preview_only:
        if not output_file:
            default_path = f"preview_{page_type}.html"
            Path(default_path).write_text(html)
            console.print(f"[green]â[/green] Preview saved to {default_path}")
        console.print("[yellow]Preview mode â not pushing to HubSpot.[/yellow]")
        raise typer.Exit(0)

    # ââ Step 3: Push to HubSpot âââââââââââââââââââââââââââââââââââââ
    with console.status("[bold cyan]Creating page in HubSpot...[/bold cyan]"):
        hs = HubSpotService(config.hubspot_access_token)

        try:
            page = hs.create_landing_page(
                name=f"{business_name} â {content.page_title}",
                html_body=html,
                slug=slug,
                meta_description=content.meta_description,
                page_title=content.page_title,
                publish=publish,
            )
        except HubSpotError as e:
            console.print(f"[bold red]HubSpot error:[/bold red] {e.message}")
            if e.details:
                console.print(json.dumps(e.details, indent=2))
            raise typer.Exit(1)

    status = "[green]PUBLISHED[/green]" if publish else "[yellow]DRAFT[/yellow]"
    console.print()
    console.print(Panel(
        f"Page ID: {page.get('id')}\n"
        f"Status: {status}\n"
        f"URL slug: {page.get('slug', 'N/A')}\n"
        f"Created: {page.get('createdAt', 'N/A')}",
        title="ð Page Created in HubSpot",
        border_style="green",
    ))


@app.command()
def list_pages(
    limit: int = typer.Option(20, "--limit", "-l", help="Number of pages to list"),
):
    """List existing landing pages in your HubSpot account."""
    check_config()

    hs = HubSpotService(config.hubspot_access_token)

    with console.status("[bold cyan]Fetching pages from HubSpot...[/bold cyan]"):
        try:
            result = hs.list_landing_pages(limit=limit)
        except HubSpotError as e:
            console.print(f"[bold red]Error:[/bold red] {e.message}")
            raise typer.Exit(1)

    pages = result.get("results", [])
    if not pages:
        console.print("[yellow]No landing pages found.[/yellow]")
        raise typer.Exit(0)

    table = Table(title="HubSpot Landing Pages")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Slug")
    table.add_column("State", style="cyan")
    table.add_column("Updated")

    for p in pages:
        table.add_row(
            str(p.get("id", "")),
            p.get("name", "")[:50],
            p.get("slug", ""),
            p.get("state", ""),
            str(p.get("updatedAt", ""))[:10],
        )

    console.print(table)


@app.command()
def test_connection():
    """Test your HubSpot API connection."""
    check_config()

    hs = HubSpotService(config.hubspot_access_token)
    with console.status("[bold cyan]Testing HubSpot connection...[/bold cyan]"):
        ok = hs.test_connection()

    if ok:
        console.print("[bold green]â Connected to HubSpot successfully![/bold green]")
    else:
        console.print("[bold red]â Could not connect. Check your HUBSPOT_ACCESS_TOKEN.[/bold red]")
        raise typer.Exit(1)


@app.command()
def templates():
    """List available landing page templates."""
    engine = TemplateEngine(config.template_dir)
    available = engine.list_templates()

    console.print("\n[bold]Available Templates:[/bold]\n")
    descriptions = {
        "lead_gen": "Lead capture / opt-in page with form",
        "service": "Service showcase with process steps & CTA",
        "event": "Event / workshop registration page",
    }
    for t in available:
        desc = descriptions.get(t, "")
        console.print(f"  â¢ [cyan]{t}[/cyan] â {desc}")
    console.print()


@app.command()
def themes():
    """List all available visual themes."""
    theme_list = list_themes()

    table = Table(title="Available Themes")
    table.add_column("Slug", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Best For", style="dim")

    for t in theme_list:
        table.add_row(t["slug"], t["name"], t["description"], t["best_for"])

    console.print()
    console.print(table)
    console.print("\n[dim]Use --theme <slug> with the create command.[/dim]\n")


if __name__ == "__main__":
    app()
