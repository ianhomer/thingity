#
# ContextFilter is a string that defines multiple filters
#
# (part0):(part):(part)
#
# Where
#
#   part0 = -A,-B => exclude A and B from contexts to be displayed by default
#   part = A>B,C>a-name
#     => context A should also include B and C
#     => context A should be written to repository called "a-name"
#
# For example the following context filter excludes A and B by default from
# show todos. Further context B implies C and D, so C and D are also excluded.
# Context E (along with the implied F and G) should should be written to the
# repository e-notes. Context P sould be written to the repository p-notes.
#
#   -A,-V:B>C,D:E>F,G>e-notes:P>>p-notes
#
#
# This string is a lightweight string that can be set in envrionment and drive
# defaults for the "do" command.
#
class ContextFilter:
    def __init__(self, value: str):
        self.value = value
        self.filterParts = self.value.split(":")
        self.localContexts = self.filterParts[0]

    def excludes(self):
        excludes = []
        for contextName in self.localContexts.split(","):
            if contextName.startswith("-"):
                excludes += self.family(contextName[1:])
        return excludes

    def children(self, contextName: str):
        return self.context(contextName).children

    def family(self, contextName: str):
        return [contextName.upper()] + self.children(contextName)

    def repository(self, contextName: str):
        return self.context(contextName).repository

    def pattern(self, contextName: str):
        return "(" + "|".join(self.family(contextName)) + ")"

    def context(self, contextName: str):
        filterPartMatcher = contextName.upper() + ">"
        for filterPart in self.filterParts:
            if filterPart.startswith(filterPartMatcher):
                return Context(filterPart)
        return Context()


class Context:
    def __init__(self, filterPart=None):
        if not filterPart:
            self.children = []
            self.repository = None
            return
        contextParts = filterPart.split(">")
        self.children = contextParts[1].split(",") if len(contextParts) > 1 else []
        self.repository = contextParts[2] if len(contextParts) > 2 else None
