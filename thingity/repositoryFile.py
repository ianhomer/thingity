import subprocess
import os
from pathlib import Path


def upFind(directory):
    cwd = Path(".").resolve()
    print(cwd)
    candidate = Path(directory).resolve()
    pathRoot = candidate.root
    while len(candidate.name) > 1 and pathRoot != candidate.name:
        print(candidate)
        if candidate.parent.name == "things":
            if candidate.is_relative_to(cwd):
                return str(candidate.relative_to(cwd))
            else:
                return str(candidate)
        else:
            candidate = candidate.parent


def gitRoot(directory, cmd):
    # No need to change directory if just echo which is done from unit test
    # when mock command is injected
    kwargs = {}
    if cmd[0] != "echo":
        kwargs["cwd"] = directory

    return (
        subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, **kwargs)
        .communicate()[0]
        .rstrip()
    )


class RepositoryFile:
    def __init__(self, base: str, path="", cmd=["git", "rev-parse", "--show-toplevel"]):
        fullPath = base + "/" + path
        directory = os.path.dirname(base + "/" + path)

        self._root = upFind(directory)
        if not self._root:
            self._root = gitRoot(directory, cmd)

        self._path = fullPath[len(self._root) + 1 :]

    @property
    def root(self):
        return self._root

    @property
    def path(self):
        return self._path
