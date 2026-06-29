import sys
from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTabWidget,
)
from pages.ge_page import GEWindow
from pages.bestiary_page import BestiaryWindow
from pages.profile_page import ProfileWindow
from pages.wiki_page import WikiPortal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RS3-DataTool")
        self.resize(1250, 800)
        self.setMinimumSize(1050, 700)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setDrawBase(False)
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(False)

        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.tabBar().setDrawBase(False)
        self.tabs.tabBar().setContentsMargins(0, 0, 0, 0)

        self.ge_page = GEWindow()
        self.beast_page = BestiaryWindow()
        self.prof_page = ProfileWindow()
        self.wikiportal = WikiPortal()

        self.tabs.addTab(self.ge_page, "GE")
        self.tabs.addTab(self.beast_page, "Bestiary")
        self.tabs.addTab(self.prof_page, "Profile")
        self.tabs.addTab(self.wikiportal, "Wiki")

        self.tabs.currentChanged.connect(self.onTabChanged)

        self.setCentralWidget(self.tabs)

    def onTabChanged(self, index):
        curr_widget = self.tabs.widget(index)

        if curr_widget == self.wikiportal:
            self.wikiportal.refreshSavedPages()