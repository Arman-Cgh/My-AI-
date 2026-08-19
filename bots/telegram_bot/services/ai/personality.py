class Personality:

    def __init__(
        self,
        profile: dict = None,
        memory=None,
        state: dict = None,
    ):

        self.profile = (
            profile
            if isinstance(profile, dict)
            else {}
        )

        self.memory = self.format_memory(
            memory
        )

        self.state = (
            state
            if isinstance(state, dict)
            else {}
        )

    def format_memory(self, memory):

        if isinstance(memory, dict):

            lines = [
                f"- {key}: {value}"
                for key, value in memory.items()
                if value is not None
            ]

            return "\n".join(lines)

        return str(
            memory or ""
        )

    def build(self):

        name = self.profile.get(
            "first_name",
            "",
        )

        if not name:

            name = self.extract_memory(
                "name"
            )

        job = self.extract_memory(
            "job"
        )

        interests = self.extract_memory(
            "interests"
        )

        text = f"""
╪┤╪«╪╡█î╪¬ AetherAI:

┘å╪º┘à ┌⌐╪º╪▒╪¿╪▒:
{name}


╪┤╪║┘ä ┌⌐╪º╪▒╪¿╪▒:
{job}


╪╣┘ä╪º█î┘é ╪¿╪▒:
{interests}


┘é┘ê╪º┘å█î┘å ╪▒┘ü╪¬╪º╪▒:

- ╪¬┘ê AetherAI ┘ç╪│╪¬█î╪î ╪»╪│╪¬█î╪º╪▒ ┘ç┘ê╪┤┘à┘å╪» ╪┤╪«╪╡█î ┌⌐╪º╪▒╪¿╪▒.
- ╪»┘ê╪│╪¬╪º┘å┘ç ┘ê ╪╖╪¿█î╪╣█î ╪╡╪¡╪¿╪¬ ┌⌐┘å.
- ╪º┌»╪▒ ┘å╪º┘à ┌⌐╪º╪▒╪¿╪▒ ╪▒╪º ┘à█îΓÇî╪»╪º┘å█î ┌»╪º┘ç█î ╪º╪│╪¬┘ü╪º╪»┘ç ┌⌐╪▒.
- ╪º╪╖┘ä╪º╪╣╪º╪¬ ╪¡╪º┘ü╪╕╪º╪▒╪º ╪▒╪º ╪»╪▒ ┘╛╪º╪│╪«ΓÇî┘ç╪º ╪º╪│╪¬┘ü╪º╪»┘ç ┌⌐╪▒.
- ╪«┘ê╪»╪¬ ╪▒╪º ┘à╪»┘ä ╪╣┘à┘ê┘à█î ┘ç┘ê╪┤ ┘à╪╡┘å┘ê╪╣█î ┘à╪╣╪▒╪▒┘ü█î ┘å┌⌐╪▒.
- ┘╛╪º╪│╪«ΓÇî┘ç╪º ╪▒╪º ┘ê╪º╪╢╪¡ ┘ê ┌⌐╪º╪▒╪¿╪▒╪»█î ╪¿╪»┘ç.
- ╪¿╪▒╪º█î ┘à╪│╪º╪ª┘ä ┘ü┘å█î ╪¬┘ê╪╢█î╪¡ ┘à╪▒╪¡┘ä┘çΓÇî╪º█î ╪¿╪»┘ç.
- ╪¿╪▒╪º█î ╪│┘ê╪º┘äΓÇî┘ç╪º█î ╪│╪º╪»┘ç ┌⌐┘ê╪¬╪º┘ç ╪¼┘ê╪º╪¿ ╪¿╪»┘ç.
"""

        return text.strip()

    def extract_memory(
        self,
        key,
    ):

        for line in self.memory.split("\n"):

            if key in line:

                return (
                    line
                    .replace("-", "")
                    .replace(
                        key + ":",
                        "",
                    )
                    .strip()
                )

        return ""