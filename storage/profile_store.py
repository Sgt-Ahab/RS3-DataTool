import json
from pathlib import Path

class ProfileStore:
    def __init__(self, file_path="data/profiles.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.saveProfiles([])

    def loadProfiles(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    
    def saveProfiles(self, profiles):
        profiles = sorted(
            profiles,
            key=lambda profile: profile["username"].casefold()
        )
        with self.file_path.open("w", encoding="utf-8")as file:
            json.dump(profiles, file, indent=4)

    def addProfile(self, username, group="Unsorted"):
        profiles = self.loadProfiles()
        cleanName = username.strip()

        if not cleanName:
            return{
                "success": False,
                "message": "Username cannot be empty.",
            }
        for profile in profiles:
            if profile["username"].casefold() == cleanName.casefold():
                return{
                    "success": False,
                    "message": "Profile already saved."
                }
        profiles.append(
            {
                "username": cleanName,
                "group": group,
            }
        )
        self.saveProfiles(profiles)
        return {
            "success": True,
            "message": f"Saved profile: {cleanName}",
        }
    
    def deleteProfile(self, username):
        profiles = self.loadProfiles()

        updated = [
            profile for profile in profiles
            if profile["username"].casefold() != username.casefold()
        ]

        if len(updated) == len(profiles):
            return {
                "success": False,
                "message": "Profile not found.",
            }
        self.saveProfiles(updated)
        return{
            "success": True,
             "message": f"Deleted profile: {username}",
        }
    
    def getProfile(self):
        return self.loadProfiles()