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
from gucker.api.schema import get_export_stage, get_export_dataset
from mikro import Stage, Image
import tifffile
from arkitekt.tqdm import tqdm
import json

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
        self.export_dir = self.settings.value("export_dir", "")

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
        self.exportbutton = QtWidgets.QPushButton("Select Directory to export")
        self.exportbutton.clicked.connect(self.on_export_dir)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)

        self.centralWidget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.center_label)
        layout.addWidget(self.button)
        layout.addWidget(self.exportbutton)
        layout.addWidget(self.magic_bar)
        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)

        # self.app.rekuest.register(on_provide=self.on_stream_provide)(self.stream_folder)
        self.app.rekuest.register()(self.stream_files)
        self.app.rekuest.register()(self.export_stage)
        self.app.rekuest.register()(self.export_dataset)
        self.setWindowTitle("Gucker")

        self.check_folders_sane()

    def on_base_dir(self):
        self.base_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Stream Folder"
        )
        if self.base_dir:
            self.settings.setValue("base_dir", self.base_dir)
            self.button.setText(f"Selected {self.base_dir}")
        else:
            self.button.setText("Select Watching Folder")

        self.check_folders_sane()

    def check_folders_sane(self):
        if not self.base_dir:
            self.button.setText("Select Watching Folder")
            self.statusBar.showMessage("Select a folder to watch first")
            self.magic_bar.magicb.setDisabled(True)
            return False

        self.button.setText(f"Selected {self.base_dir}")
        if not self.export_dir:
            self.exportbutton.setText("Select Export Folder")
            self.statusBar.showMessage("Select a folder to export first")
            self.magic_bar.magicb.setDisabled(True)
            return False

        self.exportbutton.setText(f"Selected {self.export_dir}")
        self.statusBar.showMessage("All set ready to go")
        self.magic_bar.magicb.setDisabled(False)
        return True

    def on_export_dir(self):
        self.export_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Export Folder"
        )
        if self.export_dir:
            self.settings.setValue("export_dir", self.export_dir)
            self.exportbutton.setText(f"Selected {self.export_dir}")
        else:
            self.exportbutton.setText("Select Export Folder")

        self.check_folders_sane()

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

    def export_representation(self, representation: Image, dir: str) -> None:
        tifffile.imsave(
            os.path.join(dir, f"ID({representation.id}) {representation.name}.tiff"),
            representation.data,
        )
        with open(
            os.path.join(
                dir, f"ID({representation.id}) {representation.name} meta.json"
            ),
            "w",
        ) as f:
            f.write(
                json.dumps(representation.dict(), indent=4, sort_keys=True, default=str)
            )

    def export_stage(self, stage: Stage) -> None:
        """Export Stage

        Exports the stage to the export directory

        Args:
            stage (Stage): The stage to export
        """
        assert self.export_dir, "No export directory selected"
        export_stage = get_export_stage(stage)
        print(export_stage)

        stage_dir = os.path.join(self.export_dir, f"ID({stage.id}) {export_stage.name}")
        os.makedirs(stage_dir, exist_ok=True)
        for item in tqdm(export_stage.positions):
            pos_dir = os.path.join(stage_dir, f"ID({item.id}) {item.name}")
            os.makedirs(pos_dir, exist_ok=True)
            with open(os.path.join(pos_dir, "position.json"), "w") as f:
                f.write(
                    json.dumps(item.dict(), indent=4, sort_keys=True, default=str),
                )
            for image in item.omeros:
                image_dir = os.path.join(
                    pos_dir,
                    f"ID({image.representation.id}) {image.representation.name} {image.acquisition_date}",
                )
                os.makedirs(image_dir, exist_ok=True)
                with open(os.path.join(image_dir, "raw.json"), "w") as f:
                    f.write(
                        json.dumps(image.dict(), indent=4, sort_keys=True, default=str)
                    )
                self.export_representation(image.representation, image_dir)

                for file in image.representation.derived:
                    self.export_representation(file, image_dir)

    def export_dataset(self, dataset: DatasetFragment) -> None:
        """Export Files in Dataset

        Exports the files of a dataset to the export directory
        (does not include images but only original files))

        Args:
            stage (Stage): The stage to export
        """
        assert self.export_dir, "No export directory selected"
        export_dataset = get_export_dataset(dataset)
        print(export_dataset)

        export_dir = os.path.join(
            self.export_dir, f"ID({export_dataset.id}) {export_dataset.name}"
        )
        os.makedirs(export_dir, exist_ok=True)
        for item in tqdm(export_dataset.omerofiles):
            item.file.download(filename=os.path.join(export_dir, item.name))


def main(**kwargs) -> None:
    """Entrypoint for the application"""
    qtapp = QtWidgets.QApplication(sys.argv)
    main_window = Gucker(**kwargs)
    main_window.show()
    sys.exit(qtapp.exec_())


if __name__ == "__main__":
    main()
