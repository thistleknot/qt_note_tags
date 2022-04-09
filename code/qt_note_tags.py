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
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QTableView,\
    QStackedLayout, QLineEdit, QLabel, QListWidget, QDataWidgetMapper, QComboBox, QFormLayout, QSpinBox)

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
        self.setWindowTitle("qt_note_tags")

        form = QFormLayout()

        self.note_input_id = QSpinBox()
        self.m_m_input_id = QSpinBox()
        self.tag_input_id = QSpinBox()

        form.addRow(QLabel("Note ID"), self.note_input_id)
        form.addRow(QLabel("m to m ID"), self.m_m_input_id)
        form.addRow(QLabel("Tag ID"), self.tag_input_id)

        #used for inputting new note
        self.model_note_input = QSqlTableModel(db=db)
        self.model_m_m_input = QSqlTableModel(db=db)
        self.model_tag_input = QSqlTableModel(db=db)

        self.mapper_note_input = QDataWidgetMapper()
        self.mapper_m_m_input = QDataWidgetMapper()
        self.mapper_tag_input = QDataWidgetMapper()

        self.mapper_note_input.setModel(self.model_note_input)
        self.mapper_m_m_input.setModel(self.model_m_m_input)
        self.mapper_tag_input.setModel(self.model_tag_input)

        self.mapper_note_input.addMapping(self.note_input_id, 0)
        self.mapper_m_m_input.addMapping(self.m_m_input_id, 0)
        self.mapper_tag_input.addMapping(self.tag_input_id, 0)

        self.model_note_input.setTable("one_m_notes")
        self.model_m_m_input.setTable("m_m_notes_tags")
        self.model_tag_input.setTable("one_m_tags")

        #this needs to have tags mapped to a delegate?
        #how to get a table to work with a QSqlRelationalTableModel which doesn't allow for editing.
        #need to show bridge table that can be edited.
        #so option to input new notes
        #option to input new tags
        #option to input new m_m between both (likely without lookups)


        self.title_input = QLineEdit()
        self.note_input = QLineEdit()
        self.tag_input = QComboBox()

        self.model_rtag = QSqlRelationalTableModel(db=db)
        self.model_rnote = QSqlRelationalTableModel(db=db)
        self.model_rtitle = QSqlRelationalTableModel(db=db)

        self.model_tags = QSqlTableModel(db=db)
        self.model_notes = QSqlTableModel(db=db)


        self.button_create_db = QPushButton("Create Database")
        self.button_delete_db = QPushButton("Delete Database")
        self.button_query_db = QPushButton("Query Database")
        self.button_insert_tag_db = QPushButton("Insert Tag")

        self.button_close_app = QPushButton("Close App")

        self.insert_label = QLabel("Insert Tag")

        self.insert_tag = QLineEdit()

        self.insert_tag.returnPressed.connect(self.add_tag)

        self.filter_list_tags = QListWidget()
        self.filter_list_note_title = QListWidget()

        self.filter_list_tags.itemSelectionChanged.connect(self.filter_by_tag)
        self.filter_list_note_title.itemSelectionChanged.connect(self.filter_by_note_title)

        self.model_tags_table = QTableView()

        self.table_note_edit = QTableView()
        self.model_note_edit = QSqlTableModel(db=db)

        self.table_rtag = QTableView()
        self.table_rnote = QTableView()
        self.table_rtitle = QTableView()

        self.model_notes_table = QTableView()

        self.model_tags.setTable("tags")
        self.model_notes.setTable("notes")

        layout_V_top_not_notes = QVBoxLayout()

        layout_H_left_buttons = QHBoxLayout()

        layout_V_bottom_notes = QVBoxLayout()
        layout_H_bottom_notes = QHBoxLayout()
        layout_V_bottom_note = QVBoxLayout()

        layout_V_top_not_notes.addLayout(layout_H_left_buttons)
        layout_V_top_not_notes.addLayout(layout_H_bottom_notes)
        layout_H_bottom_notes.addLayout(layout_V_bottom_notes)
        layout_V_top_not_notes.addLayout(layout_V_bottom_note)
        layout_V_bottom_note.addWidget(self.table_note_edit)

        layout_H_right_tables = QHBoxLayout()

        layout_V0 = QVBoxLayout()
        layout_V0.addWidget(self.button_create_db)
        layout_V0.addWidget(self.button_delete_db)
        layout_V0.addWidget(self.button_query_db)
        layout_V0.addWidget(self.insert_label)
        self.insert_label.setAlignment(Qt.AlignBottom)

        layout_V0.addWidget(self.insert_tag)
        self.insert_tag.setAlignment(Qt.AlignTop)
        layout_V0.addWidget(self.button_close_app)

        layout_H_left_buttons.addLayout(layout_V0)

        layout_H_left_buttons.addLayout(layout_H_right_tables)

        layout_H_right_tables.addWidget(self.filter_list_tags)
        layout_H_right_tables.addWidget(self.model_tags_table)
        #layout_H_right_tables.addWidget(self.table_rtag)

        layout_H_bottom_notes.addWidget(self.table_rtitle)

        layout_H_bottom_notes.addWidget(self.table_rnote)
        layout_H_bottom_notes.addWidget(self.filter_list_note_title)
        #layout_H_right_tables.addWidget(self.table_rnote)
        #layout_H_right_tables.addWidget(self.table_rtitle)

        layout_H_right_tables.addWidget(self.model_notes_table)

        #connect to a function
        self.button_create_db.clicked.connect(self.create_db_button)

        self.button_delete_db.clicked.connect(self.delete_db_button)

        self.button_query_db.clicked.connect(self.query_db_button)

        self.button_close_app.clicked.connect(self.close_app_button)

        self.setFixedSize(QSize(800, 600))

        widget = QWidget()
        widget.setLayout(layout_V_top_not_notes)
        self.setCentralWidget(widget)
        # Set the central widget of the Window.
        #self.setCentralWidget(button_db)
        #self.setCentralWidget(button_query)

    def add_tag(self):

        if db.isOpen():
            db.close()

        conn = sqlite3.connect(db_filename)

        tag = self.insert_tag.text()

        #I can't get PyQT5 query to work

        q_string = "insert into one_m_tags (tag) values ('" + tag + "');"
        with sqlite3.connect(db_filename) as conn:
            conn.executescript(q_string)

        conn.close()

        db.open()

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

        self.model_tags.setTable("one_m_tags")
        self.model_notes.setTable("one_m_notes")

        self.model_tags.select()
        self.model_notes.select()

        self.filter_list_tags.clear()
        #populate tag filter list
        for row in range(self.model_tags.rowCount()):
            #for column in range(self.model_tags.columnCount()):
            #skip column 0 which is id
            index = self.model_tags.index(row, 1)
            #print(self.model_rtag.index(row, column).data())
            text = self.model_tags.data(index)
            self.filter_list_tags.addItem(text)

        #query = QSqlQuery("SELECT one_m_notes.note, one_m_tags.tag from m_m_notes_tags left join one_m_notes on m_m_notes_tags.note_id = one_m_notes.note_id left join one_m_tags on m_m_notes_tags.tag_id = one_m_tags.tag_id",db=db)

        #self.model.setQuery(query)

    def filter_by_tag(self):

        #if count(self.filter_list_tags.selectedItems)>0:

        self.model_rtag.setTable("m_m_notes_tags")
        self.model_rnote.setTable("m_m_notes_tags")
        self.model_rtitle.setTable("m_m_notes_tags")

        self.model_rtag.setRelation(0, QSqlRelation("one_m_notes", "note_id",
                                               "note"))

        self.model_rtag.setRelation(1, QSqlRelation("one_m_tags",
                                               "tag_id", "tag"))


        self.model_rtitle.setRelation(0, QSqlRelation("one_m_notes", "note_id",
                                               "title"))

        self.model_rtitle.setRelation(1, QSqlRelation("one_m_tags",
                                   "tag_id", "tag"))

        self.model_rnote.setRelation(0, QSqlRelation("one_m_notes", "note_id",
                                                     "note"))

        self.model_rnote.setRelation(1, QSqlRelation("one_m_tags",
                                               "tag_id", "tag"))


        selected_tag_filter = self.filter_list_tags.currentItem().text()
        print(selected_tag_filter)

        filter_str = 'tag = "{}"'.format(selected_tag_filter)
        print(filter_str)
        #for row in range(len(self.filter_list_tags.selectedItems())):
            #filter_str = self.filter_list_tags.selectedItems().index(row)

            #filter rnote by tag
        self.model_rtag.setFilter(filter_str)
        self.model_rtitle.setFilter(filter_str)
        self.model_rnote.setFilter(filter_str)

        delegate0 = QSqlRelationalDelegate(self.table_rtag.setModel(self.model_rtag))
        delegate1 = QSqlRelationalDelegate(self.table_rtitle.setModel(self.model_rtitle))
        delegate2 = QSqlRelationalDelegate(self.table_rnote.setModel(self.model_rnote))

        self.table_rtag.setItemDelegate(delegate0)
        self.table_rtitle.setItemDelegate(delegate1)
        self.table_rnote.setItemDelegate(delegate2)

        #columns_to_remove = ['tag']

        self.model_rtag.select()
        self.model_rtitle.select()
        self.model_rnote.select()

        #remove after filter, after select
        self.model_rtag.removeColumn(0)
        #self.model_rtitle.removeColumn(1)
        #self.model_rnote.removeColumn(1)

        #populate notes filter

        self.filter_list_note_title.clear()
        #populate tag filter list
        #temp_model = self.table_rnote.model()
        for row in range(self.model_rtitle.rowCount()):
            #for column in range(self.model_tags.columnCount()):
            #skip column 0 which is id
            index = self.model_rtitle.index(row, 0)
            #print(self.model_rtag.index(row, column).data())
            text = self.model_rtitle.data(index)
            self.filter_list_note_title.addItem(text)

    def filter_by_note_title(self):

        self.table_note_edit.setModel(self.model_note_edit)
        self.model_note_edit.setTable("one_m_notes")
        #self.model_note_edit.select()

        selected_note_title_filter = self.filter_list_note_title.currentItem().text()
        filter_str = 'title = "{}"'.format(selected_note_title_filter)

        self.model_note_edit.setFilter(filter_str)
        #self.model_note_edit.removeColumn(1)
        #self.model_note_edit.removeColumn(0)
        self.model_note_edit.select()

        #print("hi")

#event loop
app = QApplication(sys.argv)

#window = QWidget()
window = MainWindow()
window.show()

app.exec_()

