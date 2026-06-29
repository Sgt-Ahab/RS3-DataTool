import json
from pathlib import Path

class WikiPageStore:
    def __init__(self, file_path="data/wiki_pages.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.savePages([])

    def loadPages(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def savePages(self, pages):
        pages = sorted(
            pages,
            key=lambda page: page["title"].casefold()
        )
        
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(pages, file, indent=4)

    def getPages(self):
        return self.loadPages()
    
    def addPage(self, title, url, page_id=None):
        pages = self.loadPages()
        cleanName = title.strip()
        cleanURL = url.strip()

        if not cleanName:
            return{
                "success": False,
                "message": "Wiki page title cannot be empty.",
            }
        if not cleanURL:
            return{
                "success": False,
                "message": "Wiki page URL cannot be empty.",                
            }
        for page in pages:
            if page["title"].casefold() == cleanName.casefold():
             return{
                "success": False,
                "message": "Wiki page already saved.",                
            }   

        pages.append(
            {
                "title": cleanName,
                "url": cleanURL,
                "page_id": page_id,
            }
        )
        self.savePages(pages)
        
        return {
            "success": True,
            "message": f"Saved Wiki page: {cleanName}",
        }

    def deletePage(self, title):
        pages = self.loadPages()

        updatedPages = [
            page for page in pages
            if page["title"].casefold() != title.casefold()
        ]
        if len(updatedPages) == len(pages):
            return {
                "success": False,
                "message": "Wiki page not found.",
            }
        self.savePages(updatedPages)
        return {
            "success": True,
            "message": f"Deleted Wiki page: {title}",
        }

    def getPageByTitle(self, title):
        pages = self.loadPages()
        
        for page in pages:
            if page["title"].casefold() == title.casefold():
                return page
            
        return None
