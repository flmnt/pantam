# pantam

<img src="https://raw.githubusercontent.com/FilamentSolutions/pantam/master/logo/logo.png" alt="Peter the Pantam Python" width="300">

Pantam is an extensible, ultra lightweight, Python framework for creating RESTful microservices.

Features include:

- built on top of [Starlette](https://www.starlette.io/)
- statically typed with [mypy](https://github.com/python/mypy)
- simple REST routing
- [segregated business logic](https://en.wikipedia.org/wiki/Separation_of_concerns)
- [convention over configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) paradigm
- expressive logging (decent error reporting!)
- live reloading in developer mode

Need to build a Python microservice? [Check out Pantam](https://github.com/flmnt/pantam)

## Getting started

Our goal with Pantam is reduce the work bootstrapping microservices.

With Pantam you can create a basic REST API in 5 minutes or less.

### Examples

- [Domain segregated example](https://github.com/flmnt/pantam/tree/master/example/domain)
- [Event based example](https://github.com/flmnt/pantam/tree/master/example/event)

### Installation

First, install the required packages.

```
% poetry add @flmnt/pantam
```

Once you have installed Pantam you can initialise your app; this can be done with either a brand new or existing app.

```
% poetry @flmnt/pantam init
```

Follow the CLI instructions and then start building your microservice!

### Setup

Pantam expects the following folder structure:

```
| index.py       // can have any name, it's where you run your app
| actions        // where your domain logic sits
|  |  index.py   // primary logic lives here (might be all you need)
|  |  other.py   // add as many other "domains" as you like (optional)
```

In the root level `index.py` file add the following to run Pantam:

```
import Pantam from '@flmnt/pantam';

const app = new Pantam();

app.run();
```

In the `actions` folder create the following files.

`actions/index.py`

```
class Index {

  fetchAll: () => { ... },

  fetchSingle: (id) => { ... },

  create: (data, ctx) => { ... },

  update: (id, data, ctx) => { ... },

  delete: (id) => { ... },

}
```

`actions/other.py`

```
class Other {

  fetchSingle: (id) => { ... },

  create: (data, ctx) => { ... },

  // NB: add as few methods as you need...

}
```

The setup above will make the following routes available:

```
GET      /            // Index.fetchAll()
GET      /:id         // Index.fetchSingle()
POST     /            // Index.create()
PATCH    /:id         // Index.update()
DELETE   /:id         // Index.delete()

GET      /other/:id   // Other.fetchSingle()
POST     /other       // Other.create()
```

And that's you ready to go!

### Development

Start the development server with:

```
% npx @flmnt/pantam serve --dev
```

Your application will be served on http://localhost:3000

In development mode, when you make changes to files the application will update itself.

### Production

To serve your microservice in production use:

```
% npx @flmnt/pantam serve
```

Your application is served at http://your-host:3000

You can change the port number via the configuration options.

## .pantamrc.py

After running `npx @flmnt/pantam init` you will have a `.pantamrc.json` file in your directory with some CLI config options like this:

```
module.exports = {
  actionsFolder: 'actions',
  language: 'typescript',
  entrypoint: 'index.py',
};
```

The `.pantamrc` file provides configuration options for the CLI. You only need to change it if you switch language, change your main file (entrypoint) or rename your actions folder.

## Add New Routes

To add a new action (resource) you can either create a new file in the actions folder or use the CLI to make the file for you:

```
% npx @flmnt/pantam action index.py
```

You can add the standard methods (`fetchAll`, `fetchSingle`, `create`, `update`, `delete`) to an action class which will automatically create the standard routes.

If you'd like to create custom methods for your action class you can create custom getters like this:

```
// GET -> /custom-method/
getCustomMethod(ctx) {
  return ctx.body = 'Custom response';
}
```

And custom setters like this:

```
// POST -> /custom-method/
setCustomMethod(data, ctx) {
  console.log(data);
  return ctx.body = 'Custom response';
}
```

Pantam will ignore methods that are not "standard" methods or do not start with `get` or `set`. However if you want to _ensure_ that your method will be ignored you can prefix the method with an underscore, like this:

```
_myHiddenMethod() {
  // do something secret
}
```

## Creating Responses

Each method in an action file is passed a context (ctx) argument which you use to build a response. You can read the Koa [context API here](https://github.com/koajs/koa/blob/master/docs/api/context.md).

Creating standard responses is very straightforward.

```
fetchAll(ctx) {
  ctx.body = 'Your response here';
}
```

Changing status code is also simple.

```
fetchAll(ctx) {
  ctx.body = 'Your response here';
  ctx.status = 201;
}
```

Adjusting headers requires you to use the `ctx.set()` method.

```
fetchAll(ctx) {
  ctx.body = 'Your response here';
  ctx.status = 201;
  ctx.set('Cache-Control', 'no-cache');
}
```

## Async/Await Support

Feel free to create synchronous or asynchronous action, methods. Pantam can handle both.

```
async getAsyncExample() {
  const result = await findRecords();
  ctx.body = result;
}

getSyncExample() {
  ctx.body = 'static content';
}
```

## Configuration Options

For advanced configuration pass an options object when instantiating Pantam.

```
import Pantam from '@flmnt/pantam';

const options = {
  port: 80,
  ...
};

const app = new Pantam(options);

app.run();
```

The options object can have the following properties:

**port**: `integer`

Sets the port number when serving the app in production mode.

`Default: 3000`

<br>

**devPort**: `integer`

Sets the port number when serving the app in development mode.

`Default: 3000`

<br>

**actionsFolder**: `string`

The folder that contains your action files.

`Default: "actions"`

<br>

**actionsIndexFile**: `string`

The primary action file in your action folder.

`Default: "index"`

<br>

**actionsFileExt**: `string`

The file extension for action files.

`Default: "ts"`

## Extending Pantam

Pantam has been built on top of [Koa](https://github.com/koajs/koa), to expose the Koa application and extend Pantam's functionality you can do the following:

```
import Pantam from '@flmnt/pantam';

const app = new Pantam();

app.extend((koaApp) => {

  koaApp.use(async (ctx, next) => {
    // your code here...
    await next();
  });

  return koaApp;
});

app.run();
```

If you need to add middlewear to specific routes, you'll likely want to interact with the Pantam router, which is provided by [Koa Router](https://github.com/ZijianHe/koa-router).

```
import Pantam from '@flmnt/pantam';

const app = new Pantam();

app.extend((koaApp, koaRouter) => {

  koaApp.use(initMiddlewear());

  koaRouter.use('/url', useMiddlewear());

  return [koaApp, koaRouter];
});

app.run();
```

_NB: if you adjust the router as well as the Koa app, make sure your callback returns an array with the app and then the router (in that order)_

## Debugging

If you're struggling to debug and issue and unsure what routes Pantam has created for you, you can use `logRoutes()` to find out.

```
const app = new Pantam();

app.run().then((app) => {
  app.logRoutes();
});
```

Also check trailing slashes in your urls, these are important.

In the example below the url `test/1` and `test/custom-method` both trigger `fetchSingle()` but the url `test/custom-method/` (with the trailing slash) triggers `getCustomMethod()`.

```
// actions/test.py

// GET -> test/custom-method
// GET -> test/:id
fetchSingle() {}

// GET -> test/custom-method/
getCustomMethod() {}
```

## Contribution

We welcome feedback, suggestions and contributions.

If you have an idea you want to discuss please [open an issue](https://github.com/FilamentSolutions/pantam/issues/new).

## Licenses

Free for personal and commerical use under the [MIT License](https://github.com/FilamentSolutions/pantam/blob/master/LICENSE.md)

_Basil the Pantam_ was created with a free vector from [Vectorportal.com](https://vectorportal.com)
