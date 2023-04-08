#!/usr/bin/python3
import os
import pathlib
import sys
import pygubu
from classes.definitions import test

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


PROJECT_PATH = resource_path(pathlib.Path(__file__).parent)
PROJECT_UI= os.path.join(PROJECT_PATH, "assets\\test.ui")


class NewprojectApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        self.entry_user_entry = builder.get_object("entryTest")
    def run(self):
        self.mainwindow.mainloop()

    def buttonTestPress(self, event=None):
        message = test()
        self.entry_user_entry.insert(0, message)




if __name__ == "__main__":
    app = NewprojectApp()
    app.run()
