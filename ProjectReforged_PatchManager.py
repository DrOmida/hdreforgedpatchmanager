"""
Project Reforged Patch Manager
A standalone tool to manage and update Project Reforged HD patches for Turtle WoW 1.12.

Requirements: pip install requests tkinter (tkinter is usually bundled with Python)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
import re


def app_dir() -> Path:
    """Return the folder next to the .exe (frozen) or next to the .py (dev)."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent

# ─────────────────────────────────────────────
# Patch definitions (scraped from projectreforged.github.io/downloads/index.html)
# Update the VERSION strings here when new versions are released.
# ─────────────────────────────────────────────
PATCHES = [
    # Core Modules
    {
        "id": "Patch-A",
        "name": "Patch-A — Player Characters & NPCs",
        "category": "Core",
        "version": "5.1.0",
        "filename": "Patch-A.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-A.mpq",
        "description": "Core character/NPC visuals and foundations used by other modules.",
        "tags": ["Core"],
        "icon": "🧙",
    },
    {
        "id": "Patch-B",
        "name": "Patch-B — Buildings",
        "category": "Core",
        "version": "5.0.0",
        "filename": "Patch-B.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-B.mpq",
        "description": "Part of the Environment & World set. Install with D + E.",
        "tags": ["Install with D+E"],
        "icon": "🏰",
    },
    {
        "id": "Patch-C",
        "name": "Patch-C — Creatures",
        "category": "Core",
        "version": "5.1.0",
        "filename": "Patch-C.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-C.mpq",
        "description": "Creatures and related assets for the classic client.",
        "tags": ["Core"],
        "icon": "🐉",
    },
    {
        "id": "Patch-D",
        "name": "Patch-D — Doodads",
        "category": "Core",
        "version": "5.0.2",
        "filename": "Patch-D.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-D.mpq",
        "description": "World doodads + Textures. Install with B + E.",
        "tags": ["Install with B+E"],
        "icon": "🌿",
    },
    {
        "id": "Patch-E",
        "name": "Patch-E — Environment",
        "category": "Core",
        "version": "5.0.0",
        "filename": "Patch-E.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-E.mpq",
        "description": "Environment textures and world visuals + Fog Push-back. Install with B + D.",
        "tags": ["Install with B+D", "Fog Push-back"],
        "icon": "🌄",
    },
    {
        "id": "Patch-G",
        "name": "Patch-G — Gear & Weapons",
        "category": "Core",
        "version": "5.0.1",
        "filename": "Patch-G.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-G.mpq",
        "description": "Gear and weapon visuals used by multiple enhancements.",
        "tags": ["Core"],
        "icon": "⚔️",
    },
    {
        "id": "Patch-I",
        "name": "Patch-I — Interface",
        "category": "Core",
        "version": "5.0.4",
        "filename": "Patch-I.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-I.mpq",
        "description": "Interface visuals + SuperWoW selection circle texture support.",
        "tags": ["SuperWoW"],
        "icon": "🧭",
    },
    # Optional Enhancements
    {
        "id": "Patch-L",
        "name": "Patch-L — A Little Extra for Females",
        "category": "Optional",
        "version": "5.0.0",
        "filename": "Patch-L.mpq",
        "description": "Optional body model enhancement. Requires Patch-A. Install only ONE variant.",
        "tags": ["Requires A", "Choose variant"],
        "icon": "💃",
        # variants: list of (label, url) — user picks one
        "variants": [
            ("Regular (by Watchers3D)",
             "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-L.mpq"),
            ("Less Thicc (by Deezhugs)",
             "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/extras/patch-L.mpq"),
        ],
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-L.mpq",  # default
    },
    {
        "id": "Patch-M",
        "name": "Patch-M — Maps & Loading Screens",
        "category": "Optional",
        "version": "5.0.0",
        "filename": "Patch-M.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-M.mpq",
        "description": "Enhanced maps and loading screens.",
        "tags": [],
        "icon": "🗺️",
    },
    {
        "id": "Patch-N",
        "name": "Patch-N — Darker Nights",
        "category": "Optional",
        "version": "5.0.0",
        "filename": "Patch-N.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-N.mpq",
        "description": "Darker nights for a more atmospheric experience.",
        "tags": [],
        "icon": "🌑",
    },
    {
        "id": "Patch-O",
        "name": "Patch-O — Raid Visuals (Compatible Build)",
        "category": "Optional",
        "version": "5.1.0",
        "filename": "Patch-O.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-O.mpq",
        "description": "Compatible version of Marceline's Turtle WoW Raid Visuals Mod. Requires C + S.",
        "tags": ["Requires C+S"],
        "icon": "🔥",
    },
    {
        "id": "Patch-V",
        "name": "Patch-V — Spell Visual Effects",
        "category": "Optional",
        "version": "5.0.2",
        "filename": "Patch-V.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-V.mpq",
        "description": "Spell visuals and effect enhancements.",
        "tags": [],
        "icon": "✨",
    },
    # Audio
    {
        "id": "Patch-S",
        "name": "Patch-S — Sounds & Music",
        "category": "Audio",
        "version": "5.0.0",
        "filename": "Patch-S.mpq",
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-S.mpq",
        "description": "Sounds and music enhancements.",
        "tags": [],
        "icon": "🎵",
    },
    # Ultra Tier
    {
        "id": "Patch-U",
        "name": "Patch-U — Ultra HD Characters & Gear",
        "category": "Ultra",
        "version": "5.1.0",
        "filename": "Patch-U.mpq",
        "description": "Ultra tier textures for characters and gear. Requires A + G. Install only ONE variant.",
        "tags": ["Requires A+G", "Heavy", "Choose variant"],
        "icon": "💎",
        "variants": [
            ("Standard (best quality, heavier)",
             "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-U.mpq"),
            ("Performance (use if you get crashes)",
             "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/extras/patch-U.mpq"),
        ],
        "url": "https://pub-0f05631d243e4046993fc02ca7be9542.r2.dev/patches/patch-U.mpq",  # default
    },
]

