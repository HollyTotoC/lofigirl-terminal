"""
Rice-style TUI (Terminal User Interface) for LofiGirl Terminal.

Compact, beautiful interface inspired by btop and other rice terminals.
Features: ASCII art, audio visualization, minimal controls, clean design.
"""

import random
import webbrowser
from datetime import datetime
from typing import Any, Optional

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Label, Static

from lofigirl_terminal.config import get_config
from lofigirl_terminal.logger import get_logger
from lofigirl_terminal.modules.ascii_art import AsciiArt, get_ascii_art
from lofigirl_terminal.modules.player_mpv import MPVPlayer, PlayerState
from lofigirl_terminal.modules.stations import Station, StationManager
from lofigirl_terminal.modules.themes import ColorPalette, get_theme

logger = get_logger(__name__)


class CompactAsciiArt(Static):
    """Compact animated ASCII art - rice style."""

    def __init__(
        self, theme: ColorPalette, ascii_art: AsciiArt, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.theme = theme
        self.ascii_art = ascii_art
        self.current_frame = 0
        self.num_frames = len(ascii_art.frames)

    def on_mount(self) -> None:
        """Set up animation."""
        interval = 0.8 if self.num_frames > 2 else 2.0
        self.set_interval(interval, self.update_animation)

    def update_animation(self) -> None:
        """Cycle through frames."""
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.update(self.render_art())

    def render_art(self) -> Text:
        """Render compact ASCII art."""
        color = (
            self.theme.accent
            if self.current_frame % 2 == 0
            else self.theme.secondary
        )
        return Text(
            self.ascii_art.frames[self.current_frame],
            style=color,
            justify="center",
        )

    def render(self) -> Text:
        """Render the widget."""
        return self.render_art()


class CompactWaveform(Static):
    """Compact audio waveform visualization - rice style."""

    def __init__(self, theme: ColorPalette, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.theme = theme
        self.bars = [0] * 40  # 40 bars for visualization

    def on_mount(self) -> None:
        """Start waveform animation."""
        self.set_interval(0.05, self.update_waveform)

    def update_waveform(self) -> None:
        """Update waveform bars with random values (simulated)."""
        # Simulate audio by smoothly transitioning bars
        for i in range(len(self.bars)):
            target = random.uniform(0.3, 1.0)
            self.bars[i] = self.bars[i] * 0.7 + target * 0.3

        self.update(self.render_waveform())

    def render_waveform(self) -> Text:
        """Render compact waveform."""
        blocks = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        waveform = ""

        for bar in self.bars:
            block_idx = min(int(bar * len(blocks)), len(blocks) - 1)
            waveform += blocks[block_idx]

        return Text(waveform, style=self.theme.accent, justify="center")

    def render(self) -> Text:
        """Render the widget."""
        return self.render_waveform()


class CompactInfo(Static):
    """Compact info panel - btop style."""

    station_name: reactive[str] = reactive("No Station")
    state: reactive[str] = reactive("●")
    volume: reactive[int] = reactive(50)
    elapsed_time: reactive[str] = reactive("00:00")

    def __init__(self, theme: ColorPalette, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.theme = theme

    def on_mount(self) -> None:
        """Start time update."""
        self.set_interval(1.0, self.update_time)

    def update_time(self) -> None:
        """Update elapsed time."""
        # This would be connected to the actual player
        # For now, just increment
        parts = self.elapsed_time.split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
        seconds += 1
        if seconds >= 60:
            seconds = 0
            minutes += 1
        self.elapsed_time = f"{minutes:02d}:{seconds:02d}"

    def render(self) -> Text:
        """Render compact info."""
        info = Text()

        # Station line
        info.append("♫ ", style=self.theme.accent)
        info.append(self.station_name, style=self.theme.text)
        info.append("\n")

        # Status line
        state_color = "green" if self.state == "▶" else "yellow"
        info.append(f"{self.state} ", style=state_color)
        info.append(f"{self.elapsed_time}", style=self.theme.text_dim)
        info.append(" │ ", style=self.theme.border)

        # Volume bar
        volume_blocks = int(self.volume / 10)
        volume_bar = "━" * volume_blocks + "╸" + "─" * (10 - volume_blocks)
        info.append(f"🔊 {volume_bar} {self.volume}%", style=self.theme.secondary)

        return info


class CompactControls(Static):
    """Compact control panel - one-line rice style."""

    def __init__(self, theme: ColorPalette, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.theme = theme

    def compose(self) -> ComposeResult:
        """Compose the control buttons."""
        with Horizontal(id="controls"):
            yield Button("◀◀", id="prev", variant="primary")
            yield Button("▶/⏸", id="play_pause", variant="success")
            yield Button("⏹", id="stop", variant="error")
            yield Button("▶▶", id="next", variant="primary")
            yield Button("🔇", id="mute", variant="default")
            yield Button("─", id="vol_down", variant="default")
            yield Button("+", id="vol_up", variant="default")
            yield Button("🌐", id="youtube", variant="default")


class RiceLofiApp(App):
    """
    Rice-style LofiGirl Terminal Application.

    Compact, beautiful, minimal design inspired by btop.
    """

    CSS = """
    Screen {
        background: $surface;
    }

    #main_container {
        height: 100%;
        padding: 1;
    }

    #ascii_art {
        height: auto;
        max-height: 30;
        border: round $primary;
        padding: 1 2;
        margin-bottom: 1;
    }

    #waveform {
        height: 3;
        border: round $accent;
        padding: 0 1;
        margin-bottom: 1;
    }

    #info {
        height: auto;
        border: round $secondary;
        padding: 1 2;
        margin-bottom: 1;
    }

    #controls {
        height: auto;
        align: center middle;
        margin-bottom: 1;
    }

    #controls Button {
        min-width: 6;
        margin: 0 1;
    }

    #help_text {
        height: auto;
        text-align: center;
        color: $text-muted;
        padding: 1;
    }

    Footer {
        background: $primary-background-lighten-1;
    }

    Header {
        background: $primary-background-lighten-1;
        color: $text;
    }
    """

    BINDINGS = [
        ("space", "play_pause", "Play/Pause"),
        ("s", "stop", "Stop"),
        ("n", "next_station", "Next Station"),
        ("p", "prev_station", "Prev Station"),
        ("m", "toggle_mute", "Mute"),
        ("+", "volume_up", "Vol+"),
        ("-", "volume_down", "Vol-"),
        ("y", "open_youtube", "YouTube"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.config = get_config()

        # Load theme
        self.theme = get_theme(self.config.theme)

        # Load ASCII art
        self.ascii_art = get_ascii_art(self.config.ascii_art)

        # Initialize player and station manager
        self.player: Optional[MPVPlayer] = None
        self.station_manager = StationManager()
        self.current_station: Optional[Station] = None
        self.current_station_index = 0
        self.stations = self.station_manager.get_all_stations()

        logger.info("RiceLofiApp initialized")

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header(show_clock=True)

        with VerticalScroll(id="main_container"):
            yield CompactAsciiArt(self.theme, self.ascii_art, id="ascii_art")
            yield CompactWaveform(self.theme, id="waveform")
            yield CompactInfo(self.theme, id="info")
            yield CompactControls(self.theme, id="controls")
            yield Label(
                "SPACE: play/pause │ N/P: next/prev │ +/-: volume │ Y: youtube │ Q: quit",
                id="help_text",
            )

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application."""
        self.title = "🎵 LofiGirl Terminal - Rice Edition"

        # Set theme colors
        self.design.update({
            "primary": self.theme.primary,
            "secondary": self.theme.secondary,
            "accent": self.theme.accent,
            "surface": self.theme.background,
            "text": self.theme.text,
            "text-muted": self.theme.text_dim,
            "primary-background-lighten-1": self.theme.surface,
        })

        # Initialize player
        try:
            self.player = MPVPlayer(video_mode=False)
            logger.info("MPV Player initialized")

            # Load first station
            if self.stations:
                self.load_station(0)
        except Exception as e:
            logger.exception(f"Failed to initialize player: {e}")
            self.notify(f"Player error: {e}", severity="error", timeout=5)

    def load_station(self, index: int, auto_play: bool = False) -> None:
        """Load a station by index and optionally start playback.

        Args:
            index: Station index to load
            auto_play: If True, automatically start playback after loading
        """
        if not self.stations or not self.player:
            return

        self.current_station_index = index % len(self.stations)
        self.current_station = self.stations[self.current_station_index]

        try:
            self.player.load_station(self.current_station)
            info = self.query_one("#info", CompactInfo)
            info.station_name = self.current_station.name

            if auto_play:
                # Automatically start playback
                self.player.play()
                info.state = "▶"
                logger.info(f"Loaded and playing station: {self.current_station.name}")
            else:
                info.state = "●"
                logger.info(f"Loaded station: {self.current_station.name}")
        except Exception as e:
            logger.exception(f"Failed to load station: {e}")
            self.notify(f"Failed to load station: {e}", severity="error")

    @on(Button.Pressed, "#play_pause")
    def action_play_pause(self) -> None:
        """Toggle play/pause."""
        if not self.player:
            return

        try:
            if self.player.is_playing():
                self.player.pause()
                info = self.query_one("#info", CompactInfo)
                info.state = "⏸"
                self.notify("Paused", timeout=1)
            else:
                self.player.play()
                info = self.query_one("#info", CompactInfo)
                info.state = "▶"
                self.notify("Playing", timeout=1)
        except Exception as e:
            logger.exception(f"Play/pause error: {e}")
            self.notify(f"Error: {e}", severity="error")

    @on(Button.Pressed, "#stop")
    def action_stop(self) -> None:
        """Stop playback."""
        if not self.player:
            return

        try:
            self.player.stop()
            info = self.query_one("#info", CompactInfo)
            info.state = "⏹"
            info.elapsed_time = "00:00"
            self.notify("Stopped", timeout=1)
        except Exception as e:
            logger.exception(f"Stop error: {e}")

    @on(Button.Pressed, "#next")
    def action_next_station(self) -> None:
        """Next station."""
        if not self.player:
            return

        # Remember if we were playing
        was_playing = self.player.is_playing()

        # Stop current playback if playing
        if was_playing:
            self.player.stop()

        # Load next station and auto-play if we were playing
        self.load_station(self.current_station_index + 1, auto_play=was_playing)

        self.notify(
            f"→ {self.current_station.name if self.current_station else 'Unknown'}",
            timeout=2,
        )

    @on(Button.Pressed, "#prev")
    def action_prev_station(self) -> None:
        """Previous station."""
        if not self.player:
            return

        # Remember if we were playing
        was_playing = self.player.is_playing()

        # Stop current playback if playing
        if was_playing:
            self.player.stop()

        # Load previous station and auto-play if we were playing
        self.load_station(self.current_station_index - 1, auto_play=was_playing)

        self.notify(
            f"← {self.current_station.name if self.current_station else 'Unknown'}",
            timeout=2,
        )

    @on(Button.Pressed, "#mute")
    def action_toggle_mute(self) -> None:
        """Toggle mute."""
        if not self.player:
            return

        try:
            self.player.toggle_mute()
            status = "Muted 🔇" if self.player.muted else "Unmuted 🔊"
            self.notify(status, timeout=1)
        except Exception as e:
            logger.exception(f"Mute error: {e}")

    @on(Button.Pressed, "#vol_up")
    def action_volume_up(self) -> None:
        """Increase volume."""
        if not self.player:
            return

        try:
            self.player.volume_up()
            info = self.query_one("#info", CompactInfo)
            info.volume = self.player.get_volume()
            self.notify(f"Vol: {info.volume}%", timeout=0.5)
        except Exception as e:
            logger.exception(f"Volume up error: {e}")

    @on(Button.Pressed, "#vol_down")
    def action_volume_down(self) -> None:
        """Decrease volume."""
        if not self.player:
            return

        try:
            self.player.volume_down()
            info = self.query_one("#info", CompactInfo)
            info.volume = self.player.get_volume()
            self.notify(f"Vol: {info.volume}%", timeout=0.5)
        except Exception as e:
            logger.exception(f"Volume down error: {e}")

    @on(Button.Pressed, "#youtube")
    def action_open_youtube(self) -> None:
        """Open current station in YouTube."""
        if not self.current_station:
            self.notify("No station loaded", severity="warning")
            return

        try:
            webbrowser.open(self.current_station.url)
            self.notify(f"Opening {self.current_station.name} in browser...", timeout=2)
        except Exception as e:
            logger.exception(f"Failed to open browser: {e}")
            self.notify(f"Error: {e}", severity="error")

    def action_quit(self) -> None:
        """Quit the application."""
        if self.player:
            self.player.cleanup()
        self.exit()


def run_rice_tui() -> None:
    """Run the rice-style TUI application."""
    app = RiceLofiApp()
    app.run()


if __name__ == "__main__":
    run_rice_tui()
