from typing import Any, Callable, Final, List, Literal, Optional, TypedDict, Union
from functools import reduce
from importlib import import_module
from inspect import getmembers, isfunction
from re import match, sub
from os import listdir
from starlette.applications import Starlette
from starlette.routing import Route
from .services import Logger


class Config(TypedDict):
    actions_folder: str
    actions_index: str
    debug: bool
    dev_port: int
    port: int
    reload: Optional[bool]


VERB = Literal["get", "post", "patch", "delete"]


class ActionRoute(TypedDict):
    method: str
    verb: VERB
    url: str


class ActionResource(TypedDict, total=False):
    file_name: str
    module_name: str
    class_name: str
    action_class: Callable[[], Any]
    action_obj: Any
    routes: List[ActionRoute]


class Methods(TypedDict):
    get: List[str]
    post: List[str]
    patch: List[str]
    delete: List[str]


GET_METHOD_RE = r"^(get\w*|fetch_all|fetch_single)$"
POST_METHOD_RE = r"^(set\w*|do\w*|create)$"
PATCH_METHOD_RE = r"^update$"
DELETE_METHOD_RE = r"^delete$"

INDI_RES_RE = r"^(fetch_single|update|delete|do\w*)$"

CUSTOM_METHOD_RE = r"^(get|set|do)\w*$"


def introspect_methods(action_class: Callable[[], Any]) -> Methods:
    """Map action class methods to method dictionary"""

    def predicate(attribute: Any) -> bool:
        return isfunction(attribute)

    methods: Methods = {
        "get": list(
            filter(
                lambda x: match(GET_METHOD_RE, x),
                map(lambda x: x[0], getmembers(action_class, predicate)),
            )
        ),
        "post": list(
            filter(
                lambda x: match(POST_METHOD_RE, x),
                map(lambda x: x[0], getmembers(action_class, predicate)),
            )
        ),
        "patch": list(
            filter(
                lambda x: match(PATCH_METHOD_RE, x),
                map(lambda x: x[0], getmembers(action_class, predicate)),
            )
        ),
        "delete": list(
            filter(
                lambda x: match(DELETE_METHOD_RE, x),
                map(lambda x: x[0], getmembers(action_class, predicate)),
            )
        ),
    }
    return methods


