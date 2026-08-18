class SmellDetector:

    def detect(self, analysis):

        smells = []

        for func in analysis.functions:

            if len(func.parameters) > 5:

                smells.append(
                    {
                        "type": "Long Parameter List",
                        "function": func.name,
                    }
                )

        return smells