CATEGORY_ORDER = ["Core", "Optional", "Audio", "Ultra"]
CATEGORY_COLORS = {
    "Core": "#4a9eff",
    "Optional": "#a78bfa",
    "Audio": "#34d399",
    "Ultra": "#fbbf24",
}

VERSION_STORE = "patch_versions.json"
VERSION_STORE = "patch_versions.json"
VERSION_STORE = "patch_versions.json"
APP_VERSION = "1.2.0"

ICON_B64 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA8UlEQVR4nO2XsQ3CMBBFfVcwBAOwBiNQQ8USTMESVLhmBNZgAA9BA0phZFl28n32HU1+FSWW30v8rSTOrflzyALir+9PPD5eNjREIDxOv0ljtoc7zcFLEuwM7zyC0/OsKVCTScNWAjUJtoSVOkAjypfn+bpVr3XtgiCE51CRQMjgki1XCmvC97vz4tyMCGjBp1DLOufwaWxtzdF52AkzB2+Zh6UCI+BigZ417xbwFXipnEgIGRQLhT72tIBLYoyaSuBIWBOOLAtpFQ7tBKFQDXhRAH2Po9+ETR3wIHxk2BIGC1hKkPSjYlQHqPVPZo0bnC8N7Zorp0y1+wAAAABJRU5ErkJggg=='

# ─────────────────────────────────────────────
# Version persistence (stored next to the script)
# ─────────────────────────────────────────────

