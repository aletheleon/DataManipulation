'''
Queue by Alejandro Hernandez
Featutes added:
- Official Georgia Tech Colors
- Prefilled Name Input Field
- Checkbox to disable adding further students
- Time Arrived is displayed alongside student name
- Stylized fonts
- A Pixmap Widget of Buzz using URL (online connection needed)
- Changed window background color
- Added the current day
- Added the current time
- Added timer to update the day and the time
- Pressing Return / Enter key will act as pressing the Add button
- Pressing Delete key will act as pressing the Remove button
- Pressing Escape key will close the GUI
- Pressing Alt key will minimize the GUI window
'''

import sys
from PyQt5.QtCore import QRect, QDateTime, QDate, QTime, QTimer, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QCheckBox,
    QVBoxLayout, QApplication, QLineEdit, QListWidget, QPushButton)
from PyQt5 import QtGui
import urllib.request
import time

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Official Georgia Tech colors
        TechGold = QtGui.QColor(179,163,105)
        TechBlue = QtGui.QColor(0,38,58)
        BuzzGold = QtGui.QColor(234,179,0)

        left_box = QVBoxLayout()

        url = 'https://hamblen.ece.gatech.edu/ALTERA/onedge/gatech/images/gtbuzz.gif'
        data = urllib.request.urlopen(url).read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        buzz = QLabel()
        buzz.setPixmap(pixmap)
        left_box.addWidget(buzz)

        ta_box = QHBoxLayout()
        ta_label = QLabel()
        ta_label.setFont(QtGui.QFont("Arial", 33, QtGui.QFont.Black))
        ta_label.setText("TA's On Duty:")
        self.ta_show = QLineEdit()
        self.ta_show.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Expanded))
        self.ta_show.setPlaceholderText("There are no TA's Signed In")
        self.ta_show.setAlignment(Qt.AlignCenter)
        ta_box.addWidget(ta_label)
        ta_box.addWidget(self.ta_show)

        left_box.addLayout(ta_box)

        timer = QTimer(self)
        timer.timeout.connect(self.showDateTime)
        timer.start(1000)

        self.date_label = QLabel()
        self.date_label.setFont(QtGui.QFont("Arial", 25, QtGui.QFont.Black, QtGui.QFont.Expanded))
        self.date_label.setAlignment(Qt.AlignCenter)
        self.time_label = QLabel()
        self.time_label.setFont(QtGui.QFont("Arial", 25, QtGui.QFont.Black, QtGui.QFont.Expanded))
        self.time_label.setAlignment(Qt.AlignCenter)
        left_box.addWidget(self.date_label)
        left_box.addWidget(self.time_label)

        wrapper_box = QHBoxLayout()
        wrapper_box.setAlignment(Qt.AlignCenter)
        self.is_open = QCheckBox('Open')
        self.is_open.setFont(QtGui.QFont("Arial", 25, QtGui.QFont.Expanded))
        self.is_open.toggle()
        self.is_open.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.is_open.stateChanged.connect(self.close_queue)

        wrapper_box.addWidget(self.is_open)
        left_box.addLayout(wrapper_box)

        self.is_open.setStyleSheet("margin-left:50%; margin-right:50%;")

        self.student_count = QLabel()
        self.student_count.setFont(QtGui.QFont("Arial", 25))
        self.student_count.setAlignment(Qt.AlignCenter)
        left_box.addWidget(self.student_count)
        left_box.setAlignment(Qt.AlignCenter)

        student_box = QVBoxLayout()
        student_label = QLabel()
        student_label.setFont(QtGui.QFont("Arial", 33, QtGui.QFont.Black))
        student_label.setText("Student Queue:")
        self.student_show = QListWidget()
        self.student_show.setFont(QtGui.QFont("Arial", 18))
        self.student_in = QLineEdit()
        self.student_in.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Expanded))
        self.student_in.setPlaceholderText("Your Name Here")
        self.student_in.setAlignment(Qt.AlignCenter)
        self.student_add = QPushButton()
        self.student_add.setText('Add')
        self.student_add.setFont(QtGui.QFont("Arial", 16))
        student_rem = QPushButton()
        student_rem.setText('Remove')
        student_rem.setFont(QtGui.QFont("Arial", 16))
        student_box.addWidget(student_label)
        student_box.addWidget(self.student_show)
        student_box.addWidget(self.student_in)
        student_box.addWidget(self.student_add)
        student_box.addWidget(student_rem)

        self.student_count.setText("Queue Count: " + str(self.student_show.count()))

        self.student_add.clicked.connect(self.add_student)
        student_rem.clicked.connect(self.rem_student)

        hbox = QHBoxLayout()
        hbox.addLayout(left_box)
        hbox.addLayout(student_box)
        hbox.setAlignment(Qt.AlignCenter)

        p = self.palette()
        p.setColor(self.backgroundRole(), TechGold)
        self.setPalette(p)

        self.setLayout(hbox)
        self.setWindowTitle('CS2316 Help Desk Queue')
        self.showFullScreen()

    def add_student(self):
        if all(char.isalpha() or char.isspace() for char in str(self.student_in.text())) and len(str(self.student_in.text())) and self.student_add.isEnabled():
            time_in = QTime.currentTime()
            self.student_show.addItem("   "+self.student_in.text() + ' ('+time_in.toString(Qt.DefaultLocaleLongDate)+')')
            self.student_in.clear()
            self.student_count.setText("Queue Count: " + str(self.student_show.count()))
        else:
            self.student_in.clear()

    def rem_student(self):
        self.student_show.takeItem(self.student_show.currentIndex().row())
        self.student_count.setText("Queue Count: " + str(self.student_show.count()))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.add_student()
        elif e.key() == Qt.Key_Delete:
            self.student_rem()
        elif e.key() == Qt.Key_Alt:
            self.showNormal()

    def showDateTime(self):
        self.time_label.setText(QTime.currentTime().toString(Qt.DefaultLocaleLongDate))
        self.date_label.setText(QDate.currentDate().toString(Qt.DefaultLocaleLongDate))

    def close_queue(self):
        if self.is_open.isChecked():
            self.student_add.setEnabled(True)
        else:
            self.student_add.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
