import configparser
import os
import shutil
from pathlib import Path


class Environment:
    @staticmethod
    def withConfig(withConfig=True):
        return Environment() if withConfig else Environment(configFile=None)

    def __init__(self, directory=None, configFile="~/.config/thingity/thingity.ini"):
        self.home = str(Path.home())
        self.isFish = os.environ.get("SHELL", "").endswith("fish")
        if directory:
            self.directory = directory
            self.confg = {}
        elif configFile:
            normalisedConfigFile = configFile.replace("~", self.home)
            if os.path.isfile(normalisedConfigFile):
                config = configparser.ConfigParser()
                config.read(normalisedConfigFile)
                self.config = config["DEFAULT"]
                self.directory = self.config["THINGS_DIR"]
            else:
                self.directory = os.getcwd()
                self.config = {}
        else:
            self.directory = os.getcwd()
            self.config = {}

    @property
    def editor(self):
        return self.config.get("EDITOR", "nvim")

    @property
    def myDo(self):
        return self.config.get("MY_DO", "")

    @property
    def myNotes(self):
        return self.config.get("MY_NOTES")

    @property
    def streamDir(self):
        return self.config.get("STREAM_DIR") or "stream"

    @property
    def myNotesDir(self):
        return self.directory + "/" + self.myNotes if self.myNotes else self.directory

    def getNotesDir(self, repository):
        return self.directory + "/" + repository

    @property
    def hasGitSynk(self):
        return shutil.which("git-synk")

    @property
    def subshellOpen(self):
        return "(" if self.isFish else "$("
