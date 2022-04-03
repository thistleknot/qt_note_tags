qt_note_tags
	qt_note_tags.py

gui application for tag based note system

setup
  QT
    linux
      yum install python3-qt5

    windows
      Install QT dev tools from QT

  tkinter
    yum install python3-tkinter

Direction

App idea
	pyqt5
	sqlite3
	
	migrate from pyqt5 to tkinter

Future Features

	I'm trying to figure out how best to show notes.

	Either a [section] type setup that mimics an ini file with the [section] being each note title.

	A QTextEdit

	or one of these widgets.

	I need a way to present a table where the contents are editable

	https://doc.qt.io/qt-5/sql-presenting.html

	Ability to type notes, title, choose tags from drop down, if not exists, then input new tags up to multiple tags.

	separate tag and note bridge items from the query function and make it part of a text changed from the filter

	So the order of operations is

	events based on actions
	delete button
	create button
	query button
		populate just tags and notes dimensions but not the bridge table
		populate filter
	select tag in filter QWidgetList
		generate bridge results with filter applied

synonyms
	tags
		eg.
			Causal
				Causation
				Causality
				
Browse current tags

Hiearchies
Sort alphabetically by Title
	
Notes_View
	Note Title (Title_Dim.Title_ID)
	Note Notes (Note_Dim.Note_ID FK)
	Note Tags (M_M_Note_Tag.Note_ID FK)
	
Title_Dim
	ID
	Title

Note_Dim
	ID
	Notes

Tag_Dim
	ID
	Tag
	
M_M_Note_Tag_ID
	Note_Dim.ID (FK)
	Tag_Dim.ID (FK)
	

