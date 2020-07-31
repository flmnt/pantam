from pantam import Pantam

pantam = Pantam(debug=True)

app = pantam.build()

if __name__ == "__main__":
    pantam.run("event", "app")
