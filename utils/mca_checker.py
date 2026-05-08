from rapidfuzz import fuzz
import re


def clean_text(text):
    """
    Clean company names for matching.
    """
    text = str(text).lower()

    remove_words = [
        "private limited",
        "pvt ltd",
        "pvt. ltd.",
        "pvt. ltd",
        "limited",
        " ltd",
        " llp",
        " private",
        " public",
        "company profile",
        "overview"
    ]

    for word in remove_words:
        text = text.replace(word, "")

    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = " ".join(text.split())

    return text.strip()


def find_company_column(df):
    """
    Automatically find company name column.
    """
    print("All MCA columns:", df.columns.tolist())

    priority_names = [
        "COMPANY_NAME", "CompanyName", "Company Name",
        "company_name", "NAME", "Name",
        "ENTITY_NAME", "Entity Name",
    ]

    for col in priority_names:
        if col in df.columns:
            print(f"Matched priority column: {col}")
            return col

    for col in df.columns:
        if "company" in col.lower() and "name" in col.lower():
            print(f"Matched fuzzy column: {col}")
            return col

    for col in df.columns:
        if "name" in col.lower():
            print(f"Matched name column: {col}")
            return col

    fallback = df.columns[0]
    print(f"Fallback to first column: {fallback}")
    return fallback


def get_match_label(score):
    """
    Convert numeric similarity to match label.
    """
    if score == 100:
        return "exact", "100% Exact Match"
    elif score >= 85:
        return "strong", "Strong Match"
    elif score >= 70:
        return "average", "Average Match"
    else:
        return "none", "No Match"


def check_mca(company_name, search_results, mca_df):
    """
    Cross-check company name against MCA CSV.
    Uses strict whole-name similarity, not word-level matching.
    """

    company_col = find_company_column(mca_df)
    print("Using MCA Column:", company_col)

    mca_df = mca_df.copy()
    mca_df[company_col] = mca_df[company_col].astype(str)

    # Clean the user input
    cleaned_input = clean_text(company_name)
    print("Cleaned Input:", cleaned_input)

    best_match = None
    best_score = 0

    for original_name in mca_df[company_col]:

        cleaned_mca = clean_text(original_name)

        if not cleaned_mca:
            continue

        # --- Exact match after cleaning ---
        if cleaned_input == cleaned_mca:
            print("EXACT MATCH:", original_name)
            return {
                "found": True,
                "match": original_name,
                "similarity": 100,
                "match_type": "exact",
                "match_label": "100% Exact Match"
            }

        # --- Strict ratio: compares full string, not word bags ---
        # ratio()         → character-level, order-sensitive
        # partial_ratio() → checks if input is a substring of MCA name
        ratio_score   = fuzz.ratio(cleaned_input, cleaned_mca)
        partial_score = fuzz.partial_ratio(cleaned_input, cleaned_mca)

        # Weighted: prefer full-name match over substring match
        combined = (ratio_score * 0.7) + (partial_score * 0.3)

        if combined > best_score:
            best_score = combined
            best_match = original_name

    print(f"BEST MATCH: {best_match} | Score: {round(best_score, 2)}")

    match_type, match_label = get_match_label(best_score)

    # No match — score too low
    if best_score < 70:
        return {
            "found": False,
            "match": None,
            "similarity": round(best_score, 2),
            "match_type": "none",
            "match_label": "No Match Found"
        }

    # Average or strong match
    return {
        "found": True,
        "match": best_match,
        "similarity": round(best_score, 2),
        "match_type": match_type,
        "match_label": match_label
    }