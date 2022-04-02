import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView

db = QSqlDatabase("QSQLITE")
#db.setDatabaseName("Chinook_Sqlite.sqlite")
db.setDatabaseName("todo.db")
db.open()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()
        self.model = QSqlQueryModel()
        self.table.setModel(self.model)

        #query = QSqlQuery("SELECT Name, Composer FROM track ", db=db)
        query = QSqlQuery("SELECT * from m_m_notes_tags left join one_m_notes on m_m_notes_tags.note_id = one_m_notes.note_id left join one_m_tags on m_m_notes_tags.tag_id = one_m_tags.tag_id",db=db)

        self.model.setQuery(query)

        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(self.table)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()