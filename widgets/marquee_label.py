from PyQt5 import QtWidgets, QtCore, QtGui
import time


class CheckHoverThread(QtCore.QThread):

    mouse_enter = QtCore.pyqtSignal()
    mouse_leave = QtCore.pyqtSignal()
    mouse_hovering = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.hovering = False

    def run(self):
        while True:
            if self.parent.underMouse() and not self.hovering:
                self.mouse_enter.emit()
                self.hovering = True
            elif not self.parent.underMouse() and self.hovering:
                self.mouse_leave.emit()
                self.hovering = False
            elif self.hovering:
                self.mouse_hovering.emit()
            time.sleep(0.05)



class MarqueeLabel(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_x = 0
        self.marquee = False
        self.check_hover_thread = CheckHoverThread(self)
        self.check_hover_thread.mouse_enter.connect(self.start_marquee)
        self.check_hover_thread.mouse_hovering.connect(self.repaint)
        self.check_hover_thread.mouse_leave.connect(self.end_marquee)
        self.check_hover_thread.start()

    def setColour(self, colour):
        self._colour = colour

    def start_marquee(self):
        self.marquee = True
        self.repaint()
    
    def end_marquee(self):
        self.marquee = False
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        if self.marquee:
            font_width = QtGui.QFontMetrics(self.font()).width(self.text())
            if self.label_x > -font_width:
                self.label_x -= 2
            else:
                self.label_x = self.width()
        else:
            self.label_x = 0

        painter.setFont(self.font())
        painter.setPen(QtCore.Qt.white)
        painter.drawText(self.label_x, self.height() - 4, self.text())