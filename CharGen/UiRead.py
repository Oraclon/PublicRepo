import sys;
from PyQt5 import uic;
from PyQt5.QtWidgets import *;

class MainUi(QWidget):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi('uis/CharGenUI.ui', self);
        self.show()

if __name__== '__main__':
    app= QApplication(sys.argv);
    window= MainUi();
    app.exec();
