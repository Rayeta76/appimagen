from __future__ import annotations
import os
from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QProgressBar,
    QAction,
    QApplication,
)
from PySide6.QtCore import Qt

from processing.db import DBManager, ImageRecord
from processing.florence_wrapper import Florence2ImageTagger
from processing.thumbnails import ThumbnailGenerator
from gui.search_window import SearchWindow

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AppImagen")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.select_btn = QPushButton("Seleccionar carpeta de imágenes")
        layout.addWidget(self.select_btn)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        search_action = QAction("Buscar", self)
        search_action.triggered.connect(self.open_search)
        self.menuBar().addAction(search_action)

        self.select_btn.clicked.connect(self.select_folder)

        self.db = DBManager()
        self.tagger = Florence2ImageTagger()
        self.thumb = ThumbnailGenerator()

    def log_message(self, msg: str) -> None:
        self.log.append(msg)

    def select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            self.process_folder(Path(folder))

    def process_folder(self, folder: Path) -> None:
        files: List[Path] = [
            p
            for p in folder.rglob("*")
            if p.suffix.lower() in IMAGE_EXTS and p.is_file()
        ]
        total = len(files)
        self.progress.setMaximum(total)
        for i, fpath in enumerate(files, start=1):
            self.progress.setValue(i)
            title, desc, tags = self.tagger.process(str(fpath))
            new_name = fpath.with_stem(title)
            os.rename(fpath, new_name)
            xml_path = new_name.with_suffix(".xml")
            xml_path.write_text(desc, encoding="utf-8")
            tags_path = new_name.with_suffix(".tags.txt")
            tags_path.write_text(",".join(tags), encoding="utf-8")
            thumb_path = self.thumb.create_thumbnail(str(new_name))
            record = ImageRecord(title, desc, str(new_name), thumb_path)
            self.db.insert_image(record, tags)
            self.log_message(f"Procesado: {new_name.name}")
        self.log_message("Completado")
        self.progress.setValue(0)

    def open_search(self) -> None:
        dlg = SearchWindow(self.db)
        dlg.exec()


def main() -> None:
    app = QApplication([])
    win = MainWindow()
    win.resize(600, 400)
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
