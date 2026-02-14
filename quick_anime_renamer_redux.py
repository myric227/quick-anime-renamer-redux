import os
import re

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QCheckBox, QFileDialog,
    QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMenuBar
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QSettings, Qt

# -----------------------
# App Info
# -----------------------
APP_NAME = "Quick Anime Renamer Redux"
APP_VERSION = "1.0.1"

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".avi", ".mov", ".wmv"}


class AnimeRenamer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(800, 500)

        self.settings = QSettings("AnimeTools", "QuickAnimeRenamerRedux")

        self.files = []
        self.rename_history = []

        self.build_ui()
        self.load_settings()

    # -----------------------
    # UI
    # -----------------------
    def build_ui(self):
        main_layout = QVBoxLayout()

        # Menu bar
        menu = QMenuBar()
        help_menu = menu.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        main_layout.setMenuBar(menu)

        title = QLabel("Drag & Drop Anime Videos or Select a Folder")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        # Rules
        self.cb_brackets = QCheckBox("Remove [ ]")
        self.cb_parentheses = QCheckBox("Remove ( )")
        self.cb_curly = QCheckBox("Remove { }")
        self.cb_underscore = QCheckBox("Replace _ with spaces")
        self.cb_dots = QCheckBox("Replace . with spaces")
        self.cb_episode = QCheckBox("Auto-detect episode numbers")

        for cb in (
            self.cb_brackets, self.cb_parentheses, self.cb_curly,
            self.cb_underscore, self.cb_dots, self.cb_episode
        ):
            main_layout.addWidget(cb)

        # Buttons
        btn_row = QHBoxLayout()
        self.btn_folder = QPushButton("Select Folder")
        self.btn_preview = QPushButton("Preview")
        self.btn_apply = QPushButton("Apply Rename")
        self.btn_undo = QPushButton("Undo Last Rename")
        self.btn_undo.setEnabled(False)

        for btn in (self.btn_folder, self.btn_preview, self.btn_apply, self.btn_undo):
            btn_row.addWidget(btn)

        main_layout.addLayout(btn_row)

        # Preview table
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Original Name", "New Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.setAcceptDrops(True)

        # Signals
        self.btn_folder.clicked.connect(self.select_folder)
        self.btn_preview.clicked.connect(self.preview_files)
        self.btn_apply.clicked.connect(self.apply_rename)
        self.btn_undo.clicked.connect(self.undo_rename)

    # -----------------------
    # Drag & Drop
    # -----------------------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.files.clear()
        self.table.setRowCount(0)

        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path) and self.is_video(path):
                self.files.append(path)

        self.preview_files()

    # -----------------------
    # Delete key removes from list
    # -----------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            rows = sorted(
                {index.row() for index in self.table.selectionModel().selectedRows()},
                reverse=True
            )

            for row in rows:
                del self.files[row]
                self.table.removeRow(row)

            event.accept()
        else:
            super().keyPressEvent(event)

    # -----------------------
    # File Handling
    # -----------------------
    def is_video(self, path):
        return os.path.splitext(path)[1].lower() in VIDEO_EXTENSIONS

    def select_folder(self):
        start = self.settings.value("last_dir", "")
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", start)

        if folder:
            self.settings.setValue("last_dir", folder)
            self.files = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if self.is_video(f)
            ]
            self.preview_files()

    # -----------------------
    # Episode Detection
    # -----------------------
    def detect_episode(self, name):
        # Season + episode (S02E06)
        m = re.search(r"[sS](\d{1,2})[eE](\d{1,4})", name)
        if m:
            return m.group(1), m.group(2)

        # Episode only
        m = re.search(r"\b[eE][pP]? ?(\d{1,4})\b", name)
        if m:
            return None, m.group(1)

        m = re.search(r"[ ._-](\d{1,4})[ ._-]", name)
        if m:
            return None, m.group(1)

        return None, None

    # -----------------------
    # Rename Logic
    # -----------------------
    def clean_name(self, filename):
        name, ext = os.path.splitext(filename)

        season, episode = (
            self.detect_episode(name) if self.cb_episode.isChecked() else (None, None)
        )

        # Remove junk tags
        if self.cb_brackets.isChecked():
            name = re.sub(r"\[.*?\]", "", name)
        if self.cb_parentheses.isChecked():
            name = re.sub(r"\(.*?\)", "", name)
        if self.cb_curly.isChecked():
            name = re.sub(r"\{.*?\}", "", name)

        # Remove episode tokens
        if episode is not None:
            if season is not None:
                name = re.sub(r"[ ._-]-?[ ._-]*[sS]\d{1,2}[eE]\d{1,4}", "", name)
            else:
                name = re.sub(r"\b[eE][pP]? ?\d{1,4}\b", "", name)
                name = re.sub(r"[ ._-]\d{1,4}[ ._-]", " ", name)

        if self.cb_underscore.isChecked():
            name = name.replace("_", " ")
        if self.cb_dots.isChecked():
            name = name.replace(".", " ")

        # Normalize spacing
        name = re.sub(r"\s*-\s*", " - ", name)
        name = re.sub(" +", " ", name).strip(" -")

        # Rebuild
        if episode is not None:
            if season is not None:
                return f"{name} - S{season.zfill(2)} - {episode}{ext}"
            return f"{name} - {episode}{ext}"

        return f"{name}{ext}"

    # -----------------------
    # Preview
    # -----------------------
    def preview_files(self):
        self.table.setRowCount(0)

        for f in self.files:
            old = os.path.basename(f)
            new = self.clean_name(old)

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(old))
            self.table.setItem(row, 1, QTableWidgetItem(new))

        self.save_settings()

    # -----------------------
    # Apply / Undo
    # -----------------------
    def apply_rename(self):
        self.rename_history.clear()

        for f in self.files:
            folder = os.path.dirname(f)
            old = os.path.basename(f)
            new = self.clean_name(old)

            old_path = f
            new_path = os.path.join(folder, new)

            if old_path != new_path:
                os.rename(old_path, new_path)
                self.rename_history.append((old_path, new_path))

        if self.rename_history:
            self.btn_undo.setEnabled(True)
            QMessageBox.information(self, "Done", "Files renamed successfully.")

        self.table.setRowCount(0)

    def undo_rename(self):
        for old, new in reversed(self.rename_history):
            if os.path.exists(new):
                os.rename(new, old)

        self.rename_history.clear()
        self.btn_undo.setEnabled(False)

        QMessageBox.information(self, "Undo", "Last rename operation has been undone.")

    # -----------------------
    # Settings
    # -----------------------
    def save_settings(self):
        self.settings.setValue("brackets", self.cb_brackets.isChecked())
        self.settings.setValue("parentheses", self.cb_parentheses.isChecked())
        self.settings.setValue("curly", self.cb_curly.isChecked())
        self.settings.setValue("underscore", self.cb_underscore.isChecked())
        self.settings.setValue("dots", self.cb_dots.isChecked())
        self.settings.setValue("episode", self.cb_episode.isChecked())

    def load_settings(self):
        self.cb_brackets.setChecked(self.settings.value("brackets", True, bool))
        self.cb_parentheses.setChecked(self.settings.value("parentheses", True, bool))
        self.cb_curly.setChecked(self.settings.value("curly", False, bool))
        self.cb_underscore.setChecked(self.settings.value("underscore", True, bool))
        self.cb_dots.setChecked(self.settings.value("dots", False, bool))
        self.cb_episode.setChecked(self.settings.value("episode", True, bool))

    # -----------------------
    # About
    # -----------------------
    def show_about(self):
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"""
<b>{APP_NAME}</b><br>
Version {APP_VERSION}<br><br>

<b>Created by Justin Morland</b><br><br>

Inspired by the original <i>Quick Anime Renamer</i><br>
by <b>Joshua Park</b>.<br><br>

<i>Not affiliated with the original project.</i><br><br>

© 2026
"""
        )


# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    app = QApplication([])
    window = AnimeRenamer()
    window.show()
    app.exec()
