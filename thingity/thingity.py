import glob
import os
import subprocess
import time
import re
from . import Environment, runner, Signal, Thing

environment = Environment()


def synk(force, justMyNotes=False, inLine=False):
    shouldSynkFile = (
        environment.home + "/.config/dotme/should-run/last-run-git-synk-things"
    )
    if not force and not runner.should(shouldSynkFile):
        return
    if force:
        if environment.hasGitSynk:
            dir = environment.myNotesDir if justMyNotes else environment.directory
            subprocess.run(["git", "synk"], cwd=dir)
            runner.has(shouldSynkFile)
            time.sleep(1)
    else:
        if environment.inKitty and not inLine:
            subprocess.run(
                [
                    "kitty",
                    "@",
                    "launch",
                    "--location",
                    "hsplit",
                    "--dont-take-focus",
                    "--no-response",
                    "fish",
                    "-c",
                    "things --synk -m",
                ]
            )
        elif environment.hasGitSynk:
            subprocess.run(["things", "--synk", "-m"])
    return force


def lint(fix=False, things=[]):
    signals = []
    if things:
        filenames = [os.path.abspath(thing) for thing in things]
    else:
        filenames = glob.iglob(f"{environment.directory}/**/*.md", recursive=True)

    for filename in filenames:
        if re.match(r".*/(node_modules)/.*", filename):
            continue
        try:
            thing = Thing(filename, root=environment.directory)
            if not thing.normal:
                thing.normalise(fix)
        except Exception as exception:
            signals += [Signal(exception=exception, context=filename)]

    for signal in signals:
        print(f"{signal.context} {signal.exception}")
