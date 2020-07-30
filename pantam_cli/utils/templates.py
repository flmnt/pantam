index_template = (
    lambda: """from pantam import Pantam

pantam = Pantam(debug=True)

app = pantam.build()
"""
)


action_template = lambda class_name: """from pantam import PlainTextResponse

class {class_name}:
    def fetch_all(self):
        \"\"\"Fetch all items\"\"\"
        return PlainTextResponse("Pantam: {class_name} -> fetch_all()")

    def fetch_single(self, uid):
        \"\"\"Fetch single item\"\"\"
        return PlainTextResponse("Pantam: {class_name} -> fetch_single()")

    def create(self, data):
        \"\"\"Create an item\"\"\"
        return PlainTextResponse("Pantam: {class_name} -> create()")

    def update(self, uid, data):
        \"\"\"Update an item\"\"\"
        return PlainTextResponse("Pantam: {class_name} -> update()")

    def delete(self, uid):
        \"\"\"Delete single item\"\"\"
        return PlainTextResponse("Pantam: {class_name} -> delete()")
""".format(
    class_name=class_name
)
