# pantam

<img src="https://raw.githubusercontent.com/flmnt/pantam/master/logo/logo.png" alt="Peter the Pantam Python" width="300">

Pantam is an extensible, ultra lightweight, Python framework for creating RESTful microservices.

Features include:

- built on top of [Starlette](https://www.starlette.io/)
- served using [Uvicorn](https://www.uvicorn.org/)
- simple REST routing
- [segregated business logic](https://en.wikipedia.org/wiki/Separation_of_concerns)
- [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) paradigm
- expressive logging (decent error reporting!)
- live reloading in developer mode

Need to build a Javascript microservice? [Check out Bantam](https://github.com/flmnt/bantam)

## Getting started

Our goal with Pantam is reduce the work bootstrapping microservices.

With Pantam you can create a basic REST API in 5 minutes or less.

### Examples

- [Domain segregated example](https://github.com/flmnt/pantam/tree/master/example/domain)
- [Event based example](https://github.com/flmnt/pantam/tree/master/example/event)

### Installation

We recommend using [Poetry](https://python-poetry.org/) with [Pyenv](https://github.com/pyenv/pyenv) for dependency and environment management (this documentation will use Poetry throughout) but if you prefer `pip` or `conda` then crack on!

If you haven't done so already, setup your python environment and Poetry project:

```
% pyenv install 3.8.2
% pyenv local 3.8.2
% poetry init
```

_NB: if you specify pantam as a package during the setup process, run `poetry install` and skip the next step._

Now install the Pantam package:

```
% poetry add pantam
```

Once you have installed Pantam you can initialise your app.

```
% poetry shell
% pantam init
```

Follow the CLI instructions and then start building your microservice!

### Setup

Pantam expects the following folder structure:

```
| main.py       // can have any name, it's where you run your app
| actions        // where your domain logic sits
|  |  index.py   // primary logic lives here (might be all you need)
|  |  other.py   // add as many other "domains" as you like (optional)
```

In the root level `main.py` file add the following to run Pantam:

```
from pantam import Pantam

pantam = Pantam()

app = pantam.build()

if __name__ == "__main__":
    pantam.run("main", "app")
```

In the `actions` folder create the following files.

`actions/index.py`

```
class Index:
  def fetch_all(self):
    pass

  def fetch_single(self, uid):
    pass

  def create(self, data):
    pass

  def update(self, uid, data):
    pass

  def delete(self, uid):
    pass
```

`actions/other.py`

```
class Other:
  def fetch_single(self, uid):
    pass

  def create(self, data):
    pass
```

The setup above will make the following routes available:

```
GET      /            // Index.fetch_all()
GET      /:id         // Index.fetch_single()
POST     /            // Index.create()
PATCH    /:id         // Index.update()
DELETE   /:id         // Index.delete()

GET      /other/:id   // Other.fetch_single()
POST     /other       // Other.create()
```

And that's you ready to go!

### Development

Configure the application to live reload on a given port as follows:

```
from pantam import Pantam

pantam = Pantam(debug=True)

app = pantam.build()
```

Then serve the app:

```
% pantam serve --dev
```

Your application will be served on http://localhost:5000

_NB: Pantam looks for a `PANTAM_ENV` environment variable when serving the application and defaults to `development` if no variable is set._

### Production

To serve your microservice in production use:

```
% pantam serve
```

Your application is served at http://your-host:5000

You can change the port number via the configuration options.

_NB: in production you should set a `PANTAM_ENV=production` environment variable._

## .pantamrc.json

After running `pantam init` you will have a `.pantamrc.json` file in your directory with some CLI config options like this:

```
{
  "actions_folder": "actions",
  "entrypoint": "example.py",
  "port": 5000,
  "dev_port": 5000
}
```

The `.pantamrc.json` file provides configuration options for the CLI. You only need to change it if you change your main file (entrypoint) or rename your actions folder.

## Add New Routes

To add a new action (resource) you can either create a new file in the actions folder or use the CLI to make the file for you:

```
% pantam action index.py
```

You can add the standard methods (`fetch_all`, `fetch_single`, `create`, `update`, `delete`) to an action class which will automatically create the standard routes.

If you'd like to create custom methods for your action class you can create custom getters like this:

```
// GET -> /custom-method/
def get_custom_method(self):
  # your code here
```

And custom setters like this:

```
// POST -> /custom-method/
def set_custom_method(self, data):
  print(data)
  # your code here
```

Pantam will ignore methods that are not "standard" methods or do not start with `get` or `set`. However if you want to _ensure_ that your method will be ignored you can prefix the method with a double underscore, like this:

```
def __my_hidden_method(self):
  // do something secret
```

## Creating Responses

To create a response, make use of the [Starlette response API](https://www.starlette.io/responses/), you can import all responses from starlette or import common responses from Pantam directly, including: `JSONResponse`, `HTMLResponse`, `PlainTextResponse`, `FileResponse`, `RedirectResponse`.

Here are a few examples:

```
from pantam import PlainTextResponse

class YourClass:
  def fetch_all():
    return PlainTextResponse("This is fetch all!")
```

```
from pantam import JSONResponse

class YourClass:
  def fetch_all():
    return JSONResponse([{ "content": "example" }])
```

Changing status code is also simple.

```
def fetch_all(self):
  return PlainTextResponse("This is fetch all!", status_code=404)
```

Adjusting headers can also be achieved.

```
def fetch_all(self):
  headers = {
    "Cache-Control": "no-cache"
  }
  return PlainTextResponse("This is fetch all!", headers=headers)
```

## Configuration Options

For advanced configuration pass options in when instantiating Pantam.

```
from pantam import Pantam

pantam = Pantam(debug=True) # add options as below

app = pantam.build()

if __name__ == "__main__":
    pantam.run("main", "app")
```

You can set the following options:

**debug**: `bool`

Turns debugging mode on for Pantam (and underlying Starlette). Provides more verbose error messages. Should be off in production.

`Default: False`

**actions_folder**: `string`

The folder that contains your action files.

`Default: "actions"`

<br>

**actions_index**: `string`

The primary action file in your action folder.

`Default: "index"`

## Debugging

If you're struggling to debug and issue and unsure what routes Pantam has created for you, set the `debug` option to True.

```
from pantam import Pantam

pantam = Pantam(debug=True)

app = pantam.build()
```

Also check trailing slashes in your urls, these are important.

In the example below the url `test/1` and `test/custom-method` both trigger `fetch_single()` but the url `test/custom-method/` (with the trailing slash) triggers `get_custom_method()`.

```
// actions/test.py

// GET -> test/custom-method
// GET -> test/:id
fetch_single()

// GET -> test/custom-method/
get_custom_method()
```

## Contribution

We welcome feedback, suggestions and contributions.

If you have an idea you want to discuss please [open an issue](https://github.com/flmnt/pantam/issues/new).

## Licenses

Free for personal and commerical use under the [MIT License](https://github.com/flmnt/pantam/blob/master/LICENSE.md)
