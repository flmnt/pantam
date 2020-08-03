# Event based microservice example

The following example microservice has been created using [Pantam](https://github.com/flmnt/pantam).

Follow the quickstart steps below to checkout this repo and explore this exact example or skip this step and creating this example yourself from scratch.

## Quickstart

Open a terminal and run the following: (you will need [Pyenv](https://github.com/pyenv/pyenv) and [Poetry](https://python-poetry.org/) installed)

```
% git clone git@github.com:flmnt/pantam.git
% cd pantam/example/event
% pyenv install 3.8.2
% pyenv local 3.8.2
% poetry install
% poetry shell
% pantam serve --dev
```

To test the example app out, in a new terminal, run:

```
curl --request POST 'http://localhost:5000/add-product-to-cart/' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'product=Ducati Panigale' \
  --data-urlencode 'cost=25000'
```

## Tutorial

Let's build the example in this folder from scratch together.

We're going to build an [event based microservice](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/integration-event-based-microservice-communications). Once we're done we'll have an example ecommerce cart service.

Start by creating a new folder, initialising your app and install pantam with few other dependencies.

```
% mkdir cart_service
% cd cart_service
% pyenv install 3.8.2
% pyenv local 3.8.2
% poetry init
% poetry add pantam
```

Next we'll use the Pantam CLI to make our application.

```
% poetry shell
% pantam serve
```

Follow the steps, accepting the defaults, to create just one action file (index.js) and you should have a structure like this:

```
| cart_service.py
| actions
|   index.js
```

Now let's run the application!

```
% pantam serve --dev
```

You should see something like this:

```
PANTAM: Application loaded! Serving at http://localhost:5000/
PANTAM: Available Routes:

GET    -> /    -> index.py -> fetchAll
GET    -> /{id} -> index.py -> fetchSingle
POST   -> /    -> index.py -> create
PATCH  -> /{id} -> index.py -> update
DELETE -> /{id} -> index.py -> delete
```

Now let's build out our app further.

In the code editor of your choice open `actions/index.py` and setup a database in the class `__init__` method:

```
import sqlite3
from pantam import JSONResponse, PlainTextResponse

class Index:
    def __init__(self):
        database = sqlite3.connect("db")
        cursor = database.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cart
            (product text, cost integer)''')
        database.commit()
```

Now replace all the standard methods with following new code:

```
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


def get_cart_contents(self, request):
    """Get cart contents"""
    database = sqlite3.connect("db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM cart")
    return JSONResponse(cursor.fetchall())


def get_cart_total(self, request):
    """Get cart total value"""
    database = sqlite3.connect("db")
    cursor = database.cursor()
    cursor.execute("SELECT SUM(cost) FROM cart")
    return PlainTextResponse(str(cursor.fetchone()[0]))
```

The first method adds products to the database, the second method retieves the contents of the cart, and the final method calculates the total.

Save your file and the server should automatically reload. Well done you've created a microservice with Pantam, let's test it out!

In a new terminal window run this command to create a product:

```
curl --request POST 'http://localhost:5000/add-product-to-cart/' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'product=Ducati Panigale' \
  --data-urlencode 'cost=25000'
```

Create another product:

```
curl --request POST 'http://localhost:5000/add-product-to-cart/' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'product=Honda C90' \
  --data-urlencode 'cost=1500'
```

Then fetch all of your products from the system.

```
curl --request GET 'http://localhost:5000/cart-contents/'
```

And finally calculate the total cost of all products in the cart.

```
curl --request GET 'http://localhost:5000/cart-total/'
```

That's the end of this guide, thanks for using Pantam!
