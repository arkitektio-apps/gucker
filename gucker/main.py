import os
import re
import sys
import time
from typing import Optional
from koil.vars import check_cancelled
from rekuest.messages import Provision

from rekuest.structures.registry import StructureRegistry
from gucker.env import get_asset_file
from mikro.api.schema import (
    ChannelInput,
    ExperimentFragment,
    OmeroFileFragment,
    OmeroRepresentationInput,
    RepresentationFragment,
    RepresentationVariety,
    aget_representation,
    create_experiment,
    create_sample,
    from_xarray,
    upload_bigfile,
    DatasetFragment
)
from qtpy import QtWidgets, QtGui
from qtpy import QtCore
from arkitekt.qt.magic_bar import MagicBar
from arkitekt.builders import publicqt
from arkitekt import log
import tifffile
import namegenerator
import xarray as xr


stregistry = StructureRegistry()


stregistry.register_as_structure(
    RepresentationFragment, "representation", aget_representation
)


class Gucker(QtWidgets.QMainWindow):
    is_watching = QtCore.Signal(bool)
    is_uploading = QtCore.Signal(str)
    has_uploaded = QtCore.Signal(str)


    def __init__(self, **kwargs):
        super().__init__()
        # self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'share\\assets\\icon.png')))
        self.setWindowIcon(QtGui.QIcon(get_asset_file("logo.ico")))

        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.settings = QtCore.QSettings("Gucker", "gg")
        self.base_dir = self.settings.value("base_dir", "")

        self.is_watching.connect(self.is_watching_changed)
        self.is_uploading.connect(self.is_uploading_changed)
        self.has_uploaded.connect(self.has_uploaded_changed)

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


    def is_watching_changed(self, select):
        if select:
            self.center_label.setPixmap(self.watching_bitmap)
        else:
            self.center_label.setPixmap(self.idle_bitmap)

    def is_uploading_changed(self, select):
        if select:
            self.statusBar.showMessage(f"Uploading {select}")

    def has_uploaded_changed(self, select):
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
        """        """"""
        proper_file = re.compile(regexp) if regexp else re.compile(".*")
        base_dir = self.settings.value("base_dir")

        datadir = os.path.join(base_dir)

        log(f"Streaming items of {datadir}")
        sample_map = {}
        first_break = False
        self.is_watching.emit(True)

        while not first_break:
            onlyfiles = [
                f
                for f in os.listdir(datadir)
                if os.path.isfile(os.path.join(datadir, f))
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

                    m = proper_file.match(file_name)
                    if m:
                        self.is_uploading.emit(file_path)
                        yield upload_bigfile(
                            file=file_path,
                            datasets=[dataset] if dataset else None
                        )
                        self.has_uploaded.emit(file_path)

                    os.remove(file_path)

        self.is_watching.emit(False)
    

def main(**kwargs):
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'share\\assets\\icon.png')))
    main_window = Gucker(**kwargs)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
