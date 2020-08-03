# Domain based microservice example

The following example microservice has been created using [Pantam](https://github.com/flmnt/pantam).

Follow the quickstart steps below to checkout this repo and explore this exact example or skip this step and creating this example yourself from scratch.

## Quickstart

Open a terminal and run the following: (you will need [Pyenv](https://github.com/pyenv/pyenv) and [Poetry](https://python-poetry.org/) installed)

```
% git clone git@github.com:flmnt/pantam.git
% cd pantam/example/domain
% pyenv install 3.8.2
% pyenv local 3.8.2
% poetry install
% poetry shell
% pantam serve --dev
```

To test the example app out, in a new terminal, run:

```
curl --request GET 'http://localhost:5000'
```

## Tutorial

Let's build the example in this folder from scratch together.

We're going to build a [domain segregated microservice](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model). Once we're done we'll have an example "user" service.

Start by creating a new folder, initialising your app and install pantam with few other dependencies.

```
% mkdir user_service
% cd user_service
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

Follow the steps, accepting the defaults, to create just one action file (index.py) and you should have a structure like this:

```
| user_service.js
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS users
            (uid text, first_name text, last_name text, email string)""")
        database.commit()
```

Now change the `fetchAll` method to look like this:

```
def fetch_all(self, request):
    """Fetch all items"""
    database = sqlite3.connect("db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users")
    return JSONResponse(cursor.fetchall())
```

Save your file and the server should automatically reload.

In a new terminal window run this command:

```
curl --request GET 'http://localhost:5000'
```

And you should see an empty list `[]`. Let's created the rest of the methods to populate the database.

```
    def fetch_single(self, request):
        """Fetch single item"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        uid = request.path_params["id"]
        cursor.execute("SELECT * FROM users WHERE uid=?", (uid))
        return JSONResponse(cursor.fetchone())


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


    def delete(self, request):
        """Delete single item"""
        database = sqlite3.connect("db")
        cursor = database.cursor()
        uid = request.path_params["id"]
        cursor.execute("DELETE FROM users WHERE uid=?", (uid))
        database.commit()
        return PlainTextResponse("Deleted!")
```

You'll notice that `create()` and `update()` are asynchronous, this is required to await the `request.form()` function. When developing your microservices you can choose to use synchronous or asynchronous methods.

We can test each method in order with the following CURL commands:

```
// create
curl --request POST 'http://localhost:5000' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'firstName=Homer' \
  --data-urlencode 'lastName=Simpson' \
  --data-urlencode 'email=homer@donut.me'

// fetchAll – we now get records!
curl --request GET 'http://localhost:5000

// fetchSingle
curl --request GET 'http://localhost:5000/1

// update
curl --request PATCH 'http://localhost:5000/0' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'lastName=Flanders'

// delete
curl --request DELETE 'http://localhost:5000/1'
```

And we're done! You've created your first microservice using Pantam.
