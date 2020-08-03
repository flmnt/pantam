# pylint: disable=unused-argument, pointless-string-statement

import sqlite3
from pantam import JSONResponse, PlainTextResponse

class Index:
    def __init__(self):
        database = sqlite3.connect("db")
        cursor = database.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users
            (uid text, first_name text, last_name text, email string)""")
        database.commit()


    """
    TRY THIS: curl --request GET 'http://localhost:5000'
    """
    def fetch_all(self, request):
        """Fetch all items"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM users")
        return JSONResponse(cursor.fetchall())


    """
    TRY THIS: curl --request GET 'http://localhost:5000/1'
    """
    def fetch_single(self, request):
        """Fetch single item"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        uid = request.path_params["id"]
        cursor.execute("SELECT * FROM users WHERE uid=?", (uid))
        return JSONResponse(cursor.fetchone())


    """
    TRY THIS:
    curl --request POST 'http://localhost:5000' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'first_name=Homer' \
    --data-urlencode 'last_name=Simpson' \
    --data-urlencode 'email=homer@donut.me'
    """
    async def create(self, request):
        """Create an item"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        data = await request.form()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO users VALUES (?,?,?,?)",
            (count + 1, data["first_name"], data["last_name"], data["email"])
        )
        database.commit()
        return PlainTextResponse("Created!")


    """
    TRY THIS:
    curl --request PATCH 'http://localhost:5000/1' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'last_name=Flanders'
    """
    async def update(self, request):
        """Update an item"""
        database = sqlite3.connect("db")
        database.row_factory = sqlite3.Row
        cursor = database.cursor()
        uid = request.path_params["id"]
        cursor.execute("SELECT * FROM users WHERE uid=?", (uid))
        user = cursor.fetchone()
        if user is not None:
            data = await request.form()
            cursor.execute(
                "UPDATE users set first_name = ?, last_name = ?, email = ? WHERE uid=?",
                (
                    data.get("first_name", user["first_name"]),
                    data.get("last_name", user["last_name"]),
                    data.get("email", user["email"]),
                    user["uid"]
                )
            )
            database.commit()
            return PlainTextResponse("Updated!")
        else:
            return PlainTextResponse("User Not Found", status_code=404)


    """
    TRY THIS: curl --request DELETE 'http://localhost:5000/1'
    """
    def delete(self, request):
        """Delete single item"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        uid = request.path_params["id"]
        cursor.execute("DELETE FROM users WHERE uid=?", (uid))
        database.commit()
        return PlainTextResponse("Deleted!")
