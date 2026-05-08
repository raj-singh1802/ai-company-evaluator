from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def clean_json_response(content):
    """
    Removes markdown code blocks from LLM responses.
    """

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return content


def analyze_company(company_name, search_results):
    """
    Uses Groq LLM to analyze trustworthiness.
    """

    prompt = f"""
You are a company trust evaluator.

Analyze the company below based on web search data.

Company:
{company_name}

Search Results:
{json.dumps(search_results, indent=2)}

Return ONLY valid JSON in this format:

{{
    "trust_score": 0-100,
    "web_presence": "strong/moderate/weak",
    "news_coverage": "positive/neutral/negative",
    "red_flags": ["flag1", "flag2"],
    "reason": "short explanation",
    "verdict_explanation": "Detailed human-like explanation of why the company appears genuine, suspicious, or risky based on online presence, MCA verification likelihood, reputation, and trust indicators."
}}

Scoring Rules:
- Strong online presence increases score
- Professional website increases score
- LinkedIn/Crunchbase/news coverage increases score
- Scam complaints decrease score
- No digital footprint is suspicious

The verdict explanation should:
- sound natural and professional
- reference online presence and credibility
- mention reputation signals
- mention trust concerns if present
- avoid repetitive generic wording
- be 3–5 lines long
- vary dynamically for different companies
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    # Clean markdown formatting
    content = clean_json_response(content)

    try:
        result = json.loads(content)
        return result

    except Exception:
        return {
            "trust_score": 50,
            "web_presence": "unknown",
            "news_coverage": "unknown",
            "red_flags": ["AI parsing failed"],
            "reason": content
        }