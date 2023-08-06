# ! python3
# -*- encoding: utf-8 -*-
# mypy: ignore-errors

import os
import sys
from glob import glob

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QKeySequence, QPalette, QPixmap
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QAction,
    QApplication,
    QBoxLayout,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QScrollArea,
    QSizePolicy,
    QToolBar,
    QWidget,
)

from .abstract_convert_to_pil import AbstractConvertToPil


class QtDatasetViewer(QMainWindow):
    images = dict()
    pointer = 0

    def __init__(self, dataloader: AbstractConvertToPil = None):
        super().__init__()
        self.scale_factor = 0.0

        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Ignored
        )
        self.image_label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setVisible(False)

        self.progress_bar = QProgressBar()

        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.progress_bar)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Image Viewer")
        self.window_width, self.window_height = (
            self.geometry().width(),
            self.geometry().height(),
        )
        self.setWindowIcon(QIcon("../icons/favicon.jpeg"))
        self.resize(self.window_width * 1.5, self.window_height * 1.5)

        self.filemenu = self.menuBar().addMenu("&File")

        self.filetoolbar = QToolBar("File")
        self.filetoolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.filetoolbar)

        self.open_doc_opt = self.makeAction(
            self,
            "../icons/open.png",
            "Open Folder...",
            "Open Folder...",
            self.open_folder,
        )
        self.open_doc_opt.setShortcut(QKeySequence.Open)
        self.prev_image = self.makeAction(
            self, "", "Prev image", "Prev image", self.prev_image
        )
        self.prev_image.setShortcut(QKeySequence("Left"))
        self.next_image = self.makeAction(
            self, "", "Next image", "Next image", self.next_image
        )
        self.next_image.setShortcut(QKeySequence("Right"))
        self.filemenu.addActions([self.open_doc_opt])
        self.filemenu.addSeparator()

        self.exit_opt = self.makeAction(self, "", "Exit", "Exit", self.close)
        self.filemenu.addActions([self.exit_opt])
        self.filetoolbar.addActions([self.prev_image, self.next_image])

        if dataloader is not None:
            self.pointer = 0
            self.dataloader = dataloader
            self.progress_bar.setMaximum(
                max(0, self.dataloader.get_size() - 1)
            )
            self.open_image_from_dataloader()

    def open_image_from_dataloader(self):
        pil_image = self.dataloader.convert(
            self.dataloader.get_dataloader()[self.pointer]
        )
        image = QPixmap.fromImage(ImageQt(pil_image))
        self.image_label.setPixmap(image)
        self.scale_factor = 1.0
        self.scroll_area.setVisible(True)
        self.fit_window_to_image()
        self.fit_to_window()

    def next_image(self):
        if (
            self.pointer + 1 < len(self.images)
            or self.pointer + 1 < self.dataloader.get_size()
        ):
            self.pointer += 1
            self.open_image_by_pointer()

    def prev_image(self):
        if self.pointer > 0:
            self.pointer -= 1
            self.open_image_by_pointer()

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")

        types = ("*.jpg", "*.png", "*.webp", ".jpeg")
        images = []
        for files in types:
            images.extend(glob(folder_path + os.sep + files))
        self.images = {i: images[i] for i in range(len(images))}
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(max(0, len(images) - 1))
        self.pointer = 0
        self.open_image_by_pointer()

    def open_image_by_pointer(self):
        self.progress_bar.setValue(self.pointer)
        if self.dataloader is not None:
            self.open_image_from_dataloader()
        else:
            self.open_image(self.images.get(self.pointer, None))

    def open_image(self, file_name: str):
        if file_name:
            self.setWindowTitle(file_name.split(os.sep)[-1])
            image = QImage(file_name)
            if image.isNull():
                QMessageBox.information(
                    self, "Image Viewer", "Cannot load %s." % file_name
                )
                return
            self.image_label.setPixmap(QPixmap.fromImage(image))
            self.scale_factor = 1.0

            self.scroll_area.setVisible(True)
            self.fit_to_window()

    def fit_window_to_image(self):
        im_width = self.image_label.pixmap().size().width()
        im_height = self.image_label.pixmap().size().height()
        self.window_width, self.window_height = (
            im_width * 1.04,
            im_height * 1.16,
        )
        self.resize(self.window_width, self.window_height)

    def fit_to_window(self):
        im_width = self.image_label.pixmap().size().width()
        im_height = self.image_label.pixmap().size().height()
        scale = 1
        if im_width > self.window_width:
            scale = self.window_width / im_width
        elif im_height > self.window_height:
            scale = self.window_height / im_height
        self.scale_image(scale)

    def scale_image(self, sf: float):
        self.scale_factor *= sf
        self.image_label.resize(
            self.scale_factor * self.image_label.pixmap().size()
        )

        self.adjust_scroll_bar(self.scroll_area.horizontalScrollBar(), sf)
        self.adjust_scroll_bar(self.scroll_area.verticalScrollBar(), sf)

    def adjust_scroll_bar(self, scroll_bar: QAbstractScrollArea, sf: float):
        scroll_bar.setValue(
            int(
                sf * scroll_bar.value()
                + ((sf - 1) * scroll_bar.pageStep() / 2)
            )
        )

    def makeAction(
        self,
        parent_obj,
        icon_destination,
        name_of_action,
        status_tip,
        triggered_method,
    ):
        act = QAction(QIcon(icon_destination), name_of_action, parent_obj)
        act.setStatusTip(status_tip)
        act.triggered.connect(triggered_method)
        return act


def run_qt_dataset_viewer(dataloader: AbstractConvertToPil = None):
    the_app = QApplication(sys.argv)
    app = QtDatasetViewer(dataloader)
    app.show()
    sys.exit(the_app.exec_())


if __name__ == "__main__":
    run_qt_dataset_viewer()
