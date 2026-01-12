import random

class MarketBrain:
    def __init__(self):
        self.name = "Market Intelligence Agent"

    def analyze(self, target_audience, marketing_status):
        """
        Analyzes market fit based on audience type and marketing readiness.
        """
        score = 70  # Base Score
        
        # Rule 1: Audience Impact
        if 'student' in target_audience.lower():
            score += 15  # High viral potential
        elif 'enterprise' in target_audience.lower():
            score += 10  # High value
        else:
            score += 5

        # Rule 2: Marketing Strategy
        if marketing_status == 'No':
            score -= 30  # Critical Failure factor
        else:
            score += 10

        # Normalizing score 0-100
        final_score = max(0, min(100, score))
        
        return {
            "agent": self.name,
            "score": final_score,
            "feedback": "Demand is high." if final_score > 75 else "Marketing push needed."
        }