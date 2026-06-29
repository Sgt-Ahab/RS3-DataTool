import requests

class WikiApi:
    WIKI_API_URL = "https://runescape.wiki/api.php"
    def __init__(self):
        self.headers={
            "User-Agent":(
                "RS3-DataTool v1.0 - "
                "your-email-here"
            ) 
        }

    def searchPage(self, searchTerm):
        params={
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": searchTerm,
            "srlimit": 10,
        }
        response = requests.get(
            self.WIKI_API_URL,
            params=params,
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        results = data["query"]["search"]

        bestResult = None
        bestScore = 0

        for result in results:
            score = self.scoreCandidate(searchTerm, result["title"])

            if score > bestScore:
                bestScore = score
                bestResult = result

        if bestResult is None or bestScore == 0:
            return{
                "found": False,
                "broad": False,
                "message": "No matching Wiki page found.",
            }
        if bestScore == 1:
            return{
                "found": False,
                "broad": True,
                "message": f"Search too broad for {searchTerm}, closest result: {bestResult["title"]}",
                "suggested_title": bestResult["title"],
            }

        return {
            "found": True,
            "broad": False,
            "title": bestResult["title"],
            "url": self.buildWikiUrl(bestResult["title"]),
            "page_id": bestResult['pageid'],
            "match_score": bestScore,
        }   
    
    def normName(self, name):
        if not isinstance(name, str):
            return ""
        return name.strip().casefold()
    
    def scoreCandidate(self, searchTerm, candidateTitle):
        search = self.normName(searchTerm)
        candidate = self.normName(candidateTitle)

        if not search or not candidate:
            return 0
        if candidate == search:
            return 3
        
        searchTokens = set(search.split())
        candidateTokens = set(candidate.split())

        if len(searchTokens) >= 2 and searchTokens.issubset(candidateTokens):
            return 2
        
        if search.split()[0] == candidate.split()[0]:
            return 1
        
        return 0
    
    def buildWikiUrl(self, title):
        safe_title = title.replace(" ", "_")
        return f"https://runescape.wiki/w/{safe_title}"
