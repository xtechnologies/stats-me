import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from os import path



def get_resource_path(relative_path):
    """
    Get the absolute path to the resource based on whether the script is running as an executable or as a script.
    """
    if getattr(sys, 'frozen', False):
        # Running as an executable, use sys._MEIPASS to access bundled files
        base_path = sys._MEIPASS
    else:
        # Running as a script, use the script's directory
        base_path = path.dirname(path.abspath(__file__))
    
    resource_path = path.join(base_path, relative_path)
    return resource_path

pBui,_ = loadUiType(get_resource_path("ProgressUI.ui"))
counter = 0

class ProgressbarUI(QMainWindow, pBui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)        


        # ProgresBar timer 
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        
        self.timer.start(35)
        
    def progress(self):
        global counter
        
        self.progressBar.setValue(counter)
        
        if counter > 100:
            self.timer.stop()
            ...
            
            # self.mainapp = MainApp()
            # self.mainapp.show()
            
            self.close()
            
        counter += 1
        
        
app = QApplication([])
window = ProgressbarUI()
window.show()
app.exec_()
            
            
            