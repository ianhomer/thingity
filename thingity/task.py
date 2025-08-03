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


def thingFromFile(file):
    match = re.search("([^/]+).md", file)
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
        """Parse the task line using semantic parsing steps."""
        # Initialize all task properties
        self._initialize_properties()

        # Preprocess the line for natural mode
        processed_line = self._preprocess_line()

        # Parse each component in sequence
        file_part, remaining = self._parse_file_part(processed_line)
        remaining = self._parse_markdown_prefix(remaining)
        context_part, remaining = self._parse_context_part(remaining)
        date_part, remaining = self._parse_date_part(remaining)
        time_part, remaining = self._parse_time_part(remaining)
        subject_part = remaining.strip()

        # Set parsed values
        self._set_file_properties(file_part)
        self._set_context(context_part)
        self._set_date(date_part)
        self._set_time(time_part)
        self._set_subject_and_modifiers(subject_part)

    def _initialize_properties(self):
        """Initialize all task properties to default values."""
        self.mission = False
        self.garage = False
        self.backlog = False
        self.question = False
        self.next = False
        self.toDate = None
        self.file = None
        self.repository = None
        self.thing = None
        self.context = self.defaultContext
        self.date = None
        self.time = None
        self.subject = self.line
        self.dateIn = None
        self.timeAsNumbers = None

    def _preprocess_line(self):
        """Preprocess line for natural mode, adding MEM prefix if needed."""
        if not self.natural:
            return self.line

        # Check if line starts with non-category or time
        starts_with_non_category = self.line[:3] in NON_CATEGORIES
        starts_with_time = re.match(r"^[0-9]{2}:?[0-9]{2}", self.line)

        if starts_with_non_category or starts_with_time:
            return f"MEM {self.line}"
        return self.line

    def _parse_file_part(self, line):
        """Parse the file part from the beginning of the line."""
        if self.natural:
            return None, line

        match = re.match(r"^([^:]*?):", line)
        if match:
            return match.group(1), line[match.end():]
        return None, line

    def _parse_markdown_prefix(self, line):
        """Remove optional markdown checkbox prefix."""
        match = re.match(r"^- \[ \] ", line)
        if match:
            return line[match.end():]
        return line

    def _parse_context_part(self, line):
        """Parse the context (3-letter code) from the line."""
        match = re.match(r"^([A-Z]{3})(?=\s)", line)
        if match:
            return match.group(1), line[match.end():].lstrip()
        return None, line

    def _parse_date_part(self, line):
        """Parse date information from the line."""
        # Check if this looks like a time first to avoid consuming part of time as date
        time_lookahead = re.match(r"^[0-9]{2}:[0-9]{2}", line)
        if time_lookahead:
            return None, line

        # Numeric dates (various formats) - but not single/double digits that could be times
        match = re.match(r"^([0-9]{4,})", line)  # At least 4 digits for proper dates
        if match:
            return match.group(1), line[match.end():].lstrip()

        # Also handle specific shorter date formats that are clearly dates
        match = re.match(r"^([0-9]{1,2})(?=\s|$)", line)
        if match and not re.match(r"^[0-9]{2}:[0-9]{2}", line):
            # Only if not followed by colon (time pattern)
            return match.group(1), line[match.end():].lstrip()

        # Natural language dates (only in natural mode)
        if self.natural:
            date_patterns = [
                r"^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(?:\s+([0-9]{1,2}))?",
                r"^(MON|TUE|WED|THU|FRI|SAT|SUN)",
                r"^(TOD|TOM)"
            ]

            for pattern in date_patterns:
                match = re.match(pattern, line)
                if match:
                    date_str = match.group(0)
                    return date_str, line[match.end():].lstrip()

        return None, line

    def _parse_time_part(self, line):
        """Parse time information from the line."""
        match = re.match(r"^([0-9]{2}:?[0-9]{2})(?=\s|$)", line)
        if match:
            return match.group(1), line[match.end():].lstrip()
        return None, line

    def _set_file_properties(self, file_part):
        """Set file-related properties."""
        if file_part:
            self.file = file_part
            self.repository = repositoryFromFile(file_part)
            self.thing = thingFromFile(file_part)

    def _set_context(self, context_part):
        """Set the context property."""
        if context_part:
            # Validate context is exactly 3 uppercase letters
            if len(context_part) == 3 and context_part.isalpha():
                self.context = context_part.upper()
            else:
                # Invalid context, keep default
                pass
        # Keep default context if no context parsed

    def _set_date(self, date_part):
        """Set date-related properties."""
        if date_part:
            try:
                self.dateIn = date_part
                self.date = HumanDate(date_part, today=self.today)
                self.dateInclude = True
            except Exception:
                # Invalid date format, skip date setting
                pass

    def _set_time(self, time_part):
        """Set time-related properties."""
        if time_part:
            try:
                self.timeAsNumbers = time_part
                self.time = HumanTime(time_part)
                self.timeInclude = self.time.include
                # If time is set but no date, default to today
                if self.date is None:
                    self.date = HumanDate(today=self.today)
                    self.dateInclude = True
            except Exception:
                # Invalid time format, skip time setting
                pass

    def _set_subject_and_modifiers(self, subject_part):
        """Parse subject and set task type modifiers."""
        if not subject_part:
            self.subject = ""
            return

        # Check for task type prefixes
        first_char = subject_part[:1]
        if first_char == "~":
            self.mission = True
            subject_part = subject_part[1:].strip()
        elif first_char == "^":
            self.next = True
            subject_part = subject_part[1:].strip()
        elif first_char == ".":
            self.backlog = True
            subject_part = subject_part[1:].strip()
        elif first_char == "-":
            self.garage = True
            subject_part = subject_part[1:].strip()

        # Check for question suffix
        if subject_part.endswith("?"):
            self.question = True

        # Check for "to date" pattern
        to_match = re.search(r"to ([0-9]{8}) (.*)", subject_part)
        if to_match:
            self.end = HumanDate(to_match.group(1), today=self.today)
            subject_part = to_match.group(2)

        self.subject = subject_part

    def __str__(self):
        return self.code

    @property
    def code(self):
        parts = []
        if self.context:
            parts += [self.context]
        if self.next:
            parts += "^"
        elif self.mission:
            parts += "~"
        elif self.backlog:
            parts += "."
        elif self.garage:
            parts += "-"
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
        return self.date and not self.near and self.date.daysAhead < self.nearDays * 10

    @property
    def future(self):
        return self.date and not (self.upcoming or self.near)

    @property
    def inbox(self):
        return not self.date and not (
            self.mission
            or self.garage
            or self.backlog
            or self.question
            or self.next
            or self.awaits
        )

    @property
    def awaits(self):
        return re.match("{[A-Z]{3}}", self.subject)

    @property
    def rankGroup(self):
        return (
            (1000 if self.near else 3000 if self.upcoming else 6000)
            if self.date is not None
            else (
                9000
                if self.mission
                else (
                    8000
                    if self.garage
                    else (
                        7000
                        if self.backlog
                        else 5000 if self.question else 4000 if not self.next else 2000
                    )
                )
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

    def __lt__(self, obj):
        return self.rank < obj.rank
