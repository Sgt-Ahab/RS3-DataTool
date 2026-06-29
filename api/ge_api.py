# This is the process for the GE API via Jagex Endpoint

# https://secure.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item=X 
# where X is the ItemID
# graph is https://secure.runescape.com/m=itemdb_rs/api/graph/X.json 
# where X is the ItemID, returns 180 days, with ms since 1-1-70;
import requests, math

class GEApi:
    WIKI_API_URL = "https://runescape.wiki/api.php"

    def __init__(self):
        # Proper User Agent for web-etiquette, use a personal/accessible email in the headers
        self.headers ={
            "User-Agent": (
                "RS3-DataTool v1.0 - "
                "your-email-here"
            )
        }
    
    def searchWiki(self, itemName):
        params = {
            "action": "query",
            "list": "search",
            "srsearch": itemName,
            "srnamespace": 112,
            "srlimit": 10,
            "format": "json",
        }
        response = requests.get(
            self.WIKI_API_URL,
            params=params,
            timeout=10,
            headers=self.headers,
        )
        response.raise_for_status()

        data = response.json()
        results = data["query"]["search"]
        bestResult = None
        bestScore = 0

        for result in results:
            score = self.scoreCandidate(itemName, result["title"])
            if score > bestScore:
                bestScore = score
                bestResult = result

        if bestResult is None or bestScore == 0:
            return {
                "found": False,
                "message": "No matching Wiki item found.",
            }
        cleanName = self.cleanWikiTitle(bestResult["title"])
        if bestScore == 1:
            return {
                "found": False,
                "message": f"Search too broad. Closest result: {cleanName}",
            }
            

        return {
            "found": True,
            "name": cleanName,
            "wiki_title": bestResult["title"],
            "wiki_page_id": bestResult["pageid"],
            "match_score": bestScore,
        }
    
    
    def normName(self, name):
        return name.strip().casefold()

    def cleanWikiTitle(self, title):
        """
        Sanitizes 'Exchange: itemName' into 'itemName'
        """
        if title.startswith("Exchange:"):
            return title.replace("Exchange:", "", 1)
        return title
    
    def scoreCandidate(self, searchTerm, candidateTitle):
        search = self.normName(searchTerm)
        candidate = self.cleanWikiTitle(candidateTitle)
        candidate = self.normName(candidate)

        if candidate == search:
            return 3
        
        searchTokens = set(search.split())
        candidateTokens = set(candidate.split())

        if len(searchTokens) >= 2 and searchTokens.issubset(candidateTokens):
            return 2
        
        if search.split() and candidate.split():
            if search.split()[0] == candidate.split()[0]:
                return 1
            
        return 0

    def itemSearch(self, itemName):
        wikiData = self.searchWiki(itemName)
        if not wikiData["found"]:
            return wikiData
        
        gloopData = self.gloopItem(wikiData["name"])
        itemData = self.jagexItem(gloopData["item_id"])
        return{
            "found": True,
            "wiki":{
                "title": wikiData["wiki_title"],
                "page_id": wikiData["wiki_page_id"],
                "match_score": wikiData["match_score"],
            },
            "gloop": gloopData,
            "item": itemData,
        }
    def gloopItem(self, cleanName):
        url = "https://api.weirdgloop.org/exchange/history/rs/latest"
        params = {
            "name": cleanName,
        }
        response = requests.get(
            url,
            params=params,
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        itemID = data[cleanName]["id"]
        price = data[cleanName]['price']
        return {
            "name": cleanName,
            "item_id": itemID,
            "price": price,
            "volume": data[cleanName]['volume'],
            "raw": data,
        }
    
    def jagexItem(self, itemID):
        # Return Jagex item
        url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/detail.json"

        params = {
            "item": itemID,
        }
        response = requests.get(
            url,
            params=params,
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        item = data["item"]
        return{
            "id": item["id"],
            "name": item["name"],
            "description": item["description"],
            "type": item["type"],
            "members": item["members"] == "true",
            
            "icons":{
                "small":item["icon"],
                "large":item["icon_large"],
            },

            "current":{
                "price": item["current"]["price"],
                "trend": item["current"]["trend"],
            },
            "today":{
                "price": item["today"]["price"],
                "trend": item["today"]["trend"],
            },
            "history":{
                "day30":{
                    "trend": item["day30"]["trend"],
                    "change": item["day30"]["change"],
                },
                "day90":{
                    "trend": item["day90"]["trend"],
                    "change": item["day90"]["change"],
                },
                "day180":{
                    "trend": item["day180"]["trend"],
                    "change": item["day180"]["change"],
                },
            },
        }        