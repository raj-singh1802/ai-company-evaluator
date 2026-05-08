from utils.web_search import search_company
from utils.ai_scoring import analyze_company
from utils.mca_checker import check_mca
from utils.verdict import generate_verdict


def evaluate_company(
    company_name,
    mca_df,
    threshold=55
):
    """
    Full company evaluation pipeline.
    """

    # STEP 1 — Web Search
    search_results = search_company(company_name)

    # STEP 2 — AI Analysis
    ai_result = analyze_company(
        company_name,
        search_results
    )

    # STEP 3 — MCA Check
    mca_result = check_mca(
        company_name,
        search_results,
        mca_df
    )

    # STEP 4 — Final Verdict
    verdict = generate_verdict(
        ai_result,
        mca_result,
        threshold
    )

    return {
        "company_name": company_name,
        "search_results": search_results,
        "ai_result": ai_result,
        "mca_result": mca_result,
        "final_verdict": verdict
    }