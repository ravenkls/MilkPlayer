from PyQt5 import QtWidgets, QtGui, QtCore


class QueueItem(QtWidgets.QFrame):

    def __init__(self, icon, text):
        super().__init__()
        self.icon_data = icon
        self.text = text
        self.init_ui()

    def init_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setSpacing(16)

        self.icon_label = QtWidgets.QLabel()
        thumb = QtGui.QPixmap()
        thumb.loadFromData(self.icon_data)
        self.icon_label.setPixmap(thumb.scaledToHeight(30))
        self.icon_label.setStyleSheet('border-radius: 5px;')
        self.main_layout.addWidget(self.icon_label)

        self.text_label = QtWidgets.QLabel(self.text)
        self.text_label.setFont(QtGui.QFont('Karla', 12))
        self.main_layout.addWidget(self.text_label)

        self.main_layout.addStretch()
        self.setFixedHeight(50)
        self.setLayout(self.main_layout)

        self.set_dark(False)

    def set_dark(self, flag):
        if flag:
            drop_shadow = QtWidgets.QGraphicsDropShadowEffect()
            drop_shadow.setXOffset(0)
            drop_shadow.setYOffset(0)
            drop_shadow.setBlurRadius(15)
            self.setGraphicsEffect(drop_shadow)
            self.setStyleSheet('QFrame{ border-radius: 5px; background: #242424; }')
            self.text_label.setStyleSheet('color: white;')
        else:
            self.setStyleSheet('QFrame{ border-radius: 5px; }')
            self.text_label.setStyleSheet('color: black;')