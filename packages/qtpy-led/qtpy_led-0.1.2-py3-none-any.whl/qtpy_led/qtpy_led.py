# -*- coding: utf-8 -*-

# Python imports
import numpy as np
import pyautogui

# QtPy imports
from qtpy.QtCore import QSize, Signal
from qtpy.QtWidgets import QPushButton


class Led(QPushButton):
    status_changed: Signal = Signal(bool)  # type: ignore

    black = np.array([0x00, 0x00, 0x00], dtype=np.uint8)
    white = np.array([0xFF, 0xFF, 0xFF], dtype=np.uint8)
    blue = np.array([0x73, 0xCE, 0xF4], dtype=np.uint8)
    green = np.array([0xAD, 0xFF, 0x2F], dtype=np.uint8)
    orange = np.array([0xFF, 0xA5, 0x00], dtype=np.uint8)
    purple = np.array([0xAF, 0x00, 0xFF], dtype=np.uint8)
    red = np.array([0xF4, 0x37, 0x53], dtype=np.uint8)
    yellow = np.array([0xFF, 0xFF, 0x00], dtype=np.uint8)

    capsule = 1
    circle = 2
    rectangle = 3

    def __init__(
        self, parent, on_color=green, off_color=black, shape=rectangle, build="release"
    ):
        super().__init__(parent=parent)  # type: ignore
        if build == "release":
            self.setDisabled(True)
        else:  # For example 'debug'
            self.setEnabled(True)

        self._qss = "QPushButton {{ \
                                   border: 3px solid lightgray; \
                                   border-radius: {}px; \
                                   background-color: \
                                       QLinearGradient( \
                                           y1: 0, y2: 1, \
                                           stop: 0 white, \
                                           stop: 0.2 #{}, \
                                           stop: 0.8 #{}, \
                                           stop: 1 #{} \
                                       ); \
                                 }}"
        self._on_qss = ""
        self._off_qss = ""

        self._status = False
        self._end_radius = 0

        # Properties that will trigger changes on qss.
        self.__on_color = None
        self.__off_color = None
        self.__shape = None
        self.__height = 0

        self._on_color = on_color
        self._off_color = off_color
        self._shape = shape
        self._height = self.sizeHint().height()

        self.set_status(False)

    # =================================================== Reimplemented Methods
    def mousePressEvent(self, event):
        QPushButton.mousePressEvent(self, event)
        if self._status is False:
            self.set_status(True)
        else:
            self.set_status(False)

    def sizeHint(self):
        res_w, res_h = pyautogui.size()  # Available resolution geometry
        base_w = 0
        base_h = 0
        if self._shape == Led.capsule:
            base_w = 50
            base_h = 30
        elif self._shape == Led.circle:
            base_w = 30
            base_h = 30
        elif self._shape == Led.rectangle:
            base_w = 40
            base_h = 30
        width = int(base_w * res_h / 1080)
        height = int(base_h * res_h / 1080)
        return QSize(width, height)  # type: ignore

    def resizeEvent(self, event):
        self._height = self.size().height()
        QPushButton.resizeEvent(self, event)

    def setFixedSize(self, width, height):  # noqa
        self._height = height
        if self._shape == Led.circle:
            QPushButton.setFixedSize(self, height, height)  # type: ignore
        else:
            QPushButton.setFixedSize(self, width, height)  # type: ignore

    # ============================================================== Properties
    @property
    def _on_color(self):
        return self.__on_color

    @_on_color.setter
    def _on_color(self, color):
        self.__on_color = color
        self._update_on_qss()

    @_on_color.deleter
    def _on_color(self):
        del self.__on_color

    @property
    def _off_color(self):
        return self.__off_color

    @_off_color.setter
    def _off_color(self, color):
        self.__off_color = color
        self._update_off_qss()

    @_off_color.deleter
    def _off_color(self):
        del self.__off_color

    @property
    def _shape(self):
        return self.__shape

    @_shape.setter
    def _shape(self, shape):
        self.__shape = shape
        self._update_end_radius()
        self._update_on_qss()
        self._update_off_qss()
        self.set_status(self._status)

    @_shape.deleter
    def _shape(self):
        del self.__shape

    @property
    def _height(self):
        return self.__height

    @_height.setter
    def _height(self, height):
        self.__height = height
        self._update_end_radius()
        self._update_on_qss()
        self._update_off_qss()
        self.set_status(self._status)

    @_height.deleter
    def _height(self):
        del self.__height

    # ================================================================= Methods
    def _update_on_qss(self):
        color, grad = self._get_gradient(self.__on_color)
        self._on_qss = self._qss.format(self._end_radius, grad, color, color)

    def _update_off_qss(self):
        color, grad = self._get_gradient(self.__off_color)
        self._off_qss = self._qss.format(self._end_radius, grad, color, color)

    def _get_gradient(self, color):
        grad = ((self.white - color) / 2).astype(np.uint8) + color
        grad = "{:02X}{:02X}{:02X}".format(grad[0], grad[1], grad[2])
        color = "{:02X}{:02X}{:02X}".format(color[0], color[1], color[2])
        return color, grad

    def _update_end_radius(self):
        if self.__shape == Led.rectangle:
            self._end_radius = int(self.__height / 10)
        else:
            self._end_radius = int(self.__height / 2)

    def _toggle_on(self):
        self.setStyleSheet(self._on_qss)
        self.status_changed.emit(True)

    def _toggle_off(self):
        self.setStyleSheet(self._off_qss)
        self.status_changed.emit(False)

    def set_on_color(self, color):
        self._on_color = color

    def set_off_color(self, color):
        self._off_color = color

    def set_shape(self, shape):
        self._shape = shape

    def set_status(self, status):
        self._status = True if status else False
        if self._status is True:
            self._toggle_on()
        else:
            self._toggle_off()

    def turn_on(self, status=True):
        self.set_status(status)

    def turn_off(self, status=False):
        self.set_status(status)

    def is_on(self):
        return True if self._status is True else False

    def is_off(self):
        return True if self._status is False else False


if __name__ == "__main__":
    from qtpy.QtCore import Qt
    from qtpy.QtWidgets import QApplication
    from qtpy.QtWidgets import QGridLayout
    from qtpy.QtWidgets import QWidget
    import sys

    class Demo(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent)
            self._shape = np.array(["capsule", "circle", "rectangle"])
            self._color = np.array(
                ["blue", "green", "orange", "purple", "red", "yellow"]
            )
            self._layout = QGridLayout(self)
            self._create_leds()
            self._arrange_leds()

        def keyPressEvent(self, e):
            if e.key() == Qt.Key_Escape:
                self.close()

        def _create_leds(self):
            for s in self._shape:
                for c in self._color:
                    exec(
                        'self._{}_{} = Led(self, on_color=Led.{}, \
                          shape=Led.{}, build="debug")'.format(
                            s, c, c, s
                        )
                    )
                    exec("self._{}_{}.setFocusPolicy(Qt.NoFocus)".format(s, c))

        def _arrange_leds(self):
            for r in range(3):
                for c in range(6):
                    exec(
                        "self._layout.addWidget(self._{}_{}, {}, {}, 1, 1, \
                          Qt.AlignCenter)".format(
                            self._shape[r], self._color[c], r, c
                        )
                    )
                    c += 1
                r += 1

    app = QApplication(sys.argv)  # type: ignore
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
