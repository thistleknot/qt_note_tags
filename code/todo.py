import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from MainWindow import Ui_MainWindow

class TodoModel(QtCore.QAbstractListModel):

    def __init__(self, parent, items=None):
        super(self.__class__, self).__init__()
        print("initiating MyListModel")
        self.parent = parent
        self._items = list()

        for thing in items:
            self._items.append(thing)

        self.setSupportedDragActions(QtCore.Qt.MoveAction)

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self._items)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if (role == QtCore.Qt.DisplayRole) or (role == QtCore.Qt.EditRole):
            return self._items[index.row()].name
        else:
            return

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        print("Setting Data", value, "at", index.row())

        if role == QtCore.Qt.EditRole:
            print("EditRole")
            self._items[index.row()].name = value
            return True
        elif role == QtCore.Qt.DisplayRole:
            print("DisplayRole")
            print(role)
            return False
        else:
            print("other")
            print(role)
            return False


    def flags(self, index):
        return (QtCore.Qt.ItemIsEnabled |
                      QtCore.Qt.ItemIsSelectable |
                      QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsDragEnabled |
                      QtCore.Qt.ItemIsDropEnabled)

    def insertRows(self, row, count, parent):
        print("insertRows")
        self.beginInsertRows(parent, row, (row + (count - 1)))
        #self._items.insert(row, object)
        self.endInsertRows()
        return True


    def supportedDropActions(self):
        print("supportedDrop")
        return (QtCore.Qt.MoveAction | QtCore.Qt.CopyAction)

    def supportedDragActions(self):
        print("supportedDraw")
        return (QtCore.Qt.MoveAction | QtCore.Qt.CopyAction)

    def mimeData(self, indexes):
        print("mimeData at (", indexes[0].row(), ",", indexes[0].column(), ")")
        self.old_index = indexes[0].row()

        old_stuff = pickle.dumps(self._items[indexes[0].row()])
        print =(type(old_stuff))
        mimeData = QtCore.QMimeData()
        mimeData.setText(old_stuff)

        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        print("dropMimeData")
        '''
        self.beginInsertRows(parentIndex, row, row)
    
        if action == QtCore.Qt.IgnoreAction: 
            return True 
    
        if data.hasText():
            print data
        return False
        '''

    def mimeTypes(self):
        print('mimeTypes')
        return list("text/plain")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = TodoModel()
        self.todoView.setModel(self.model)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()