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

    def parts(self, pattern, options):
        """
        Provide ag.py compatible interface for backward compatibility.
        Maps ag options to equivalent rg options.
        """
        # Map ag options to rg equivalents
        rg_options = []
        for option in options:
            if option == "--noheading":
                rg_options.append("--no-heading")
            elif option == "--nonumbers":
                pass  # rg doesn't show numbers by default in this mode
            elif option == "--nocolor":
                rg_options.extend(["--color", "never"])
            elif option == "--nobreak":
                pass  # rg doesn't add breaks by default
            elif option == "--follow":
                rg_options.append("--follow")
            else:
                # Pass through other options as-is
                rg_options.append(option)

        # Check if pattern contains regex features that require PCRE2
        if self._needs_pcre2(pattern):
            rg_options.append("--pcre2")

        return ["rg", "-i"] + self.globParts + rg_options + [pattern, self.environment.directory]

    def _needs_pcre2(self, pattern):
        """
        Check if pattern contains regex features that require PCRE2 support.
        """
        # Check for lookaround patterns that require PCRE2
        return any(lookaround in pattern for lookaround in ['(?!', '(?=', '(?<', '(?<='])