class Pantam:
    logger: Final[Logger] = Logger()

    def __init__(
        self,
        actions_folder="actions",
        actions_index="index",
        debug=False,
        dev_port=5000,
        port=5000,
        reload=None,
    ) -> None:
        self.config: Config = {
            "actions_folder": actions_folder,
            "actions_index": actions_index,
            "debug": debug,
            "dev_port": dev_port,
            "port": port,
            "reload": reload,
        }
        self.actions: List[ActionResource] = []
        self.routes: List[Route] = []

    def get_config(self) -> Config:
        """Get Pantam app config"""
        return self.config

    def set_config(self, config: Config) -> None:
        """Set Pantam app config"""
        self.config = config

    def read_actions_folder(self) -> List[str]:
        """Read action files from actions folder"""
        config = self.get_config()
        files: List[str] = []

        def predicate(file_name: str):
            return ".py" in file_name and "__init__" not in file_name

        try:
            files.extend(filter(predicate, listdir(config["actions_folder"])))
        except:
            self.logger.error(
                "Unable to read actions folder! Check `actions_folder` config setting."
            )
        return files

    def get_actions(self) -> List[ActionResource]:
        """Get Pantam actions"""
        if len(self.actions) == 0:
            self.logger.error(
                "You have no loaded actions. Check for files in the actions folder."
            )
        return self.actions

    def log_routes(self) -> None:
        """Print Pantam routes in human readable format"""
        actions = self.get_actions()

        routes: List[ActionRoute] = []
        for action in actions:
            routes.extend(action["routes"])

        if len(routes) == 0:
            self.logger.error("No available routes!")
            return

        routes_to_log: List[str] = []
        routes_to_log.append("Available Routes:\n")

        longest_file_name = reduce(max, map(lambda z: len(z["file_name"]), actions), 0)

        longest_url = reduce(max, map(lambda z: len(z["url"]), routes), 0)

        def column_format(text: str, padding: int) -> str:
            return "{text:{padding}}".format(text=text, padding=padding)

        for action in actions:
            for route in action["routes"]:
                routes_to_log.append(
                    " -> ".join(
                        (
                            column_format(route["verb"].upper(), 6),
                            column_format(route["url"], longest_url),
                            column_format(action["file_name"], longest_file_name),
                            route["method"],
                        )
                    )
                )

        self.logger.info("\n".join(routes_to_log))

    def discover_actions(self) -> List[ActionResource]:
        """Parse methods from action files"""
        action_files = self.read_actions_folder()
        actions: List[ActionResource] = []
        for file_name in action_files:
            module_name = file_name.replace("_", "-").replace(".py", "")
            class_name = module_name.replace("-", " ").title().replace(" ", "")
            actions.append(
                {
                    "file_name": file_name,
                    "module_name": module_name,
                    "class_name": class_name,
                    "routes": [],
                }
            )
        self.actions = actions
        return actions

    def import_action_module(
        self, module_name: str, class_name: str
    ) -> Union[Callable[[], Any], None]:
        """Load an action file"""
        try:
            actions_folder = self.get_config()["actions_folder"]
            action_module: Any = import_module("%s.%s" % (actions_folder, module_name))
            action_class: Any = getattr(action_module, class_name)
            return action_class
        except:
            self.logger.error(
                "Unable to load `%s.%s` module." % (actions_folder, module_name)
            )
            return None

    def load_actions(self) -> None:
        """Import and instantiate action classes"""
        actions = self.get_actions()

        def action_loader(action: ActionResource) -> ActionResource:
            try:
                action_class = self.import_action_module(
                    action["module_name"], action["class_name"]
                )
                if action_class is not None:
                    action["action_class"] = action_class
                    action["action_obj"] = action_class()
            except:
                self.logger.error(
                    "Unable to instantiate `%s` action class." % action["class_name"]
                )
            return action

        self.actions = list(map(action_loader, actions))

    def make_url(self, module_name: str, method: str) -> str:
        """Create URL for action routes"""
        actions_index = self.get_config()["actions_index"]
        url = "/" if actions_index == module_name else "/%s/" % module_name
        is_custom_method = match(CUSTOM_METHOD_RE, method)
        if is_custom_method:
            slug = sub(r"^(get|set|do)_", "", method).replace("_", "-").lower()
            url = "%s%s/" % (url, slug)
        is_individual_res = match(INDI_RES_RE, method)
        if is_individual_res:
            url = "%s{id}" % url
        return url

    def make_routes(
        self, path: str, action: Callable[[], Any] = None
    ) -> List[ActionRoute]:
        """Create action routes with method, verb, and URL"""
        if action is None:
            return []
        methods = introspect_methods(action)

        def map_to_route(verb: VERB):
            return lambda method: {
                "method": method,
                "verb": verb,
                "url": self.make_url(path, method),
            }

        get_routes = list(map(map_to_route("get"), methods["get"]))
        post_routes = list(map(map_to_route("post"), methods["post"]))
        patch_routes = list(map(map_to_route("patch"), methods["patch"]))
        delete_routes = list(map(map_to_route("delete"), methods["delete"]))
        return get_routes + post_routes + patch_routes + delete_routes

    def bind_routes(self) -> None:
        """Create starlette routes"""
        actions = self.get_actions()

        starlette_routes: List[Route] = []

        for action in actions:
            try:
                routes = self.make_routes(action["module_name"], action["action_class"])
                action["routes"] = routes

                if len(routes) == 0:
                    self.logger.error(
                        "No methods found for `%s` action." % action["module_name"]
                    )
                    continue

                def prepare_verb(verb: VERB) -> List[str]:
                    return [verb.upper()]

                for route in routes:
                    starlette_routes.append(
                        Route(
                            route["url"],
                            getattr(action["action_obj"], route["method"]),
                            methods=prepare_verb(route["verb"]),
                        )
                    )
            except:
                self.logger.error(
                    "Unable to bind `%s` action methods to route."
                    % action["module_name"]
                )

        self.routes = starlette_routes

    def get_routes(self, skip_check: bool = False) -> List[Route]:
        """Get underlying Starlette routes"""
        if len(self.routes) == 0 and skip_check is False:
            self.logger.error("No routes have been defined.")
        return self.routes

    def build(self) -> Optional[Starlette]:
        """Build Pantam application"""
        config = self.get_config()
        self.discover_actions()
        self.load_actions()
        self.bind_routes()
        routes = self.get_routes()
        if config["debug"]:
            self.log_routes()
        try:
            return Starlette(routes=routes, debug=config["debug"])
        except:
            self.logger.error("Unable to build Pantam application!")
        return None
