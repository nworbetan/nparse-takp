import glob, re

from PyQt5.QtWidgets import (QDialog, QComboBox, QPushButton)

from PyQt5.QtCore import Qt

from helpers import config

eq_char_log = ""

class LogSelect(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Select an EQ Character Log')

        listcharbox = QComboBox(self)
        listcharbox.move(10,10)
        listcharbox.currentTextChanged.connect(self.set_char_log)

        self.accept_button = QPushButton(self)
        self.accept_button.setToolTip("Accept log selection")
        self.accept_button.setText("Accept")
        self.accept_button.move(250,50)
        self.accept_button.clicked.connect(self.acc)

        cancel_button = QPushButton(self)
        cancel_button.setToolTip("Cancel log selection")
        cancel_button.setText("Cancel")
        cancel_button.move(350,50)
        cancel_button.clicked.connect(self.canc)

        if config.data['general']['eq_log_dir']:
            for logfile in sorted(glob.glob(config.data['general']['eq_log_dir'] + '/eqlog_*')):
                listcharbox.addItem(logfile)

    def acc(self):
        config.save()
        self.accept()

    def canc(self):
        self.reject()

    def set_char_log(self, text):
        config.data['general']['eq_char_log'] = text
        charname = re.sub(".*eqlog_","",text)
        charname = re.sub("_loginse.*","",charname)
        config.data['general']['eq_charname'] = charname
        self.accept_button.setText("Load {}".format(charname))
