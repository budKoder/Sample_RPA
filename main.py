import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from library import read_single_tag, read_double_tag, update_single_tag, update_double_tag
from message_box import showMbox, MB_OK, MB_YESNO, ICON_INFO
from file_control import bringFront
from ui_interface import *
from bot import run


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/icon/icon/sample_icon.ico'))

        # set default page
        self.ui.tabWidget.setCurrentIndex(0)
        # show saved information
        self.set_data()

        # event listener
        self.ui.type.currentIndexChanged.connect(self.__onCombo_Changed)
        self.ui.btn_save.clicked.connect(self.__btnSave)
        self.ui.btn_run.clicked.connect(self.__btnRun)
        self.ui.btn_exit.clicked.connect(self.__btnExit)

        QAction(QIcon(':/icon/icon/sample_icon.ico'),'Exit',self)

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
        self.ui.body.setPlainText(body)

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
        idx = self.ui.tabWidget.currentIndex()
        if idx == 0:
            self.__saveBot()
        else:
            self.__saveEmail()

    def __saveBot(self):
        result = showMbox("Do yon want to save?", "Info", MB_YESNO|ICON_INFO)
        if result == 7:
            return

        url = self.ui.url.text()
        date = self.ui.date.date().getDate()
        date_val = str(date[0]) + str(date[1]).zfill(2) + str(date[2]).zfill(2)
        type = self.ui.type.currentIndex()
        type_dtl = self.ui.type_dtl.value()
        path = self.ui.path.text()
        name = self.ui.name.text()

        options = ["url","search_date","search_type","search_type_dtl","move_path","move_name"]
        params = [url, date_val, type, type_dtl, path, name]

        for i in range(len(options)):
            opt = options[i]
            val = params[i]
            update_single_tag(opt, val)

        showMbox("Save Complete!", "Info", MB_OK|ICON_INFO)

    def __saveEmail(self):
        result = showMbox("Do you want to save?", "Info", MB_YESNO|ICON_INFO)
        if result == 7:
            return

        to = self.ui.receiver.text()
        cc = self.ui.cc.text()
        title = self.ui.title.text()
        body = self.ui.body.toPlainText()
        options = ["to","cc","title","body"]
        params = [to,cc,title,body]

        for i in range(len(options)):
            opt = options[i]
            val = params[i]
            update_double_tag("mail",opt,val)

        showMbox("Save Complete!", "Info", MB_OK|ICON_INFO)

    def __btnRun(self):
        run()
        bringFront("RPA Sample")

    def __btnExit(self):
        self.close()
        sys.exit()


if __name__=="__main__":
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())