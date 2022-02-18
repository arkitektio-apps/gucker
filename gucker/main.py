from genericpath import isfile
from os import listdir
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSettings
from arkitekt.messages.postman.provide.bounced_provide import BouncedProvideMessage
from arkitekt.qt.agent import QtAgent
from arkitekt.qt.widgets.magic_bar import MagicBar
from arkitekt.qt.widgets.provisions import ProvisionsWidget
from arkitekt.registry import get_current_agent
import fakts
from fakts.qt import QtFakts
from gucker.env import get_asset_file
import sys
from fakts.grants.qt.qtbeacon import QtSelectableBeaconGrant
from arkitekt import register, useUser
import os
import time

from herre.qt import QtHerre
from mikro.structures import (
    ChannelInput,
    ExperimentFragment,
    OmeroRepresentationInput,
    RepresentationFragment,
    RepresentationVariety,
    Representation,
    Sample,
    create_experiment,
    create_sample,
    from_xarray,
)
import re
import tifffile
import xarray as xr
import namegenerator

BASE_DIR = ""


async def on_stream_provide(provision: BouncedProvideMessage):

    agent = get_current_agent()
    base_dir = agent.settings.value("base_dir")
    if base_dir == "":
        raise Exception("No Basedir was selected!")

    userdir = os.path.join(base_dir, provision.meta.context.user)
    if not os.path.exists(userdir):
        print(f"Creating {userdir}")
        os.makedirs(userdir)

    return base_dir


@register(on_provide=on_stream_provide)
def stream_folder(
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
    creator = useUser()
    exp = experiment or create_experiment(
        name=namegenerator.gen(),
        creator=creator,
        description="A beautiful Little Experiment",
    )

    proper_file = re.compile(regexp)

    agent = get_current_agent()
    base_dir = agent.settings.value("base_dir")

    basedir = os.path.join(base_dir, creator)
    datadir = os.path.join(basedir, subfolder) if subfolder else basedir

    sample_map = {}
    first_break = False

    while not first_break:
        onlyfiles = [f for f in listdir(datadir) if isfile(os.path.join(datadir, f))]
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


class Gucker(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        # self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'share\\assets\\icon.png')))
        self.setWindowIcon(QtGui.QIcon(get_asset_file("logo.ico")))

        self.settings = QSettings("Gucker", "App1")
        self.base_dir = self.settings.value("base_dir", "")

        self.fakts = QtFakts(grants=[QtSelectableBeaconGrant()], subapp="gucker")
        self.herre = QtHerre()
        self.agent = QtAgent()
        self.agent.settings = self.settings
        self.agent.provide_signal.connect(self.on_provide_changed)
        self.agent.provision_signal.connect(self.update_provisions)

        self.provision_widget = ProvisionsWidget(self.agent)

        self.bar = MagicBar(self.fakts, self.herre, self.agent)
        self.button = QtWidgets.QPushButton("Select Base Directory to watch")
        self.button.clicked.connect(self.on_base_dir)

        if self.base_dir == "":
            self.qlabel = QtWidgets.QLabel("No Folder.. nothing to watch")
        else:
            self.qlabel = QtWidgets.QLabel(f"Selected {self.base_dir}")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.qlabel)
        self.layout.addWidget(self.bar)
        self.layout.addWidget(self.provision_widget)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.setWindowTitle("Gucker")
        self.show()

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


def main(**kwargs):
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), 'share\\assets\\icon.png')))
    main_window = Gucker(**kwargs)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
