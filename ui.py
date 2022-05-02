import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from library import read_single_tag, read_double_tag
from ui_interface import *


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set default page
        self.ui.tabWidget.setCurrentIndex(0)
        # show saved information
        self.set_data()

        # event listener
        self.ui.type.currentIndexChanged.connect(self.__onCombo_Changed)
        self.ui.btn_save.clicked.connect(self.__btnSave)
        self.ui.btn_run.clicked.connect(self.__btnRun)
        self.ui.btn_exit.clicked.connect(self.__btnExit)

    def set_data(self):
        """
        set saved information
        """
        # set bot information
        url = read_single_tag("url")
        self.ui.url.setText(url)
        move_path = read_single_tag("move_path")
        self.ui.path.setText(move_path)
        move_name = read_single_tag("move_name")
        self.ui.name.setText(move_name)
        search_date = read_single_tag("search_date")
        date = datetime.datetime.strptime(search_date,"%Y%m%d")
        self.ui.date.setDate(date)
        search_type = int(read_single_tag("search_type"))
        self.ui.type.setCurrentIndex(int(search_type))
        if search_type == 2:
            search_type_dtl = read_single_tag("search_type_dtl")
            self.ui.type_dtl.setValue(int(search_type_dtl))
            self.ui.type_dtl.setReadOnly(False)
            self.ui.type_dtl.setStyleSheet("background-color: white;")
        else:
            self.ui.type_dtl.clear()

        # set file information
        move_path = read_single_tag("move_path")
        self.ui.path.setText(move_path)
        move_name = read_single_tag("move_name")
        self.ui.name.setText(move_name)

        # email tab
        to = read_double_tag("mail","to")
        self.ui.receiver.setText(to)
        cc = read_double_tag("mail","cc")
        self.ui.cc.setText(cc)
        title = read_double_tag("mail","title")
        self.ui.title.setText(title)
        body = read_double_tag("mail","body")
        self.ui.body.setText(body)

    def __onCombo_Changed(self):
        """
        type combobox change event
        if type == 2 activate type_dtl spin box
        else, set type_dtl readonly mode
        """
        if self.ui.type.currentIndex() == 2:
            self.ui.type_dtl.setReadOnly(False)
            self.ui.type_dtl.setStyleSheet("background-color: white;")
        else:
            self.ui.type_dtl.clear()
            self.ui.type_dtl.setReadOnly(True)
            self.ui.type_dtl.setStyleSheet("background-color: rgb(238, 238, 238);")

    def __btnSave(self):
        print("save")

    def __btnRun(self):
        print("run")

    def __btnExit(self):
        self.close()
        sys.exit()


if __name__=="__main__":
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())