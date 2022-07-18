from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
from os import stat, remove
import pyAesCrypt

buffer_size = 128 * 1024
password = '1511'


class FileLabel(QLabel):
    def __init__(self):
        super().__init__()
        # set center alignment of image label
        self.setAlignment(Qt.AlignCenter)
        # set text on image label
        self.setText('Drop File Here')
        # set the label style
        self.setStyleSheet('''QLabel{border: 3px dashed green}''')


class dragDrop(QWidget):
    def __init__(self):
        super().__init__()
        # set window title
        self.setWindowTitle("File encrypt or decrypt")
        # set window geometry
        self.setGeometry(500, 200, 400, 400)
        # set Dop event to True
        self.setAcceptDrops(True)
        # create box layout
        layout = QVBoxLayout()
        # create label for image
        self.file_label = FileLabel()
        # add image label in box layout
        layout.addWidget(self.file_label)
        # set layout
        self.setLayout(layout)
        # show window
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()

            name, ext = os.path.splitext(file_path)
            # print(name, ext)

            if ext == '.aes':
                end_file_size = stat(file_path).st_size

                with open(file_path, 'rb') as file:
                    try:
                        with open(name, 'wb') as out:
                            pyAesCrypt.decryptStream(file, out, password, buffer_size, end_file_size)
                    except ValueError:
                        remove(name)

            else:
                with open(file_path, 'rb') as file:
                    with open(file_path + '.aes', 'wb') as out:
                        pyAesCrypt.encryptStream(file, out, password, buffer_size)


app = QApplication(sys.argv)
drag_drop_app = dragDrop()
sys.exit(app.exec_())
