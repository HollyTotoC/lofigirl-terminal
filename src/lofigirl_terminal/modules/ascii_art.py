"""
ASCII Art collection for LofiGirl Terminal.

This module provides various ASCII art designs for the TUI with animations.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AsciiArt:
    """
    ASCII art design with metadata.

    Attributes:
        id: Unique identifier
        name: Display name
        description: Brief description
        frames: List of ASCII art frames for animation
        author: Artist credit (optional)
    """

    id: str
    name: str
    description: str
    frames: List[str]
    author: str = "Community"


# Classic Lofi Girl studying
LOFI_GIRL_CLASSIC = AsciiArt(
    id="lofi-girl-classic",
    name="Lofi Girl - Classic",
    description="The iconic lofi girl studying at her desk",
    frames=[
        """
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

          Lofi Girl - Beats to Study/Relax To
""",
        """
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

          Lofi Girl - Beats to Study/Relax To
""",
    ],
    author="Lofi Girl Community",
)

# Minimalist music notes
MUSIC_NOTES = AsciiArt(
    id="music-notes",
    name="Music Notes",
    description="Simple animated music notes floating",
    frames=[
        """
                    ♪
              ♫           ♪
        ♪                      ♫
                  ♫
    ♫                   ♪
              ♪                 ♫

        ╔═══════════════════════════════╗
        ║                               ║
        ║    L O F I   R A D I O        ║
        ║                               ║
        ║    Chill Beats & Vibes        ║
        ║                               ║
        ╚═══════════════════════════════╝

              ♫           ♪
        ♪                      ♫
                  ♪
    ♫                   ♫
""",
        """
              ♫
        ♪                      ♫
                  ♪                 ♪
    ♫                   ♫
              ♪
                          ♫

        ╔═══════════════════════════════╗
        ║                               ║
        ║    L O F I   R A D I O        ║
        ║                               ║
        ║    Chill Beats & Vibes        ║
        ║                               ║
        ╚═══════════════════════════════╝

    ♪                 ♫
              ♫           ♪
                    ♫
        ♪                      ♫
""",
        """
        ♪                 ♫
              ♫           ♪
                    ♫          ♪
        ♪                      ♫
                  ♫
    ♫                   ♪

        ╔═══════════════════════════════╗
        ║                               ║
        ║    L O F I   R A D I O        ║
        ║                               ║
        ║    Chill Beats & Vibes        ║
        ║                               ║
        ╚═══════════════════════════════╝

              ♪
                          ♫
    ♫                   ♫
              ♫           ♪
""",
    ],
    author="LofiGirl Terminal",
)

# Vinyl record spinning
VINYL_RECORD = AsciiArt(
    id="vinyl-record",
    name="Vinyl Record",
    description="Classic vinyl record spinning animation",
    frames=[
        """
              ████████████
          ████░░░░░░░░░░████
        ██░░░░░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
    ██░░░░░░░░████░░░░░░░░░░░░██
    ██░░░░░░██    ██░░░░░░░░░░██
    ██░░░░██        ██░░░░░░░░██
    ██░░██            ██░░░░░░██
    ██░░██    ●●●●    ██░░░░░░██
    ██░░░░██        ██░░░░░░░░██
    ██░░░░░░██    ██░░░░░░░░░░██
    ██░░░░░░░░████░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
        ██░░░░░░░░░░░░░░░░██
          ████░░░░░░░░░░████
              ████████████

           Now Spinning...
""",
        """
              ████████████
          ████░░░░░░░░░░████
        ██░░░░░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
    ██░░░░░░████░░░░░░░░░░░░░░██
    ██░░░░██    ██░░░░░░░░░░░░██
    ██░░██        ██░░░░░░░░░░██
    ██░░██          ██░░░░░░░░██
    ██░░██    ●●●●  ██░░░░░░░░██
    ██░░░░██        ██░░░░░░░░██
    ██░░░░░░██    ██░░░░░░░░░░██
    ██░░░░░░░░████░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
        ██░░░░░░░░░░░░░░░░██
          ████░░░░░░░░░░████
              ████████████

           Now Spinning...
""",
        """
              ████████████
          ████░░░░░░░░░░████
        ██░░░░░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
    ██░░░░░░░░████░░░░░░░░░░░░██
    ██░░░░░░██    ██░░░░░░░░░░██
    ██░░░░██        ██░░░░░░░░██
    ██░░░░██          ██░░░░░░██
    ██░░░░██  ●●●●    ██░░░░░░██
    ██░░░░░░██        ██░░░░░░██
    ██░░░░░░░░██    ██░░░░░░░░██
    ██░░░░░░░░░░████░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
        ██░░░░░░░░░░░░░░░░██
          ████░░░░░░░░░░████
              ████████████

           Now Spinning...
