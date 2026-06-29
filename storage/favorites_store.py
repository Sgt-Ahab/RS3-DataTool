import json
from pathlib import Path

class FavoriteStore:
    def __init__(self, file_path ="data/favorites.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.saveFavorites(
                {
                    "items": [],
                    "monsters": [],
                }
            )
    
    def loadFavorites(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
        
    def saveFavorites(self, favorites):
        favorites["items"] = sorted(
            favorites.get("items", []),
            key=lambda item: item["name"].casefold()
        )
        favorites["monsters"] = sorted(
            favorites.get("monsters", []),
            key=lambda item: item["name"].casefold()
        )
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(favorites, file, indent=4)

    def getItems(self):
        favorites = self.loadFavorites()
        return favorites.get("items", [])
    
    def getMonsters(self):
        favorites = self.loadFavorites()
        return favorites.get("monsters", [])
    
    def addItem(self, itemName, item_id=None):
        favorites = self.loadFavorites()
        cleanName = itemName.strip()

        if not cleanName:
            return{
                "success": False,
                "message": "Item name cannot be empty.",
            }
        for item in favorites.get("items", []):
            if item["name"].casefold() == cleanName.casefold():
                return {
                    "success": False,
                    "message": "Item already favorited.",
                }
            
        favorites.setdefault("items", []).append(
            {
                "name": cleanName,
                "id": item_id,
            }
        )
        self.saveFavorites(favorites)
        return {
            "success": True,
            "message": f"Favorited item: {cleanName}",
        }

    def deleteItems(self, itemName):
        favorites = self.loadFavorites()
        originalItems = favorites.get("items", [])
        updatedItems = [
            item for item in originalItems
            if item["name"].casefold() != itemName.casefold()
        ]

        if len(updatedItems) == len(originalItems):
            return {
                "success": False,
                "message": "Favorite item not found.",
            }
        favorites["items"] = updatedItems
        self.saveFavorites(favorites)

        return {
            "success": True,
            "message": f"Deleted favorite item: {itemName}",
        }
    
    def addMonster(self, monsterName, monster_id=None):
        favorites = self.loadFavorites()
        cleanName = monsterName.strip()

        if not cleanName:
            return {
                "success": False,
                "message": "Monster name cannot be empty.",
            }
        
        for monster in favorites.get("monsters", []):
            if monster["name"].casefold() == cleanName.casefold():
                return {
                    "success": False,
                    "message": "Monster already favorited.",
                }
        favorites.setdefault("monsters", []).append(
            {
                "name": cleanName,
                "id": monster_id,
            }
        )
        self.saveFavorites(favorites)

        return {
            "success": True,
            "message": f"Favorited monster: {cleanName}",
        }
    
    def deleteMonster(self, monsterName):
        favorites = self.loadFavorites()
        originalMonsters = favorites.get("monsters", [])

        updatedMonsters = [
            monster for monster in originalMonsters
            if monster["name"].casefold() != monsterName.casefold()
        ]

        if len(updatedMonsters) == len(originalMonsters):
            return {
                "success": False,
                "message": "Favorite monster not found.",
            }
        favorites["monsters"] = updatedMonsters
        self.saveFavorites(favorites)

        return {
            "success": True,
            "message": f"Deleted favorite monster: {monsterName}",
        }
    
