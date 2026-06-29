# Bestiary Page for RS3-DataTool

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (QLabel,
                               QWidget,
                               QVBoxLayout,
                               QLineEdit,
                               QPushButton,
                               QHBoxLayout,
                               QListWidget,
                               QGroupBox,
                               QPlainTextEdit)
from api.bestiary_api import BestiaryApi
from storage.favorites_store import FavoriteStore
from storage.page_store import WikiPageStore
from PySide6.QtGui import QDesktopServices
class BestiaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.BEApi = BestiaryApi()
        main_layout = QVBoxLayout(self)
        title = QLabel("RS3 Bestiary Monster Search:")
        self.monster_input = QLineEdit(placeholderText="Enter Beast")
        self.monster_input.setFixedHeight(34)
        self.monster_input.setMaximumWidth(600)
        self.favorites_store = FavoriteStore()
        self.page_store = WikiPageStore()
        self.current_page = None
        self.current_monster = None

        self.current_label = QLabel("Current Monster: None")
        self.status_label = QLabel("Status: Ready")
        self.status_label.setObjectName("StatusLabel")
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedSize(120, 34)
        self.fav_btn = QPushButton("Favorite")
        self.load_btn = QPushButton("Load Favorite")
        self.del_btn = QPushButton("Delete Favorite")
        self.load_btn.setFixedSize(180, 34)
        self.del_btn.setFixedSize(180, 34)
        self.fav_btn.setFixedSize(140, 34)

        self.favorite_item_list = QListWidget()
        self.favorite_item_list.setMinimumHeight(220)
        self.favorite_item_list.setFocusPolicy(Qt.NoFocus)
        self.resultLabel = QPlainTextEdit()
        self.resultLabel.setPlainText("Search for a Beast")
        self.resultLabel.setObjectName("ResultPanel")
        self.resultLabel.setReadOnly(True)
        self.resultLabel.setMinimumHeight(260)
        self.resultLabel.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.favorite_item_list.setMinimumHeight(220)

        self.open_wiki_btn = QPushButton("Open RS Wiki")
        self.save_wiki_btn = QPushButton("Save to WikiPortal")
        self.open_wiki_btn.setEnabled(False)
        self.save_wiki_btn.setEnabled(False)
        self.save_wiki_btn.setFixedSize(180, 34)
        self.open_wiki_btn.setFixedSize(180, 34)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.monster_input)
        search_layout.addWidget(self.search_btn)
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
        left_column.addWidget(title)
        left_column.addWidget(self.current_label)
        left_column.addWidget(self.status_label)
        left_column.addLayout(search_layout)
        left_column.addWidget(self.fav_btn)
        left_column.addStretch()

        right_column = QVBoxLayout()
        right_column.addWidget(self.resultLabel)

        top_layout.addLayout(left_column, 2)
        top_layout.addLayout(right_column, 4)

        favorites_box = QGroupBox("Favorite Beast(s)")
        box_layout = QVBoxLayout()
        box_layout.addWidget(self.favorite_item_list)
        box_layout.addLayout(favorite_layout)
        box_layout.addLayout(wiki_layout)
        favorites_box.setLayout(box_layout)



        main_layout.addLayout(top_layout)
        main_layout.addWidget(favorites_box)
        main_layout.addStretch()

        self.search_btn.clicked.connect(self.monsterSearch)
        self.monster_input.returnPressed.connect(self.monsterSearch)
        self.fav_btn.clicked.connect(self.favoriteCurrentItem)
        self.load_btn.clicked.connect(self.loadSelectFavoriteItem)
        self.del_btn.clicked.connect(self.deleteSelectFavoriteItem)
        self.favorite_item_list.itemDoubleClicked.connect(self.loadSelectFavoriteItem)
        self.open_wiki_btn.clicked.connect(self.openWikiPage)
        self.save_wiki_btn.clicked.connect(self.saveWikiPage)

        self.refreshFavoriteItems()

    def yesNo(self, value):
        return "Yes" if value else "No"
    
    def monsterSearch(self):
        monsterName = self.monster_input.text().strip().lower()
        if not monsterName:
            self.status_label.setText("Status: Enter Monster name.")
            self.clearCurrentMonsterState()
            self.monster_input.setFocus()


            return
        result = self.BEApi.searchMonster(monsterName)

        if not result['found']:
            self.status_label.setText(f"Status: {result['message']}")
            self.clearCurrentMonsterState()
            self.monster_input.clear()
            self.monster_input.setFocus()
            return
        
        monster = result['monster']
        memStatus = "Members" if monster['members'] else "Free-to-Play"
        candidate = result['candidate']
        self.current_monster = monster
        self.updateCurrentMonsterLabel()

        combat = monster['combat']
        slayer = monster['slayer']
        behavior = monster['behavior']
        locations = monster['locations']
        #Bestiary does not return a ID, therefore WikiPortal can clean it if called
        self.current_page = {
            "title": monster['name'],
            "url": self.buildWikiURL(monster['name']),
            "page_id": None
        }
        self.open_wiki_btn.setEnabled(True)
        self.save_wiki_btn.setEnabled(True)

        if locations:
            location_text = "\n".join(f"- {area}" for area in locations)
        else:
            location_text = "No Locations Found"

        self.resultLabel.setPlainText(
            f"{monster['name']}\n"
            f"ID: {monster['id']} | {memStatus}\n\n"
            f"Description\n"
            f"{monster['desc']}\n\n"

            f"Combat\n"
            f"Combat level: {combat['level']}\n"
            f"Hitpoints: {combat['hp']}\n"
            f"XP: {combat['xp']}\n"
            f"Weakness: {combat['weakness']}\n"
            f"Size: {combat['size']}\n\n"

            f"Levels\n"
            f"Attack: {combat['attack']}\n"
            f"Defence: {combat['defence']}\n"
            f"Magic: {combat['magic']}\n"
            f"Ranged: {combat['ranged']}\n\n"
            
            f"Slayer\n"
            f"Category: {slayer['category']}\n"
            f"Required Level: {slayer['level']}\n\n"
            
            f"Behavior\n"
            f"Poison: {self.yesNo(behavior['poisonous'])}\n"
            f"Aggressive: {self.yesNo(behavior['aggressive'])}\n"
            f"Attackable: {self.yesNo(behavior['attackable'])}\n\n"

            f"Locations\n"
            f"{location_text}\n\n"
        )
        self.monster_input.clear()
        self.monster_input.setFocus()
    
    def refreshFavoriteItems(self):
        self.favorite_item_list.clear()

        items = self.favorites_store.getMonsters()
        for item in items:
            self.favorite_item_list.addItem(item['name'])

    def favoriteCurrentItem(self):
        if not self.current_monster:
            self.status_label.setText("Status: Search a monster before favoriting.")
            return
        
        result = self.favorites_store.addMonster(
            self.current_monster['name'],
            self.current_monster.get('id')
        )

        self.status_label.setText(f"Status: {result['message']}")
        self.refreshFavoriteItems()

    def loadSelectFavoriteItem(self, item=None):
        selected_items = self.favorite_item_list.selectedItems()

        if not selected_items:
            self.status_label.setText("Status: Select a favorite monster first.")
            return
        
        item_name = selected_items[0].text()

        self.monster_input.setText(item_name)
        self.monsterSearch()

    def deleteSelectFavoriteItem(self):
        selected_items = self.favorite_item_list.selectedItems()

        if not selected_items:
            self.status_label.setText("Status: Select a favorite monster first.")
            return
        
        item_name = selected_items[0].text()
        if self.current_monster and self.current_monster['name'].casefold() == item_name.casefold():
            self.current_monster = None
            self.clearCurrentMonsterState()
        result = self.favorites_store.deleteMonster(item_name)

        self.status_label.setText(f"Status: {result['message']}")
        self.refreshFavoriteItems()

    def buildWikiURL(self, title):
        prepTitle = title.strip().replace(" ", "_")
        return f"https://runescape.wiki/w/{prepTitle}"
    
    def openWikiPage(self):
        if not self.current_page:
            self.status_label.setText("Status: Search a monster before opening the Wiki page.")
            return
        QDesktopServices.openUrl(QUrl(self.current_page['url']))

    def saveWikiPage(self):
        if not self.current_page:
            self.status_label.setText("Status: Search a monster before saving its Wiki page.")
            return
        
        result = self.page_store.addPage(
            self.current_page['title'],
            self.current_page['url'],
            self.current_page.get('page_id')
        )

        self.status_label.setText(f"Status: {result['message']}")

    def updateCurrentMonsterLabel(self):
        if not self.current_monster:
            self.current_label.setText("Current Monster: None")
            return
        
        self.current_label.setText(
            f"Current Monster: {self.current_monster['name']}"
        )
    
    def clearCurrentMonsterState(self):
        self.current_monster = None
        self.current_page = None

        self.open_wiki_btn.setEnabled(False)
        self.save_wiki_btn.setEnabled(False)

        self.updateCurrentMonsterLabel()    