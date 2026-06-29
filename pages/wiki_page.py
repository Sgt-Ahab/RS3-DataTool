# Wiki Page for RS3-DataTool

from PySide6.QtWidgets import (QLabel,
                               QWidget,
                               QVBoxLayout,
                               QLineEdit,
                               QPushButton,
                               QHBoxLayout,
                               QListWidget,
                               QGroupBox,)
from api.wiki_api import WikiApi
from storage.page_store import WikiPageStore
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
class WikiPortal(QWidget):
    def __init__(self):
        super().__init__()
        self.current_wiki_url = None
        self.open_btn = QPushButton("Open Wiki")
        self.open_btn.setEnabled(False)
        self.open_btn.setFixedSize(140, 34)
        
        self.wiki_api = WikiApi()
        self.page_store = WikiPageStore()
        self.current_page = None

        title = QLabel("RS3 Wiki Portal")
        self.status_label = QLabel("Status: Ready")
        self.status_label.setObjectName("StatusLabel")
        self.current_label = QLabel("Current Wiki Page: None")
        main_layout = QVBoxLayout(self)

        self.wiki_input = QLineEdit(placeholderText="Enter Page Name to Search for")
        self.wiki_input.setFixedHeight(34)
        self.wiki_input.setMaximumWidth(600)
        self.search_btn = QPushButton("Search")
        self.suggest_btn = QPushButton("Use Suggested Page")
        self.save_btn = QPushButton("Save Wiki Page")
        self.load_btn = QPushButton("Load Saved Page")
        self.del_btn = QPushButton("Delete Saved Page")
        self.pages_list = QListWidget()
        self.pages_list.setMinimumHeight(220)
        self.pages_list.setFocusPolicy(Qt.NoFocus)
        self.suggest_btn.setEnabled(False)
        self.suggest_title = None
        self.load_btn.setFixedSize(180, 34)
        self.search_btn.setFixedSize(160, 34)
        self.del_btn.setFixedSize(180, 34)
        self.save_btn.setFixedSize(140, 34)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.wiki_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addStretch()

        self.result_label = QLabel("Search for a Wiki page.")
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_label.setMinimumHeight(110)
        self.pages_list.setMinimumHeight(240)
        self.result_label.setObjectName("ResultPanel")
        self.result_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        save_layout = QHBoxLayout()
        save_layout.addStretch()
        save_layout.addWidget(self.load_btn)
        save_layout.addWidget(self.del_btn)
        save_layout.addStretch()

        top_layout = QHBoxLayout()
        top_layout.setSpacing(18)

        utility_row = QHBoxLayout()
        utility_row.addStretch()
        utility_row.addWidget(self.open_btn)
        utility_row.addWidget(self.save_btn)
        utility_row.addStretch()

        left_column = QVBoxLayout()
        left_column.addWidget(title)
        left_column.addWidget(self.current_label)
        left_column.addWidget(self.status_label)
        left_column.addLayout(search_layout)
        left_column.addLayout(utility_row)
        left_column.addStretch()

        right_column = QVBoxLayout()
        right_column.addWidget(self.result_label)

        top_layout.addLayout(left_column, 2)
        top_layout.addLayout(right_column, 4)

        wiki_portal = QGroupBox("Saved Wiki Page(s)")
        wiki_layout = QVBoxLayout()
        wiki_layout.addWidget(self.pages_list)
        wiki_layout.addLayout(save_layout)
        wiki_portal.setLayout(wiki_layout)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(wiki_portal)
        main_layout.addStretch()
        
        self.search_btn.clicked.connect(self.pageSearch)
        self.wiki_input.returnPressed.connect(self.pageSearch)
        self.suggest_btn.clicked.connect(self.useSuggestion)
        self.open_btn.clicked.connect(self.openWikiPage)
        self.save_btn.clicked.connect(self.saveCurrentPage)
        self.pages_list.itemDoubleClicked.connect(self.openSelectSavePage)
        self.load_btn.clicked.connect(self.loadSelectPage)
        self.del_btn.clicked.connect(self.deleteSelectPage)

        self.refreshSavedPages()


    def pageSearch(self):
        search = self.wiki_input.text().strip()
        if not search:
            self.status_label.setText("Status: Enter a Page")
            self.wiki_input.setFocus()

            return
        result = self.wiki_api.searchPage(search)
        if not result['found']:
            self.status_label.setText(f"Status: {result['message']}")
            self.current_wiki_url = None
            self.current_page = None
            self.updateCurrentPageLabel()
            self.wiki_input.setFocus()
            self.wiki_input.clear()
            self.open_btn.setEnabled(False)
            if result.get('broad'):
                self.suggest_title = result['suggested_title']
                self.suggest_btn.setEnabled(True)
            else:
                self.suggest_title = None
                self.suggest_btn.setEnabled(False)

            return
        else:
            self.open_btn.setEnabled(True)
            self.current_wiki_url = result['url']
            self.current_page = {
                "title": result['title'],
                "url": result['url'],
                "page_id": result.get('page_id'),
            }
            self.updateCurrentPageLabel()
        self.suggest_btn.setEnabled(False)
        self.result_label.setText(
            f"Page Details\n\n"
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"ID: {result['page_id']}"
        )
        self.wiki_input.clear()
        self.wiki_input.setFocus()

    def openWikiPage(self):
        if not self.current_wiki_url:
            return
        
        QDesktopServices.openUrl(QUrl(self.current_wiki_url))            

    def useSuggestion(self):
        if not self.suggest_title:
            return
        
        self.wiki_input.setText(self.suggest_title)
        self.pageSearch()

    def refreshSavedPages(self):
        self.pages_list.clear()
        pages = self.page_store.getPages()
        for page in pages:
            self.pages_list.addItem(page['title'])

    def saveCurrentPage(self):
        if not self.current_page:
            self.status_label.setText("Status: Search a Wiki page before saving.")
            return
        result = self.page_store.addPage(
            self.current_page['title'],
            self.current_page['url'],
            self.current_page.get('page_id')
        )


        self.status_label.setText(f"Status: {result['message']}")
        self.refreshSavedPages()

    def loadSelectPage(self):
        selected = self.pages_list.selectedItems()

        if not selected:
            self.status_label.setText("Status: Select a saved Wiki page first.")
            return
        
        title = selected[0].text()
        page = self.page_store.getPageByTitle(title)

        if not page:
            self.status_label.setText("Status: Saved Wiki page could not be loaded.")
            return
        
        self.wiki_input.setText(page['title'])
        self.current_wiki_url = page['url']
        self.current_page = page
        self.updateCurrentPageLabel()
        self.result_label.setText(
            f"Loaded Wiki page:\n\n"
            f"Title: {page['title']}\n"
            f"URL: {page['url']}\n"
            f"ID: {self.current_page.get('page_id')}"
        )

        self.open_btn.setEnabled(True)

    def deleteSelectPage(self):
        selected = self.pages_list.selectedItems()

        if not selected:
            self.status_label.setText("Status: Select a saved Wiki page first.")
            return
        
        title = selected[0].text()
        if self.current_page and self.current_page['title'].casefold() == title.casefold():
            self.current_page = None
            self.updateCurrentPageLabel()

        result = self.page_store.deletePage(title)

        self.status_label.setText(f"Status: {result['message']}")
        self.refreshSavedPages()

    def openSelectSavePage(self, item):
        title = item.text()
        page = self.page_store.getPageByTitle(title)

        if not page:
            self.status_label.setText("Status: Saved Wiki page could not be loaded.")
            return
        
        self.wiki_input.setText(page['title'])
        self.current_wiki_url = page['url']
        self.current_page = page
        self.updateCurrentPageLabel()

        self.result_label.setText(
            f"Loaded Wiki page:\n\n"
            f"Title: {page['title']}\n"
            f"URL: {page['url']}\n"
            f"ID: {self.current_page.get('page_id')}"
        )
        self.open_btn.setEnabled(True)

        self.openWikiPage()
    
    def updateCurrentPageLabel(self):
        if not self.current_page:
            self.current_label.setText("Current Wiki Page: None")
            return
        
        self.current_label.setText(
            f"Current Wiki Page: {self.current_page['title']}"
        )    