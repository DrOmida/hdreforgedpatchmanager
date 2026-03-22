# Project Reforged Patch Manager

A simple, dynamic, and automated tool to manage and update HD patches for **Turtle WoW 1.12**.

> ⚠️ **Disclaimer:** This tool is an independent, community-made project. It is not affiliated with, endorsed by, or associated with Project Reforged or any of its developers. All patch files and assets belong to their respective creators. This tool simply automates downloading and tracking the patches they make publicly available.

---

## 🌟 Features
- **Dynamic Updates:** Automatically scrapes the Project Reforged changelog on startup to detect the latest patch versions without requiring manual app updates.
- **Built-in Changelog Viewer:** Read the precise patch notes for the latest updates directly inside the app.
- **Turtle WoW Launcher Integration:** Automatically generates `.json` and `.txt` metadata files when downloading a patch. The Turtle WoW launcher will read these, applying formatted labels and link integrations out-of-the-box!
- **Play-and-Patch:** Safely handles file locks (WinError 32) so you can download background patch updates while you are currently playing WoW.

## 📦 Installation

No installation needed. Just grab the `.exe` from the `dist\` folder and put it anywhere you like — for example, next to your WoW folder.

Two small files will be created automatically next to the `.exe` the first time you run it:
- `patch_manager_config.json` — remembers your WoW Data folder path and variant choices
- `patch_versions.json` — tracks which version of each patch you have installed

---

## 🚀 How to Use

### 1. Set your WoW Data folder
At the top of the window, click **Browse…** and navigate to your Turtle WoW `Data` folder. This is usually something like `C:\TurtleWoW\Data\`.

### 2. Scan for existing patches
Click **Scan** to detect which `.mpq` patch files are already present in your Data folder. 

### 3. Downloading or updating a patch
Click any row to select it. The sidebar on the right will allow you to download updates. A progress bar at the bottom shows download progress.

### 4. Reading the Changelog
Click **View Changelog** at the top bar to see precisely what changed in the latest updates.

### 5. Update All Outdated
Click **Update All Outdated** in the sidebar to update every patch that has a newer version available. A confirmation window will appear listing all patches to be updated.

---

## 🔧 Building from Source

If you'd rather run the Python script directly or build the `.exe` yourself:

**Requirements:** Python 3.8 or newer. No third-party Python packages are required to run the script!

**To run the script directly:**
```
python ProjectReforged_PatchManager.py
```

**To build the `.exe` yourself:**
Place `ProjectReforged_PatchManager.py`, `ProjectReforged_PatchManager.spec`, and `build.bat` in the same folder, then double-click `build.bat`.

---

## 📜 License & Credits

- **Patch files** — all credit goes to the Project Reforged team and contributing artists. Visit their page at [projectreforged.github.io](https://projectreforged.github.io/) and consider supporting them on Ko-fi.
- **This tool** — free to use, modify, and share. No warranty provided.
