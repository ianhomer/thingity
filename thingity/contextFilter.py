#
# ContextFilter is a string that defines multiple filters
#
# (part0):(part):(part)
#
# Where
#
#   part0 = -A,-B => exclude A and B as default context
#   part = A>B,C => context A should also include B and C
#
# For example
#   -A1,-A2:B>C,D:E>F,G
#
# This string is a lightweight string that can be set in envrionment and drive
# defaults for the "do" command.
#
class ContextFilter:
    def __init__(self, value: str):
        self.value = value
        self.parts = self.value.split(":")
        self.localPart = self.parts[0]

    def excludes(self):
        excludes = []
        for category in self.localPart.split(","):
            if category.startswith("-"):
                excludes += self.family(category[1:])
        return excludes

    def children(self, parent: str):
        context = self.context(parent)
        return context.children if context else []

    def family(self, parent: str):
        return [parent.upper()] + self.children(parent)

    # def repository(self, parent: str):
    #     context = self.context(parent)
    #     return context.repository if context else None

    def pattern(self, pattern: str):
        return "(" + "|".join(self.family(pattern)) + ")"

    def context(self, parent: str):
        matcher = parent.upper() + ">"
        for part in self.parts:
            if part.startswith(matcher):
                return Context(part)
        return None


class Context:
    def __init__(self, part):
        parts = part.split(">")
        self.children = parts[1].split(",") if len(parts) > 0 else [""]
