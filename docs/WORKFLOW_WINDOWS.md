# 🪟 Workflow Windows PowerShell - Guide Complet

Guide pas-à-pas pour installer et utiliser LofiGirl Terminal sur Windows avec PowerShell uniquement.

---

## 📦 **Installation (Une seule fois)**

### **Étape 1 : Installation Automatique**

Ouvrez **PowerShell** et exécutez :

```powershell
irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.ps1 | iex
```

**Ce que fait l'installateur :**
1. ✅ Détecte Python (`py`, `python`, ou `python3`)
2. ✅ Vérifie Git
3. ✅ Vérifie MPV (propose l'installation via Chocolatey si manquant)
4. ✅ Clone le projet dans `C:\Users\VotreNom\lofigirl-terminal`
5. ✅ Crée l'environnement virtuel Python
6. ✅ Installe toutes les dépendances
7. ⚠️ **AVERTIT** si `libmpv-2.dll` est manquant

---

### **Étape 2 : Fix libmpv-2.dll (Si nécessaire)**

**Symptôme** : L'installateur affiche un warning jaune sur `libmpv-2.dll`.

#### **Solution Rapide (5 minutes)**

1. **Télécharger MPV avec libmpv** :
   - Aller sur : https://github.com/shinchiro/mpv-winbuild-cmake/releases
   - Télécharger : `mpv-x86_64-v3-YYYYMMDD-git-XXXXXXX.7z` (version la plus récente)
   - Exemple : `mpv-x86_64-v3-20241117-git-d2a8820.7z`

2. **Extraire l'archive** :
   - Installer 7-Zip si nécessaire : `choco install 7zip -y`
   - Clic droit → 7-Zip → Extraire ici

3. **Copier la DLL** :
   ```powershell
   # Trouver le dossier MPV
   $mpvPath = (Get-Command mpv.exe).Source | Split-Path

   # Copier libmpv-2.dll (remplacer le chemin selon votre extraction)
   Copy-Item "C:\Users\VotreNom\Downloads\mpv-x86_64...\libmpv-2.dll" -Destination $mpvPath

   # Vérifier
   Get-ChildItem "$mpvPath\libmpv-2.dll"
   ```

4. **C'est tout !** ✅

**Guide détaillé** : [Windows Installation Guide](WINDOWS_INSTALL.md)

---

## 🎵 **Utilisation (À chaque fois)**

### **Méthode Standard**

```powershell
# 1. Aller dans le projet
cd "$env:USERPROFILE\lofigirl-terminal"

# 2. Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# 3. Ajouter MPV au PATH (temporaire, pour cette session)
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"

# 4. Lancer LofiGirl Terminal (style rice par défaut)
lofigirl tui
```

**Raccourcis clavier dans le TUI :**
- `SPACE` - Play/Pause
- `N` - Station suivante
- `P` - Station précédente
- `M` - Mute/Unmute
- `+` / `-` - Volume +/-
- `Y` - Ouvrir dans YouTube
- `Q` - Quitter

---

### **Méthode Rapide (Alias PowerShell)**

**Configuration unique** - Ajouter à votre profil PowerShell :

```powershell
# Ouvrir votre profil PowerShell
notepad $PROFILE

# Ajouter ces lignes :
function Start-Lofigirl {
    Set-Location "$env:USERPROFILE\lofigirl-terminal"
    .\venv\Scripts\Activate.ps1
    $env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
    lofigirl tui
}
Set-Alias -Name lofi -Value Start-Lofigirl

# Sauvegarder et fermer
```

**Puis, à chaque fois, juste taper** :
```powershell
lofi
```

---

### **PATH Permanent (Optionnel mais recommandé)**

Pour ne plus avoir à ajouter MPV au PATH à chaque fois :

```powershell
# Ouvrir PowerShell en Administrateur
# Puis exécuter :

[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\ProgramData\chocolatey\lib\mpvio.install\tools",
    "Machine"
)

# Redémarrer PowerShell
```

**Après ça, plus besoin de** :
```powershell
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
```

---

## 🎨 **Styles d'Interface**

LofiGirl Terminal a 2 styles d'interface :

### **Rice Style (Par défaut)** - Compact, inspiré de btop
```powershell
lofigirl tui
# OU explicitement
lofigirl tui --style rice
```

**Caractéristiques** :
- ✨ Design ultra-compact
- 📊 Waveform en temps réel (▁▂▃▄▅▆▇█)
- 🎨 ASCII art animé
- 📋 Panneau info style btop
- 🎛️ Contrôles one-line

### **Classic Style** - Interface complète
```powershell
lofigirl tui --style classic
```

**Caractéristiques** :
- 🖼️ Grande zone ASCII art
- 📊 Visualisation détaillée
- 🎮 Contrôles séparés
- ℹ️ Plus d'informations affichées

---

## 📻 **Autres Commandes**

```powershell
# Lister toutes les stations disponibles
lofigirl list

# Jouer une station spécifique (mode CLI, sans TUI)
lofigirl play --station lofi-hip-hop

# Voir les infos d'une station
lofigirl station-info --station lofi-jazz

# Configurer thèmes et polices
lofigirl setup

# Voir toutes les commandes
lofigirl --help

# Voir les informations de configuration
lofigirl info
```

---

## 🎯 **Stations Disponibles**

| ID | Nom | Description |
|----|-----|-------------|
| `lofi-hip-hop` | 📚 Lofi Hip Hop Radio | Beats to relax/study (défaut) |
| `lofi-sleep` | 💤 Lofi Sleep Radio | Beats to sleep/chill |
| `synthwave` | 🌌 Synthwave Radio | Beats to chill/game |
| `lofi-jazz` | 🎷 Jazz Lofi Radio | Beats to chill/study |

---

## ⚙️ **Configuration Avancée**

### **Changer de Thème**

```powershell
# Lancer le setup wizard
lofigirl setup

# Choisir parmi :
# - Catppuccin Mocha (défaut)
# - Dracula
# - Nord
# - Tokyo Night
# - Gruvbox
# - Solarized Dark
```

### **Fichier de Configuration**

Créer/modifier : `C:\Users\VotreNom\.config\lofigirl-terminal\config.env`

```env
# Thème
THEME=catppuccin-mocha

# Volume par défaut
DEFAULT_VOLUME=50

# Station par défaut
DEFAULT_STATION=lofi-hip-hop

# ASCII art
ASCII_ART=lofi-girl-classic

# Police (Nerd Font)
TERMINAL_FONT=JetBrainsMono Nerd Font

# Mode debug
DEBUG_MODE=false
```

---

## 🔄 **Mise à Jour**

```powershell
# Aller dans le projet
cd "$env:USERPROFILE\lofigirl-terminal"

# Activer venv
.\venv\Scripts\Activate.ps1

# Mettre à jour depuis GitHub
git pull origin main

# Mettre à jour les dépendances
pip install -r requirements\base.txt --upgrade

# Réinstaller le package
pip install -e .
```

---

## 🗑️ **Désinstallation**

```powershell
# Supprimer le projet
Remove-Item "$env:USERPROFILE\lofigirl-terminal" -Recurse -Force

# Supprimer la config (optionnel)
Remove-Item "$env:USERPROFILE\.config\lofigirl-terminal" -Recurse -Force

# Supprimer l'alias du profil PowerShell (optionnel)
notepad $PROFILE
# Supprimer les lignes de l'alias Start-Lofigirl
```

---

## 🐛 **Troubleshooting Rapide**

### **Problème : Virtual environment activation fails**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problème : Python not found**
```powershell
# Vérifier quelle commande fonctionne
py --version
python --version
python3 --version

# Utiliser celle qui fonctionne pour créer le venv
```

### **Problème : MPV not found**
```powershell
# Vérifier l'installation
where.exe mpv

# Réinstaller si nécessaire
choco install mpv -y
```

### **Problème : libmpv-2.dll not found**
Voir **Étape 2** de l'installation ou le guide complet : [Windows Installation Guide](WINDOWS_INSTALL.md)

### **Problème : yt-dlp errors**
```powershell
pip install --upgrade yt-dlp
```

---

## 📊 **Résumé du Workflow**

```
┌─────────────────────────────────────────┐
│  1️⃣  INSTALLATION (une fois)           │
├─────────────────────────────────────────┤
│  • Exécuter install.ps1                 │
│  • Copier libmpv-2.dll si besoin        │
└─────────────────────────────────────────┘
           ⬇️
┌─────────────────────────────────────────┐
│  2️⃣  UTILISATION (à chaque fois)       │
├─────────────────────────────────────────┤
│  • cd lofigirl-terminal                 │
│  • .\venv\Scripts\Activate.ps1          │
│  • $env:PATH = "...\tools;$env:PATH"    │
│  • lofigirl tui                         │
└─────────────────────────────────────────┘
           ⬇️
┌─────────────────────────────────────────┐
│  3️⃣  PROFITER ! 🎵                     │
├─────────────────────────────────────────┤
│  • SPACE: play/pause                    │
│  • N/P: next/prev station               │
│  • +/-: volume                          │
│  • Q: quit                              │
└─────────────────────────────────────────┘
```

---

## 💡 **Tips & Tricks**

### **1. Raccourci Bureau**

Créer un fichier `LofiGirl.ps1` sur le bureau :

```powershell
Set-Location "$env:USERPROFILE\lofigirl-terminal"
.\venv\Scripts\Activate.ps1
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
lofigirl tui
```

### **2. Windows Terminal Integration**

Ajouter au profil Windows Terminal (`settings.json`) :

```json
{
  "name": "LofiGirl Terminal",
  "commandline": "powershell.exe -NoExit -Command \"cd $env:USERPROFILE\\lofigirl-terminal; .\\venv\\Scripts\\Activate.ps1; $env:PATH = 'C:\\ProgramData\\chocolatey\\lib\\mpvio.install\\tools;' + $env:PATH; lofigirl tui\"",
  "icon": "🎵"
}
```

### **3. Lancer au démarrage de Windows**

Ajouter un raccourci dans :
```
C:\Users\VotreNom\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

---

**🎉 Profitez de vos sessions lofi ! 🎧**

Des questions ? → [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)
