class RiskBrain:
    def __init__(self):
        self.name = "Risk Assessment Agent"

    def analyze(self, completion, market_ready):
        """
        Calculates safety score. High Score = Low Risk.
        """
        base_safety = 50
        
        # If product is incomplete, Risk is HIGH (Safety Low)
        if int(completion) < 70:
            base_safety -= 20
        else:
            base_safety += 30
            
        # If no marketing, Business Risk is HIGH
        if market_ready == 'No':
            base_safety -= 15
            
        final_score = max(0, min(100, base_safety))

        return {
            "agent": self.name,
            "score": final_score,
            "feedback": "Low Risk." if final_score > 70 else "High Risk detected!"
        }