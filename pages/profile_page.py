# Profile Page for RS3 API

from PySide6.QtWidgets import (QLabel,
                               QWidget,
                               QVBoxLayout,
                               QLineEdit,
                               QPushButton,
                               QHBoxLayout,
                               QListWidget,
                               QGroupBox,
                               QPlainTextEdit)
from api.profile_api import ProfileApi
from storage.profile_store import ProfileStore
from PySide6.QtCore import Qt
class ProfileWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.profile_api = ProfileApi()
        title = QLabel("RS3 PROFILE SEARCH (MUST BE PUBLIC TO SEARCH)")
        main_layout = QVBoxLayout(self)
        self.status_label = QLabel("Status: Ready")
        self.status_label.setObjectName("StatusLabel")

        self.profile_store = ProfileStore()
        self.current_username = None
        self.current_label = QLabel("Current Profile: None")
        self.username_input = QLineEdit(placeholderText="Enter Username")
        self.username_input.setFixedHeight(34)
        self.username_input.setMaximumWidth(600)

        self.saved_profile_list = QListWidget()
        self.saved_profile_list.setMinimumHeight(220)
        self.saved_profile_list.setFocusPolicy(Qt.NoFocus)

        self.search_btn = QPushButton("Search")
        self.save_btn = QPushButton("Save Profile")
        self.load_btn = QPushButton("Load Profile")
        self.del_btn = QPushButton("Delete Profile")
        self.search_btn.setFixedSize(120, 34)
        self.load_btn.setFixedSize(180, 34)
        self.del_btn.setFixedSize(180, 34)
        self.save_btn.setFixedSize(180, 34)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.username_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addStretch()

        self.result_label = QPlainTextEdit()
        self.result_label.setPlainText("Search for a player profile.")
        self.result_label.setReadOnly(True)
        self.result_label.setMinimumHeight(260)
        self.result_label.setObjectName("ResultPanel")
        self.result_label.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.saved_profile_list.setMinimumHeight(220)
  
        saveProfileLayout = QHBoxLayout()
        saveProfileLayout.addStretch()
        saveProfileLayout.addWidget(self.load_btn)
        saveProfileLayout.addWidget(self.del_btn)
        saveProfileLayout.addStretch()        

        top_layout = QHBoxLayout()
        top_layout.setSpacing(18)

        left_column = QVBoxLayout()
        left_column.addWidget(title)
        left_column.addWidget(self.current_label)
        left_column.addWidget(self.status_label)
        left_column.addLayout(search_layout)
        left_column.addWidget(self.save_btn)
        left_column.addStretch()

        right_column = QVBoxLayout()
        right_column.addWidget(self.result_label)

        top_layout.addLayout(left_column, 2)
        top_layout.addLayout(right_column, 4)

        favorites_box = QGroupBox("Saved Profile(s)")
        box_layout = QVBoxLayout()
        box_layout.addWidget(self.saved_profile_list)
        box_layout.addLayout(saveProfileLayout)
        favorites_box.setLayout(box_layout)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(favorites_box)
        main_layout.addStretch()

        self.search_btn.clicked.connect(self.profileSearch)
        self.username_input.returnPressed.connect(self.profileSearch)
        self.save_btn.clicked.connect(self.saveCurrentProfile)
        self.saved_profile_list.itemDoubleClicked.connect(self.loadSelectProfile)
        self.load_btn.clicked.connect(self.loadSelectProfile)
        self.del_btn.clicked.connect(self.deleteSelectProfile)
        
        self.refreshSavedProfiles()

    def profileSearch(self):
        username = self.username_input.text().strip()

        if not username:
            self.status_label.setText("Status: Enter a Username")
            self.username_input.setFocus()
            return
        
        result = self.profile_api.searchPlayer(username)

        if not result['found']:
            self.status_label.setText(f"Status: {result['message']}")
            self.current_username = None
            self.updateCurrentProfileLabel()
            self.username_input.clear()
            self.username_input.setFocus()
            return

        player = result['player']
        skills = result['skills']
        self.current_username = player['display_name']
        self.updateCurrentProfileLabel()
        skill_lines = []
        skill_lines.append(f"{'Skill':<16}{'Level':>7}{'XP':>16}{'Rank':>16}")
        skill_lines.append('-' * 55)
        for skill_name, skill_data in skills.items():
            if skill_name == 'overall':
                continue
            skill_lines.append(
                f"{skill_name.title():<16}"
                f"{skill_data['level']:>7}"
                f"{skill_data['xp']:>16,}"
                f"{skill_data['rank']:>16,}"
            )
        skills_text = "\n".join(skill_lines)

        self.result_label.setPlainText(
            f"{player['display_name']}\n"
            f"Overall rank: {player['overall_rank']:,}\n"
            f"Total level: {player['total_level']:,}\n"
            f"Total XP: {player['total_xp']:,}\n\n"

            f"Skills\n"
            f"{skills_text}"
        )
        self.username_input.clear()
        self.username_input.setFocus()

    def saveCurrentProfile(self):
        if not self.current_username:
            self.status_label.setText("Status: Search a profile before saving.")
            return

        result = self.profile_store.addProfile(self.current_username)
        self.status_label.setText(f"Status: {result['message']}")
        self.refreshSavedProfiles()
    
    def refreshSavedProfiles(self):
        self.saved_profile_list.clear()
        profiles = self.profile_store.getProfile()

        for profile in profiles:
            self.saved_profile_list.addItem(profile['username'])
        
        self.updateCurrentProfileLabel()

    def loadSelectProfile(self, item=None):
        selected = self.saved_profile_list.selectedItems()

        if not selected:
            self.status_label.setText("Status: Select a saved profile first.")
            return
        
        username = selected[0].text()

        self.username_input.setText(username)
        self.profileSearch()

    def deleteSelectProfile(self):
        selected = self.saved_profile_list.selectedItems()

        if not selected:
            self.status_label.setText("Status: Select a saved profile first.")
            return
        
        username = selected[0].text()
        if self.current_username and self.current_username.casefold() == username.casefold():
            self.current_username = None

        result = self.profile_store.deleteProfile(username)

        self.status_label.setText(f"Status: {result['message']}")
        self.refreshSavedProfiles()

    def updateCurrentProfileLabel(self):
        if not self.current_username:
            self.current_label.setText("Current Profile: None")
            return
        
        self.current_label.setText(
            f"Current Profile: {self.current_username}"
        )