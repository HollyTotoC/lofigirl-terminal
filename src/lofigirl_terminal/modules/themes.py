"""
Theme system for LofiGirl Terminal.

This module provides color themes and palettes for customizing the TUI appearance.
Includes popular themes like Catppuccin, Dracula, Nord, Tokyo Night, and more.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ColorPalette:
    """
    Color palette for the TUI.

    Attributes:
        name: Theme name
        description: Brief description of the theme
        background: Background color
        foreground: Foreground/text color
        primary: Primary accent color
        secondary: Secondary accent color
        accent: Highlight color
        error: Error message color
        warning: Warning message color
        success: Success message color
        border: Border color
        muted: Muted/dim text color
    """

    name: str
    description: str
    background: str
    foreground: str
    primary: str
    secondary: str
    accent: str
    error: str
    warning: str
    success: str
    border: str
    muted: str


# Catppuccin Mocha (Dark)
CATPPUCCIN_MOCHA = ColorPalette(
    name="Catppuccin Mocha",
    description="Soothing pastel theme for the high-spirited - Dark variant",
    background="#1e1e2e",
    foreground="#cdd6f4",
    primary="#89b4fa",  # Blue
    secondary="#f5c2e7",  # Pink
    accent="#a6e3a1",  # Green
    error="#f38ba8",  # Red
    warning="#f9e2af",  # Yellow
    success="#a6e3a1",  # Green
    border="#89b4fa",  # Blue
    muted="#6c7086",  # Surface 2
)

# Catppuccin Latte (Light)
CATPPUCCIN_LATTE = ColorPalette(
    name="Catppuccin Latte",
    description="Soothing pastel theme for the high-spirited - Light variant",
    background="#eff1f5",
    foreground="#4c4f69",
    primary="#1e66f5",  # Blue
    secondary="#ea76cb",  # Pink
    accent="#40a02b",  # Green
    error="#d20f39",  # Red
    warning="#df8e1d",  # Yellow
    success="#40a02b",  # Green
    border="#1e66f5",  # Blue
    muted="#9ca0b0",  # Surface 2
)

# Dracula
DRACULA = ColorPalette(
    name="Dracula",
    description="A dark theme with vibrant colors",
    background="#282a36",
    foreground="#f8f8f2",
    primary="#bd93f9",  # Purple
    secondary="#ff79c6",  # Pink
    accent="#8be9fd",  # Cyan
    error="#ff5555",  # Red
    warning="#f1fa8c",  # Yellow
    success="#50fa7b",  # Green
    border="#bd93f9",  # Purple
    muted="#6272a4",  # Comment
)

# Nord
NORD = ColorPalette(
    name="Nord",
    description="An arctic, north-bluish color palette",
    background="#2e3440",
    foreground="#eceff4",
    primary="#88c0d0",  # Frost 1
    secondary="#81a1c1",  # Frost 2
    accent="#8fbcbb",  # Frost 3
    error="#bf616a",  # Red
    warning="#ebcb8b",  # Yellow
    success="#a3be8c",  # Green
    border="#5e81ac",  # Frost 4
    muted="#4c566a",  # Polar Night 3
)

# Tokyo Night
TOKYO_NIGHT = ColorPalette(
    name="Tokyo Night",
    description="A clean, dark theme inspired by Tokyo's night skyline",
    background="#1a1b26",
    foreground="#c0caf5",
    primary="#7aa2f7",  # Blue
    secondary="#bb9af7",  # Purple
    accent="#7dcfff",  # Cyan
    error="#f7768e",  # Red
    warning="#e0af68",  # Yellow
    success="#9ece6a",  # Green
    border="#7aa2f7",  # Blue
    muted="#565f89",  # Comment
)

# Gruvbox Dark
GRUVBOX_DARK = ColorPalette(
    name="Gruvbox Dark",
    description="Retro groove color scheme with warm, earthy tones",
    background="#282828",
    foreground="#ebdbb2",
    primary="#83a598",  # Bright blue
    secondary="#d3869b",  # Bright purple
    accent="#8ec07c",  # Bright aqua
    error="#fb4934",  # Bright red
    warning="#fabd2f",  # Bright yellow
    success="#b8bb26",  # Bright green
    border="#83a598",  # Bright blue
    muted="#928374",  # Gray
)

# Solarized Dark
SOLARIZED_DARK = ColorPalette(
    name="Solarized Dark",
    description="Precision colors for machines and people",
    background="#002b36",
    foreground="#839496",
    primary="#268bd2",  # Blue
    secondary="#d33682",  # Magenta
    accent="#2aa198",  # Cyan
    error="#dc322f",  # Red
    warning="#b58900",  # Yellow
    success="#859900",  # Green
    border="#268bd2",  # Blue
    muted="#586e75",  # Base01
)

# One Dark
ONE_DARK = ColorPalette(
    name="One Dark",
    description="Iconic dark theme from Atom editor",
    background="#282c34",
    foreground="#abb2bf",
    primary="#61afef",  # Blue
    secondary="#c678dd",  # Purple
    accent="#56b6c2",  # Cyan
    error="#e06c75",  # Red
    warning="#e5c07b",  # Yellow
    success="#98c379",  # Green
    border="#61afef",  # Blue
    muted="#5c6370",  # Comment
)

# Monokai Pro
MONOKAI_PRO = ColorPalette(
    name="Monokai Pro",
    description="Professional color scheme with warm tones",
    background="#2d2a2e",
    foreground="#fcfcfa",
    primary="#78dce8",  # Cyan
    secondary="#ab9df2",  # Purple
    accent="#a9dc76",  # Green
    error="#ff6188",  # Red
    warning="#ffd866",  # Yellow
    success="#a9dc76",  # Green
    border="#78dce8",  # Cyan
    muted="#727072",  # Comment
)

# Default theme (Catppuccin Mocha)
DEFAULT_THEME = CATPPUCCIN_MOCHA

# All available themes
THEMES: Dict[str, ColorPalette] = {
    "catppuccin-mocha": CATPPUCCIN_MOCHA,
    "catppuccin-latte": CATPPUCCIN_LATTE,
    "dracula": DRACULA,
    "nord": NORD,
    "tokyo-night": TOKYO_NIGHT,
    "gruvbox-dark": GRUVBOX_DARK,
    "solarized-dark": SOLARIZED_DARK,
    "one-dark": ONE_DARK,
    "monokai-pro": MONOKAI_PRO,
}


def get_theme(theme_name: str) -> ColorPalette:
    """
    Get a theme by name.

    Args:
        theme_name: Name of the theme (e.g., "catppuccin-mocha")

    Returns:
        ColorPalette for the theme, or default theme if not found
    """
    return THEMES.get(theme_name.lower(), DEFAULT_THEME)


def list_themes() -> List[str]:
    """
    Get list of all available theme names.

    Returns:
        List of theme names
    """
    return list(THEMES.keys())


def get_theme_preview(theme_name: str) -> str:
    """
    Get a preview string showing the theme colors.

    Args:
        theme_name: Name of the theme

    Returns:
        Formatted string with color preview
    """
    theme = get_theme(theme_name)
    return f"""{theme.name}
{theme.description}

Primary:   {theme.primary}
Secondary: {theme.secondary}
Accent:    {theme.accent}
Success:   {theme.success}
Warning:   {theme.warning}
Error:     {theme.error}""".strip()
