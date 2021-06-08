import glob

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

        btnchar = QPushButton(self)
        btnchar.setToolTip("Cancel log selection")
        btnchar.setText("Cancel")
        btnchar.move(350,50)
        btnchar.clicked.connect(self.cancelled)

        if config.data['general']['eq_log_dir']:
            for logfile in glob.glob(config.data['general']['eq_log_dir'] + '/eqlog_*'):
                listcharbox.addItem(logfile)

    def cancelled(self):
        self.reject()

    def set_char_log(self, text):
        config.data['general']['eq_char_log'] = text
        config.save()
        self.close()
