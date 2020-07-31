index_template = lambda file_name: """from pantam import Pantam

pantam = Pantam(debug=True)

app = pantam.build()

if __name__ == "__main__":
    pantam.run("{file_name}", "app")
""".format(
    file_name=file_name
)


action_template = lambda class_name: """from pantam import PlainTextResponse

class {class_name}:
    def fetch_all(self, request):
        \"\"\"Fetch all items\"\"\"
        return PlainTextResponse("Pantam: {class_name} -> fetch_all()")

    def fetch_single(self, request):
        \"\"\"Fetch single item\"\"\"
        uid = request.path_params["id"]
        return PlainTextResponse("Pantam: {class_name} -> fetch_single()")

    def create(self, request):
        \"\"\"Create an item\"\"\"
        return PlainTextResponse("Pantam: {class_name} -> create()")

    def update(self, request):
        \"\"\"Update an item\"\"\"
        uid = request.path_params["id"]
        return PlainTextResponse("Pantam: {class_name} -> update()")

    def delete(self, request):
        \"\"\"Delete single item\"\"\"
        uid = request.path_params["id"]
        return PlainTextResponse("Pantam: {class_name} -> delete()")
""".format(
    class_name=class_name
)
