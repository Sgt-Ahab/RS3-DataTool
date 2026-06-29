# GE Page for RS3-DataTool

from PySide6.QtWidgets import (QLabel,
                               QWidget,
                               QVBoxLayout,
                               QLineEdit,
                               QPushButton,
                               QHBoxLayout,
                               QListWidget,
                               QGroupBox)
from PySide6.QtGui import QPixmap, QDesktopServices
from api.ge_api import GEApi
from storage.favorites_store import FavoriteStore
from storage.page_store import WikiPageStore
from PySide6.QtCore import Qt, QUrl
import requests
class GEWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grand Exchange API Search")
        self.geAPI = GEApi()
        self.favorites_store = FavoriteStore()
        self.page_store = WikiPageStore()
        self.current_page = None
        self.current_item = None

        main_layout = QVBoxLayout(self)
        # Title Label
        self.label1 = QLabel("Grand Exchange Item Search:")
        self.label4 = QLabel("Current Item: None")
        # Result Label
        self.label2 = QLabel("Item Results")
        self.label2.setWordWrap(True)
        self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label2.setMinimumHeight(260)
        self.label2.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label2.setObjectName("ResultPanel")
        self.iconLabel = QLabel()
        self.iconLabel.setFixedSize(200,200)
        self.iconLabel.setScaledContents(True)
        self.status_label = QLabel("Status: Ready")
        self.status_label.setObjectName("StatusLabel")
        self.item_input = QLineEdit(placeholderText="Enter GE Item")
        self.item_input.setFixedHeight(34)
        self.item_input.setMaximumWidth(600)
        self.item_btn = QPushButton("Search")
        self.item_btn.setFixedSize(120, 34)
        self.fav_btn = QPushButton("Favorite")
        self.fav_btn.setFixedSize(100, 34)
        self.load_btn = QPushButton("Load Favorite")
        self.del_btn = QPushButton("Delete Favorite")
        self.load_btn.setFixedSize(180, 34)
        self.del_btn.setFixedSize(180, 34)
        self.favorite_item_list = QListWidget()
        self.favorite_item_list.setMinimumHeight(220)
        self.favorite_item_list.setFocusPolicy(Qt.NoFocus)

        self.open_wiki_btn = QPushButton("Open RS Wiki")
        self.save_wiki_btn = QPushButton("Save to WikiPortal")
        self.open_wiki_btn.setEnabled(False)
        self.save_wiki_btn.setEnabled(False)
        self.save_wiki_btn.setFixedSize(180, 34)
        self.open_wiki_btn.setFixedSize(180, 34)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.item_input)
        search_layout.addWidget(self.item_btn)
        search_layout.addStretch()

        favorite_layout = QHBoxLayout()
        favorite_layout.addStretch()
        favorite_layout.addWidget(self.load_btn)
        favorite_layout.addWidget(self.del_btn)
        favorite_layout.addStretch()

        wiki_layout = QHBoxLayout()
        wiki_layout.addStretch()
        wiki_layout.addWidget(self.open_wiki_btn)
        wiki_layout.addWidget(self.save_wiki_btn)
        wiki_layout.addStretch()

        top_layout = QHBoxLayout()
        top_layout.setSpacing(18)

        left_column = QVBoxLayout()
        left_column.addWidget(self.label1)
        left_column.addWidget(self.label4)
        left_column.addWidget(self.status_label)
        left_column.addLayout(search_layout)
        left_column.addStretch()
        left_column.addWidget(self.iconLabel, alignment=Qt.AlignCenter)
        left_column.addWidget(self.fav_btn, alignment=Qt.AlignCenter)
        left_column.addStretch()
        
        right_column = QVBoxLayout()
        right_column.addWidget(self.label2)

        top_layout.addLayout(left_column, 2)
        top_layout.addLayout(right_column, 4)
        

        favorites_box = QGroupBox("Favorite Item(s)")
        favorites_box_layout = QVBoxLayout()
        favorites_box_layout.addWidget(self.favorite_item_list)
        favorites_box_layout.addLayout(favorite_layout)
        favorites_box_layout.addLayout(wiki_layout)
        favorites_box.setLayout(favorites_box_layout)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(favorites_box)
        main_layout.addStretch()


        self.item_btn.clicked.connect(self.itemSearch)
        self.item_input.returnPressed.connect(self.itemSearch)
        self.fav_btn.clicked.connect(self.favoriteCurrentItem)
        self.load_btn.clicked.connect(self.loadSelectFavoriteItem)
        self.del_btn.clicked.connect(self.deleteSelectFavoriteItem)
        self.favorite_item_list.itemDoubleClicked.connect(self.loadSelectFavoriteItem)
        self.open_wiki_btn.clicked.connect(self.openWikiPage)
        self.save_wiki_btn.clicked.connect(self.saveWikiPage)        

        self.refreshFavoriteItems()


    def itemSearch(self):
        itemName = self.item_input.text().strip().lower()
        
        if not itemName:
            self.status_label.setText("Status: Enter Item Name.")
            self.item_input.setFocus()
            return
        itemData = self.geAPI.itemSearch(itemName)
        if not itemData['found']:
            self.status_label.setText(f"Status: {itemData['message']}")
            self.clearCurrentItemState()
            self.iconLabel.clear()
            self.item_input.clear()
            self.item_input.setFocus()
            return
        item = itemData['item']
        self.loadItemIcon(item['icons']['large'])
        wiki = itemData['wiki']
        gloop = itemData['gloop']
        self.current_item = item
        self.updateCurrentItemLabel()
        self.current_page = {
            "title": item['name'],
            "url": self.buildWikiURL(item['name']),
            "page_id": wiki['page_id'], 
        }
        self.open_wiki_btn.setEnabled(True)
        self.save_wiki_btn.setEnabled(True)

        memberStatus = "Members" if item['members'] else "Free-to-Play"

        self.label2.setText(
            f"{item['name']}\n"
            f"ID: {item['id']} | {memberStatus} | {item['type']}\n\n"
            
            f"Price\n"
            f"Current: {item['current']['price'] }\n"
            f"Exact: {gloop['price']:,} GP\n"
            f"Trade volume: {gloop['volume']:,}\n\n"
            
            f"Trends\n"
            f"Current: {item['current']['trend']}\n"
            f"Today: {item['today']['price']} ({item['today']['trend']})\n"
            f"30-days: {item['history']['day30']['change']} ({item['history']['day30']['trend']})\n"
            f"90-days: {item['history']['day90']['change']} ({item['history']['day90']['trend']})\n"
            f"180-days: {item['history']['day180']['change']} ({item['history']['day180']['trend']})\n\n"
        )
        self.item_input.clear()
        self.item_input.setFocus()

    def loadItemIcon(self, icon_url):
        response = requests.get(icon_url, timeout=10)
        response.raise_for_status()
        pixMap = QPixmap()
        pixMap.loadFromData(response.content)
        self.iconLabel.setPixmap(pixMap)
        

    def refreshFavoriteItems(self):
        self.favorite_item_list.clear()

        items = self.favorites_store.getItems()
        for item in items:
            self.favorite_item_list.addItem(item['name'])

    def favoriteCurrentItem(self):
        if not self.current_item:
            self.status_label.setText("Status: Search an item before favoriting.")
            return
        
        result = self.favorites_store.addItem(
            self.current_item['name'],
            self.current_item.get('id')
        )
        self.status_label.setText(f"Status: {result['message']}")
        self.refreshFavoriteItems()

    def loadSelectFavoriteItem(self, item=None):
        selected_items = self.favorite_item_list.selectedItems()

        if not selected_items:
            self.status_label.setText("Status: Select a favorite item first.")
            return
        
        item_name = selected_items[0].text()
        self.label4.setText(f"Loading Item: {item_name}")

        self.item_input.setText(item_name)
        self.itemSearch()

    def deleteSelectFavoriteItem(self):
        selected_items = self.favorite_item_list.selectedItems()

        if not selected_items:
            self.status_label.setText("Status: Select a favorite item first.")
            return
        
        item_name = selected_items[0].text()

        if self.current_item and self.current_item['name'].casefold() == item_name.casefold():
            self.clearCurrentItemState()

        result = self.favorites_store.deleteItems(item_name)

        self.status_label.setText(f"Status: {result['message']}")
        self.refreshFavoriteItems()
    
    def buildWikiURL(self, title):
        prepTitle = title.strip().replace(" ", "_")
        return f"https://runescape.wiki/w/{prepTitle}"
    
    def openWikiPage(self):
        if not self.current_page:
            self.status_label.setText("Status: Search an item before opening the Wiki page.")
            return
        
        QDesktopServices.openUrl(QUrl(self.current_page['url']))

    def saveWikiPage(self):
        if not self.current_page:
            self.status_label.setText("Status: Search an item before saving its Wiki page.")
            return
        
        result = self.page_store.addPage(
            self.current_page['title'],
            self.current_page['url'],
            self.current_page.get('page_id')
        )
        self.status_label.setText(f"Status: {result['message']}")

    def updateCurrentItemLabel(self):
        if not self.current_item:
            self.label4.setText("Current Item: None")
            return
        
        self.label4.setText(
            f"Current Item: {self.current_item['name']}"
        )

    def clearCurrentItemState(self):
        self.current_item = None
        self.current_page = None

        self.open_wiki_btn.setEnabled(False)
        self.save_wiki_btn.setEnabled(False)

        self.updateCurrentItemLabel()