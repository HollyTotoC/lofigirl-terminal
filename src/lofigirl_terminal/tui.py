"""
Textual TUI (Terminal User Interface) for LofiGirl Terminal.

This module provides a beautiful, interactive terminal interface for the
lofi radio player with visualizations, controls, and animations.
"""

import webbrowser
from datetime import datetime
from typing import Any, Optional

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

from lofigirl_terminal.logger import get_logger
from lofigirl_terminal.modules.player_mpv import MPVPlayer, PlayerState
from lofigirl_terminal.modules.stations import StationManager

logger = get_logger(__name__)


LOFI_GIRL_ASCII = """
    ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣾⣿⣷⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀
    ⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀
    ⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
    ⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
    ⢸⣿⣿⣿⡿⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿
    ⣿⣿⡿⠋⠀⠀  ⢀⣀⣀⣀⣀⡀⠀⠀⠀   ⠙⢿⣿⣿⣿⣿
    ⣿⣿⠁⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿
    ⣿⡏⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿
    ⣿⡇⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿
    ⣿⣧⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿
    ⢿⣿⣦⠀⠀⠀⠀⠀⠈⠙⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⡿
    ⠈⢿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⡿⠁
    ⠀⠀⠻⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⠟⠀⠀
    ⠀⠀⠀⠈⠻⢿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠿⠿⠿⠟⠛⠉⠁⠀⠀⠀⠀⠀⠀

      📚 Lofi Girl - Beats to Study/Relax To 🎧
"""


class LofiAsciiArt(Static):
    """
    Animated ASCII art component displaying the Lofi Girl.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.frame = 0

    def on_mount(self) -> None:
        """Set up animation when mounted."""
        self.set_interval(2.0, self.update_animation)

    def update_animation(self) -> None:
        """Update the ASCII art animation (simple frame alternation)."""
        self.frame = (self.frame + 1) % 2
        self.update(self.render_art())

    def render_art(self) -> Panel:
        """Render the ASCII art in a panel."""
        # Add a subtle animation by alternating colors
        style = "cyan" if self.frame == 0 else "blue"
        text = Text(LOFI_GIRL_ASCII, style=style, justify="center")
        return Panel(
            Align.center(text),
            title="🎵 Lofi Girl",
            border_style="bright_cyan",
            padding=(1, 2),
        )

    def render(self) -> Panel:
        """Render the widget."""
        return self.render_art()


class WaveformDisplay(Static):
    """
    Audio waveform visualization widget.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.frame = 0
        self.bars = "▁▂▃▄▅▆▇█"

    def on_mount(self) -> None:
        """Set up animation when mounted."""
        self.set_interval(0.1, self.update_animation)

    def update_animation(self) -> None:
        """Update the waveform animation."""
        self.frame += 1
        self.update(self.render_waveform())

    def render_waveform(self) -> Panel:
        """Render the waveform visualization."""
        # Generate pseudo-random waveform bars
        width = 40
        wave = ""
        for i in range(width):
            # Create a wave effect
            height = (self.frame + i * 3) % len(self.bars)
            wave += self.bars[height]

        text = Text(wave, style="bright_green", justify="center")
        return Panel(
            Align.center(text),
            title="🎵 Audio Visualization",
            border_style="green",
        )

    def render(self) -> Panel:
        """Render the widget."""
        return self.render_waveform()


class StationInfo(Static):
    """
    Widget displaying current station information.
    """

    station_name: reactive[str] = reactive("No Station")
    status: reactive[str] = reactive("Stopped")
    time_info: reactive[str] = reactive("00:00")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def render(self) -> Panel:
        """Render station info."""
        content = Text()
        content.append("🎵 Station: ", style="bold cyan")
        content.append(f"{self.station_name}\n", style="bright_white")
        content.append("📡 Status: ", style="bold cyan")
        content.append(f"{self.status}\n", style="bright_yellow")
        content.append("⏱️  Time: ", style="bold cyan")
        content.append(f"{self.time_info}", style="bright_white")

        return Panel(
            content,
            title="📻 Now Playing",
            border_style="bright_blue",
        )


