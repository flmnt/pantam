# pylint: disable=missing-function-docstring too-few-public-methods
from unittest.mock import Mock, patch
from typing import Any
from pantam import Pantam, introspect_methods


def test_get_default_options():
    app = Pantam()
    default_config = {
        "actions_folder": "actions",
        "actions_index": "index",
    }
    assert app.get_config() == default_config


def test_override_some_options():
    app = Pantam(actions_folder="axs")
    default_config = {
        "actions_folder": "axs",
        "actions_index": "index",
    }
    assert app.get_config() == default_config


def test_override_all_options():
    app = Pantam(actions_folder="axs", actions_index="main")
    default_config = {
        "actions_folder": "axs",
        "actions_index": "main",
    }
    assert app.get_config() == default_config


def test_set_options_programmatically():
    app = Pantam()
    config = app.get_config()
    config["port"] = 82
    app.set_config(config)
    assert app.get_config() == config


@patch("pantam.pantam.listdir")
def test_read_actions_folder(mock):
    mock.return_value = ["foo.py", "bar.py", "rubbish.txt", "__init__.py"]
    app = Pantam()
    files = app.read_actions_folder()
    assert files == ["foo.py", "bar.py"]


@patch("pantam.pantam.listdir")
@patch("pantam.pantam.Logger.error")
def test_handle_read_actions_error(logger_mock, os_mock):
    def throw_error():
        raise Exception("Fake Error")

    os_mock.side_effect = throw_error
    app = Pantam()
    app.read_actions_folder()
    logger_mock.assert_called_with(
        "Unable to read actions folder! Check `actions_folder` config setting."
    )


def test_get_action_routes():
    app = Pantam()
    app.actions = "test"
    assert app.get_actions() == "test"


@patch("pantam.pantam.Logger.error")
def test_action_routes_error(logger_mock):
    app = Pantam()
    app.get_actions()
    logger_mock.assert_called_with(
        "You have no loaded actions. Check for files in the actions folder."
    )


class MockAction:
    def fetch_all(self) -> None:
        pass

    def fetch_single(self, uid: str) -> None:
        pass

    def create(self, data: Any) -> None:
        pass

    def update(self, uid: str, data: Any) -> None:
        pass

    def delete(self, uid: str) -> None:
        pass

    def get_custom(self) -> None:
        pass

    def set_custom(self) -> None:
        pass

    def __private_method(self) -> None:
        pass


@patch("pantam.pantam.Logger.info")
def test_log_routes(logger_mock):
    action_object = MockAction()
    app = Pantam()
    app.actions = [
        {
            "file_name": "index.py",
            "path_name": "index",
            "action_class": MockAction,
            "action_obj": action_object,
            "routes": [
                {"method": "fetchAll", "verb": "get", "url": "/",},
                {"method": "fetchSingle", "verb": "get", "url": "/:id",},
            ],
        },
    ]
    app.log_routes()
    logger_mock.assert_called_with(
        """Available Routes:

GET    -> /    -> index.py -> fetchAll
GET    -> /:id -> index.py -> fetchSingle"""
    )


def test_discover_actions():
    app = Pantam()
    app.read_actions_folder = Mock(return_value=["index.py", "auth_test.py"])  # type: ignore
    actions = app.discover_actions()
    expected = [
        {
            "file_name": "index.py",
            "path_name": "index",
            "module_name": "Index",
            "routes": [],
        },
        {
            "file_name": "auth_test.py",
            "path_name": "auth-test",
            "module_name": "AuthTest",
            "routes": [],
        },
    ]
    assert actions == expected


@patch("pantam.pantam.Logger.error")
def test_import_action_module(logger_mock):
    app = Pantam()
    app.import_action_module("Index")
    logger_mock.assert_called_with("Unable to load `actions.Index` module.")


