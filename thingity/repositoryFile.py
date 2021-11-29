import subprocess
import os
from pathlib import Path


def upFind(directory):
    path = Path(directory)
    if path.parent.name == "things":
        return directory
    return next(
        (
            str(parent)
            for parent in path.parents
            if parent.parent.name == "things"
        ),
        None,
    )


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

        if not self._root:
            raise Exception(f"Cannot find root of {fullPath}")

        self._path = fullPath[len(self._root) + 1 :]

    @property
    def root(self):
        return self._root

    @property
    def path(self):
        return self._path
