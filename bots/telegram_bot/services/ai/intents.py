class IntentResult:



    def __init__(
        self,
        intent: str,
        confidence: float,
        source: str = "keyword"
    ):

        self.intent = intent

        self.confidence = confidence

        self.source = source



    def to_dict(
        self
    ):

        return {

            "intent": self.intent,

            "confidence": self.confidence,

            "source": self.source

        }



    def __str__(
        self
    ):

        return self.intent



    def __repr__(
        self
    ):

        return (

            f"IntentResult("
            f"intent='{self.intent}', "
            f"confidence={self.confidence}, "
            f"source='{self.source}')"

        )



    def __eq__(
        self,
        other
    ):


        if isinstance(
            other,
            str
        ):

            return self.intent == other



        if isinstance(
            other,
            IntentResult
        ):

            return (

                self.intent == other.intent

                and

                self.source == other.source

            )



        return False



    def __hash__(
        self
    ):

        return hash(
            (
                self.intent,
                self.source
            )
        )



    def has_confidence(
        self,
        threshold=0.5
    ):

        return self.confidence >= threshold