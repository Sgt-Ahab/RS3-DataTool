# This will be what calls to the beastiary API

import requests

class BestiaryApi:
    BESTIARY_SEARCH_URL = "https://secure.runescape.com/m=itemdb_rs/bestiary/beastSearch.json"
    BESTIARY_DATA_URL = "https://secure.runescape.com/m=itemdb_rs/bestiary/beastData.json"
    def __init__(self):
        self.headers ={
            "User-Agent":(
                "RS3-DataTool v1.0 - "
                "your-email-here"
            )
        }
    
    def searchMonster(self, monsterName):
        searchData = self.searchBestiary(monsterName)
        candidate = self.selectBestCandidate(monsterName, searchData)
        
        if not candidate["found"]:
            return candidate
        
        beastData = self.beastData(candidate["id"])
        
        return{
                "found": True,
                "candidate":{
                    "source_label": candidate["label"],
                    "match_score": candidate["match_score"],
                },
            "monster": beastData,
            }
    
    def searchBestiary(self, monsterName):
        params={
            "term": monsterName,
        }
        response = requests.get(
            self.BESTIARY_SEARCH_URL,
            params=params,
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        #print("BESTIARY SEARCH: ", data)
        return data
    
    def cleanMonsterLabel(self, label):
        """
        Converts:
        'Abyssal demon (98)' -> 'Abyssal demon'
        'Cow (2)' -> 'Cow'
        """    
        if not isinstance(label, str):
            return ""
        label = label.strip()
        if " (" in label:
            return label.rsplit(" (", 1)[0]
        return label
    
    def extractCombatLevel(self, label):
        """
        Converts:
        'Abyssal demon (98)' -> 98
        'Cow (2)' -> 2
        'Plague Cow' -> None
        """
        if " (" not in label or not label.endswith(")"):
            return None
        rawLevel = label.rsplit(" (", 1)[1].replace(")", "")
        if rawLevel.isdigit():
            return int(rawLevel)
        return None
    
    def normName(self, name):
        if not isinstance(name, str):
            return ""
        return name.strip().casefold()
    
    def scoreCandidate(self, searchTerm, candidateLabel):
        search = self.normName(searchTerm)

        candidateName = self.cleanMonsterLabel(candidateLabel)
        candidate = self.normName(candidateName)

        if not search or not candidate:
            return 0

        if candidate == search:
            return 3
        
        searchTokens = set(search.split())
        candidateTokens = set(candidate.split())

        if len(searchTokens) >= 2 and searchTokens.issubset(candidateTokens):
            return 2
        searchWords = search.split()
        candidateWords = candidate.split()

        if searchWords and candidateWords:
            if searchWords[0] == candidateWords[0]:
                return 1
            
        return 0
    
    def selectBestCandidate(self, monsterName, results):
        bestResult = None
        bestScore = 0
        
        for result in results:
            score = self.scoreCandidate(monsterName, result["label"])
            
            if score > bestScore:
                bestScore = score
                bestResult = result
        if bestResult is None or bestScore == 0:
            return {
                "found": False,
                "message": "No matching monster found",
            }
        
        cleanName = self.cleanMonsterLabel(bestResult["label"])
        combatLevel = self.extractCombatLevel(bestResult["label"])

        if bestScore == 1:
            return {
                "found": False,
                "message": f"Search too broad. Closest result: {cleanName}",
            }
        return{
            "found": True,
            "name": cleanName,
            "label": bestResult["label"],
            "id": bestResult["value"],
            "combat_level": combatLevel,
            "match_score": bestScore,
        }
    def beastData(self, beastId):
        params={
            "beastid": beastId,
        }
        response = requests.get(
            self.BESTIARY_DATA_URL,
            params=params,
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        animations = data.get("animations", {})
        #print("BEAST DATA: ", data)
        return {
            "id": data.get("id", beastId),
            "name": data.get("name", "Unknown"),
            "desc": data.get("description", "No description available"),
            "members": data.get("members", "Membership data unknown"),
            
            "combat":{
                "level": data.get("level", 0),
                "hp": data.get("lifepoints", 0),
                "xp": data.get("xp", "0"),
                "attack": data.get("attack", 0),
                "defence": data.get("defence", 0),
                "magic": data.get("magic", 0),
                "ranged": data.get("ranged", 0),
                "weakness": data.get("weakness", "Unknown"),
                "size": data.get("size", "Unknown"),
            },
            "slayer":{
                "category": data.get("slayercat", "N/A"),
                "level": data.get("slayerlevel", "N/A"),
            },
            "behavior":{
                "poisonous": data.get("poisonous", False),
                "aggressive": data.get("aggressive", False),
                "attackable": data.get("attackable", False),
            },
            "locations": data.get("areas", []),
            
            "animations": {
                "death": animations.get("death"),
                "attack": animations.get("attack"),
            },
        }