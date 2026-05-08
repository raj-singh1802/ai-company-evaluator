def calculate_risk_factors(
    ai_result,
    mca_result
):

    factors = []

    score = ai_result["trust_score"]

    if mca_result.get("found"):
        factors.append(
            ("MCA Registration Found", "+15")
        )

    if ai_result["web_presence"] == "strong":
        factors.append(
            ("Strong Web Presence", "+20")
        )

    if ai_result["web_presence"] == "weak":
        factors.append(
            ("Weak Web Presence", "-20")
        )

    if ai_result["news_coverage"] == "positive":
        factors.append(
            ("Positive News Coverage", "+15")
        )

    if ai_result["news_coverage"] == "negative":
        factors.append(
            ("Negative News Coverage", "-25")
        )

    if ai_result["red_flags"]:
        factors.append(
            ("Detected Red Flags", "-15")
        )

    return factors

def generate_verdict(
    ai_result,
    mca_result,
    threshold=55
):
    """
    Generates final company verdict.
    LLM generates explanation dynamically.
    Python handles deterministic classification.
    """

    score = ai_result["trust_score"]

    # -----------------------------------
    # DETERMINE VERDICT LABEL
    # -----------------------------------

    if score >= 70:

        verdict = "GENUINE"

    elif score >= 40:

        verdict = "SUSPICIOUS"

    else:

        verdict = "NOT GENUINE"

    # -----------------------------------
    # USE LLM-GENERATED EXPLANATION
    # -----------------------------------

    explanation = ai_result.get(
        "verdict_explanation"
    )

    # Fallback if missing
    if not explanation:

        explanation = ai_result.get(
            "reason",
            "No explanation generated."
        )

    # -----------------------------------
    # OPTIONAL MCA NOTE
    # -----------------------------------

    mca_note = ""

    if mca_result.get("found"):

        mca_note = f"""

MCA Verification:
Matched company:
{mca_result['match']}
"""

    # -----------------------------------
    # FINAL RESPONSE
    # -----------------------------------

    return {
        "verdict": verdict,
        "reason": f"""
{explanation}

AI Confidence Score: {score}/100
{mca_note}
"""
    }