#!/usr/bin/env python3

import argparse
import os
import subprocess
import re
import shutil
from typing import Optional
from subprocess import PIPE
from .. import Environment, RepositoryFile, thingity


def run():
    parser = argparse.ArgumentParser(description="things")
    parser.add_argument("thing", nargs="*", help="thing")
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--lint", action="store_true")
    parser.add_argument("-m", "--my", help="just sync my things", action="store_true")
    parser.add_argument("-n", "--name", help="find things with named search")
    parser.add_argument("-o", "--open", help="open my things", action="store_true")
    parser.add_argument("-r", "--recent", help="recent things", action="store_true")
    parser.add_argument("-s", "--search", help="find things", action="store_true")
    parser.add_argument("--synk", help="sync things", action="store_true")

    # General settings
    parser.add_argument("--noconfig", help="ignore config files", action="store_true")
    parser.add_argument("--filter", help="filter")
    parser.add_argument("--test", help="test mode")
    parser.add_argument("--noedit", help="don't edit file", action="store_true")

    parser.add_argument("--info", action="store_true")
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--justarchive", action="store_true")
    parser.add_argument("--witharchive", action="store_true")

    args = parser.parse_args()

    if args.test:
        args.filter = args.test
        args.noconfig = True
        args.noedit = True

    environment = Environment.withConfig(not args.noconfig)

    if args.info:
        print(f"Things directory : {environment.directory}")
        print(f"My notes : {environment.myNotes}")
        print(f"My notes directory : {environment.myNotesDir}")
        return

    if (not args.filter) and thingity.synk(args.synk, args.my):
        return

    if args.open:
        return open(environment)

    if args.lint:
        return thingity.lint(fix=args.fix)

    more = True
    while more:
        if args.recent:
            more = recent(environment, args)
        else:
            more = search(environment, args)


def open(environment: Environment):
    subprocess.run(["nvim"], cwd=environment.directory)


class Fzf:
    # Command Fzf command
    # Stream into fzf has three ":" separated parts
    # 1) sort key
    # 2) filename
    # 3) line number in file for preview
    # 4) display string
    def __init__(
        self,
        environment: Environment,
        thingsSearchArgs: Optional[str] = None,
        filter: Optional[str] = None,
        noedit: bool = False,
        dry: bool = False,
    ):
        self.environment = environment
        self.noedit = noedit
        self.dry = dry
        self.filter = filter
        self.cmd = [
            "fzf",
            "--multi",
            "--height",
            "100%",
            "--ansi",
            "--no-sort",
            "--color",
            "dark",
        ]
        if not self.dry:
            self.cmd += ["-d", ":", "--with-nth", "4.."]
        if filter:
            if self.dry:
                self.cmd += ["--filter", "."]
            else:
                self.cmd += ["--filter", filter]
        else:
            terminal = shutil.get_terminal_size((80, 24))
            if terminal.columns > 60 or terminal.lines > 10:
                if terminal.columns > 100:
                    width = (
                        120 if terminal.columns > 150 else int(terminal.columns * 0.6)
                    )
                    self.cmd += [
                        "--preview-window",
                        f"right,{width}",
                    ]
                else:
                    width = terminal.columns
                    height = "5" if terminal.lines < 20 else "50%"
                    self.cmd += [
                        "--preview-window",
                        f"bottom,{height}",
                    ]
                self.cmd += [
                    "--preview",
                    "cat "
                    + environment.subshellOpen
                    + "echo {} | cut -d: -f2) | cut -c 1-"
                    + str(width - 2)
                    + " | "
                    + "bat --style=header --color=always "
                    + "--file-name "
                    + environment.subshellOpen
                    + "echo {} | cut -d: -f2) "
                    + "-l md "
                    + "-r "
                    + environment.subshellOpen
                    + "echo {} | cut -d: -f3): ",
                ]
        self.parts = []
        self.defaultCommand = "true"
        self.filenameMatcher = "^[^:]*:([^:]*)"
        search = (
            "things-search " + thingsSearchArgs if thingsSearchArgs else "things-search"
        )
        self.binds = [
            "ctrl-f:reload("
            + "fd --changed-within 3months md --exec stat -f '%m:%N:1:%N' {q} "
            + "| sort -r)",
            "ctrl-t:reload(" + search + "-n tags --witharchive {q} || true)",
            "ctrl-e:reload(" + search + "-n sort-modified --witharchive {q} || true)",
            "ctrl-b:reload(" + search + "-n bookmarks --witharchive {q} || true)",
            "ctrl-g:reload(" + search + "-n links --witharchive {q} || true)",
            "ctrl-s:reload(" + search + "-n headings --witharchive {q} || true)",
            # Note that ctrl-x aborts so that a subsequence ctrl-x in fish shell
            # opens cheats. Similarly for ctrl-w opening todos.
            "ctrl-w:abort",
            "ctrl-x:abort",
            "ctrl-space:abort",
        ]

    def run(self):
        cmd = self.cmd + self.parts
        if len(self.binds) > 0:
            cmd += ["--bind", ",".join(self.binds)]
        if self.dry:
            print(cmd)
        process = subprocess.run(
            cmd,
            stdout=PIPE,
            text=True,
            stderr=None,
            env={**os.environ, "FZF_DEFAULT_COMMAND": self.defaultCommand},
            cwd=self.environment.directory,
        )
        if self.dry:
            print(process.stdout)
            return
        lines = process.stdout.splitlines()
        if self.filter:
            print(lines)
            return False
        selected = []
        for line in lines:
            match = re.search(self.filenameMatcher, line)
            if match:
                selected.append(match.group(1))

        if len(selected) > 0:
            repositoryFile = RepositoryFile(self.environment.directory, selected[0])
            if self.noedit:
                print(repositoryFile.path)
                return False
            else:
                subprocess.call(
                    ["nvim"] + [repositoryFile.path], cwd=repositoryFile.root
                )
            return True
        return False


def recent(environment: Environment, args):
    fzf = Fzf(environment, filter=args.filter)
    period = args.thing[0] if args.thing else "1week"
    fzf.defaultCommand = (
        f"fd --changed-within {period} md " + "--exec stat -f '%m:%N:1:%N' {} | sort -r"
    )
    return fzf.run()


def search(environment: Environment, args):
    thingsSearchArgs = (
        ""
        + ("--witharchive " if args.witharchive else "")
        + ("--justarchive " if args.justarchive else "")
        + ("--noconfig " if args.noconfig else "")
        + ("--dry " if args.dry else "")
    )
    fzf = Fzf(
        environment,
        thingsSearchArgs,
        filter=args.filter,
        noedit=args.noedit,
        dry=args.dry,
    )

    if args.name:
        searchPrefix = f"things-search {thingsSearchArgs}-n {args.name}"
    else:
        searchPrefix = f"things-search {thingsSearchArgs}-n headings"
    if args.thing and len(args.thing) > 0:
        pattern = " ".join(args.thing)
        fzf.defaultCommand = f"{searchPrefix} '{pattern}' || true"
    else:
        fzf.defaultCommand = f"{searchPrefix} || true"

    return fzf.run()