""",
        """
              ████████████
          ████░░░░░░░░░░████
        ██░░░░░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
    ██░░░░░░░░░░████░░░░░░░░░░██
    ██░░░░░░░░██    ██░░░░░░░░██
    ██░░░░░░██        ██░░░░░░██
    ██░░░░░░██          ██░░░░██
    ██░░░░░░██    ●●●●  ██░░░░██
    ██░░░░░░░░██        ██░░░░██
    ██░░░░░░░░░░██    ██░░░░░░██
    ██░░░░░░░░░░░░████░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░██
        ██░░░░░░░░░░░░░░░░██
          ████░░░░░░░░░░████
              ████████████

           Now Spinning...
""",
    ],
    author="LofiGirl Terminal",
)

# Cassette tape
CASSETTE_TAPE = AsciiArt(
    id="cassette-tape",
    name="Cassette Tape",
    description="Retro cassette tape with spinning reels",
    frames=[
        """
    ╔═══════════════════════════════════╗
    ║  ╔═════════════════════════════╗  ║
    ║  ║  L O F I   M I X   T A P E  ║  ║
    ║  ╚═════════════════════════════╝  ║
    ║                                   ║
    ║   ┌──────┐           ┌──────┐    ║
    ║   │ ●──● │           │ ●──● │    ║
    ║   │ │  │ │           │ │  │ │    ║
    ║   │ ●──● │           │ ●──● │    ║
    ║   └──────┘           └──────┘    ║
    ║                                   ║
    ║  ═══════════════════════════════  ║
    ║                                   ║
    ║    [■]  [▶]  [●]  [◀◀]  [▶▶]     ║
    ╚═══════════════════════════════════╝

           Side A - Chill Vibes
""",
        """
    ╔═══════════════════════════════════╗
    ║  ╔═════════════════════════════╗  ║
    ║  ║  L O F I   M I X   T A P E  ║  ║
    ║  ╚═════════════════════════════╝  ║
    ║                                   ║
    ║   ┌──────┐           ┌──────┐    ║
    ║   │ ●●─● │           │ ●─●● │    ║
    ║   │ ││ │ │           │ │ ││ │    ║
    ║   │ ●──● │           │ ●──● │    ║
    ║   └──────┘           └──────┘    ║
    ║                                   ║
    ║  ═══════════════════════════════  ║
    ║                                   ║
    ║    [■]  [▶]  [●]  [◀◀]  [▶▶]     ║
    ╚═══════════════════════════════════╝

           Side A - Chill Vibes
""",
    ],
    author="LofiGirl Terminal",
)

# Simple wave pattern
WAVE_PATTERN = AsciiArt(
    id="wave-pattern",
    name="Wave Pattern",
    description="Smooth wave animation",
    frames=[
        """

    ～～～～～～～～～～～～～～～～～～～～～

         L O F I   W A V E S

    ～～～～～～～～～～～～～～～～～～～～～

         ╔═══════════════════╗
         ║                   ║
         ║  Relax & Unwind   ║
         ║                   ║
         ╚═══════════════════╝

    ～～～～～～～～～～～～～～～～～～～～～

         Smooth Beats Playing

    ～～～～～～～～～～～～～～～～～～～～～
""",
        """
    ～～～～～～～～～～～～～～～～～～～～～


         L O F I   W A V E S
    ～～～～～～～～～～～～～～～～～～～～～

         ╔═══════════════════╗
         ║                   ║
         ║  Relax & Unwind   ║
         ║                   ║
         ╚═══════════════════╝

    ～～～～～～～～～～～～～～～～～～～～～
         Smooth Beats Playing


    ～～～～～～～～～～～～～～～～～～～～～
""",
        """

    ～～～～～～～～～～～～～～～～～～～～～

         L O F I   W A V E S

    ～～～～～～～～～～～～～～～～～～～～～
         ╔═══════════════════╗
         ║                   ║
         ║  Relax & Unwind   ║
         ║                   ║
         ╚═══════════════════╝
    ～～～～～～～～～～～～～～～～～～～～～

         Smooth Beats Playing
    ～～～～～～～～～～～～～～～～～～～～～

""",
    ],
    author="LofiGirl Terminal",
)

# Headphones
HEADPHONES = AsciiArt(
    id="headphones",
    name="Headphones",
    description="Headphones with sound waves",
    frames=[
        """
            ╭─────────────╮
           ╱               ╲
          │    ♪  ♫  ♪    │
          │                │
           ╲               ╱
            ╰─────────────╯
             │           │
             │           │
            ┌┴─────────┴┐
            │ ♫ ♪ ♫ ♪ ♫ │
            │           │
            │  LOFI ON  │
            │           │
            │ ♪ ♫ ♪ ♫ ♪ │
            └───────────┘

        Headphones On, World Off
