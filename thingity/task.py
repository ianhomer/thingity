#
# Parse a task line. See test cases for examples
#
import re
from . import HumanDate, HumanTime, TaskRenderer
from datetime import date

NON_CATEGORIES = [
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
    "MON",
    "TUE",
    "WED",
    "THU",
    "FRI",
    "SAT",
    "SUN",
    "TOD",
    "TOM",
]


def repositoryFromFile(file):
    match = re.search(".*things/([^/]*)/.*", file)
    if match:
        return match.group(1)


#
# When natural is true then line interpretted as entered by human.
#


class Task:
    def __init__(
        self,
        line,
        natural=False,
        # How many days are considered near
        nearDays=3,
        defaultContext=None,
        today: date = date.today(),
    ):
        self.dateInclude = False
        self.nearDays = nearDays
        self.defaultContext = defaultContext
        self.end = None
        self.line = line
        self.natural = natural
        self.timeInclude = False
        self.today = today
        self._parse()

    def _parse(self):
        match = re.search(
            # File part
            ("()" if self.natural else "^([^:]*):") +
            # Optional markdown part
            "(?:- \\[ \\] )?" +
            # Context part
            "((?:[A-Z]{3}(?=\\s))?)\\s*" +
            # Date part
            "((?:(?:[0-9]+"
            + (
                "|(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|"
                + "MON|TUE|WED|THU|FRI|SAT|SUN|TOD|TOM)(?:\\s[0-9]{1,2})?"
                if self.natural
                else ""
            )
            + ")(?=\\s)\\s)?)\\s*"
            +
            # Time part
            "((?:[0-9]{2}:?[0-9]{2}(?=\\s)\\s)?)\\s*" +
            # Subject part
            "(.*)$",
            # Pre-pepend MEM category if natural and starts with a non-category,
            # e.g. day of week
            (
                "MEM "
                if (
                    self.natural
                    and (
                        (self.line[0:3] in NON_CATEGORIES)
                        or re.search("^[0-9]{2}:?[0-9]{2}", self.line[0:5])
                    )
                )
                else ""
            )
            + self.line,
        )
        self.mission = False
        self.garage = False
        self.backlog = False
        self.question = False
        self.next = False
        self.toDate = None
        if match:
            self.file = match.group(1)
            self.repository = repositoryFromFile(self.file)
            self.context = match.group(2) or self.defaultContext
            self.dateIn = match.group(3) or None
            if self.dateIn is None:
                self.date = None
            else:
                self.date = HumanDate(self.dateIn, today=self.today)
                self.dateInclude = True
            self.timeAsNumbers = match.group(4) or None
            if self.timeAsNumbers is None:
                self.time = None
                self.timeInclude = False
            else:
                self.time = HumanTime(self.timeAsNumbers)
                self.timeInclude = self.time.include
                if self.date is None:
                    self.date = HumanDate(today=self.today)
                    self.dateInclude = True
            subject = match.group(5)

            first = subject[:1]
            if first == "~":
                self.mission = True
                self.subject = subject[1:].strip()
            elif first == "^":
                self.next = True
                self.subject = subject[1:].strip()
            elif first == ".":
                self.backlog = True
                self.subject = subject[1:].strip()
            elif first == "-":
                self.garage = True
                self.subject = subject[1:].strip()
            else:
                self.subject = subject

            last = subject[-1]
            if last == "?":
                self.question = True

            # Extra toDate part
            match = re.search("to ([0-9]{8}) (.*)", subject)
            if match:
                self.end = HumanDate(match.group(1), today=self.today)
                self.subject = match.group(2)
        else:
            self.file = None
            self.context = None
            self.date = None
            self.time = None
            self.subject = self.line
            self.repository = None

    def __str__(self):
        return self.code

    @property
    def code(self):
        parts = []
        if self.context:
            parts += [self.context]
        if self.date:
            parts += [self.date.code]
        if self.time and self.timeInclude:
            parts += [self.time.code]
        if self.end:
            parts += ["to", self.end.code]
        parts += [self.subject]
        return " ".join(parts)

    @property
    def display(self):
        return TaskRenderer().renderBody(self)

    @property
    def row(self):
        return TaskRenderer().render(self)

    @property
    def near(self):
        return self.date and self.date.daysAhead < self.nearDays

    @property
    def upcoming(self):
        return self.date and self.date.daysAhead < self.nearDays * 10

    @property
    def rankGroup(self):
        return (
            (1000 if self.near else 3000 if self.upcoming else 6000)
            if self.date is not None
            else (
                9000
                if self.mission
                else 8000
                if self.garage
                else 7000
                if self.backlog
                else 5000
                if self.question
                else 4000
                if not self.next
                else 2000
            )
        )

    @property
    def rank(self):
        return (
            str(self.rankGroup)
            + self.date.code
            + (self.time.code if self.time is not None else "0000")
            if self.date is not None
            else str(self.rankGroup)
        )

    @property
    def primaryType(self):
        if self.mission:
            return "mission"
        elif self.backlog:
            return "backlog"
        elif self.garage:
            return "garage"
        elif self.question:
            return "question"
        else:
            return "normal"
