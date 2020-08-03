# pylint: disable=unused-argument, pointless-string-statement

import sqlite3
from pantam import JSONResponse, PlainTextResponse

class Index:
    def __init__(self):
        database = sqlite3.connect("db")
        cursor = database.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cart
            (product text, cost integer)''')
        database.commit()


    """
    TRY THIS:
    curl --request POST 'http://localhost:5000/add-product-to-cart/' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'product=Ducati Panigale' \
    --data-urlencode 'cost=25000'
    """
    async def set_add_product_to_cart(self, request):
        """Add product to cart"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        data = await request.form()
        cursor.execute(
            "INSERT INTO cart VALUES (?,?)",
            (data["product"], data["cost"])
        )
        database.commit()
        return PlainTextResponse("Added Cart")


    """
    TRY THIS: curl --request GET 'http://localhost:5000/cart-contents/'
    """
    def get_cart_contents(self, request):
        """Get cart contents"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM cart")
        return JSONResponse(cursor.fetchall())


    """
    TRY THIS: curl --request GET 'http://localhost:5000/cart-total/'
    """
    def get_cart_total(self, request):
        """Get cart total value"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        cursor.execute("SELECT SUM(cost) FROM cart")
        return PlainTextResponse(str(cursor.fetchone()[0]))