""",
        """
            ╭─────────────╮
           ╱               ╲
          │  ♪  ♫  ♪  ♫  │
          │                │
           ╲               ╱
            ╰─────────────╯
             │           │
             │           │
            ┌┴─────────┴┐
            │ ♪ ♫ ♪ ♫ ♪ │
            │           │
            │  LOFI ON  │
            │           │
            │ ♫ ♪ ♫ ♪ ♫ │
            └───────────┘

        Headphones On, World Off
""",
    ],
    author="LofiGirl Terminal",
)

# Piano keys
PIANO_KEYS = AsciiArt(
    id="piano-keys",
    name="Piano Keys",
    description="Piano keyboard with notes",
    frames=[
        """
        ┌──┬──┬─┬──┬──┬──┬──┬─┬──┬──┬─┬──┬──┐
        │  │▓▓│ │▓▓│  │  │▓▓│ │▓▓│  │ │▓▓│  │
        │  │▓▓│ │▓▓│  │  │▓▓│ │▓▓│  │ │▓▓│  │
        │  └──┘ └──┘  │  └──┘ └──┘  │ └──┘  │
        │  ♪           │      ♫      │       │
        │              │             │       │
        └──────────────┴─────────────┴───────┘

        ╔════════════════════════════════════╗
        ║                                    ║
        ║      L O F I   P I A N O           ║
        ║                                    ║
        ║      Smooth Jazz & Beats           ║
        ║                                    ║
        ╚════════════════════════════════════╝
""",
        """
        ┌──┬──┬─┬──┬──┬──┬──┬─┬──┬──┬─┬──┬──┐
        │  │▓▓│ │▓▓│  │  │▓▓│ │▓▓│  │ │▓▓│  │
        │  │▓▓│ │▓▓│  │  │▓▓│ │▓▓│  │ │▓▓│  │
        │  └──┘ └──┘  │  └──┘ └──┘  │ └──┘  │
        │      ♫       │  ♪          │       │
        │              │             │       │
        └──────────────┴─────────────┴───────┘

        ╔════════════════════════════════════╗
        ║                                    ║
        ║      L O F I   P I A N O           ║
        ║                                    ║
        ║      Smooth Jazz & Beats           ║
        ║                                    ║
        ╚════════════════════════════════════╝
""",
    ],
    author="LofiGirl Terminal",
)

# Coffee cup
COFFEE_CUP = AsciiArt(
    id="coffee-cup",
    name="Coffee Cup",
    description="Steaming coffee cup for coding sessions",
    frames=[
        """
              (  )   (   )  )
               ) (   )  (  (
               ( )  (    ) )
               _____________
              <_____________> ___
              |             |/ _ \\
              |   LOFI      | | | |
              |   COFFEE    |_| | |
          ___|             |\\___/
         /    \\___________/    \\
         \\_____________________/

        ╔════════════════════════════╗
        ║  Code Better with Coffee   ║
        ║     & Lofi Beats           ║
        ╚════════════════════════════╝
""",
        """
               (  )   (   )  )
              ) (   )  (  (
               ( )  (    ) )
               _____________
              <_____________> ___
              |             |/ _ \\
              |   LOFI      | | | |
              |   COFFEE    |_| | |
          ___|             |\\___/
         /    \\___________/    \\
         \\_____________________/

        ╔════════════════════════════╗
        ║  Code Better with Coffee   ║
        ║     & Lofi Beats           ║
        ╚════════════════════════════╝
""",
    ],
    author="LofiGirl Terminal",
)

# All available ASCII arts
ASCII_ARTS: Dict[str, AsciiArt] = {
    "lofi-girl-classic": LOFI_GIRL_CLASSIC,
    "music-notes": MUSIC_NOTES,
    "vinyl-record": VINYL_RECORD,
    "cassette-tape": CASSETTE_TAPE,
    "wave-pattern": WAVE_PATTERN,
    "headphones": HEADPHONES,
    "piano-keys": PIANO_KEYS,
    "coffee-cup": COFFEE_CUP,
}

# Default ASCII art
DEFAULT_ASCII_ART = "lofi-girl-classic"


def get_ascii_art(art_id: str) -> AsciiArt:
    """
    Get ASCII art by ID.

    Args:
        art_id: ID of the ASCII art

    Returns:
        AsciiArt object, or default if not found
    """
    return ASCII_ARTS.get(art_id, ASCII_ARTS[DEFAULT_ASCII_ART])


def list_ascii_arts() -> List[str]:
    """
    Get list of all available ASCII art IDs.

    Returns:
        List of ASCII art IDs
    """
    return list(ASCII_ARTS.keys())