class ControlPanel(Static):
    """
    Widget with playback controls.
    """

    def compose(self) -> ComposeResult:
        """Create control buttons."""
        with Horizontal(classes="controls"):
            yield Button("⏮️ Prev", id="prev", variant="primary")
            yield Button("⏯️ Play", id="play", variant="success")
            yield Button("⏸️ Pause", id="pause", variant="warning")
            yield Button("⏹️ Stop", id="stop", variant="error")
            yield Button("⏭️ Next", id="next", variant="primary")

        with Horizontal(classes="volume-controls"):
            yield Button("🔇 Mute", id="mute", variant="default")
            yield Button("🔉 Vol-", id="vol_down", variant="default")
            yield Button("🔊 Vol+", id="vol_up", variant="default")
            yield Button("🌐 YouTube", id="youtube", variant="default")


class LofiGirlApp(App):
    """
    Main Textual application for LofiGirl Terminal.
    """

    CSS = """
    Screen {
        background: $surface;
    }

    .controls {
        height: 3;
        dock: top;
        margin: 1;
    }

    .volume-controls {
        height: 3;
        margin: 1;
    }

    Button {
        margin: 0 1;
    }

    #ascii-art {
        height: 20;
        margin: 1;
    }

    #waveform {
        height: 5;
        margin: 1;
    }

    #station-info {
        height: 7;
        margin: 1;
    }
    """

    BINDINGS = [
        ("space", "toggle_play", "Play/Pause"),
        ("s", "stop", "Stop"),
        ("n", "next_station", "Next"),
        ("p", "prev_station", "Previous"),
        ("m", "mute", "Mute"),
        ("+", "volume_up", "Volume Up"),
        ("-", "volume_down", "Volume Down"),
        ("y", "open_youtube", "Open YouTube"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.station_manager = StationManager()
        self.player: Optional[MPVPlayer] = None
        self.current_station_index = 0
        self.stations = self.station_manager.get_all_stations()
        self.start_time: Optional[datetime] = None

    def compose(self) -> ComposeResult:
        """Create the application layout."""
        yield Header()

        yield LofiAsciiArt(id="ascii-art")
        yield WaveformDisplay(id="waveform")
        yield StationInfo(id="station-info")
        yield ControlPanel()

        yield Footer()

    def on_mount(self) -> None:
        """Initialize when app is mounted."""
        self.title = "🎵 LofiGirl Terminal - Lofi Radio Player"

        # Initialize player
        try:
            self.player = MPVPlayer(video_mode=False)
            self.player.set_state_callback(self.on_player_state_change)
            logger.info("Player initialized")
        except Exception as e:
            logger.exception(f"Failed to initialize player: {e}")
            self.notify(
                f"Failed to initialize player: {e}",
                severity="error",
                timeout=10,
            )

        # Update station info display
        self.update_station_info()

        # Set up time update timer
        self.set_interval(1.0, self.update_time)

    def update_station_info(self) -> None:
        """Update the station info widget."""
        station_info = self.query_one("#station-info", StationInfo)

        if self.current_station_index < len(self.stations):
            station = self.stations[self.current_station_index]
            station_info.station_name = station.name
        else:
            station_info.station_name = "No Station"

        if self.player:
            state = self.player.get_state()
            station_info.status = state.value.capitalize()

    def update_time(self) -> None:
        """Update time display."""
        station_info = self.query_one("#station-info", StationInfo)

        if self.player and self.player.is_playing():
            if self.start_time:
                elapsed = datetime.now() - self.start_time
                hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)

                if self.player.is_live_stream():
                    station_info.time_info = (
                        f"{hours:02d}:{minutes:02d}:{seconds:02d} (LIVE)"
                    )
                else:
                    station_info.time_info = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                station_info.time_info = "00:00:00 (LIVE)"
        else:
            station_info.time_info = "--:--:--"
            self.start_time = None

    def on_player_state_change(self, state: PlayerState) -> None:
        """Called when player state changes."""
        self.update_station_info()

        if state == PlayerState.PLAYING and self.start_time is None:
            self.start_time = datetime.now()
        elif state in (PlayerState.STOPPED, PlayerState.ERROR):
            self.start_time = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "play":
            self.action_toggle_play()
        elif button_id == "pause":
            self.action_toggle_play()
        elif button_id == "stop":
            self.action_stop()
        elif button_id == "next":
            self.action_next_station()
        elif button_id == "prev":
            self.action_prev_station()
        elif button_id == "mute":
            self.action_mute()
        elif button_id == "vol_up":
            self.action_volume_up()
        elif button_id == "vol_down":
            self.action_volume_down()
        elif button_id == "youtube":
            self.action_open_youtube()

    def action_toggle_play(self) -> None:
        """Toggle play/pause."""
        if not self.player:
            self.notify("Player not initialized", severity="error")
            return

        try:
            if self.player.is_playing():
                self.player.pause()
                self.notify("⏸️ Paused")
            elif self.player.get_state() == PlayerState.PAUSED:
                self.player.play()
                self.notify("▶️ Resumed")
            else:
                # Load and play current station
                station = self.stations[self.current_station_index]
                self.notify(f"Loading {station.name}...", timeout=5)

                self.player.load_station(station)
                self.player.play()

                self.start_time = datetime.now()
                self.notify(f"▶️ Playing: {station.name}")
        except Exception as e:
            logger.exception(f"Error toggling play: {e}")
            self.notify(f"Error: {e}", severity="error")

    def action_stop(self) -> None:
        """Stop playback."""
        if self.player:
            self.player.stop()
            self.start_time = None
            self.notify("⏹️ Stopped")

    def action_next_station(self) -> None:
        """Play next station."""
        self.current_station_index = (self.current_station_index + 1) % len(
            self.stations
        )
        self.update_station_info()

        if self.player and self.player.is_playing():
            self.player.stop()
            self.action_toggle_play()
        else:
            self.notify(f"Selected: {self.stations[self.current_station_index].name}")

    def action_prev_station(self) -> None:
        """Play previous station."""
        self.current_station_index = (self.current_station_index - 1) % len(
            self.stations
        )
        self.update_station_info()

        if self.player and self.player.is_playing():
            self.player.stop()
            self.action_toggle_play()
        else:
            self.notify(f"Selected: {self.stations[self.current_station_index].name}")

    def action_mute(self) -> None:
        """Toggle mute."""
        if self.player:
            self.player.toggle_mute()
            muted = self.player.muted
            self.notify("🔇 Muted" if muted else "🔊 Unmuted")

    def action_volume_up(self) -> None:
        """Increase volume."""
        if self.player:
            self.player.volume_up(5)
            self.notify(f"🔊 Volume: {self.player.get_volume()}%")

    def action_volume_down(self) -> None:
        """Decrease volume."""
        if self.player:
            self.player.volume_down(5)
            self.notify(f"🔉 Volume: {self.player.get_volume()}%")

    def action_open_youtube(self) -> None:
        """Open current station in YouTube."""
        station = self.stations[self.current_station_index]
        try:
            webbrowser.open(station.url)
            self.notify(f"🌐 Opening {station.name} in browser...")
        except Exception as e:
            logger.exception(f"Failed to open browser: {e}")
            self.notify(f"Failed to open browser: {e}", severity="error")

    async def action_quit(self) -> None:
        """Quit the application."""
        if self.player:
            self.player.cleanup()
        self.exit()


def run_tui() -> None:
    """
    Run the TUI application.

    This is the main entry point for the interactive TUI mode.
    """
    app = LofiGirlApp()
    app.run()


if __name__ == "__main__":
    run_tui()
