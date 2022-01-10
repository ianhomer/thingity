#!/usr/bin/env python3

import argparse
import os
import os.path
import subprocess
import re
import sys
from datetime import datetime
from pathlib import Path
from subprocess import PIPE
from .. import Ag, ContextFilter, Environment, Factory, Task, thingity, TaskRenderer

PURPLE = "\033[95m"
ORANGE = "\033[33m"
CYAN = "\033[36m"
GREEN = "\033[32m"
GREY = "\033[90m"
END = "\033[0m"


# - [ ] ABC Todo
# - [x] ABC Done
# - [ ] ABC . Backlog
# - [ ] ABC - Garage
# - [ ] ABC ~ Alignment
# - [x] ABC x Cancelled
# - [ ] ABC Q Question


def run():
    parser = argparse.ArgumentParser(description="todoer")
    parser.add_argument("do", nargs="*", help="do")
    parser.add_argument(
        "-a", "--all", help="show all types of todos", action="store_true"
    )
    parser.add_argument(
        "-i", "--include", help="include all contexts", action="store_true"
    )
    parser.add_argument(
        "-c", "--context", help="list all contexts", action="store_true"
    )
    parser.add_argument("--days", type=int, help="days")
    parser.add_argument("--encoding", help="character encoding", default="utf-8")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("-t", "--today", help="add today item", action="store_true")

    # General settings
    parser.add_argument("--noconfig", help="ignore config files", action="store_true")
    parser.add_argument("--filter", help="filter")
    parser.add_argument("--test", help="test mode")
    parser.add_argument("--noedit", help="don't edit file", action="store_true")

    parser.add_argument("--getfilename", help="just return filename instead of editing")
    parser.add_argument("--justarchive", action="store_true")
    parser.add_argument("--witharchive", action="store_true")
    parser.add_argument("--hiderepository", action="store_true")
    parser.add_argument("-r", "--repository")

    args = parser.parse_args()

    if args.test:
        args.filter = args.test
        args.noconfig = True
        args.noedit = True

    environment = Environment.withConfig(not args.noconfig)

    if (not args.filter) and thingity.synk(False):
        return

    if args.do and len(args.do) > 1:
        words = []

        # Scan words
        for word in args.do:
            if environment.home == word:
                words.append("~")
            else:
                words.append(word)
        # do to add
        do = " ".join(words)
        add(environment, args.repository, do)
        return

    if args.context:
        context(environment)
        return

    # Repeat search until we exit (Ctrl-C)
    more = True
    while more:
        more = search(environment, args)


def context(environment: Environment):
    ag = subprocess.Popen(
        [
            "ag",
            "--nocolor",
            "--nobreak",
            "--nofilename",
            "--follow",
            "\\- \\[ \\] [A-Z]{3}",
            environment.directory,
        ],
        stdout=PIPE,
    )
    sed = subprocess.Popen(
        ["sed", "s/- \\[ \\] \\([A-Z]\\{3\\}\\) .*/\\1/g"],
        stdin=ag.stdout,
        stdout=PIPE,
    )
    result = subprocess.run(["sort", "-u"], stdin=sed.stdout, stdout=PIPE, text=True)
    for line in result.stdout.splitlines():
        print(line)
    return


