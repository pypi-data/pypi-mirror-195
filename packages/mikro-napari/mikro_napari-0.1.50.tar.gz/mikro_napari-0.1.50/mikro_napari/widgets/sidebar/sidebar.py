import napari
from koil.qt import QtRunner
from mikro.api.schema import (
    ROIFragment,
    aexpand_roi,
)
from qtpy import QtWidgets
from qtpy import QtCore
from arkitekt.apps.connected import ConnectedApp
from mikro_napari.utils import NapariROI


class RoiWidget(QtWidgets.QWidget):
    """A widget for displaying ROIs."""

    def __init__(self, app: ConnectedApp, roi: NapariROI, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self.detailquery = QtRunner(aexpand_roi)
        self.detailquery.returned.connect(self.update_layout)
        self.detailquery.run(roi.id)

    def update_layout(self, roi: ROIFragment):
        self._layout.addWidget(QtWidgets.QLabel(roi.label))
        if roi.creator.email:
            self._layout.addWidget(QtWidgets.QLabel(roi.creator.email))
        self._layout.addWidget(QtWidgets.QLabel(roi.id))


class SidebarWidget(QtWidgets.QWidget):
    emit_image: QtCore.Signal = QtCore.Signal(object)

    def __init__(
        self, viewer: napari.Viewer, app: ConnectedApp = None, *args, **kwargs
    ) -> None:
        super(SidebarWidget, self).__init__(*args, **kwargs)
        self.viewer = viewer
        self.viewer.window.sidebar = self

        self.mylayout = QtWidgets.QVBoxLayout()
        self.app = app

        self.open_image_button = QtWidgets.QPushButton("Change Content")

        self._active_widget = QtWidgets.QLabel("Nothing selected")
        self.mylayout.addWidget(self._active_widget)
        self.mylayout.addStretch()

        self.setLayout(self.mylayout)

    def replace_widget(self, widget):
        self.mylayout.removeWidget(self._active_widget)
        del self._active_widget
        self._active_widget = widget
        self.mylayout.addWidget(self._active_widget)

    def select_roi(self, roi: NapariROI):
        self.replace_widget(RoiWidget(self.app, roi))
        pass
