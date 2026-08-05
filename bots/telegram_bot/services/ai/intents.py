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



    def to_dict(self):

        return {

            "intent": self.intent,

            "confidence": self.confidence,

            "source": self.source

        }



    def __str__(self):

        return self.intent



    def __eq__(self, other):

        if isinstance(other, str):

            return self.intent == other

        return False