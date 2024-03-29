from . import Environment, Search


# Ripgrep specific searching
class Rg(Search):
    def __init__(
        self, environment: Environment, match=None, justArchive=False, withArchive=False
    ):
        super(Rg, self).__init__(environment)
        self.environment = environment
        self.match = match
        self.globParts = self.createGlobParts(justArchive, withArchive)
        self.withPcre2 = False

    def createGlobParts(self, justArchive, withArchive):
        if justArchive:
            return ["--glob", "**/archive/**/*.md"]
        elif withArchive:
            return ["--glob", "**/*.md"]
        else:
            return ["--glob", "!archive/", "--glob", "**/*.md"]

    def createCommand(self):
        parts = (
            ["rg", "-i"]
            + self.globParts
            + [
                "--no-heading",
                "--follow",
                "--color",
                "never",
                "-n",
            ]
        )
        if self.withPcre2:
            parts += ["--pcre2"]
        if self.maxPerFile > 0:
            parts.extend(["-m", str(self.maxPerFile)])
        parts.append(self.matchPrefix + (self.match or ""))
        parts.append(".")
        return parts
