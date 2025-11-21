# CLAUDE.md - LofiGirl Terminal Project Tracker

## 📻 Project Overview
**LofiGirl Terminal** is a cross-platform terminal-based lofi radio player that brings the relaxing vibes of lofi music to your command line. Inspired by the popular "lofi girl" YouTube streams, this project provides a beautiful, minimalist terminal interface for streaming lofi music while you code, study, or relax.

**🆕 MAJOR UPDATE**: Project migrated from Python to Node.js/TypeScript for superior cross-platform support!

## 🎯 Project Goals
- ✅ Create an accessible, easy-to-use terminal music player
- ✅ Support multiple lofi radio stations/streams
- ✅ Provide a beautiful terminal UI with visualizations
- ✅ True cross-platform: PowerShell (Windows), Terminal (Mac/Linux)
- ✅ Keep dependencies minimal and code clean
- ✅ Build a welcoming community-driven project

## 🏗️ Architecture Decisions

### Technology Stack (Updated 2025-11)
- **Language**: Node.js/TypeScript 5.3+ (universal, easy for contributors)
- **Audio**: node-mpv (MPV media player bindings)
- **UI**: blessed (cross-platform TUI library)
- **CLI**: Commander.js (command-line interface)
- **Terminal Output**: chalk, cli-table3, boxen (rich formatting)
- **Package Management**: npm (universal across all platforms)

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

### Phase 1: Foundation ✅
- [x] Repository creation
- [x] Project structure setup (TypeScript)
- [x] Basic configuration files (package.json, tsconfig.json)
- [x] Development environment setup
- [x] Documentation framework

### Phase 2: Core Features ✅
- [x] Audio streaming functionality (node-mpv)
- [x] Basic playback controls (play/pause/stop)
- [x] Multiple station support (4 stations)
- [x] Configuration management (dotenv + zod)
- [x] Error handling and logging (winston)

### Phase 3: User Interface ✅
- [x] CLI interface (Commander.js)
- [x] Terminal UI design (blessed)
- [x] Interactive controls (keyboard shortcuts)
- [x] Visual feedback (status, volume, etc.)
- [x] Keyboard shortcuts (SPACE, N, P, M, +/-, Q)

### Phase 4: Cross-Platform Support ✅
- [x] PowerShell installer (install-node.ps1)
- [x] Bash installer (install-node.sh)
- [x] Windows compatibility
- [x] Mac/Linux compatibility
- [x] Universal npm package

### Phase 5: Enhancement (In Progress)
- [x] Volume control
- [x] Station management
- [ ] Audio visualizations (advanced)
- [ ] Playlist/favorites system
- [ ] YouTube integration (ytdl-core)

### Phase 6: Community & Polish (Planned)
- [x] Cross-platform testing
- [x] Contribution guidelines
- [x] User documentation
- [ ] npm package publication
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Release automation
- [ ] Windows Store / Homebrew packages

## 🔧 Technical Decisions Log

### Decision 4: Migration to Node.js/TypeScript ⭐
**Date**: 2025-11-21
**Decision**: Migrate from Python to Node.js/TypeScript
**Rationale**:
- **Better cross-platform**: npm works identically on Windows, Mac, Linux
- **PowerShell first-class**: Native support without workarounds
- **Simpler installation**: No virtual environments needed
- **Global CLI support**: `npm install -g` works everywhere
- **Type safety**: TypeScript provides better DX than Python+mypy
- **Active ecosystem**: Larger package ecosystem and community
- **Windows support**: No more libmpv-2.dll issues

**Migration completed**: All core features ported successfully! ✅

### Decision 3: Dependency Management (Updated)
**Date**: 2025-11-21
**Approach**: npm with package.json
**Rationale**:
- Universal across all platforms
- No virtual environments needed
- Lock files (package-lock.json) ensure reproducibility
- Global install support built-in

### Decision 2: Code Quality Tools (Updated)
**Date**: 2025-11-21
**Tools Selected**:
- `eslint`: Linting with TypeScript support
- `prettier`: Code formatting
- `typescript`: Type checking (built-in)
- `jest`: Testing framework
- `ts-node`: Development execution

**Rationale**: Modern JavaScript/TypeScript tooling standard

### Decision 1: Project Structure (Updated)
**Date**: 2025-11-21
**Decision**: TypeScript src layout with dist output
**Rationale**:
- Clean separation of source and compiled code
- Professional standard for npm packages
- Better for npm/global distribution
- TypeScript declaration files for better IDE support

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
