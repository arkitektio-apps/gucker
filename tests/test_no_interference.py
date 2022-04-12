from gucker.main import Gucker
import pytest

@pytest.mark.qt
def test_fetch_from_windowed_grant(qtbot):
    widget = Gucker()
    qtbot.addWidget(widget)