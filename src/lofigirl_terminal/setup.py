"""
Interactive setup for LofiGirl Terminal.

This module provides an interactive configuration wizard for first-time setup,
allowing users to choose themes, fonts, and other preferences.
"""

import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from lofigirl_terminal.logger import get_logger
from lofigirl_terminal.modules.ascii_art import ASCII_ARTS
from lofigirl_terminal.modules.themes import THEMES, get_theme_preview

logger = get_logger(__name__)
console = Console()


# Popular Nerd Fonts recommended for terminal use
RECOMMENDED_FONTS = [
    ("JetBrainsMono Nerd Font", "Modern, clear monospace font (recommended)"),
    ("FiraCode Nerd Font", "Popular font with programming ligatures"),
    ("Hack Nerd Font", "Clean, readable monospace font"),
    ("CascadiaCode Nerd Font", "Microsoft's modern monospace font"),
    ("MesloLGS Nerd Font", "Menlo variant with extra glyphs"),
    ("UbuntuMono Nerd Font", "Ubuntu's monospace font"),
    ("DejaVuSansMono Nerd Font", "Classic, widely compatible font"),
    ("System Default", "Use your terminal's current font"),
]


def print_welcome() -> None:
    """Print welcome message."""
    welcome_text = Text()
    welcome_text.append("Welcome to ", style="bold cyan")
    welcome_text.append("LofiGirl Terminal", style="bold magenta")

    panel = Panel(
        welcome_text,
        title="[bold]Setup Wizard[/bold]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print("\n")
    console.print(panel)
    console.print(
        "\n[dim]Let's customize your lofi experience! This will only take a minute.[/dim]\n"
    )


def choose_theme() -> str:
    """
    Interactive theme selection.

    Returns:
        Selected theme name
    """
    console.print("[bold cyan]Step 1: Choose Your Theme[/bold cyan]\n")
    console.print("[dim]Select a color palette that matches your vibe.[/dim]\n")

    # Create a table showing all themes
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        title="Available Themes",
        title_style="bold cyan",
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Theme Name", style="bold")
    table.add_column("Description", style="dim")

    theme_list = list(THEMES.items())
    for idx, (_theme_id, theme) in enumerate(theme_list, 1):
        table.add_row(
            str(idx),
            theme.name,
            theme.description,
        )

    console.print(table)
    console.print()

    # Get user choice
    while True:
        choice = Prompt.ask(
            "[cyan]Enter theme number[/cyan]",
            default="1",
            show_default=True,
        )

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(theme_list):
                selected_theme_id, selected_theme = theme_list[idx]

                # Show preview
                console.print(f"\n[bold]Preview of {selected_theme.name}:[/bold]")
                preview_panel = Panel(
                    get_theme_preview(selected_theme_id),
                    border_style=selected_theme.primary,
                    padding=(1, 2),
                )
                console.print(preview_panel)

                # Confirm choice
                if Confirm.ask("\n[cyan]Use this theme?[/cyan]", default=True):
                    console.print(
                        f"[green]Theme set to [bold]{selected_theme.name}[/bold][/green]\n"
                    )
                    return selected_theme_id
            else:
                console.print(
                    f"[red]Please enter a number between 1 and {len(theme_list)}[/red]"
                )
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")


def choose_font() -> Optional[str]:
    """
    Interactive font selection.

    Returns:
        Selected font name, or None for system default
    """
    console.print("\n[bold cyan]Step 2: Choose Your Font[/bold cyan]\n")
    console.print(
        "[dim]Nerd Fonts include extra icons and glyphs for a better experience.[/dim]\n"
    )

    # Create a table showing recommended fonts
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        title="Recommended Fonts",
        title_style="bold cyan",
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Font Name", style="bold")
    table.add_column("Description", style="dim")

    for idx, (font_name, description) in enumerate(RECOMMENDED_FONTS, 1):
        table.add_row(str(idx), font_name, description)

    console.print(table)
    console.print()

    # Show font installation instructions
    console.print(
        Panel(
            "[yellow]Note:[/yellow] If you don't have Nerd Fonts installed:\n"
            "Visit: https://www.nerdfonts.com/\n"
            "Or use Oh My Posh: https://ohmyposh.dev/docs/installation/fonts\n"
            "Quick install: [cyan]oh-my-posh font install[/cyan]",
            border_style="yellow",
            padding=(1, 2),
        )
    )
    console.print()

    # Get user choice
    while True:
        choice = Prompt.ask(
            "[cyan]Enter font number[/cyan]",
            default=str(len(RECOMMENDED_FONTS)),  # Default to system default
            show_default=True,
        )

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(RECOMMENDED_FONTS):
                font_name, _ = RECOMMENDED_FONTS[idx]

                if font_name == "System Default":
                    console.print("[green]Using system default font[/green]\n")
                    return None
                else:
                    console.print(
                        f"[green]Font set to [bold]{font_name}[/bold][/green]\n"
                    )
                    return font_name
            else:
                console.print(
                    f"[red]Please enter a number between 1 and {len(RECOMMENDED_FONTS)}[/red]"
                )
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")


def choose_ascii_art() -> str:
    """
    Interactive ASCII art selection.

    Returns:
        Selected ASCII art ID
    """
    console.print("\n[bold cyan]Step 3: Choose Your ASCII Art[/bold cyan]\n")
    console.print("[dim]Select an animated ASCII art for your TUI.[/dim]\n")

    # Create a table showing all ASCII arts
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        title="Available ASCII Art",
        title_style="bold cyan",
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Name", style="bold")
    table.add_column("Description", style="dim")
    table.add_column("Frames", style="dim", width=7)

    art_list = list(ASCII_ARTS.items())
    for idx, (_art_id, art) in enumerate(art_list, 1):
        table.add_row(
            str(idx),
            art.name,
            art.description,
            f"{len(art.frames)} frames",
        )

    console.print(table)
    console.print()

    # Get user choice
    while True:
        choice = Prompt.ask(
            "[cyan]Enter ASCII art number[/cyan]",
            default="1",
            show_default=True,
        )

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(art_list):
                selected_art_id, selected_art = art_list[idx]

                # Show preview
                console.print(f"\n[bold]Preview of {selected_art.name}:[/bold]")
                console.print(f"[dim]By: {selected_art.author}[/dim]\n")

                # Show first frame
                preview_panel = Panel(
                    selected_art.frames[0],
                    border_style="bright_cyan",
                    padding=(1, 2),
                )
                console.print(preview_panel)

                # Confirm choice
                if Confirm.ask("\n[cyan]Use this ASCII art?[/cyan]", default=True):
                    console.print(
                        f"[green]ASCII art set to [bold]{selected_art.name}[/bold][/green]\n"
                    )
                    return selected_art_id
            else:
                console.print(
                    f"[red]Please enter a number between 1 and {len(art_list)}[/red]"
                )
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")


def save_config(theme: str, font: Optional[str], ascii_art: str) -> None:
    """
    Save configuration to config file.

    Args:
        theme: Selected theme name
        font: Selected font name (or None for default)
        ascii_art: Selected ASCII art ID
    """
    # Get or create config file path
    config_dir = Path.home() / ".config" / "lofigirl-terminal"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.env"

    # Read existing config if it exists
    existing_lines = []
    if config_file.exists():
        with open(config_file, "r") as f:
            existing_lines = [
                line
                for line in f.readlines()
                if not line.startswith("THEME=")
                and not line.startswith("TERMINAL_FONT=")
                and not line.startswith("ASCII_ART=")
            ]

    # Write new config
    with open(config_file, "w") as f:
        # Write existing config
        f.writelines(existing_lines)

        # Add new settings
        f.write("\n# Theme configuration\n")
        f.write(f"THEME={theme}\n")

        if font:
            f.write("\n# Font configuration\n")
            f.write(f"TERMINAL_FONT={font}\n")

        f.write("\n# ASCII Art configuration\n")
        f.write(f"ASCII_ART={ascii_art}\n")

    console.print(f"[green]Configuration saved to [bold]{config_file}[/bold][/green]\n")


def run_setup(force: bool = False) -> None:
    """
    Run the interactive setup wizard.

    Args:
        force: Force setup even if already configured
    """
    # Check if already configured
    config_file = Path.home() / ".config" / "lofigirl-terminal" / "config.env"

    if config_file.exists() and not force:
        console.print("\n[yellow]Configuration file already exists.[/yellow]\n")
        if not Confirm.ask(
            "[cyan]Run setup again to reconfigure?[/cyan]", default=False
        ):
            console.print("[dim]Setup cancelled.[/dim]\n")
            return

    # Run setup wizard
    print_welcome()

    try:
        # Step 1: Choose theme
        theme = choose_theme()

        # Step 2: Choose font
        font = choose_font()

        # Step 3: Choose ASCII art
        ascii_art = choose_ascii_art()

        # Save configuration
        console.print("\n[bold cyan]Saving Configuration[/bold cyan]\n")
        save_config(theme, font, ascii_art)

        # Show success message
        success_panel = Panel(
            "[green]Setup Complete![/green]\n\n"
            "Your LofiGirl Terminal is now configured.\n\n"
            "To start: [bold cyan]lofigirl tui[/bold cyan]\n"
            "To reconfigure: [bold cyan]lofigirl setup[/bold cyan]",
            border_style="green",
            padding=(1, 2),
        )
        console.print(success_panel)
        console.print()

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup cancelled by user.[/yellow]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error during setup: {e}[/red]\n")
        logger.exception("Setup failed")
        sys.exit(1)


if __name__ == "__main__":
    run_setup()
