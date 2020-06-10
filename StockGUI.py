from PyQt5.QtWidgets import *
import Main as mainstuffdo
import os
#import MainBuffer
import sys
import MainBuffer as buff
import os
app = QApplication([])
button = QPushButton('Click')
def start():
    #mainstuffdo.mainstuff().abcabc()
    buff.runthing(run=True)


def on_button_clicked():

    start()


def on_button_clicked2():
    buff.runthing(run=False)


topRightGroupBox = QGroupBox("Group 2")

defaultPushButton = QPushButton("Start")
defaultPushButton2 = QPushButton("Stop")

layout = QVBoxLayout()
layout.addWidget(defaultPushButton)
layout.addWidget(defaultPushButton2)

layout.addStretch(1)
topRightGroupBox.setLayout(layout)


defaultPushButton.clicked.connect(on_button_clicked)
defaultPushButton2.clicked.connect(on_button_clicked2)


#button.show()
topRightGroupBox.show()


app.exec_()
