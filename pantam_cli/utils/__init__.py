from os import name, system


def clear():
    """Clear console"""
    system("cls" if name == "nt" else "clear")
