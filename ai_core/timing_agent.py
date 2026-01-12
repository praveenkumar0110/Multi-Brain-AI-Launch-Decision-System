import random

class TimingBrain:
    def __init__(self):
        self.name = "Market Timing Agent"

    def analyze(self, planned_date):
        # Simulating external market window analysis
        # In a real ML model, this would check stock markets/trends
        window_score = random.randint(60, 95)
        
        return {
            "agent": self.name,
            "score": window_score,
            "feedback": "Good launch window."
        }