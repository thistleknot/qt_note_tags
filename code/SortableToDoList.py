import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (Qt, QStringListModel, QModelIndex,
                          QMimeData, QByteArray, QDataStream, QIODevice)
from PySide6.QtWidgets import (QApplication, QMainWindow, QListView, QLineEdit, QAbstractItemView, QPushButton, QVBoxLayout, QWidget, QTextEdit, QPlainTextEdit)


class DragDropListModel(QStringListModel):
    def __init__(self, parent=None):
        super(DragDropListModel, self).__init__(parent)
        # self.myMimeTypes = 'application/vnd.text.list' # 可行

        # self.myMimeTypes = "text/plain" # 可行
        self.myMimeTypes = 'application/json'  # 可行

    def supportedDropActions(self):
        # return Qt.CopyAction | Qt.MoveAction  # 拖动时复制并移动相关项目
        return Qt.MoveAction  # 拖动时移动相关项目

    def flags(self, index):
        defaultFlags = QStringListModel.flags(self, index)

        if index.isValid():
            return Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | defaultFlags
        else:
            return Qt.ItemIsDropEnabled | defaultFlags

    def mimeTypes(self):
        return [self.myMimeTypes]

    # 直接将indexes里面对应的数据取出来，然后打包进了QMimeData()对象，并返回
    def mimeData(self, indexes):
        mmData = QMimeData()
        encodedData = QByteArray()
        stream = QDataStream(encodedData, QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                text = self.data(index, Qt.DisplayRole)
                stream << text  # 测试，也行
                # stream.writeQString(str(text))  # 原始, 可行

        mmData.setData(self.myMimeTypes, encodedData)
        return mmData

    def canDropMimeData(self, data, action, row, column, parent):
        if data.hasFormat(self.myMimeTypes) is False:
            return False
        if column > 0:
            return False
        return True

    def dropMimeData(self, data, action, row, column, parent):
        if self.canDropMimeData(data, action, row, column, parent) is False:
            return False

        if action == Qt.IgnoreAction:
            return True

        beginRow = -1
        if row != -1:  # 表示
            print("case 1: ROW IS NOT -1, meaning inserting in between, above or below an existing node")
            beginRow = row
        elif parent.isValid():
            print("case 2: PARENT IS VALID, inserting ONTO something since row was not -1, "
                  "beginRow becomes 0 because we want to "
                  "insert it at the beginning of this parents children")
            beginRow = parent.row()
        else:
            print("case 3: PARENT IS INVALID, inserting to root, "
                  "can change to 0 if you want it to appear at the top")
            beginRow = self.rowCount(QModelIndex())
        print(f"row={row}, beginRow={beginRow}")

        encodedData = data.data(self.myMimeTypes)
        stream = QDataStream(encodedData, QIODevice.ReadOnly)
        newItems = []
        rows = 0

        while stream.atEnd() is False:
            text = stream.readQString()
            newItems.append(str(text))
            rows += 1

        self.insertRows(beginRow, rows, QModelIndex())  # 先插入多行
        for text in newItems:  # 然后给每一行设置数值
            idx = self.index(beginRow, 0, QModelIndex())
            self.setData(idx, text)
            beginRow += 1

        return True


class DemoDragDrop(QWidget):
    def __init__(self, parent=None):
        super(DemoDragDrop, self).__init__(parent)

        # 设置窗口标题
        self.setWindowTitle('Sortable To Do List')
        # 设置窗口大小
        self.resize(480, 320)

        self.initUi()

    def initUi(self):
        self.vLayout = QVBoxLayout(self)
        self.listView = QListView(self)
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listView.setDragEnabled(True)
        self.listView.setAcceptDrops(True)
        self.listView.setDropIndicatorShown(True)
        self.ddm = DragDropListModel()  # 该行和下面4行的效果类似
        # self.listView.setDragDropMode(QAbstractItemView.InternalMove)
        # self.listView.setDefaultDropAction(Qt.MoveAction)
        # self.listView.setDragDropOverwriteMode(False)
        # self.ddm = QStringListModel()

        self.ddm.setStringList(['Item 1', 'Item 2', 'Item 3', 'Item 4'])
        self.listView.setModel(self.ddm)


        self.printButton = QPushButton("Print")
        self.addButton = QPushButton("Add")
        self.delButton = QPushButton("Del")

        self.textField = QLineEdit()

        self.vLayout.addWidget(self.listView)
        #self.vLayout.addWidget(self.printButton)
        self.vLayout.addWidget(self.addButton)
        self.vLayout.addWidget(self.delButton)
        #self.vLayout.addWidget(self.textField)

        self.printButton.clicked.connect(self.printModel)
        self.addButton.clicked.connect(self.addModel)
        self.delButton.clicked.connect(self.delModel)

    def printModel(self):  # 验证移动view中项目后，背后model中数据也发生了移动
        print(self.ddm.data(self.listView.currentIndex()))

    def addModel(self):
        #temp = QListString
        #text = self.textField.text()

        #self.ddm.setStringList(['Item 1', 'Item 2', 'Item 3', 'Item 4', text])
        self.ddm.insertRows(self.ddm.rowCount(),1)
        #self.listView.setModel(self.ddm)

    def delModel(self):
        #temp = QListString
        #text = self.textField.text()

        #self.ddm.setStringList(['Item 1', 'Item 2', 'Item 3', 'Item 4', text])
        #self.tableView.currentIndex().row()
        self.ddm.removeRows(self.ddm.rowCount()-1,1)
        #print(self.ddm.data(self.listView.currentIndex().row()))
        #self.ddm.removeRows(4)
        #self.listView.setModel(self.ddm)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = DemoDragDrop()
    window.show()
    sys.exit(app.exec_())