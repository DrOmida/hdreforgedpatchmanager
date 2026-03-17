# Project Reforged Patch Manager

A simple, unofficial tool to manage and update  HD patches for **Turtle WoW 1.12**.

> ⚠️ **Disclaimer:** This tool is an independent, community-made project. It is not affiliated with, endorsed by, or associated with Project Reforged or any of its developers. All patch files and assets belong to their respective creators. This tool simply automates downloading and tracking the patches they make publicly available.

---

## 📦 Installation

No installation needed. Just grab the `.exe` from the `dist\` folder and put it anywhere you like — for example, next to your WoW folder.

```
dist\
  ProjectReforged_PatchManager.exe   ← this is the only file you need
```

Two small files will be created automatically next to the `.exe` the first time you run it:

- `patch_manager_config.json` — remembers your WoW Data folder path and variant choices
- `patch_versions.json` — tracks which version of each patch you have installed

---

## 🚀 How to Use

### 1. Set your WoW Data folder

At the top of the window, click **Browse…** and navigate to your Turtle WoW `Data` folder. This is usually something like:

```
C:\TurtleWoW\Data\
```

Your path is saved automatically for next time.

### 2. Scan for existing patches

Click **Scan** to detect which `.mpq` patch files are already present in your Data folder. Any patch file found will be marked as installed. If the manager doesn't know the exact version (because it wasn't downloaded through this tool), it will show `unknown` — you can use **Mark as Installed** to set it to the current version.

### 3. Reading the patch list

The main table shows all available patches with the following columns:

| Column | Meaning |
|---|---|
| **Patch** | Name of the patch |
| **Category** | Core / Optional / Audio / Ultra |
| **Latest** | The newest available version |
| **Installed** | The version you currently have (or `—` if not installed) |
| **Status** | ✓ Up to date / ⬆ Update / Not installed |

### 4. Downloading or updating a patch

Click any row to select it. The sidebar on the right will show:

- A description of the patch
- Any dependency notes (e.g. *"Install with B + E"*)
- **Variant selector** (for patches that have multiple versions — see below)
- A **Download / Update** button

Click **Download / Update** to download the patch directly into your WoW `Data` folder. A progress bar at the bottom shows download progress. You can cancel at any time with the **Cancel** button.

### 5. Patches with variants (Patch-L and Patch-U)

Two patches come in two flavours. You can only install **one** of each:

**Patch-L — A Little Extra for Females**
- *Regular* (by Watchers3D) — the standard version
- *Less Thicc* (by Deezhugs) — a slimmer alternative

**Patch-U — Ultra HD Characters & Gear**
- *Standard* — best quality, but heavier on your system
- *Performance* — lighter version, use this if you experience crashes

Select your preferred variant using the radio buttons in the sidebar before clicking Download.

### 6. Update All Outdated

Click **Update All Outdated** in the sidebar to update every patch that has a newer version available. A confirmation window will appear listing all patches to be updated. For patches with variants, you can choose which variant to download right in that window before anything starts.

---


## 🔧 Building from Source

If you'd rather run the Python script directly or build the `.exe` yourself:

**Requirements:** Python 3.8 or newer — download from [python.org](https://www.python.org/downloads/). During installation, make sure **"Add Python to PATH"** is checked.

No third-party Python packages are required to run the script — it only uses modules from the Python standard library (`tkinter`, `urllib`, `threading`, `json`).

**To run the script directly:**
```
python ProjectReforged_PatchManager.py
```

**To build the `.exe` yourself:**

Place these three files in the same folder:
```
ProjectReforged_PatchManager.py
ProjectReforged_PatchManager.spec
build.bat
```

Then double-click `build.bat`. It will install PyInstaller and produce the `.exe` at:
```
dist\ProjectReforged_PatchManager.exe
```

---

## ❓ FAQ

**The patch file is huge — is the download stuck?**
No, some patches (especially Patch-U) are several gigabytes. The progress bar will keep moving. Be patient and don't close the app.

**I already have patches installed from before. Will the manager overwrite them?**
Only if you click Download / Update for that patch. Use **Scan** first to detect what you have, then **Mark as Installed** if the version looks correct — that way the manager knows you're up to date without re-downloading anything.

**Can I choose which patches to install?**
Yes, completely. Every patch is optional except where noted. Just download the ones you want.

**How do I know when new versions are released?**
Check [projectreforged.github.io/downloads](https://projectreforged.github.io/downloads/index.html) for updates. When a new version comes out, the version numbers in the `PATCHES` list at the top of `ProjectReforged_PatchManager.py` need to be updated manually — or wait for someone to release an updated version of this tool.

---

## 📜 License & Credits

- **Patch files** — all credit goes to the Project Reforged team and contributing artists. Visit their page at [projectreforged.github.io](https://projectreforged.github.io/) and consider supporting them on [Ko-fi](https://ko-fi.com/projectreforged).
- **This tool** — free to use, modify, and share. No warranty provided.

*This project is not affiliated with, endorsed by, or in any way officially connected with Project Reforged or Turtle WoW.*