def test_load_actions():
    app = Pantam()
    app.read_actions_folder = Mock(return_value=["index.py"])  # type: ignore
    app.import_action_module = Mock(return_value=MockAction)  # type: ignore
    app.discover_actions()
    app.load_actions()
    actions = app.get_actions()
    assert actions[0]["action_class"] == MockAction
    assert isinstance(actions[0]["action_obj"], MockAction)
    assert actions[0]["file_name"] == "index.py"
    assert actions[0]["path_name"] == "index"
    assert actions[0]["module_name"] == "Index"
    assert actions[0]["routes"] == []


def test_introspect_methods():
    methods = introspect_methods(MockAction)
    assert methods == {
        "get": ["fetch_all", "fetch_single", "get_custom"],
        "post": ["create", "set_custom"],
        "patch": ["update"],
        "delete": ["delete"],
    }


def test_make_default_urls():
    app = Pantam()
    assert app.make_url("index", "fetch_all") == "/"
    assert app.make_url("index", "fetch_single") == "/{id}"
    assert app.make_url("index", "create") == "/"
    assert app.make_url("index", "update") == "/{id}"
    assert app.make_url("index", "delete") == "/{id}"


def test_make_custom_resource_urls():
    app = Pantam()
    assert app.make_url("custom-action", "fetch_all") == "/custom-action/"
    assert app.make_url("custom-action", "fetch_single") == "/custom-action/{id}"
    assert app.make_url("custom-action", "create") == "/custom-action/"
    assert app.make_url("custom-action", "update") == "/custom-action/{id}"
    assert app.make_url("custom-action", "delete") == "/custom-action/{id}"


def test_make_custom_method_urls():
    app = Pantam()
    assert app.make_url("index", "get_my_custom_method") == "/my-custom-method/"
    assert app.make_url("foo", "set_your_magic_method") == "/foo/your-magic-method/"


def test_make_routes():
    app = Pantam()
    routes = app.make_routes("index", MockAction)
    assert routes == [
        {"method": "fetch_all", "url": "/", "verb": "get",},
        {"method": "fetch_single", "url": "/{id}", "verb": "get",},
        {"method": "get_custom", "url": "/custom/", "verb": "get",},
        {"method": "create", "url": "/", "verb": "post",},
        {"method": "set_custom", "url": "/custom/", "verb": "post",},
        {"method": "update", "url": "/{id}", "verb": "patch",},
        {"method": "delete", "url": "/{id}", "verb": "delete",},
    ]


class MockEmptyAction:
    """Empty Mock"""


@patch("pantam.pantam.Logger.error")
def test_bind_routes_error(logger_mock):
    app = Pantam()
    app.get_actions = Mock(
        return_value=[
            {
                "file_name": "index.py",
                "path_name": "index",
                "module_name": "index",
                "action_class": MockEmptyAction,
                "action_obj": MockEmptyAction(),
            },
        ]
    )
    app.bind_routes()
    logger_mock.assert_called_with("No methods found for `index` action.")


class MockSmallAction:
    def fetch_all(self) -> None:
        pass

    def fetch_single(self, uid: str) -> None:
        pass


def test_bind_routes():
    app = Pantam()
    app.get_actions = Mock(
        return_value=[
            {
                "file_name": "index.py",
                "path_name": "index",
                "module_name": "index",
                "action_class": MockSmallAction,
                "action_obj": MockSmallAction(),
            },
        ]
    )
    app.bind_routes()
    assert len(app.routes) == 2
    assert app.routes[0].path == "/"
    assert app.routes[1].path == "/{id}"


@patch("pantam.pantam.Logger.error")
def test_get_routes(logger_mock):
    app = Pantam()
    app.get_routes()
    logger_mock.assert_called_with("No routes have been defined.")


def test_extend():
    app = Pantam()
    app.routes = ["test"]
    app.extend(lambda x: ["foo", "bar"])
    assert app.routes == ["foo", "bar"]


@patch("pantam.pantam.Starlette")
@patch("pantam.pantam.Logger.error")
def test_prepare_error(logger_mock, app_mock):
    def throw_error():
        raise Exception("Fake Error")

    app_mock.side_effect = throw_error
    app = Pantam()
    app.build()
    logger_mock.assert_called_with("Unable to build Pantam application!")


def test_debug():
    app = Pantam(debug=True)
    assert app.debug
