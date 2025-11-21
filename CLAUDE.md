# CLAUDE.md - LofiGirl Terminal Project Tracker

## 📻 Project Overview
**LofiGirl Terminal** is a terminal-based lofi radio player that brings the relaxing vibes of lofi music to your command line. Inspired by the popular "lofi girl" YouTube streams, this project aims to create a beautiful, minimalist terminal interface for streaming lofi music while you code, study, or relax.

## 🎯 Project Goals
- Create an accessible, easy-to-use terminal music player
- Support multiple lofi radio stations/streams
- Provide a beautiful terminal UI with visualizations
- Keep dependencies minimal and code clean
- Build a welcoming community-driven project

## 🏗️ Architecture Decisions

### Technology Stack
- **Language**: Python 3.8+ (widely accessible, easy for contributors)
- **Audio**: Will need audio streaming library (mpv, vlc, or pygame)
- **UI**: Terminal UI library (Rich, Textual, or Curses)
- **Package Management**: Poetry or pip with requirements files

### Project Type
- **CLI Application** with potential for:
  - Interactive TUI (Text User Interface)
  - Simple command-line arguments for quick playback
  - Configuration file support

### Target Users
- Developers who want background music while coding
- Students studying with lofi beats
- Anyone who prefers terminal-based tools

## 📋 Development Phases

### Phase 1: Foundation (Current)
- [x] Repository creation
- [ ] Project structure setup
- [ ] Basic configuration files
- [ ] Development environment setup
- [ ] CI/CD pipeline
- [ ] Documentation framework

### Phase 2: Core Features
- [ ] Audio streaming functionality
- [ ] Basic playback controls (play/pause/stop)
- [ ] Multiple station support
- [ ] Configuration management
- [ ] Error handling and logging

### Phase 3: User Interface
- [ ] Terminal UI design
- [ ] Interactive controls
- [ ] Visual feedback (now playing, volume, etc.)
- [ ] Keyboard shortcuts

### Phase 4: Enhancement
- [ ] Audio visualizations
- [ ] Playlist/favorites system
- [ ] Volume control
- [ ] Station management

### Phase 5: Community & Polish
- [ ] Cross-platform testing
- [ ] Installation via pip/pipx
- [ ] Contribution guidelines
- [ ] User documentation
- [ ] Release automation

## 🔧 Technical Decisions Log

### Decision 1: Project Structure
**Date**: 2025-11-21
**Decision**: Use src layout for better package isolation
**Rationale**:
- Prevents accidental imports from development directory
- Professional standard for Python packages
- Better for eventual PyPI distribution

### Decision 2: Code Quality Tools
**Date**: 2025-11-21
**Tools Selected**:
- `black`: Code formatting (PEP 8 compliant)
- `flake8`: Linting and style checking
- `mypy`: Static type checking
- `pytest`: Testing framework
- `coverage`: Code coverage reporting
- `pre-commit`: Automated quality checks

**Rationale**: Industry standard tools that ensure code quality and consistency across contributors

### Decision 3: Dependency Management
**Date**: 2025-11-21
**Approach**: Requirements files (base/dev/prod)
**Rationale**:
- Simpler for beginners to understand
- No additional tool installation needed
- Can migrate to Poetry later if needed

## 🤝 Collaboration Guidelines

### For New Contributors
1. **Read the Documentation**: Start with README.md
2. **Check Issues**: Look for "good first issue" labels
3. **Ask Questions**: Use discussions or issues for clarification
4. **Follow Standards**: Code must pass pre-commit hooks
5. **Write Tests**: New features need test coverage

### Code Standards
- **Type Hints**: Use type annotations for all functions
- **Docstrings**: Google-style docstrings for all public functions
- **Testing**: Minimum 80% code coverage
- **Formatting**: Auto-formatted by black
- **Commits**: Conventional commits format (feat:, fix:, docs:, etc.)

### Review Process
- All PRs require at least one review
- CI must pass (tests, linting, type checking)
- Documentation must be updated if needed

## 📝 Current Sprint Tasks

### Setup & Configuration
- [ ] Create complete project structure
- [ ] Set up virtual environment
- [ ] Configure all quality tools
- [ ] Write initial tests
- [ ] Set up CI/CD
- [ ] Write comprehensive README

### Next Steps
- [ ] Research audio streaming libraries
- [ ] Design CLI interface
- [ ] Plan station configuration format
- [ ] Create project roadmap

## 🐛 Known Issues & Blockers
None yet - just getting started!

## 💡 Ideas & Future Considerations

### Potential Features
- Support for local music files
- Pomodoro timer integration
- Integration with notification systems
- Plugin system for extensibility
- Multiple themes/color schemes
- Music scrobbling (Last.fm)
- Recording functionality
- Sleep timer

### Technical Improvements
- Async audio streaming for better performance
- Caching for offline playback
- Configuration sync across devices
- Telemetry (opt-in) for improving UX

## 📚 Resources & References

### Useful Libraries to Research
- **Audio**: `python-mpv`, `python-vlc`, `pygame`, `pydub`
- **TUI**: `rich`, `textual`, `blessed`, `curses`
- **HTTP Streaming**: `requests`, `httpx`, `aiohttp`
- **Config**: `python-dotenv`, `pydantic`, `configparser`

### Similar Projects for Inspiration
- `mpv`: Command-line media player
- `youtube-dl`: CLI video/audio downloader
- `spotify-tui`: Terminal Spotify client
- Various lofi YouTube streams

## 🎓 Learning Resources for Contributors

### Python Basics
- Official Python Tutorial: https://docs.python.org/3/tutorial/
- Real Python: https://realpython.com/

### Testing
- Pytest Documentation: https://docs.pytest.org/
- Testing Best Practices: https://realpython.com/pytest-python-testing/

### Audio Programming
- Python Audio Libraries: https://wiki.python.org/moin/Audio/
- Working with Audio: https://realpython.com/playing-and-recording-sound-python/

## 📅 Version History

### v0.1.0 (Planned - Initial Setup)
- Project structure
- Basic configuration
- Development environment
- Documentation foundation

---

**Last Updated**: 2025-11-21
**Current Phase**: Phase 1 - Foundation
**Contributors**: Starting with community contributions!

## 🎯 Quick Start for Developers

```bash
# Clone the repository
git clone https://github.com/[username]/lofigirl-terminal.git
cd lofigirl-terminal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install-dev

# Run tests
make test

# Run the application
make run
```

## 📞 Contact & Community

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Contributing**: See CONTRIBUTING.md (to be created)

---

*This file is maintained by Claude and the community. Feel free to suggest improvements!*
