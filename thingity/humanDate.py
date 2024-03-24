#
# Convert a date in numbers, e.g. 202210602, to a human date relative to today
#

import datetime
import re
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# Given date as numbers, e.g. 20210531, output a nice human date from a todo
# point of view. Display is None if date is "days" days into the future.
class HumanDate:
    def __init__(self, input=None, today: date = date.today()):
        self.today = today
        self.daysAhead = 0
        self.withDays = True
        if input is None:
            self.date = today
            self.daysAhead = 0
            self.valid = True
        else:
            self.input = input.strip()
            try:
                self._parse()
                self.valid = True
            except ValueError as error:
                self.valid = False
                self.display = "---"
                print(f"Date {input} is not valid : {error}")

    def _parse(self):
        if self.input == "TOD":
            self.date = self.today
        elif self.input == "TOM":
            self.date = self.today + timedelta(days=1)
        elif match := re.search("^([0-9])$", self.input):
            self.date = self._parseRelativeDay(int(match.group(1)))
        elif match := re.search("^([A-Z]{3}\\s[0-9]+)$", self.input):
            self.date = self._parseDate(match.group(1))
        elif match := re.search("^([A-Z]{3})$", self.input):
            part = match.group(1)
            if self._isDay(part):
                self.date = self._parseDay(part)
            else:
                self.date = self._parseMonth(part)
                self.withDays = False
        elif match := re.search("^([0-9]{4})([0-9]{2})$", self.input):
            self.date = date(int(match.group(1)), int(match.group(2)), 1)
            self.withDays = False
        elif match := re.search("([0-9]{4})([0-9]{2})([0-9]{2})", self.input):
            self.date = date(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3) or 1),
            )
        else:
            self.date = self.today

        self.daysAhead = (self.date - self.today).days
        if self.daysAhead < 0:
            self.display = "***"
        elif self.daysAhead <= 7:
            self.display = self.date.strftime("%a").upper() + (
                "+" if self.daysAhead == 7 else ""
            )
        elif self.daysAhead < 180:
            if self.withDays:
                self.display = self.date.strftime("%d %b").upper()
            else:
                self.display = self.date.strftime("%b").upper()
        else:
            self.display = self.date.strftime("%d %b %Y").upper()

    def _parseRelativeDay(self, day):
        return self.today + datetime.timedelta(days=day - 1)

    def _isDay(self, part):
        return part in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    # Parse a day of the week like MON or TUE to a date based on what today is
    def _parseDay(self, day):
        for i in range(1, 8):
            candidate = self.today + timedelta(days=i)
            if candidate.strftime("%a").upper() == day:
                return candidate
        raise (Exception(f"Cannot find day {day}"))

    def _parseMonth(self, month):
        for i in range(1, 12):
            candidate = self.today + relativedelta(month=i)
            if candidate.strftime("%b").upper() == month:
                return candidate
        raise (Exception(f"Cannot find month {month}"))

    # Parse a date like JUN 8 by scanning forward for a year
    def _parseDate(self, date: str):
        needle = date.upper()
        for i in range(0, 365):
            candidate = self.today + timedelta(days=i)
            if candidate.strftime("%b %-d").upper() == needle:
                return candidate
            if candidate.strftime("%b %d").upper() == needle:
                return candidate
        raise (Exception(f"Cannot find date {date}"))

    @property
    def code(self):
        return (
            self.date.strftime("%Y%m%d" if self.withDays else "%Y%m")
            if self.valid
            else "00000000"
        )

    def __str__(self):
        return self.display
