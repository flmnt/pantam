from pantam import Pantam

pantam = Pantam(debug=True, actions_folder="domain/actions")

app = pantam.build()
