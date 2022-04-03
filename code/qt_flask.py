from flask import Flask
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from threading import Timer
import sys
# ^^ Start using all the regular flask logic ^^

flask_app = Flask(__name__) # Initiate flask app

@flask_app.route("/") #Define what happens on the home page
def hello(): #Function can really be named anything
    return "Hello World"# Define function for QtWebEngine

def ui(location): #Initiate PyQT5 app
    qt_app = QApplication(sys.argv)
    web = QWebEngineView()
    web.setWindowTitle("Window Name") #Rename to change your window name.
    # ^ This cannot change between pages
    web.resize(900, 800) # Set a size
    web.setZoomFactor(1.5) # Enlarge your content to fit screen
    web.load(QUrl(location)) #Load Home page at startup
    web.show() #Show the window
    sys.exit(qt_app.exec_())

if __name__ == "__main__":
    # start sub-thread to open the browser.
    Timer(1,lambda: ui("http://127.0.0.1:5000/")).start() #Show the home page on startup. Change the URL backend (http://127.0.0.1:5000/cool_backend, etc)
    flask_app.run(debug = False)  #Start flask engine, debug is False so that your users see ` Internal Server Error ` instead of the actual error.