def load_version_store():
    """Load locally tracked patch versions from JSON."""
    store_path = app_dir() / VERSION_STORE
    if store_path.exists():
        try:
            with open(store_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_version_store(data: dict):
    store_path = app_dir() / VERSION_STORE
    with open(store_path, "w") as f:
        json.dump(data, f, indent=2)


# ─────────────────────────────────────────────
# Download helper with progress callback
# ─────────────────────────────────────────────

def download_file(url: str, dest_path: Path, progress_cb=None, cancel_flag=None):
    """Download a file with progress reporting. Returns (success, message)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ProjectReforged-PatchManager/1.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            chunk = 8192
            tmp_path = dest_path.with_suffix(".tmp")
            with open(tmp_path, "wb") as f:
                while True:
                    if cancel_flag and cancel_flag[0]:
                        tmp_path.unlink(missing_ok=True)
                        return False, "Cancelled"
                    data = response.read(chunk)
                    if not data:
                        break
                    f.write(data)
                    downloaded += len(data)
                    if progress_cb and total:
                        progress_cb(downloaded / total)
            # Replace destination
            if dest_path.exists():
                try:
                    dest_path.unlink()
                except PermissionError:
                    import time
                    bak_path = dest_path.with_name(f"{dest_path.name}.{int(time.time())}.old")
                    try:
                        dest_path.rename(bak_path)
                    except Exception:
                        tmp_path.unlink(missing_ok=True)
                        return False, "File is locked strongly by the game. Please close WoW completely to apply this update!"
            tmp_path.rename(dest_path)
        return True, "OK"
    except urllib.error.URLError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


# ─────────────────────────────────────────────
# GUI Application
# ─────────────────────────────────────────────

class PatchManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Project Reforged — Patch Manager")
        self.geometry("920x680")
        self.minsize(800, 560)
        self.configure(bg="#0d1117")
        try:
            icon_img = tk.PhotoImage(data=ICON_B64)
            self.iconphoto(False, icon_img)
        except Exception:
            pass

        self.wow_path = tk.StringVar(value="")
        self.version_store = load_version_store()
        self.cancel_flag = [False]
        self._download_thread = None
        self._ui_queue = queue.Queue()          # thread → main thread messages
        # Persisted variant choices: patch_id -> variant index (0-based)
        self.variant_choices = {}  # loaded in _restore_saved_path
        self._variant_var = tk.IntVar(value=0)  # bound to radio buttons

        self._setup_styles()
        self._build_ui()
        self._restore_saved_path()
        self._poll_queue()                      # start UI update loop
        self.changelog_text = ""
        threading.Thread(target=self._fetch_remote_versions, daemon=True).start()

    # ── Styles ──────────────────────────────

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        bg = "#0d1117"
        fg = "#e6edf3"
        accent = "#1f6feb"
        row_even = "#161b22"
        row_odd = "#0d1117"
        sel = "#1f6feb"

        style.configure(".", background=bg, foreground=fg, font=("Segoe UI", 9))
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TButton",
                         background="#21262d", foreground=fg,
                         borderwidth=1, relief="flat", padding=(8, 4))
        style.map("TButton",
                  background=[("active", "#30363d"), ("pressed", accent)],
                  foreground=[("active", fg)])
        style.configure("Accent.TButton",
                         background=accent, foreground="#ffffff",
                         borderwidth=0, relief="flat", padding=(10, 5))
        style.map("Accent.TButton",
                  background=[("active", "#388bfd"), ("disabled", "#21262d")],
                  foreground=[("disabled", "#484f58")])
        style.configure("TEntry",
                         background="#21262d", foreground=fg,
                         insertcolor=fg, fieldbackground="#21262d",
                         borderwidth=1, relief="flat")
        style.configure("Treeview",
                         background=row_even, foreground=fg,
                         fieldbackground=row_even,
                         rowheight=26, borderwidth=0)
        style.configure("Treeview.Heading",
                         background="#161b22", foreground="#8b949e",
                         relief="flat", font=("Segoe UI", 9, "bold"))
        style.map("Treeview",
                  background=[("selected", sel)],
                  foreground=[("selected", "#ffffff")])
        style.configure("TProgressbar",
                         troughcolor="#21262d", background=accent,
                         borderwidth=0, thickness=6)
        style.configure("TNotebook", background=bg, borderwidth=0)
        style.configure("TNotebook.Tab",
                         background="#161b22", foreground="#8b949e",
                         padding=(12, 6))
        style.map("TNotebook.Tab",
                  background=[("selected", bg)],
                  foreground=[("selected", fg)])

    # ── UI Build ─────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#161b22", height=56)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        brand_frame = tk.Frame(header, bg="#161b22")
        brand_frame.pack(side="left", padx=16, pady=12)
        tk.Label(brand_frame, text="⚔ Turtle WoW", bg="#161b22",
                 fg="#3fb950", font=("Segoe UI", 14, "bold")).pack(side="left")
        tk.Label(brand_frame, text=" | Reforged Patch Manager", bg="#161b22",
                 fg="#e6edf3", font=("Segoe UI", 13, "bold")).pack(side="left", padx=(6, 0))

        tk.Label(header, text=f"Version {APP_VERSION}", bg="#161b22",
                 fg="#484f58", font=("Segoe UI", 9)).pack(side="right", padx=16)

        # WoW path bar
        path_frame = tk.Frame(self, bg="#161b22", pady=8)
        path_frame.pack(fill="x", padx=0, pady=(1, 0))
        tk.Label(path_frame, text="WoW Data folder:", bg="#161b22",
                 fg="#8b949e", font=("Segoe UI", 9)).pack(side="left", padx=(16, 6))
        path_entry = ttk.Entry(path_frame, textvariable=self.wow_path, width=52)
        path_entry.pack(side="left", padx=(0, 6))
        ttk.Button(path_frame, text="Browse…", command=self._browse_path).pack(side="left")
        ttk.Button(path_frame, text="Scan", command=self._scan_patches).pack(side="left", padx=(6, 0))

        self.btn_changelog = ttk.Button(path_frame, text="View Changelog",
                                        command=self._show_changelog,
                                        state="disabled")
        self.btn_changelog.pack(side="left", padx=(6, 0))

        # Separator
        tk.Frame(self, bg="#30363d", height=1).pack(fill="x")

        # Main content — treeview + sidebar
        content = tk.Frame(self, bg="#0d1117")
        content.pack(fill="both", expand=True, padx=0, pady=0)

        # Treeview (left/main)
        tree_frame = tk.Frame(content, bg="#0d1117")
        tree_frame.pack(side="left", fill="both", expand=True, padx=(12, 6), pady=12)

        cols = ("icon", "name", "category", "remote", "local", "status")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("icon", text="")
        self.tree.heading("name", text="Patch")
        self.tree.heading("category", text="Category")
        self.tree.heading("remote", text="Latest")
        self.tree.heading("local", text="Installed")
        self.tree.heading("status", text="Status")

        self.tree.column("icon", width=30, anchor="center", stretch=False)
        self.tree.column("name", width=240, anchor="w")
        self.tree.column("category", width=80, anchor="center")
        self.tree.column("remote", width=70, anchor="center")
        self.tree.column("local", width=70, anchor="center")
        self.tree.column("status", width=110, anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.tag_configure("uptodate", foreground="#3fb950")
        self.tree.tag_configure("update", foreground="#f0883e")
        self.tree.tag_configure("missing", foreground="#8b949e")
        self.tree.tag_configure("notinstalled", foreground="#484f58")

        # Sidebar (right)
        sidebar = tk.Frame(content, bg="#161b22", width=220)
        sidebar.pack(side="right", fill="y", padx=(0, 12), pady=12)
        sidebar.pack_propagate(False)

        self.detail_name = tk.Label(sidebar, text="Select a patch", bg="#161b22",
                                    fg="#e6edf3", font=("Segoe UI", 10, "bold"),
                                    wraplength=200, justify="left")
        self.detail_name.pack(anchor="w", padx=12, pady=(14, 4))

        self.detail_desc = tk.Label(sidebar, text="", bg="#161b22",
                                    fg="#8b949e", font=("Segoe UI", 8),
                                    wraplength=196, justify="left")
        self.detail_desc.pack(anchor="w", padx=12, pady=(0, 8))

        self.detail_tags = tk.Label(sidebar, text="", bg="#161b22",
                                    fg="#a78bfa", font=("Segoe UI", 8),
                                    wraplength=196, justify="left")
        self.detail_tags.pack(anchor="w", padx=12, pady=(0, 12))

        # Variant selector (shown only for patches with variants)
        self.variant_frame = tk.Frame(sidebar, bg="#161b22")
        self.variant_frame.pack(fill="x", padx=8, pady=(0, 4))
        self.variant_label = tk.Label(self.variant_frame, text="Choose variant:",
                                      bg="#161b22", fg="#8b949e",
                                      font=("Segoe UI", 8, "bold"))
        # radio buttons are added dynamically in _on_select
        self._variant_radios = []

        tk.Frame(sidebar, bg="#30363d", height=1).pack(fill="x", padx=8, pady=4)

        self.btn_download = ttk.Button(sidebar, text="Download / Update",
                                       style="Accent.TButton",
                                       command=self._download_selected,
                                       state="disabled")
        self.btn_download.pack(fill="x", padx=12, pady=(8, 4))

        self.btn_skip = ttk.Button(sidebar, text="Mark as Installed",
                                   command=self._mark_installed,
                                   state="disabled")
        self.btn_skip.pack(fill="x", padx=12, pady=(0, 4))

        self.btn_remove = ttk.Button(sidebar, text="Remove Version Record",
                                     command=self._remove_record,
                                     state="disabled")
        self.btn_remove.pack(fill="x", padx=12, pady=(0, 4))

        tk.Frame(sidebar, bg="#30363d", height=1).pack(fill="x", padx=8, pady=8)

        ttk.Button(sidebar, text="Update All Outdated",
                   command=self._update_all).pack(fill="x", padx=12, pady=(0, 4))

        # Bottom status bar
        bottom = tk.Frame(self, bg="#161b22", height=40)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)

        self.progress = ttk.Progressbar(bottom, orient="horizontal",
                                        mode="determinate", length=220)
        self.progress.pack(side="left", padx=(12, 8), pady=12)

        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(bottom, textvariable=self.status_var, bg="#161b22",
                 fg="#8b949e", font=("Segoe UI", 9)).pack(side="left")

        self.btn_cancel = ttk.Button(bottom, text="Cancel", command=self._cancel_download,
                                     state="disabled")
        self.btn_cancel.pack(side="right", padx=12)

        # Populate tree
        self._populate_tree()

    # ── Tree population ──────────────────────

    def _populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        has_new = False
        for p in PATCHES:
            local_ver = self.version_store.get(p["id"], {}).get("version", "—")
            remote_ver = p["version"]

            if local_ver == "—":
                status = "Not installed"
                tag = "notinstalled"
            elif local_ver == remote_ver:
                status = "✓ Up to date"
                tag = "uptodate"
            else:
                status = "⬆ Update"
                tag = "update"
                if local_ver != "—":  # Only show *New* if it's an update, not just missing
                    has_new = True

            self.tree.insert("", "end", iid=p["id"], tags=(tag,),
                             values=(p["icon"], p["name"], p["category"],
                                     remote_ver, local_ver, status))

        if hasattr(self, 'btn_changelog') and str(self.btn_changelog.cget('state')) != 'disabled':
            self.btn_changelog.config(text="View Changelog (*New*) !" if has_new else "View Changelog")

    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        patch_id = sel[0]
        patch = next((p for p in PATCHES if p["id"] == patch_id), None)
        if not patch:
            return

        self.detail_name.config(text=patch["name"])
        self.detail_desc.config(text=patch["description"])
        self.detail_tags.config(text=" · ".join(patch["tags"]) if patch["tags"] else "")

        # Rebuild variant radio buttons
        for r in self._variant_radios:
            r.destroy()
        self._variant_radios.clear()
        for w in self.variant_frame.winfo_children():
            w.destroy()

        variants = patch.get("variants")
        if variants:
            saved_idx = self.variant_choices.get(patch_id, 0)
            self._variant_var.set(saved_idx)
            tk.Label(self.variant_frame, text="Choose variant:",
                     bg="#161b22", fg="#8b949e",
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 2))
            for i, (label, _url) in enumerate(variants):
                rb = tk.Radiobutton(
                    self.variant_frame,
                    text=label,
                    variable=self._variant_var,
                    value=i,
                    bg="#161b22", fg="#e6edf3",
                    selectcolor="#0d1117",
                    activebackground="#161b22",
                    activeforeground="#e6edf3",
                    font=("Segoe UI", 8),
                    wraplength=190,
                    justify="left",
                    command=lambda pid=patch_id: self._on_variant_change(pid),
                )
                rb.pack(anchor="w", padx=4)
                self._variant_radios.append(rb)

        local = self.version_store.get(patch_id, {}).get("version", "—")
        if local == patch["version"]:
            self.btn_download.config(state="disabled")
        else:
            self.btn_download.config(state="normal")

        self.btn_skip.config(state="normal")
        self.btn_remove.config(state="normal")

    def _on_variant_change(self, patch_id):
        """Save the chosen variant index when the user clicks a radio button."""
        self.variant_choices[patch_id] = self._variant_var.get()
        self._save_path(self.wow_path.get())  # also saves variant choices via config

    # ── Path handling ────────────────────────

    def _browse_path(self):
        path = filedialog.askdirectory(title="Select your WoW Data folder")
        if path:
            self.wow_path.set(path)
            self._save_path(path)

    def _save_path(self, path):
        cfg = app_dir() / "patch_manager_config.json"
        with open(cfg, "w") as f:
            json.dump({"wow_data_path": path,
                       "variant_choices": self.variant_choices}, f)

    def _restore_saved_path(self):
        cfg = app_dir() / "patch_manager_config.json"
        if cfg.exists():
            try:
                with open(cfg) as f:
                    data = json.load(f)
                self.wow_path.set(data.get("wow_data_path", ""))
                self.variant_choices = data.get("variant_choices", {})
            except Exception:
                pass

    # ── Scan local files ──────────────────────

    def _scan_patches(self):
        path = self.wow_path.get().strip()
        if not path or not Path(path).is_dir():
            messagebox.showerror("Error", "Please set a valid WoW Data folder path first.")
            return

        found = []
        data_path = Path(path)
        for p in PATCHES:
            mpq = data_path / p["filename"]
            if mpq.exists():
                # Check if we have a stored version; if not, mark as "unknown"
                if p["id"] not in self.version_store:
                    self.version_store[p["id"]] = {"version": "unknown", "installed_at": "scanned"}
                found.append(p["filename"])

        save_version_store(self.version_store)
        self._populate_tree()
        self.status_var.set(f"Scan complete. Found {len(found)} patch file(s) in Data folder.")

    # ── Download ─────────────────────────────

    def _download_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        patch_id = sel[0]
        patch = next((p for p in PATCHES if p["id"] == patch_id), None)
        if not patch:
            return

        # If this patch has variants, resolve the chosen URL
        if patch.get("variants"):
            idx = self.variant_choices.get(patch_id, 0)
            _, chosen_url = patch["variants"][idx]
            # Make a shallow copy with the resolved URL
            patch = {**patch, "url": chosen_url}

        self._start_download([patch])

    def _update_all(self):
        outdated = []
        for p in PATCHES:
            local = self.version_store.get(p["id"], {}).get("version", "—")
            if local != "—" and local != p["version"]:
                outdated.append(p)
        if not outdated:
            messagebox.showinfo("Up to date", "All installed patches are up to date!")
            return

        # Show confirmation + variant pickers for any multi-variant patches
        resolved = self._confirm_update_all_dialog(outdated)
        if resolved is not None:
            self._start_download(resolved)

    def _confirm_update_all_dialog(self, patches):
        """
        Show a modal dialog listing patches to update.
        For any patch with variants, show radio buttons to pick which one.
        Returns resolved patch list (with correct URLs) or None if cancelled.
        """
        dlg = tk.Toplevel(self)
        dlg.title("Update All Outdated")
        dlg.configure(bg="#0d1117")
        dlg.resizable(False, False)
        dlg.grab_set()

        # Centre over parent
        self.update_idletasks()
        px, py = self.winfo_rootx(), self.winfo_rooty()
        pw, ph = self.winfo_width(), self.winfo_height()
        dlg.geometry(f"+{px + pw//2 - 220}+{py + ph//2 - 200}")

        tk.Label(dlg, text="Update All Outdated Patches",
                 bg="#0d1117", fg="#e6edf3",
                 font=("Segoe UI", 11, "bold")).pack(padx=20, pady=(16, 4))
        tk.Label(dlg, text="Review patches and choose variants where needed:",
                 bg="#0d1117", fg="#8b949e",
                 font=("Segoe UI", 8)).pack(padx=20, pady=(0, 10))

        scroll_frame = tk.Frame(dlg, bg="#0d1117")
        scroll_frame.pack(fill="both", expand=True, padx=20)

        variant_vars = {}  # patch_id -> IntVar

        for p in patches:
            row = tk.Frame(scroll_frame, bg="#161b22", pady=6)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=f"{p['icon']}  {p['name']}",
                     bg="#161b22", fg="#e6edf3",
                     font=("Segoe UI", 9, "bold"),
                     anchor="w").pack(anchor="w", padx=10)

            if p.get("variants"):
                saved_idx = self.variant_choices.get(p["id"], 0)
                var = tk.IntVar(value=saved_idx)
                variant_vars[p["id"]] = var
                for i, (label, _) in enumerate(p["variants"]):
                    tk.Radiobutton(
                        row, text=label, variable=var, value=i,
                        bg="#161b22", fg="#c9d1d9",
                        selectcolor="#0d1117",
                        activebackground="#161b22", activeforeground="#e6edf3",
                        font=("Segoe UI", 8),
                    ).pack(anchor="w", padx=22)
            else:
                tk.Label(row, text=f"  {p['filename']}  →  v{p['version']}",
                         bg="#161b22", fg="#8b949e",
                         font=("Segoe UI", 8)).pack(anchor="w", padx=10)

        result = [None]

        def on_ok():
            resolved = []
            for p in patches:
                if p.get("variants") and p["id"] in variant_vars:
                    idx = variant_vars[p["id"]].get()
                    self.variant_choices[p["id"]] = idx
                    _, chosen_url = p["variants"][idx]
                    resolved.append({**p, "url": chosen_url})
                else:
                    resolved.append(p)
            self._save_path(self.wow_path.get())
            result[0] = resolved
            dlg.destroy()

        def on_cancel():
            dlg.destroy()

        btn_row = tk.Frame(dlg, bg="#0d1117")
        btn_row.pack(fill="x", padx=20, pady=(10, 16))
        ttk.Button(btn_row, text="Start Update", style="Accent.TButton",
                   command=on_ok).pack(side="right", padx=(6, 0))
        ttk.Button(btn_row, text="Cancel",
                   command=on_cancel).pack(side="right")

        dlg.wait_window()
        return result[0]

    def _start_download(self, patches):
        path = self.wow_path.get().strip()
        if not path:
            messagebox.showerror("Error", "Please set the WoW Data folder path first.")
            return
        if not Path(path).is_dir():
            messagebox.showerror("Error", f"Path not found:\n{path}")
            return

        self.cancel_flag[0] = False
        self.btn_cancel.config(state="normal")
        self.btn_download.config(state="disabled")
        self.progress["value"] = 0

        def worker():
            total = len(patches)
            for i, patch in enumerate(patches):
                if self.cancel_flag[0]:
                    break
                self._ui_queue.put(("status", f"Downloading {patch['filename']} ({i+1}/{total})…"))
                dest = Path(path) / patch["filename"]

                def cb(frac, pi=i, tot=total):
                    self._ui_queue.put(("progress", ((pi + frac) / tot) * 100))

                ok, msg = download_file(patch["url"], dest, progress_cb=cb,
                                        cancel_flag=self.cancel_flag)
                if ok:
                    try:
                        clean_name = patch['name'].split('—')[-1].strip()
                        label_text = f"Project Reforged - {clean_name} v{patch['version']}"
                        
                        # Generate TW Launcher label files
                        with open(dest.with_suffix(".txt"), "w", encoding="utf-8") as f:
                            f.write(label_text + "\n")
                            
                        meta = {
                            "name": label_text,
                            "version": str(patch["version"]),
                            "author": "Project Reforged",
                            "description": patch.get("description", ""),
                            "link": "https://projectreforged.github.io/"
                        }
                        with open(dest.with_suffix(".json"), "w", encoding="utf-8") as f:
                            json.dump(meta, f, indent=2)
                    except Exception as e:
                        print("Failed to write label metadata:", e)

                    self.version_store[patch["id"]] = {
                        "version": patch["version"],
                        "installed_at": datetime.now().isoformat(),
                    }
                    save_version_store(self.version_store)
                else:
                    self._ui_queue.put(("error", (patch["name"], msg)))

            save_version_store(self.version_store)
            self._ui_queue.put(("done", None))

        self._download_thread = threading.Thread(target=worker, daemon=True)
        self._download_thread.start()

    # ── Queue polling (keeps UI responsive during download) ──────────────

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self._ui_queue.get_nowait()
                if kind == "progress":
                    self.progress["value"] = payload
                elif kind == "status":
                    self.status_var.set(payload)
                elif kind == "error":
                    name, msg = payload
                    messagebox.showerror("Download Error", f"{name}\n\n{msg}")
                elif kind == "done":
                    self._download_done()
                elif kind == "remote_update":
                    versions, changelog = payload
                    self.changelog_text = changelog
                    for p in PATCHES:
                        if p["id"] in versions:
                            p["version"] = versions[p["id"]]
                    self._populate_tree()
                    self.btn_changelog.config(state="normal")
                    self.status_var.set("Successfully fetched latest patches.")
        except queue.Empty:
            pass
        self.after(50, self._poll_queue)   # poll every 50 ms — smooth & cheap

    def _download_done(self):
        self.btn_cancel.config(state="disabled")
        self.progress["value"] = 100
        self._populate_tree()
        self._on_select()
        self.status_var.set("Done! All downloads complete." if not self.cancel_flag[0] else "Cancelled.")

    def _cancel_download(self):
        self.cancel_flag[0] = True
        self.status_var.set("Cancelling…")

    def _fetch_remote_versions(self):
        url = "https://projectreforged.github.io/changelog.html"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ProjectReforged-PatchManager/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode("utf-8")
            
            versions = {}
            changelog_text = ""
            parts = html.split('<p class="ver">')
            for part in parts[1:]:
                v_match = re.search(r'^v([\d\.]+)</p>', part)
                date_match = re.search(r'<p class="dateSub">(.*?)</p>', part)
                if not v_match: continue
                ver = v_match.group(1)
                date_str = date_match.group(1) if date_match else ""
                
                matches = re.findall(r'<p class="patchTitle">PATCH ([A-Z, \-\(\)]+)</p>', part)
                for p_content in matches:
                    letters = re.findall(r'\b[A-Z]\b', p_content)
                    for letter in letters:
                        pid = f'Patch-{letter}'
                        if pid not in versions:
                            versions[pid] = ver

                changelog_text += f"{'='*40}\nVersion {ver}  -  {date_str}\n{'='*40}\n\n"
                
                blocks = part.split('<div class="patchBlock">')
                for block in blocks[1:]:
                    ptitle = re.search(r'<p class="patchTitle">(.*?)</p>', block)
                    if ptitle:
                        changelog_text += f"{ptitle.group(1)}:\n"
                    
                    items = re.findall(r'<li>(.*?)</li>', block, re.DOTALL)
                    for item in items:
                        item = item.replace('\n', ' ')
                        item = re.sub(r'<[^>]*>', '', item)
                        item = re.sub(r'\s+', ' ', item).strip()
                        if item:
                            changelog_text += f"  • {item}\n"
                    changelog_text += "\n"
                    
                if changelog_text.count('Version ') >= 10:
                    break
            
            self._ui_queue.put(("remote_update", (versions, changelog_text)))
        except Exception as e:
            self._ui_queue.put(("error", ("Failed to fetch changelog", str(e))))

    def _show_changelog(self):
        if not hasattr(self, 'changelog_text') or not self.changelog_text:
            messagebox.showinfo("Changelog", "Changelog is not available yet.")
            return
            
        dlg = tk.Toplevel(self)
        dlg.title("Changelog")
        dlg.configure(bg="#0d1117")
        dlg.geometry("700x500")
        
        # Centre over parent
        self.update_idletasks()
        px = self.winfo_rootx()
        py = self.winfo_rooty()
        pw = self.winfo_width()
        ph = self.winfo_height()
        dlg.geometry(f"+{px + pw//2 - 350}+{py + ph//2 - 250}")
        
        txt = tk.Text(dlg, bg="#161b22", fg="#e6edf3", font=("Consolas", 10),
                      wrap="word", borderwidth=0, padx=10, pady=10)
        txt.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        
        vsb = ttk.Scrollbar(dlg, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        txt.insert("1.0", self.changelog_text)
        txt.config(state="disabled")

    # ── Version record helpers ───────────────

    def _mark_installed(self):
        sel = self.tree.selection()
        if not sel:
            return
        patch_id = sel[0]
        patch = next((p for p in PATCHES if p["id"] == patch_id), None)
        if not patch:
            return
        self.version_store[patch_id] = {
            "version": patch["version"],
            "installed_at": datetime.now().isoformat(),
        }
        save_version_store(self.version_store)
        self._populate_tree()
        self.status_var.set(f"Marked {patch['filename']} as v{patch['version']}.")

    def _remove_record(self):
        sel = self.tree.selection()
        if not sel:
            return
        patch_id = sel[0]
        patch = next((p for p in PATCHES if p["id"] == patch_id), None)
        if not patch:
            return
        if patch_id in self.version_store:
            del self.version_store[patch_id]
            save_version_store(self.version_store)
        self._populate_tree()
        self.status_var.set(f"Removed version record for {patch['filename']}.")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = PatchManagerApp()
    app.mainloop()