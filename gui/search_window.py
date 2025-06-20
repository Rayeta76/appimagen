from __future__ import annotations
from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QScrollArea,
    QWidget,
    QLabel,
    QGridLayout,
    QSizePolicy,
    QDialogButtonBox,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from processing.db import DBManager, ImageRecord


class SearchWindow(QDialog):
    def __init__(self, db: DBManager) -> None:
        super().__init__()
        self.setWindowTitle("Buscar")
        self.db = db

        layout = QVBoxLayout(self)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar...")
        layout.addWidget(self.search_box)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        self.inner = QWidget()
        self.grid = QGridLayout(self.inner)
        self.scroll.setWidget(self.inner)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.search_box.textChanged.connect(self.update_results)
        self.update_results()

    def clear_grid(self) -> None:
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_results(self) -> None:
        text = self.search_box.text()
        results = self.db.search(text)
        self.clear_grid()
        for i, rec in enumerate(results):
            label = QLabel()
            pix = QPixmap(rec.thumbnail)
            label.setPixmap(pix)
            label.setScaledContents(True)
            label.setFixedSize(100, 100)
            label.setSizePolicy(
                QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
            )
            label.setToolTip(f"{rec.title}\n{rec.description}")
            self.grid.addWidget(label, i // 4, i % 4)

        self.inner.adjustSize()

