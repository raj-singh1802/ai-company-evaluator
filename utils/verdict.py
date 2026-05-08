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

def generate_verdict(ai_result, mca_result, threshold=55):
    """
    Generates final company verdict.
    Score ranges:
      0–40  → NOT GENUINE
      40–70 → SUSPICIOUS
      70+   → GENUINE
    MCA only upgrades verdict, not overrides score range.
    """

    score = ai_result["trust_score"]
    web_presence = ai_result["web_presence"]
    news_coverage = ai_result["news_coverage"]
    red_flags = ai_result["red_flags"]
    mca_found = mca_result.get("found", False)

    # -----------------------------------
    # GENUINE (score 70–100)
    # MCA confirmation is a bonus, not required
    # -----------------------------------

    if score >= 70:
        mca_note = f"\nAlso confirmed in MCA database: {mca_result['match']}" if mca_found else ""
        return {
            "verdict": "GENUINE",
            "reason": f"""
The company shows a strong online presence,
credible digital footprint,
and positive trust indicators.{mca_note}

AI Confidence Score: {score}/100
"""
        }

    # -----------------------------------
    # SUSPICIOUS (score 40–69)
    # MCA found = still suspicious but noted
    # -----------------------------------

    if score >= 40:

        reasons = []

        if web_presence == "weak":
            reasons.append("limited online presence")

        if news_coverage != "positive":
            reasons.append("low media/news visibility")

        if red_flags:
            reasons.append("some cautionary trust signals")

        reason_text = (
            "- " + "\n- ".join(reasons)
            if reasons
            else "- insufficient public trust indicators"
        )

        mca_note = (
            f"\nFound in MCA database: {mca_result['match']} — but low AI trust score keeps verdict as SUSPICIOUS."
            if mca_found
            else "\nNot found in MCA database."
        )

        return {
            "verdict": "SUSPICIOUS",
            "reason": f"""
The company appears operational but raises caution.{mca_note}

Reasons:
{reason_text}

AI Confidence Score: {score}/100
"""
        }

    # -----------------------------------
    # NOT GENUINE (score 0–39)
    # Even if MCA found, score is too low
    # -----------------------------------

    mca_note = (
        f"\nFound in MCA database: {mca_result['match']} — but AI trust score is critically low."
        if mca_found
        else "\nNot found in MCA database."
    )

    return {
        "verdict": "NOT GENUINE",
        "reason": f"""
The company has:
- critically low trust indicators
- weak or missing online credibility{mca_note}

This significantly increases the likelihood
of the company being unreliable or non-genuine.

AI Confidence Score: {score}/100
"""
    }