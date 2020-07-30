from starlette.responses import PlainTextResponse

class Other:
    def fetch_all(self):
        """Fetch all items"""
        return PlainTextResponse("Pantam: Other -> fetch_all()")

    def fetch_single(self, uid):
        """Fetch single item"""
        return PlainTextResponse("Pantam: Other -> fetch_single()")

    def create(self, data):
        """Create an item"""
        return PlainTextResponse("Pantam: Other -> create()")

    def update(self, uid, data):
        """Update an item"""
        return PlainTextResponse("Pantam: Other -> update()")

    def delete(self, uid):
        """Delete single item"""
        return PlainTextResponse("Pantam: Other -> delete()")