def search(environment: Environment, args):

    contextFilter = ContextFilter(environment.myDo)
    excludes = [] if args.include or args.do else contextFilter.excludes

    todoPattern = "^[ ]*\\- \\[ \\]"
    if args.all:
        if args.do:
            pattern = f"{todoPattern} {contextFilter.pattern(args.do[0])}"
        else:
            pattern = todoPattern
    elif args.do:
        # pattern = f"\\- \\[ \\] (GEE|DOT) [^\\.\\-]"
        pattern = f"{todoPattern} {contextFilter.pattern(args.do[0])} [^\\.\\-]"
    else:
        # By default ignore todos
        pattern = f"{todoPattern}(?! ([A-Z]{3} )?[\\.\\-])"

    ag = Ag(environment, args.justarchive, args.witharchive or args.all)
    agParts = ag.parts(
        pattern, ["--noheading", "--nonumbers", "--nocolor", "--nobreak", "--follow"]
    )
    result = subprocess.run(agParts, stdout=PIPE, text=True, encoding=args.encoding)

    lines = result.stdout.splitlines()
    print(lines)
    days = args.days or (30 if args.all else 3)
    dos = []
    renderer = TaskRenderer(theme=None if args.stream else "do")
    for line in lines:
        task = Task(line, nearDays=days)
        if task.context not in excludes and (
            not args.repository or args.repository == task.repository
        ):
            dos.append(renderer.render(task) + ("" if args.stream else "\n"))
    dos.sort()
    # Simply stream the output
    if args.stream:
        for do in dos:
            print(do[5:])
        return False
    fzfArgs = [
        "fzf",
        "--ansi",
        "--height",
        "100%",
        "+m",
        "-d",
        "\t",
        "--with-nth",
        ("2,3,4" if not args.hiderepository else "2,3"),
        "--tabstop",
        "4",
        "--layout",
        "reverse",
        "--tiebreak",
        "begin",
        "--bind=ctrl-s:abort,ctrl-w:abort,ctrl-space:abort,"
        + "ctrl-o:execute(tmux split-window -v 'nvim {4}')",
    ]
    if args.filter:
        fzfArgs += ["--filter", args.filter]
    fzf = subprocess.Popen(
        fzfArgs,
        stdin=PIPE,
        stdout=PIPE,
        stderr=None,
    )
    fzfIn = fzf.stdin
    encoding = sys.getdefaultencoding()
    if fzfIn:
        if args.today:
            factory = Factory(environment)
            todayLog = (
                factory.getTodayLog(args.repository)
                if args.repository
                else factory.getTodayLog()
            )
            fzfIn.write(f"\t(today)\t{todayLog}\n".encode(encoding))
        for do in dos:
            fzfIn.write(do.encode(encoding))

        fzfIn.flush()
        fzfIn.close()
    else:
        raise Exception("Cannot open fzf stdin")
    fzf.wait()
    stdout = fzf.stdout
    if stdout:
        output = stdout.read().decode(encoding)
        match = re.search("^([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t(.*)$", output)
        file = None
        if match:
            file = match.group(5)
        else:
            match = re.search("\\(today\\)\t(.*)$", output)
            if match:
                file = match.group(1)
                if not os.path.isfile(file):
                    Path(file).touch()
        if file:
            if args.noedit:
                print(file)
                return False
            else:
                subprocess.call(["nvim", file], cwd=environment.directory)
            return True
        else:
            print(output)
    else:
        raise Exception("Cannot open fzf stdout")
    return False


# Add a do
def add(environment, repository, do):
    # MEM (Memento https://www.imdb.com/title/tt0209144/)
    task = Task(f"{do}", defaultContext="MEM", natural=True)
    contextFilter = ContextFilter(environment.myDo)

    now = datetime.now()
    if not repository and task.context:
        taskRepository = contextFilter.repository(task.context)
        if taskRepository:
            repository = taskRepository
    todayLog = Factory(environment).getTodayLog(repository, now)
    if not os.path.isfile(todayLog):
        Path(todayLog).touch()
    with open(todayLog, "r+") as file:
        file.seek(0)
        lines = file.readlines()
        length = len(lines)
        if length == 0:
            # Add date heading
            todayLong = now.strftime("%a %d %b %Y").upper()
            lines.append(f"# {todayLong}\n\n")
        elif length == 1:
            # Guard to make sure todos don't crash heading of manually created
            # file
            lines.append("\n")

        # Space between dos and next paragraph
        if len(lines) > 1 and not lines[2].startswith("-"):
            lines.insert(2, "\n")

        lines.insert(2, f"- [ ] {task}\n")
        file.seek(0)
        file.writelines(lines)
