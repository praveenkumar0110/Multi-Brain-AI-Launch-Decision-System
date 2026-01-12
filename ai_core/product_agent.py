class ProductBrain:
    def __init__(self):
        self.name = "Product Quality Agent"

    def analyze(self, completion_percentage):
        """
        Evaluates product readiness based on completion %.
        """
        comp = int(completion_percentage)
        score = comp  # Direct correlation
        
        # Penalties
        if comp < 50:
            score -= 10  # Alpha stage penalty
        elif comp > 90:
            score += 5   # Polish bonus

        final_score = max(0, min(100, score))

        return {
            "agent": self.name,
            "score": final_score,
            "feedback": "Product stable." if final_score > 80 else "Critical features missing."
        }