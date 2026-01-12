import random

class MultiAgentOrchestrator:
    def run_simulation(self, data):
        """
        ADVANCED AI LOGIC:
        Now analyzes Text Length, Keywords, and strict Completion rules.
        """
        # 1. Parse Input
        name = data.get('name', '')
        users = data.get('users', '')
        product_type = data.get('type', 'Mobile App')
        completion = int(data.get('completion', 0))
        marketing_ready = data.get('marketing', 'No')
        
        # --- 🧠 BRAIN 1: MARKET AGENT (Analyzes Text & Demand) ---
        market_score = 60 # Base Score
        
        # Rule: specific target audience is better than "everyone"
        if len(users) > 5 and "everyone" not in users.lower():
            market_score += 15
        elif "everyone" in users.lower():
            market_score -= 10 # Penalty for vague targeting
            
        # Rule: Marketing is crucial
        if marketing_ready == 'Yes':
            market_score += 20
        else:
            market_score -= 25 # Huge Penalty if no marketing
            
        # Cap score 0-100
        market_score = max(10, min(99, market_score))

        
        # --- 🧠 BRAIN 2: PRODUCT AGENT (Analyzes Readiness) ---
        product_score = completion # Base is percentage
        
        # Rule: Name quality check
        if len(name) < 3: 
            product_score -= 10 # Penalty for dummy names like "a", "xy"
            
        # Rule: Complexity Bonus
        if product_type == 'Hardware':
            product_score -= 5 # Hardware is harder to perfect
            
        product_score = max(10, min(99, product_score))


        # --- 🧠 BRAIN 3: RISK AGENT (Safety Check) ---
        # Inverse Logic: Low Completion = High Risk (Low Score)
        risk_score = completion 
        
        if marketing_ready == 'No':
            risk_score -= 20 # Business Risk
            
        if completion < 50:
            risk_score -= 30 # Crash Risk
            
        risk_score = max(10, min(95, risk_score))


        # --- 🧠 BRAIN 4: TIMING AGENT (Market Window) ---
        # Simulated External Market Factors
        timing_score = random.randint(60, 90)
        
        # If product is delayed (low completion), timing gets worse
        if completion < 60:
            timing_score -= 15


        # --- 🧠 BRAIN 5: BUSINESS AGENT (ROI) ---
        # Business depends on Market + Product
        business_score = int((market_score + product_score + risk_score) / 3)


        # --- 🏁 FINAL CONSENSUS ---
        avg_score = int((market_score + product_score + risk_score + timing_score + business_score) / 5)

        # Decision Logic
        decision = "DELAY LAUNCH"
        if avg_score >= 80: 
            decision = "LAUNCH NOW"
        elif avg_score < 50: 
            decision = "CANCEL / REWORK"

        # Explainable AI Reasons (Why did I get this score?)
        reasons = []
        
        if len(name) < 4:
            reasons.append("Product name looks invalid or too short.")
        if "everyone" in users.lower() or len(users) < 4:
            reasons.append("Target audience is too vague (Low Market Score).")
        if marketing_ready == 'No':
            reasons.append("Missing marketing strategy is a critical failure point.")
        if completion < 70:
            reasons.append(f"Feature completion ({completion}%) is too low for stability.")
        
        if not reasons:
            reasons.append("Strong alignment across all AI parameters.")
            reasons.append("Market conditions and product readiness are optimal.")

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