import os
import re
import sys
import time
from typing import Optional
from koil.vars import check_cancelled

from rekuest.structures.registry import StructureRegistry
from gucker.env import get_asset_file
from mikro.api.schema import (
    OmeroFileFragment,
    upload_bigfile,
    create_dataset,
    DatasetFragment,
)
from qtpy import QtWidgets, QtGui
from qtpy import QtCore
from arkitekt.qt.magic_bar import MagicBar, ProcessState
from arkitekt.builders import publicqt
from arkitekt import log
import logging


logger = logging.getLogger(__name__)


stregistry = StructureRegistry()


class Gucker(QtWidgets.QMainWindow):
    """The main window of the Gucker application

    This window is the main window of the Gucker application. It is responsible for
    watching a directory and uploading new files to the server.
    """

    is_watching = QtCore.Signal(bool)
    is_uploading = QtCore.Signal(str)
    has_uploaded = QtCore.Signal(str)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        # self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'share\\assets\\icon.png')))
        self.setWindowIcon(QtGui.QIcon(get_asset_file("logo.ico")))

        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.settings = QtCore.QSettings("Gucker", "gg")
        self.base_dir = self.settings.value("base_dir", "")

        self.is_watching.connect(self.is_watching_changed)
        self.is_uploading.connect(self.is_uploading_changed)
        self.has_uploaded.connect(self.has_uploaded_changed)
        self.grace_period = 2
        # Create a bitmap to use toggle for the watching state
        self.watching = False
        self.watching_bitmap = QtGui.QPixmap(get_asset_file("watching_black.png"))
        self.idle_bitmap = QtGui.QPixmap(get_asset_file("idle_black.png"))

        self.center_label = QtWidgets.QLabel()
        self.center_label.setPixmap(self.idle_bitmap)
        self.center_label.setScaledContents(True)

        self.app = publicqt("github.io.jhnnsrs.gucker", "latest", parent=self)
        self.app.enter()
        self.magic_bar = MagicBar(self.app, dark_mode=True)
        self.magic_bar.app_state_changed.connect(
            lambda: self.button.setDisabled(
                self.magic_bar.process_state == ProcessState.PROVIDING
            )
        )
        self.button = QtWidgets.QPushButton("Select Directory to watch")
        self.button.clicked.connect(self.on_base_dir)

        if self.base_dir == "":
            self.button.setText("Select Watching Folder")
            self.magic_bar.magicb.setDisabled(True)
            self.magic_bar.magicb.setText(self.magic_bar.CONNECT_LABEL)
        else:
            self.button.setText(f"Selected {self.base_dir}")
            self.magic_bar.magicb.setDisabled(False)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)

        self.centralWidget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.center_label)
        layout.addWidget(self.button)
        layout.addWidget(self.magic_bar)
        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)

        # self.app.rekuest.register(on_provide=self.on_stream_provide)(self.stream_folder)
        self.app.rekuest.register()(self.stream_files)
        self.setWindowTitle("Gucker")

    def on_base_dir(self):
        self.base_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder"
        )
        if self.base_dir:
            self.button.setText(f"Selected {self.base_dir}")
            self.magic_bar.magicb.setText("Select Folder first")
            self.settings.setValue("base_dir", self.base_dir)
            self.magic_bar.magicb.setDisabled(False)
        else:
            self.button.setText("Select Watching Folder")
            self.settings.setValue("base_dir", "")
            self.magic_bar.magicb.setDisabled(True)
            self.magic_bar.magicb.setText("Select Folder first")

    def is_watching_changed(self, select) -> None:
        if select:
            self.center_label.setPixmap(self.watching_bitmap)
        else:
            self.center_label.setPixmap(self.idle_bitmap)

    def is_uploading_changed(self, select) -> None:
        if select:
            self.statusBar.showMessage(f"Uploading {select}")

    def has_uploaded_changed(self, select) -> None:
        self.statusBar.showMessage(f"Last Upload: {select}")

    def update_provisions(self, select):
        self.qlabel.setText(f"Watching { self.base_dir}")

    def stream_files(
        self,
        dataset: Optional[DatasetFragment],
        regexp: Optional[str],
        indefinitely: bool = False,
    ) -> OmeroFileFragment:
        """Stream Files

        Streams files from a folder to Mikro

        Args:
            dataset (Optional[DatasetFragment]): The Dataset to stream to
            regexp (Optional[str]): A regular expression to filter the files
            indefinitely (bool, optional): Should we stream waiting for new files?. Defaults to False.

        Returns:
            OmeroFileFragment: The uploaded file

        Yields:
            Iterator[OmeroFileFragment]: The uploaded file
        """ """"""

        if not dataset:
            dataset = create_dataset("Streaming Dataset")

        proper_file = re.compile(regexp) if regexp else re.compile(".*")
        base_dir = self.settings.value("base_dir")

        datadir = os.path.join(base_dir)

        log(f"Streaming files of {datadir}")
        first_break = False
        self.is_watching.emit(True)

        uploaded_files = set()

        while not first_break:
            onlyfiles = [
                f
                for f in os.listdir(datadir)
                if os.path.isfile(os.path.join(datadir, f))
                and proper_file.match(f)
                and f not in uploaded_files
            ]

            if not onlyfiles:
                if indefinitely:
                    time.sleep(1)
                    check_cancelled()
                else:
                    first_break = True
            else:
                for file_name in onlyfiles:
                    file_path = os.path.join(datadir, file_name)
                    try:
                        os.rename(file_path, file_path)
                    except OSError:
                        logger.warning(
                            f"Could not rename {file_name}. Probably still in use. Trying this again in 1 seconds."
                        )
                        log(f"Could not rename {file_name}. Probably still in use.")
                        continue

                    self.is_uploading.emit(file_path)
                    yield upload_bigfile(
                        file=file_path, datasets=[dataset] if dataset else None
                    )
                    self.has_uploaded.emit(file_path)
                    uploaded_files.add(file_name)

                time.sleep(1)

        self.is_watching.emit(False)


def main(**kwargs) -> None:
    """Entrypoint for the application"""
    qtapp = QtWidgets.QApplication(sys.argv)
    main_window = Gucker(**kwargs)
    main_window.show()
    sys.exit(qtapp.exec_())


if __name__ == "__main__":
    main()
