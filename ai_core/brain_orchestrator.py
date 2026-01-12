import random

class MultiAgentOrchestrator:
    def run_simulation(self, data):
        """
        Runs 5 AI Agents based on User Input
        """
        # 1. Parse Input
        completion = int(data.get('completion', 0))
        marketing_ready = data.get('marketing', 'No')
        product_type = data.get('type', 'Mobile App')
        
        # --- 🧠 BRAIN 1: MARKET AGENT ---
        # Logic: Marketing Ready 'No' means low demand visibility
        market_score = random.randint(70, 90)
        if marketing_ready == 'No':
            market_score -= 25 # Penalty
        
        # --- 🧠 BRAIN 2: PRODUCT AGENT ---
        # Logic: Directly linked to feature completion
        product_score = completion
        if completion < 50: product_score -= 10 # Penalty for alpha stage

        # --- 🧠 BRAIN 3: RISK AGENT ---
        # Logic: Low completion = High Risk. No Marketing = Business Risk.
        risk_base = 90
        if completion < 80: risk_base -= 20
        if marketing_ready == 'No': risk_base -= 10
        risk_score = risk_base

        # --- 🧠 BRAIN 4: TIMING AGENT ---
        # Logic: Simulated Market Window
        timing_score = random.randint(65, 95)

        # --- 🧠 BRAIN 5: BUSINESS AGENT ---
        # Logic: Average of Market + Product
        business_score = int((market_score + product_score + risk_score) / 3)

        # --- 🏁 CONSENSUS (Average) ---
        avg_score = int((market_score + product_score + risk_score + timing_score + business_score) / 5)

        # Decision Logic
        decision = "DELAY LAUNCH"
        if avg_score >= 80: decision = "LAUNCH NOW"
        elif avg_score < 50: decision = "CANCEL PROJECT"

        # Generate Reasons
        reasons = []
        if marketing_ready == 'No': reasons.append("Marketing strategy is missing.")
        if completion < 100: reasons.append(f"Product is only {completion}% complete.")
        if risk_score < 60: reasons.append("High risk factors detected.")
        if not reasons: reasons.append("All systems go. Market conditions look good.")

        return {
            "scores": {
                "market": market_score,
                "product": product_score,
                "risk": risk_score,
                "timing": timing_score,
                "business": business_score
            },
            "avg": avg_score,
            "decision": decision,
            "reasons": reasons
        }