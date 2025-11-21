# 📦 Python Version - Archived

## Notice

The **Python version** of LofiGirl Terminal has been **archived** and replaced with a **Node.js/TypeScript** version for better cross-platform support.

### Migration Date
**November 21, 2025**

### Reason for Migration
The project was migrated from Python to Node.js/TypeScript to provide:
- ✅ Better cross-platform support (Windows/Mac/Linux)
- ✅ Native PowerShell compatibility
- ✅ Simpler installation (no virtual environments)
- ✅ Universal npm package manager
- ✅ Modern TypeScript with built-in type safety

---

## Archived Python Files

The following Python files are **no longer used** but kept for historical reference:

### Configuration Files
- `pyproject.toml` - Python project configuration
- `setup.py` - Python package setup
- `Makefile` - Python build commands
- `.pre-commit-config.yaml` - Python pre-commit hooks (if any)
- `.flake8` - Python linting config

### Dependencies
- `requirements/` - Python dependencies directory
  - `requirements/base.txt`
  - `requirements/dev.txt`
  - `requirements/prod.txt`

### Source Code
- `src/lofigirl_terminal/` - Python source code (archived)
  - All `.py` files in this directory are no longer active

### Installers (Old)
- `install.ps1` - Old Python PowerShell installer
- `install.sh` - Old Python bash installer
- `uninstall.sh` - Old Python uninstaller

---

## New Node.js/TypeScript Files

The active codebase now uses:

### Configuration
- `package.json` - npm configuration ✅
- `tsconfig.json` - TypeScript config ✅
- `.eslintrc.json` - ESLint config ✅
- `.prettierrc.json` - Prettier config ✅

### Source Code
- `src/` - TypeScript source (`.ts` files) ✅
- `dist/` - Compiled JavaScript (gitignored) ✅

### Installers (New)
- `install-node.ps1` - Node.js PowerShell installer ✅
- `install-node.sh` - Node.js bash installer ✅

---

## For Users

If you're **still using the Python version**, please migrate to Node.js:

### Migration Steps

1. **Uninstall Python version:**
   ```bash
   # Linux/Mac
   bash ~/.lofigirl-terminal/uninstall.sh

   # Windows PowerShell
   Remove-Item $env:USERPROFILE\lofigirl-terminal -Recurse
   ```

2. **Install Node.js version:**
   ```bash
   # Windows
   irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.ps1 | iex

   # Mac/Linux
   curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.sh | bash
   ```

3. **Done!** Use `lofigirl tui` to start.

### Migration Guide
See [MIGRATION.md](MIGRATION.md) for detailed migration instructions.

---

## For Developers

If you need to reference the **old Python code** for any reason:

### View Python Code
```bash
# Python source is still in git history and src/lofigirl_terminal/
ls -la src/lofigirl_terminal/
```

### Git History
To see the Python version before migration:
```bash
# Find the commit before migration
git log --oneline --all | grep -i python

# Checkout old Python code (read-only)
git checkout <commit-hash-before-migration>
```

### Why Keep These Files?
- **Historical reference** - For understanding project evolution
- **Git compatibility** - Avoid breaking old git checkouts
- **Documentation** - For users migrating from Python version
- **Comparison** - For developers comparing implementations

---

## Status of Python Files

| File/Directory | Status | Use |
|----------------|--------|-----|
| `src/lofigirl_terminal/*.py` | ⚠️ Archived | Old Python source |
| `pyproject.toml` | ⚠️ Archived | Old Python config |
| `setup.py` | ⚠️ Archived | Old Python setup |
| `Makefile` | ⚠️ Archived | Old Python commands |
| `requirements/` | ⚠️ Archived | Old Python deps |
| `install.ps1` | ⚠️ Archived | Old installer |
| `install.sh` | ⚠️ Archived | Old installer |
| `uninstall.sh` | ⚠️ Archived | Old uninstaller |
| `.pre-commit-config.yaml` | ⚠️ Archived | Old Python hooks |
| `.flake8` | ⚠️ Archived | Old Python lint |

**⚠️ Archived** = No longer used, kept for reference only

---

## Should You Delete These Files?

### For End Users
**No need!** The new Node.js version ignores these files completely.

### For Developers
**Keep them!** They provide:
- Historical context
- Migration reference
- Git history compatibility

### For Production Deployment
You can safely exclude these from production:
- Add to `.npmignore` if publishing to npm
- Exclude from Docker images
- Not needed for compiled application

---

## Questions?

- **Using old Python version?** Please migrate! See [MIGRATION.md](MIGRATION.md)
- **Need help?** Open an issue on GitHub
- **Found a bug in Node.js version?** Report it!

---

## Timeline

| Date | Event |
|------|-------|
| 2024-11 | Python version developed |
| 2025-11-21 | **Migration to Node.js/TypeScript** |
| 2025-11-21 | Python version archived |
| Future | Python files may be removed in v2.0 |

---

<div align="center">

**The Python version served us well!**
**Now we move forward with Node.js/TypeScript** 🚀

See [README.md](README.md) for the current Node.js version.

</div>
