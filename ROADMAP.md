# 🛣️ Quick Anime Renamer Redux — Roadmap

This document outlines planned features and direction for upcoming releases of **Quick Anime Renamer Redux**.

The project prioritizes:
- Predictable behavior
- Offline, local-only operation
- Minimal UI complexity
- Opt-in automation

---

## ✅ Current Stable Version

**v1.1.6**
- Stable persistence of settings
- Portable INI-based configuration
- Reliable startup and shutdown behavior
- Two-column rename preview
- Undo rename support

---

## 🎯 v1.2 — Quality of Life & Safety

**Focus:** Workflow efficiency, safety, and polish  
**Scope:** Non-breaking, opt-in improvements only

---

### 🔄 Auto-load Last Directory on Startup *(Optional)*
- New checkbox:
  - **“Auto-load last directory on startup”**
- When enabled:
  - Automatically scans the previously used directory when the app opens
  - Populates the rename preview immediately
- Safeguards:
  - No action if the directory no longer exists
  - Silent failure (no popups)

**Rationale:**  
Reduces repetitive setup for users working in the same folders regularly.

---

### 🗑️ Remove Files from Rename List
- Press **Delete** to remove selected rows from the preview list
- Does **not** delete files from disk
- Only affects the current rename batch

**Rationale:**  
Allows quick exclusion of files without reloading or restarting.

---

### ⚠️ Filename Conflict Detection
- Detect conflicts before renaming:
  - Target filename already exists on disk
  - Duplicate output filenames within the same batch
- Behavior:
  - Highlight conflicted rows
  - Prevent accidental overwrites
  - Display clear warnings when required

**Rationale:**  
Improves safety and builds user trust during batch operations.

---

### 🪟 Remember Window Size & Position
- Save window:
  - Width
  - Height
  - Screen position
- Restore on next launch

**Rationale:**  
Improves usability and perceived polish with minimal complexity.

---

## 🌟 Stretch Goals (Time Permitting)

### 👁️ Highlight Changed Filenames
- Visually distinguish rows where:
  - Original filename ≠ New filename
- Makes previews easier to scan at a glance

---

### 📋 Copy Rename Preview to Clipboard
- Copy original → new filename pairs
- Useful for:
  - Manual review
  - Logging
  - Sharing rename plans

---

### 🧹 Clear List Button
- Clears the current preview list
- Does not affect files on disk

---

## 🚫 Explicitly Out of Scope (v1.2)

The following are intentionally excluded from v1.2:

- Automatic renaming on launch
- Recursive subfolder scanning
- Media database integration (AniList, MAL, etc.)
- Network or online features
- Episode renumbering logic

These may be reconsidered for future versions.

---

## 🧭 Future Direction (Post-v1.2)

Future releases may explore:
- Optional recursive scanning
- Enhanced episode parsing
- Additional safety checks
- UI refinements based on user feedback

All future work will continue to prioritize simplicity and user control.

---

_Last updated: v1.1.6_
