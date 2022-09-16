from data.depot import Depot
from windows.github_login_window import GithubLoginWindow
from windows.docker_login_window import DockerLoginWindow

from tkinter import *
from pathlib import Path


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("PyGRM")
        self.minsize(800, 600)
        self.depot = Depot()
        self.docker_image_logged = None
        self.docker_image = None
        self.docker_button = None

        self.github_image_logged = None
        self.github_image = None
        self.github_button = None

        self.initialize_buttons()

    def docker_log(self):
        current_value = self.depot.docker_logged.get()
        self.depot.docker_logged.set(not current_value)
        self.update_buttons()

    def github_log(self):
        current_value = self.depot.github_logged.get()
        self.depot.github_logged.set(not current_value)
        self.update_buttons()

    def update_buttons(self):
        image1 = (self.docker_image_logged if self.depot.docker_logged.get() else self.docker_image)
        self.docker_button.configure(image=image1)
        image2 = (self.github_image_logged if self.depot.github_logged.get() else self.github_image)
        self.github_button.configure(image=image2)

    def initialize_buttons(self):
        self.initialize_docker_button()
        self.initialize_github_button()

    def initialize_docker_button(self):
        docker_image_logged_path = Path(__file__).resolve().parent.parent.parent / "images/docker_logged.png"
        docker_image_path = Path(__file__).resolve().parent.parent.parent / "images/docker.png"
        self.docker_image_logged = PhotoImage(file=docker_image_logged_path)
        self.docker_image = PhotoImage(file=docker_image_path)
        image = (self.docker_image_logged if self.depot.docker_logged.get() else self.docker_image)
        self.docker_button = Button(self, image=image, command=self.docker_log)
        self.docker_button.place(x=700, y=500)

    def initialize_github_button(self):
        github_image_logged_path = Path(__file__).resolve().parent.parent.parent / "images/github_logged.png"
        github_image_path = Path(__file__).resolve().parent.parent.parent / "images/github.png"
        self.github_image_logged = PhotoImage(file=github_image_logged_path)
        self.github_image = PhotoImage(file=github_image_path)
        image = (self.github_image_logged if self.depot.github_logged.get() else self.github_image)
        self.github_button = Button(self, image=image, command=self.github_log)
        self.github_button.place(x=700, y=420)
