#!/usr/bin/env python3

#
# Search things returning a stream of rows with 3 ":" separated parts ;
#
# 1) Sortable key, e.g. timestamp
# 2) Filename, i.e. where the match exists
# 3) Display string, i.e. what should be displayed in fzf
#

import argparse
from .. import Rg, Environment


def run():
    parser = argparse.ArgumentParser(description="things")
    parser.add_argument("thing", nargs="*", help="thing")
    parser.add_argument("--witharchive", action="store_true")
    parser.add_argument("--justarchive", action="store_true")
    parser.add_argument("-n", "--name", help="search name", default="default")
    parser.add_argument("--nofilter", action="store_true")
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--noconfig", help="ignore config files", action="store_true")
    args = parser.parse_args()

    search(args)


def search(args):
    match = " ".join(args.thing)
    environment = Environment.withConfig(not args.noconfig)

    if args.name == "default":
        search = Rg(environment, match, args.justarchive, args.witharchive)
        search.maxPerFile = 1
        search.postFilter = "s/^/0:/"
    elif args.name == "test":
        search = Rg(environment, match, False, True)
        search.maxPerFile = 1
        search.postFilter = None
    elif args.name == "sort-modified":
        search = Rg(environment, match, args.justarchive, args.witharchive)
        search.withModifiedKey = True
        search.sort = True
        search.maxPerFile = 1
        search.postFilter = (
            "s/:\\([^/]*\\)\\(.*\\/\\)"
            + "\\([^/]*\\).md:\\([0-9]*\\):\\(.*\\)/:\\1\\2\\3.md:\\4:"
            + "\\5 \033[95m(\\3)\033[2;90m (\\1)\033[0m/"
        )
    elif args.name == "bookmarks":
        search = Rg(environment)
        search.withModifiedKey = True
        search.withPcre2 = True
        matchPattern = "(?=.*" + match + ")" if match else ""
        matchPattern += "(?!.*#reject)"
        search.matchPrefix = f"^{matchPattern}(?=\\[[0-9A-Za-z\\s\\.\\-]+\\]:).*"
    elif args.name == "links":
        search = Rg(environment)
        search.withModifiedKey = True
        search.withPcre2 = True
        search.matchPrefix = "^.*<[0-9A-Za-z\\s\\:\\/\\.\\-]+>.*"
    elif args.name == "tags":
        search = Rg(environment, "", args.justarchive, args.witharchive)
        if match:
            search.matchPrefix = "#" + match
        else:
            search.matchPrefix = "(^|\\s)#[A-Za-z]+"
        search.withModifiedKey = True
        search.postFilter = (
            "s/\\(#[A-Za-z\\-]*\\)/\033[95m\\1\033[0m/g"
        )
    elif args.name == "headings":
        search = Rg(environment, match, args.justarchive, args.witharchive)
        search.matchPrefix = "^#+ .*"
        search.postFilter = (
            "s/\\([^/:]*\\).md:\\([0-9]*\\):#\\(#*\\) \\(.*\\)/\\1.md:\\2:"
            + "\033[30m\\3\033[0m\\4 \033[95m(\\1)\033[0m/"
        )
        search.withModifiedKey = True
        search.sort = True
    else:
        raise Exception(f"Search {args.name} not recognised")

    if args.nofilter:
        search.filter = None
    # search.maxPerFile = 1
    search.run(args)
