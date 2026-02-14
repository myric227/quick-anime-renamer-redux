# Quick Anime Renamer Redux

A modern Windows revival of **Quick Anime Renamer**.

## Features
- Drag & drop anime videos
- Folder batch renaming
- Two-column preview
- Smart episode detection (S02E06 → S02 - 06)
- Undo last rename
- Delete key removes files from batch
- Remembers settings
- Native light/dark mode

## Credits
Created by **Justin Morland**  
Inspired by the original *Quick Anime Renamer* by **Joshua Park**  
Not affiliated with the original project.

## Build
Requires Python 3.10+ and PySide6.

```powershell
pip install pyside6 pyinstaller
python -m PyInstaller --onefile --windowed --icon=quick_anime_renamer_redux.ico quick_anime_renamer_redux.py
