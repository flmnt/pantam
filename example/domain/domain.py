from pantam import Pantam

pantam = Pantam(debug=True, dev_port=5001)

app = pantam.build()

if __name__ == "__main__":
    pantam.run("domain", "app")
