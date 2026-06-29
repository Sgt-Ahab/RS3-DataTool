import requests

class ProfileApi:
    HISCORES_URL = "https://secure.runescape.com/m=hiscore/index_lite.ws"
    SKILL_NAMES = [
        "overall",
        "attack",
        "defence",
        "strength",
        "constitution",
        "ranged",
        "prayer",
        "magic",
        "cooking",
        "woodcutting",
        "fletching",
        "fishing",
        "firemaking",
        "crafting",
        "smithing",
        "mining",
        "herblore",
        "agility",
        "thieving",
        "slayer",
        "farming",
        "runecrafting",
        "hunter",
        "construction",
        "summoning",
        "dungeoneering",
        "divination",
        "invention",
        "archaeology",
        "necromancy",
    ]
    def __init__(self):
        self.headers ={
            "User-Agent": (
                "RS3-DataTool v1.0 - "
                "your-email-here"
            )
        }   
    def searchPlayer(self, username):
        hiscoresData = self.getHiScores(username)

        if not hiscoresData["found"]:
             return hiscoresData
         
        return self.parseHiscores(username, hiscoresData["raw"])
    
    def getHiScores(self, username):
        params={
            "player": username,
        }
        response = requests.get(
            self.HISCORES_URL,
            params=params,
            headers=self.headers,
            timeout=10,
        )
        if response.status_code == 404:
            return{
               "found": False,
                "message": "Player not found or profile unavailable.",
            }
        response.raise_for_status()
        #print("HISCORES RAW:")
        #print(response.text)

        return{
            "found": True,
            "raw": response.text,
        }
    def parseHiscores(self, username, raw_text):
        lines = raw_text.strip().splitlines()
        skills = {}

        for index, skill_name in enumerate(self.SKILL_NAMES):
            if index >= len(lines):
                break
            
            parts = lines[index].split(",")
            # Skill rows go rank, level, xp
            if len(parts) < 3:
                continue
            rank = int(parts[0])
            level = int(parts[1])
            xp = int(parts[2])

            skills[skill_name] = {
                "rank": rank,
                "level": level,
                "xp": xp,
            }
        overall = skills.get("overall", {
            "rank": -1,
            "level": 0,
            "xp": 0,
        })

        return {
            "found": True,
            "player":{
                "username": username,
                "display_name": username,
                "overall_rank": overall["rank"],
                "total_level": overall["level"],
                "total_xp": overall["xp"],
            },
            "skills": skills,
        }