# 🛠 RS3-DataTool

**RS3-DataTool** is a PySide6 desktop application focused on providing RuneScape 3 reference data in a fast, local-first interface.

The Windows release is distributed as a portable zip archive with a SHA-256 checksum for verification.

The application provides live lookup tools for Grand Exchange items, Bestiary monsters, public player hiscores, and RuneScape Wiki pages. It also supports local saved profiles, item favorites, monster favorites, and saved Wiki references through simple JSON storage.

RS3-DataTool is designed as a read-only reference companion. It does not automate gameplay, interact with the RuneScape client, collect account credentials, or provide macro functionality.

---

## 📃 Features

### 📊 Grand Exchange Lookup

Search RuneScape 3 Grand Exchange items and view item data such as:

* Item name
* Item ID
* Item type
* Membership status
* Current price
* Exact price data where available
* Trade volume where available
* Price trends
* Item icon
* RuneScape Wiki reference

**Additional GE features:**

* Save favorite items locally
* Load saved favorite items
* Delete saved favorite items
* Open the related RuneScape Wiki page
* Save item Wiki pages to the Wiki Portal

---

### 🔍 Bestiary Lookup

Search RuneScape 3 monsters and view Bestiary data such as:

* Monster name
* Monster ID
* Description
* Membership status
* Combat level
* Lifepoints
* XP
* Weakness
* Combat stats
* Slayer category
* Slayer requirement
* Behavior flags (poisonous, attackable, and aggressive)
* Known locations
* RuneScape Wiki reference

**Additional Bestiary features:**

* Save favorite monsters locally
* Load saved favorite monsters
* Delete saved favorite monsters
* Open the related RuneScape Wiki page
* Save monster Wiki pages to the Wiki Portal

---

### 📝 Profile Lookup

Search public RuneScape 3 player hiscores and view:

* Display name
* Overall rank
* Total level
* Total XP
* Individual skill levels
* Individual skill XP
* Individual skill ranks

**Additional Profile features:**

* Save player profiles locally
* Load saved profiles
* Delete saved profiles
* Current profile state label

Only public hiscore data is used. RS3-DataTool does not ask for account credentials.

---

### 🌐 Wiki Portal

Search RuneScape Wiki pages directly from the desktop app.

Wiki Portal features:

* Search RuneScape Wiki pages
* Open Wiki pages in the default browser
* Save Wiki pages locally
* Load saved Wiki pages
* Delete saved Wiki pages
* Double-click saved pages to open directly
* Use suggested page results for broad searches

The Wiki Portal acts as a reference hub for pages saved from GE, Bestiary, and direct Wiki searches.

---

## 📥 Local Storage

RS3-DataTool uses local JSON files for saved user data.

Expected local storage files:

```text
data/
├── profiles.json
├── favorites.json
└── wiki_pages.json
```

These files are created locally and should not be committed to version control.

Recommended `.gitignore` entry:

```gitignore
data/
```

---

## 📂 Project Structure

```text
RS3-DataTool/
├── api/
│   ├── ge_api.py
│   ├── bestiary_api.py
│   ├── profile_api.py
│   └── wiki_api.py
│
├── pages/
│   ├── ge_page.py
│   ├── bestiary_page.py
│   ├── profile_page.py
│   └── wiki_page.py
│
├── storage/
│   ├── profile_store.py
│   ├── favorites_store.py
│   └── page_store.py
│
├── main.py
├── main_window.py
├── requirements.txt
├── README.md
├── SUPPORT.md
└── LICENSE
```

---

## 💾 Installation

### Windows Release

The recommended way to use RS3-DataTool on Windows is to download the packaged release from the GitHub Releases page.

1. Download `RS3-DataTool-v1.0.0-win64.zip`
2. Extract the zip folder
3. Open the extracted `RS3-DataTool` folder
4. Run `RS3-DataTool.exe`

A SHA-256 checksum is provided in `SHA256SUMS.txt` so users can verify the release archive.

Verify the release zip on Windows PowerShell:

```powershell
Get-FileHash .\RS3-DataTool-v1.0.0-win64.zip -Algorithm SHA256
```

Compare the output against the hash listed in `SHA256SUMS.txt`.

---

### Run From Source

Clone the repository:

```bash
git clone https://github.com/Sgt-Ahab/RS3-Datatool.git
cd RS3-Datatool
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python main.py
```

---

## 📚 Requirements

Core dependencies:

```text
PySide6==6.11.1
requests==2.33.1
```

Install them with:

```bash
pip install -r requirements.txt
```

The packaged Windows release includes the required runtime files and does not require users to manually install Python dependencies.

---

## 🚧 Current Development Status

Implemented:

* Live Grand Exchange lookup
* Live Bestiary lookup
* Live public Profile lookup
* Live RuneScape Wiki Portal search
* Saved player profiles
* Saved GE item favorites
* Saved Bestiary monster favorites
* Saved Wiki pages
* Local JSON persistence
* Current object state labels
* Wiki open/save integration from GE and Bestiary
* Dark RuneScape-inspired UI theme
* Scrollable profile results panel
* Windows executable packaging
* SHA-256 release verification file

Current phase:

```text
RS3-DataTool v1.0.0 is released as a stable Windows desktop utility.
```

Next milestone:

```text
v1.1.0 will focus on threaded operations, stronger error handling, saved-data export/import, and in-app version labeling.
```


---

## 🕒 Planned Improvements

RS3-DataTool v1.0.0 is the initial stable Windows release.

The next planned release, **v1.1.0**, is intended to focus on polish, stability, and portability rather than major feature expansion.

### Planned for v1.1.0

* Threaded lookup operations to keep the interface responsive during network requests
* Improved error handling for failed API calls, missing data, and connection issues
* Favorite export/import tools for moving saved items, monsters, profiles, and Wiki references between installs
* A structured saved-data export format for easier backup and sharing
* Version label or About/footer area inside the application
* Minor documentation and packaging refinements

### Long-term project direction

RS3-DataTool is intended to remain a focused, read-only RuneScape 3 reference utility.

Future work should continue to prioritize:

* Local-first saved data
* Clean desktop usability
* Public data lookup
* Safe project boundaries
* No automation, macros, overlays, client hooks, or credential collection

---

## ❌ Project Boundaries

RS3-DataTool is:

* A read-only desktop reference tool
* A local-first utility
* An unofficial RuneScape 3 companion app
* A convenience tool for public data lookup

**RS3-DataTool is not:**

* A RuneScape client
* A bot
* A macro tool
* An overlay
* A gameplay automation tool
* A credential collection tool

---

## 🔗 Data Sources

RS3-DataTool uses publicly available RuneScape-related data sources, including:

* RuneScape Wiki
* RuneScape Grand Exchange data
* RuneScape Bestiary data
* RuneScape public hiscores
* Weird Gloop where applicable

This project is **unofficial** and is *not affiliated with, endorsed by, or sponsored by Jagex.*

###### RuneScape and related names are property of their respective owners.

---

## 💰 Support

If this project is useful to you, optional support is available through the project support page.

Support **helps** with:

* Continued development
* Documentation
* Testing
* Packaging
* Maintenance
* Future local-first utility projects

*Core functionality remains free.*

---

## 📄 License

This project is released under the license included in the repository.

See `LICENSE` for details.

---

###### 💛 Gielinor needs the compendium of Data!