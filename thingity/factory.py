import datetime


class Factory:
    def __init__(self, environment):
        self.environment = environment

    def getTodayLog(self, repository=None, now=datetime.datetime.now()):
        today = now.strftime("%m%d")
        return self.getPath(today, repository)

    def getPath(self, name, repository):
        notesDir = (
            self.environment.getNotesDir(repository)
            if repository
            else self.environment.myNotesDir
        )
        return f"{notesDir}/{self.environment.streamDir}/{name}.md"
