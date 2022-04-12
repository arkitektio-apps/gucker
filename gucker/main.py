import os
import re
import sys
from time import time
from typing import List
from arkitekt.definition.registry import register
from arkitekt.messages import Provision

from arkitekt.structures.registry import StructureRegistry
from fakts.fakts import Fakts
from gucker.env import get_asset_file
from koil.qt import QtRunner
from mikro.api.schema import (
    ChannelInput,
    ExperimentFragment,
    OmeroRepresentationInput,
    RepresentationFragment,
    RepresentationVariety,
    aget_representation,
    create_experiment,
    create_sample,
    from_xarray,
)
from qtpy import QtWidgets, QtGui
from fakts.grants.qt.qtbeacon import QtSelectableBeaconGrant, SelectBeaconWidget
from qtpy import QtCore
from mikro.arkitekt import ConnectedApp
from koil.composition.qt import QtPedanticKoil
from herre.fakts import FaktsHerre
from arkitekt.qt.magic_bar import MagicBar
import tifffile
import namegenerator
import xarray as xr


stregistry = StructureRegistry()


stregistry.register_as_structure(
    RepresentationFragment, "representation", aget_representation
)


class Gucker(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        # self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'share\\assets\\icon.png')))
        self.setWindowIcon(QtGui.QIcon(get_asset_file("logo.ico")))

        self.settings = QtCore.QSettings("Gucker", "App1")
        self.base_dir = self.settings.value("base_dir", "")

        self.app = ConnectedApp(
            koil=QtPedanticKoil(uvify=False, auto_connect=True, parent=self),
            fakts=Fakts(
                subapp="gucker",
                grants=[
                    QtSelectableBeaconGrant(widget=SelectBeaconWidget(parent=self))
                ],
                assert_groups={"mikro"},
            ),
            herre=FaktsHerre(login_on_enter=False),
        )
        self.app.koil.connect()

        self.magic_bar = MagicBar(self.app, dark_mode=True)
        self.button = QtWidgets.QPushButton("Select Base Directory to watch")
        self.button.clicked.connect(self.on_base_dir)

        if self.base_dir == "":
            self.qlabel = QtWidgets.QLabel("No Folder.. nothing to watch")
        else:
            self.qlabel = QtWidgets.QLabel(f"Selected {self.base_dir}")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.qlabel)
        self.layout.addWidget(self.magic_bar)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.app.arkitekt.register(on_provide=self.on_stream_provide)(
            self.stream_folder
        )
        self.setWindowTitle("Gucker")

    def on_base_dir(self):
        self.base_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder"
        )
        self.settings.setValue("base_dir", self.base_dir)
        self.qlabel.setText(f"Selected { self.base_dir}")

    def on_provide_changed(self, select):
        if select:
            self.qlabel.setText(f"Watching { self.base_dir}")
        else:
            self.qlabel.setText(f"Stoped Watching { self.base_dir}")

    def update_provisions(self, select):
        self.qlabel.setText(f"Watching { self.base_dir}")

    async def on_stream_provide(self, provision: Provision):
        if self.base_dir == "":
            raise Exception("No Basedir was selected!")

        userdir = os.path.join(self.base_dir, "user")
        if not os.path.exists(userdir):
            print(f"Creating {userdir}")
            os.makedirs(userdir)

    def stream_folder(
        self,
        subfolder: str = None,
        sleep_interval: int = 1,
        regexp: str = "(?P<magnification>[^x]*)x(?P<sample>[^_]*)__w(?P<channel_index>[0-9]*)(?P<channel_name>[^-]*)-(?P<wavelength>[^_]*)_s(?P<sample_index>[0-9]*)_t(?P<time_index>[0-9]*).TIF",
        experiment: ExperimentFragment = None,
        force_match=False,
    ) -> RepresentationFragment:
        """Stream Tiffs in Folder

        Streams Tiffs in the subfolder in the user directory that was specified.

        Args:
            folder (str, optional): The subfolder name. Defaults to None.
            sleep_interval (int, optional): The sleep interval if we didnt find a new image. Defaults to 1.
            regexp (str, optional): A regular expression defining extraction of metadata. Defaults to None.
            experiment_name (str, optional): The newly created Experiment we will create. Defaults to random name.
            force_match (bool, optional): Do you force a match for the regexp?

        Returns:
            Representation: [description]

        Yields:
            Iterator[Representation]: [description]
        """
        creator = None
        exp = experiment or create_experiment(
            name=namegenerator.gen(),
            creator=creator,
            description="A beautiful Little Experiment",
        )

        proper_file = re.compile(regexp)
        base_dir = self.settings.value("base_dir")

        basedir = os.path.join(base_dir, creator)
        datadir = os.path.join(basedir, subfolder) if subfolder else basedir

        sample_map = {}
        first_break = False

        while not first_break:
            onlyfiles = [
                f for f in os.listdir(datadir) if os.isfile(os.path.join(datadir, f))
            ]
            if not onlyfiles:
                print("No Files.. Sleeping One Second")
                # first_break = True
                time.sleep(sleep_interval)
            else:
                for file_name in onlyfiles:
                    file_path = os.path.join(datadir, file_name)

                    m = proper_file.match(file_name)
                    if m:
                        meta = m.groupdict()

                        t = int(meta["time_index"])
                        s = int(meta["sample_index"])
                        c = int(meta["channel_index"])
                        channel_name = str(meta["channel_name"])

                        if s not in sample_map:
                            sample_map[s] = create_sample(
                                experiments=[exp.id],
                                name=f"{meta['sample']} {s}",
                                meta={"s": s},
                                creator=creator,
                            )

                        sample = sample_map[s]

                        image = tifffile.imread(file_path)
                        image = image.reshape(
                            (1, 1) + image.shape
                        )  # we will deal with z-stack, lets expand them
                        array = xr.DataArray(image, dims=list("ctzyx"))

                        yield from_xarray(
                            array,
                            name=f"{sample.name} - T {t}",
                            tags=["initial"],
                            variety=RepresentationVariety.VOXEL,
                            creator=creator,
                            meta={"t": t, "c": c},
                            sample=sample,
                            omero=OmeroRepresentationInput(
                                scale=[1, 1, 4, 1, 1],
                                channels=[ChannelInput(name=channel_name)],
                            ),
                        )

                        # Simulate Acquisition
                        os.remove(file_path)


def main(**kwargs):
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'share\\assets\\icon.png')))
    main_window = Gucker(**kwargs)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
