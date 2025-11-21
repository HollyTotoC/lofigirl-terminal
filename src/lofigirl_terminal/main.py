"""
Main entry point for LofiGirl Terminal.

This module provides the CLI interface for the application using Click.
"""

import sys
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from lofigirl_terminal import __version__
from lofigirl_terminal.config import get_config
from lofigirl_terminal.logger import setup_logger
from lofigirl_terminal.modules.player import AudioPlayer
from lofigirl_terminal.modules.stations import StationManager

# Initialize console for rich output
console = Console()
logger = setup_logger("lofigirl_terminal")


@click.group()
@click.version_option(version=__version__, prog_name="lofigirl")
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode",
)
def cli(debug: bool) -> None:
    """
    🎵 LofiGirl Terminal - A terminal-based lofi radio player.

    Listen to relaxing lofi music directly from your terminal.
    Perfect for coding, studying, or just chilling.

    Examples:
        lofigirl play
        lofigirl list
        lofigirl play --station lofi-jazz
    """
    if debug:
        import os

        os.environ["LOG_LEVEL"] = "DEBUG"
        logger.setLevel("DEBUG")
        logger.debug("Debug mode enabled")


@cli.command()
@click.option(
    "--station",
    "-s",
    default=None,
    help="Station ID to play",
)
@click.option(
    "--volume",
    "-v",
    default=None,
    type=click.IntRange(0, 100),
    help="Volume level (0-100)",
)
def play(station: Optional[str], volume: Optional[int]) -> None:
    """
    🎧 Start playing a lofi radio station.

    Examples:
        lofigirl play
        lofigirl play --station lofi-jazz
        lofigirl play --station lofi-hip-hop --volume 75
    """
    config = get_config()
    station_manager = StationManager()

    # Determine which station to play
    station_id = station or config.default_station

    # Get the station
    station_obj = station_manager.get_station(station_id)
    if not station_obj:
        console.print(
            f"[red]Error:[/red] Station '{station_id}' not found",
            style="bold",
        )
        console.print("\nUse 'lofigirl list' to see available stations")
        sys.exit(1)

    # Create player and load station
    player = AudioPlayer()
    if volume:
        player.set_volume(volume)

    console.print(f"\n[green]Loading:[/green] {station_obj.name}")
    console.print(f"[dim]{station_obj.description}[/dim]\n")

    try:
        player.load_station(station_obj)
        player.play()

        console.print("[green]▶ Playing[/green]", style="bold")
        console.print(f"Volume: {player.get_volume()}%")
        console.print(
            "\n[dim]Note: This is a demo. Actual audio playback not yet implemented.[/dim]"
        )
        console.print("[dim]Press Ctrl+C to stop[/dim]")

        # TODO: Implement actual playback loop with controls
        # For now, just wait for Ctrl+C
        try:
            import time

            while player.is_playing():
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]⏹ Stopping...[/yellow]")
            player.stop()
            player.cleanup()

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        logger.exception("Error during playback")
        sys.exit(1)


@cli.command()
def list() -> None:
    """
    📻 List all available radio stations.

    Shows all stations with their descriptions and IDs.
    """
    station_manager = StationManager()
    stations = station_manager.get_all_stations()

    console.print("\n[bold cyan]Available Lofi Radio Stations[/bold cyan]\n")

    # Create a rich table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=15)
    table.add_column("Name", style="cyan", width=25)
    table.add_column("Genre", style="green", width=15)
    table.add_column("Description", style="white")

    for station in stations:
        table.add_row(
            station.id,
            station.name,
            station.genre,
            station.description,
        )

    console.print(table)
    console.print("\n[dim]Use 'lofigirl play --station <ID>' to play a station[/dim]\n")


@cli.command()
def info() -> None:
    """
    ℹ️  Show application information and configuration.

    Displays current configuration and system information.
    """
    config = get_config()

    console.print("\n[bold cyan]LofiGirl Terminal Information[/bold cyan]\n")

    info_table = Table(show_header=False, box=None)
    info_table.add_column("Key", style="bold")
    info_table.add_column("Value")

    info_table.add_row("Version", __version__)
    info_table.add_row("App Name", config.app_name)
    info_table.add_row("Log Level", config.log_level)
    info_table.add_row("Default Volume", f"{config.default_volume}%")
    info_table.add_row("Audio Quality", config.audio_quality)
    info_table.add_row("Default Station", config.default_station)
    info_table.add_row("Theme", config.theme)
    info_table.add_row("Debug Mode", str(config.debug_mode))

    console.print(info_table)
    console.print()


@cli.command()
@click.option(
    "--station",
    "-s",
    required=True,
    help="Station ID",
)
def station_info(station: str) -> None:
    """
    📡 Show detailed information about a station.

    Examples:
        lofigirl station-info --station lofi-hip-hop
    """
    station_manager = StationManager()
    station_obj = station_manager.get_station(station)

    if not station_obj:
        console.print(
            f"[red]Error:[/red] Station '{station}' not found",
            style="bold",
        )
        sys.exit(1)

    console.print(f"\n[bold cyan]{station_obj.name}[/bold cyan]\n")
    console.print(f"[bold]ID:[/bold] {station_obj.id}")
    console.print(f"[bold]Genre:[/bold] {station_obj.genre}")
    console.print(f"[bold]Description:[/bold] {station_obj.description}")
    console.print(f"[bold]URL:[/bold] [dim]{station_obj.url}[/dim]")
    console.print()


@cli.command()
def tui() -> None:
    """
    🎨 Launch the interactive TUI (Terminal User Interface).

    This opens a beautiful, full-screen terminal interface with:
    - Animated ASCII art
    - Audio waveform visualization
    - Playback controls
    - Keyboard shortcuts

    Keyboard shortcuts:
        SPACE    - Play/Pause
        S        - Stop
        N        - Next station
        P        - Previous station
        M        - Mute/Unmute
        +/-      - Volume up/down
        Y        - Open in YouTube
        Q        - Quit

    Example:
        lofigirl tui
    """
    try:
        from lofigirl_terminal.tui import run_tui

        console.print("\n[cyan]🎵 Starting LofiGirl TUI...[/cyan]\n")
        console.print("[dim]Press 'q' to quit, '?' for help[/dim]\n")

        run_tui()

    except ImportError as e:
        console.print(
            "[red]Error:[/red] Failed to import TUI module",
            style="bold",
        )
        console.print(
            "[yellow]Make sure textual is installed:[/yellow] pip install textual"
        )
        logger.exception(f"Failed to import TUI: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        logger.exception(f"Error running TUI: {e}")
        sys.exit(1)


def main() -> None:
    """
    Main entry point for the application.

    This function is called when the package is run as a script.
    """
    try:
        cli()
    except Exception as e:
        console.print(f"[red]Fatal error:[/red] {str(e)}", style="bold")
        logger.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
