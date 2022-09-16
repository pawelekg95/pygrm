from tkinter import *


class Depot:
    def __init__(self):
        self.docker_logged = BooleanVar()
        self.docker_logged.set(False)
        self.github_logged = BooleanVar()
        self.github_logged.set(False)
