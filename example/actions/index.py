# pylint: disable=no-self-use too-few-public-methods

from starlette.responses import JSONResponse


class Index:
    def fetch_all(self):
        """Example Response"""
        return JSONResponse({"hello": "world"})
