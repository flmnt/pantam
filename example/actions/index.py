from starlette.responses import PlainTextResponse

class Index:
    def fetch_all(self):
        """Fetch all items"""
        return PlainTextResponse("Pantam: Index -> fetch_all()")

    def fetch_single(self, uid):
        """Fetch single item"""
        return PlainTextResponse("Pantam: Index -> fetch_single()")

    def create(self, data):
        """Create an item"""
        return PlainTextResponse("Pantam: Index -> create()")

    def update(self, uid, data):
        """Update an item"""
        return PlainTextResponse("Pantam: Index -> update()")

    def delete(self, uid):
        """Delete single item"""
        return PlainTextResponse("Pantam: Index -> delete()")