from starlette import responses, requests
from .pantam import Pantam, introspect_methods

Request = requests.Request

Response = responses.Response
JSONResponse = responses.JSONResponse
HTMLResponse = responses.HTMLResponse
PlainTextResponse = responses.PlainTextResponse
FileResponse = responses.FileResponse
RedirectResponse = responses.RedirectResponse
