import sys
import os
import sqlite3
import pandas as pd
import numpy as np
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlRelation, QSqlQuery, QSqlRelationalTableModel, QSqlTableModel, \
    QSqlRelationalDelegate, QSqlQueryModel
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout,QVBoxLayout, QPushButton, QWidget, QTableView,\
    QStackedLayout, QLineEdit)

db_filename = '../data/tagnotes.db'

schema_filename = './sql/schema.sql'

inserts_filename = './sql/inserts.sql'

#db_is_new = not os.path.exists(db_filename)

#conn = sqlite3.connect(db_filename)

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(db_filename)

db.open()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        self.model_rtag = QSqlRelationalTableModel(db=db)
        self.model_rnote = QSqlRelationalTableModel(db=db)

        self.model_tags = QSqlTableModel(db=db)
        self.model_notes = QSqlTableModel(db=db)

        button_create_db = QPushButton("Create Database")
        button_delete_db = QPushButton("Delete Database")
        button_query_db = QPushButton("Query Database")
        button_insert_tag_db = QPushButton("Insert Tag")
        button_close_app = QPushButton("Close App")

        self.insert_tag = QLineEdit()
        #self.insert_tag.textEdited.connect(self.update_tags)
        self.insert_tag.textChanged.connect(self.update_tags)

        self.table_rtag = QTableView()
        self.table_rnote = QTableView()

        # tags/notes
        self.model_tags_table = QTableView()
        self.model_notes_table = QTableView()

        self.model_tags.setTable("tags")
        self.model_notes.setTable("notes")

        #self.model = QSqlRelationalTableModel()
        #self.model = QSqlTableModel()
        #self.model = QSqlQueryModel()

        stackedLayout = QStackedLayout()

        layout_H_left_buttons = QHBoxLayout()
        layout_H_right_tables = QHBoxLayout()


        layout_V0 = QVBoxLayout()
        layout_V1 = QVBoxLayout()
        layout_V2 = QVBoxLayout()

        #layout_H_left_buttons.setContentsMargins(0, 0, 0, 0)
        #layout_H_left_buttons.setSpacing(20)

        layout_H_left_buttons.addLayout(layout_V0)
        layout_V0.addWidget(button_create_db)
        layout_V0.addWidget(button_delete_db)
        layout_V0.addWidget(button_query_db)
        layout_V0.addWidget(self.insert_tag)

        layout_H_left_buttons.addLayout(layout_H_right_tables)
        #layout_H_right_tables.addLayout(layout_V1)
        layout_H_right_tables.addWidget(self.model_tags_table)
        layout_H_right_tables.addWidget(self.table_rtag)

        #layout_V1.addWidget(self.table_rtag)
        #layout_V1.addLayout(layout_V2)
        layout_H_right_tables.addWidget(self.table_rnote)

        layout_H_right_tables.addWidget(self.model_notes_table)
        layout_V0.addWidget(button_close_app)

        #connect to a function
        button_create_db.clicked.connect(self.create_db_button)

        button_delete_db.clicked.connect(self.delete_db_button)

        button_query_db.clicked.connect(self.query_db_button)

        button_close_app.clicked.connect(self.close_app_button)

        self.setFixedSize(QSize(800, 600))

        widget = QWidget()
        widget.setLayout(layout_H_left_buttons)
        self.setCentralWidget(widget)
        # Set the central widget of the Window.
        #self.setCentralWidget(button_db)
        #self.setCentralWidget(button_query)

    def update_tags(self, s):

        schema_filename = 'schema.sql'

        inserts_filename = 'inserts.sql'

        db_is_new = not os.path.exists(db_filename)

        conn = sqlite3.connect(db_filename)

        with open(inserts_filename, 'rt') as f:
            inserts = f.read()

        tag = s
        conn.execute("insert into one_m_tags (tag) values (?)",tag)

        conn.close()

        self.model_tags.select()
        #self.model_tags_table.setModel(self.model_tags)

        #self.query = QSqlQuery(db=db)

        #query = QSqlQuery("SELECT one_m_notes.note, one_m_tags.tag from m_m_notes_tags left join one_m_notes on m_m_notes_tags.note_id = one_m_notes.note_id left join one_m_tags on m_m_notes_tags.tag_id = one_m_tags.tag_id where note LIKE '%s' OR tag LIKE '%s'",db=db)
        #filter_str = 'note LIKE "%{}%"'.format(s)
        #self.model_tags.query(self)
        #self.model.query(query)

        self.query_db_button()

    def delete_db_button(self):
        os.remove(db_filename)
        print("db deleted")

    def close_app_button(self):
        db.close()
        self.close()

    def create_db_button(self):
        # prep DB

        db_is_new = not os.path.exists(db_filename)

        conn = sqlite3.connect(db_filename)

        if db_is_new:
            print('Need to create schema')
        else:
            print('Database exists, assume schema does, too.')

        with sqlite3.connect(db_filename) as conn:
            if db_is_new:
                print
                'Creating schema'
                with open(schema_filename, 'rt') as f:
                    schema = f.read()
                conn.executescript(schema)

                print
                'Inserting initial data'

                with open(inserts_filename, 'rt') as f:
                    inserts = f.read()
                conn.executescript(inserts)

            else:
                print
                'Database exists, assume schema does, too.'

        conn.close()

    def query_db_button(self):

        #self.model = QSqlTableModel(db=db)

        self.model_tags_table.setModel(self.model_tags)
        self.model_notes_table.setModel(self.model_notes)

        self.model_tags_table.setSortingEnabled(1)# .setSort(0, Qt.DescendingOrder)
        self.model_notes_table.setSortingEnabled(1)#

        self.model_rtag.setTable("m_m_notes_tags")
        self.model_rnote.setTable("m_m_notes_tags")
        self.model_tags.setTable("one_m_tags")
        self.model_notes.setTable("one_m_notes")

        self.model_rtag.setRelation(0, QSqlRelation("one_m_notes", "note_id",
                                               "note"))

        self.model_rtag.setRelation(1, QSqlRelation("one_m_tags",
                                               "tag_id", "tag"))


        self.model_rnote.setRelation(0, QSqlRelation("one_m_notes", "note_id",
                                               "note"))

        self.model_rnote.setRelation(1, QSqlRelation("one_m_tags",
                                               "tag_id", "tag"))

        #columns_to_remove = ['tag']
        #for n in columns_to_remove:
            #idx = self.model.fieldIndex(n)
        self.model_rtag.removeColumns(0, 1)
        self.model_rnote.removeColumns(1, 1)

        delegate = QSqlRelationalDelegate(self.table_rtag.setModel(self.model_rtag))
        delegate1 = QSqlRelationalDelegate(self.table_rnote.setModel(self.model_rnote))

        self.table_rtag.setItemDelegate(delegate)
        self.table_rnote.setItemDelegate(delegate1)

        #columns_to_remove = ['tag']

        self.model_rtag.select()
        self.model_rnote.select()

        self.model_tags.select()
        self.model_notes.select()
        #query = QSqlQuery("SELECT one_m_notes.note, one_m_tags.tag from m_m_notes_tags left join one_m_notes on m_m_notes_tags.note_id = one_m_notes.note_id left join one_m_tags on m_m_notes_tags.tag_id = one_m_tags.tag_id",db=db)

        #self.model.setQuery(query)


#event loop
app = QApplication(sys.argv)

#window = QWidget()
window = MainWindow()
window.show()

app.exec_()

