import sys
from wordinfolist import WordInfoList
from flowlayout import FlowLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class WordInfoWidget(QWidget):

    def __init__(self, wordinfolist, with_title=False, parent=None):
        super(WordInfoWidget, self).__init__(parent)

        self.wordinfolist = wordinfolist
        self.field_labels = []

        self.lyt = QGridLayout(self)
        
        if with_title:
            label = QLabel(F'{self.wordinfolist.name}')
            label.setObjectName('Title')
            self.lyt.addWidget(label, 0, 0, 1, 2)
        
        for field_name in self.wordinfolist.field_names():
            row = self.lyt.rowCount()
            self.lyt.addWidget(QLabel(F'{field_name}:'), row, 0)
            self.field_labels.append(QLabel('-'))
            self.lyt.addWidget(self.field_labels[-1], row, 1)

    def set_word(self, word):
        for i, field_data in enumerate(self.wordinfolist.field_data(word)):
            self.field_labels[i].setText(field_data)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.load_wordlists()

        self.setWindowTitle('JWordInfo')
        self.setWindowIcon(QIcon('./icon.ico'))

        try:
            stylesheet = open('stylesheet.css', 'r').read()
            self.setStyleSheet(stylesheet)
        except:
            pass

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.lyt = QVBoxLayout(self.central_widget)

        self.line_edit = QLineEdit()
        self.line_edit.textChanged.connect(self.on_line_change)
        self.lyt.addWidget(self.line_edit)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.lyt.addWidget(self.scroll_area)

        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area_lyt = FlowLayout(self.scroll_area_widget, grid=True)

        self.wordinfowidges = []

        for wordinfolist in self.wordinfolists:
            self.wordinfowidges.append(WordInfoWidget(wordinfolist, with_title=True))
            self.scroll_area_lyt.addWidget(self.wordinfowidges[-1])

        if len(self.wordinfowidges) < 1:
            self.scroll_area_lyt.addWidget(QLabel('No list loaded'))

        self.line_edit.setText('ようこそ')


    def load_wordlists(self):
        self.wordinfolists = []

        try:
            f = open('lists.txt', 'r', encoding='utf-8-sig')
        except:
            QMessageBox.warning(self, 'Error', 'Word list configuration was not found!')
            return

        for l in f:
            if l.startswith('#'):
                continue
            l = l.rstrip()
            if l != '':
                try:
                    l = WordInfoList(l)
                    self.wordinfolists.append(l)
                except ValueError as e:
                    QMessageBox.warning(self, 'Error', F'Loading a word list failed:\n\n{l}\n\n{str(e)}')

        f.close()


    def on_line_change(self, text):
        text = text.strip()

        for wordinfowidget in self.wordinfowidges:
            wordinfowidget.set_word(text)



if __name__ == "__main__":

    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
