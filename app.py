import streamlit as st
import pandas as pd
from evaluator import evaluate_company
import json
from utils.verdict import calculate_risk_factors


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Company Evaluator",
    page_icon="🔍",
    layout="wide"
)


# -----------------------------------
# LOAD MCA DATA
# -----------------------------------

@st.cache_data
def load_mca_data():

    df = pd.read_csv(
        "data/mca_companies_small.csv",
        encoding="latin-1",
        low_memory=False
    )

    # Clean column names
    df.columns = (
        df.columns
          .str.strip()
    )
    return df


mca_df = load_mca_data()


# -----------------------------------
# TITLE
# -----------------------------------

st.title("🔍 AI Company Evaluator")

st.markdown("""
AI-powered company verification system using:

- 🌐 Web Search
- 🤖 Groq LLM Analysis
- 🏢 MCA Verification
""")


# -----------------------------------
# SETTINGS
# -----------------------------------

threshold = 55


# -----------------------------------
# INPUT SECTION
# -----------------------------------

company_name = st.text_input(
    "Enter Company or Startup Name"
)


# -----------------------------------
# BUTTON
# -----------------------------------

if st.button("Evaluate Company"):

    if not company_name:
        st.error("Please enter a company name.")
        st.stop()

    # Loading Spinner
    with st.spinner("Analyzing company..."):

        result = evaluate_company(
            company_name,
            mca_df,
            threshold
        )

    # -----------------------------------
    # EXTRACT RESULTS
    # -----------------------------------

    ai_result = result["ai_result"]
    verdict = result["final_verdict"]
    mca_result = result["mca_result"]

    st.divider()

    # -----------------------------------
    # TOP METRICS
    # -----------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Trust Score",
            f"{ai_result['trust_score']}/100"
        )

    with col2:
        st.metric(
            "Web Presence",
            ai_result["web_presence"].title()
        )

    with col3:
        st.metric(
            "News Coverage",
            ai_result["news_coverage"].title()
        )

    # -----------------------------------
    # CONFIDENCE BAR
    # -----------------------------------

    st.subheader("📈 AI Confidence Level")

    score = ai_result["trust_score"]

    st.progress(score / 100)
    st.caption(f"AI Trust Confidence: {score}%")

    # -----------------------------------
    # VERDICT
    # -----------------------------------

    st.subheader("📌 Final Verdict")

    verdict_text = verdict["verdict"]

    if verdict_text == "GENUINE":
        st.success(f"✅ {verdict_text}")

    elif verdict_text == "SUSPICIOUS":
        st.warning(f"⚠️ {verdict_text}")

    else:
        st.error(f"❌ {verdict_text}")

    st.write(verdict["reason"])

    # -----------------------------------
    # RED FLAGS
    # -----------------------------------

    st.subheader("🚩 Risk Signals & Red Flags")

    red_flags = ai_result.get("red_flags", [])

    # Remove empty/null values
    red_flags = [
        flag.strip()
        for flag in red_flags
        if str(flag).strip()
    ]

    if len(red_flags) > 0:

        st.warning(
            f"{len(red_flags)} potential risk signal(s) detected."
        )

        for idx, flag in enumerate(red_flags, start=1):

            st.markdown(
                f"""
                - **Risk {idx}:**
                  {flag}
                """
            )

    else:
        st.success(
            """
            No major red flags were detected from:
            - web presence
            - public reputation
            - news visibility
            - online trust indicators
            """
        )
    
    # -----------------------------------
    # RISK FACTOR BREAKDOWN
    # -----------------------------------

    st.subheader("⚖️ Risk Factor Breakdown")

    risk_factors = calculate_risk_factors(
        ai_result,
        mca_result
    )

    for factor, impact in risk_factors:

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(factor)

        with col2:

            if "+" in impact:
                st.success(impact)
            else:
                st.error(impact)

    # -----------------------------------
    # DETAILED AI ANALYSIS
    # -----------------------------------

    with st.expander("🧠 View Detailed AI Analysis"):

        st.json(ai_result)

    st.subheader("🚩 Red Flags")

    red_flags = ai_result["red_flags"]

    if red_flags:
        for flag in red_flags:
            st.warning(flag)
    else:
        st.success("No major red flags detected.")

    # -----------------------------------
    # MCA VERIFICATION
    # -----------------------------------

    # MCA VERIFICATION
    st.subheader("🏢 MCA Verification")

    if mca_result.get("found"):
        match_type = mca_result.get("match_type", "")

        if match_type == "exact":
            st.success(f"""
                ✅ 100% Exact Match Found

                Matched Company: {mca_result['match']}
                Similarity: {mca_result['similarity']}%
            """)
        elif match_type == "strong":
            st.success(f"""
                🔵 Strong Match Found

                Matched Company: {mca_result['match']}
                Similarity: {mca_result['similarity']}%
            """)
        elif match_type == "average":
            st.warning(f"""
                🟡 Average Match Found

                Matched Company: {mca_result['match']}
                Similarity: {mca_result['similarity']}%
                This may or may not be the same company. Verify manually.
            """)
        else:
            st.error("❌ No matching MCA company found.")

    # -----------------------------------
    # SOURCE COUNT
    # -----------------------------------

    st.info(
        f"Analyzed {len(result['search_results'])} web sources."
    )

    # -----------------------------------
    # WEB SEARCH RESULTS
    # -----------------------------------

    st.subheader("🌐 Search Results")

    for item in result["search_results"]:

        st.markdown(
            f"""
            ### [{item['title']}]({item['link']})
            {item['snippet']}
            """
        )

    # -----------------------------------
    # DOWNLOAD REPORT
    # -----------------------------------

    report_data = {
        "company_name": result["company_name"],
        "ai_result": ai_result,
        "mca_result": mca_result,
        "final_verdict": verdict
    }

    report_json = json.dumps(
        report_data,
        indent=4
    )

    st.download_button(
        label="📥 Download Report",
        data=report_json,
        file_name=f"{company_name}_report.json",
        mime="application/json"
    )

    from datetime import datetime

    st.caption(
        f"""
        Analysis generated on:
        {datetime.now().strftime("%d %B %Y, %I:%M %p")}
        """
    )