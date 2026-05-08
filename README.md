# AI Company Evaluator

> Verify any Indian company or startup in seconds using AI, web intelligence, and MCA government data.

---

## What It Does

You type a company name. The system runs it through a multi-layer verification pipeline and tells you whether it's **Genuine**, **Suspicious**, or **Not Genuine** — with evidence.

```
Input: "Sanatan Communications Private Limited"

  Step 1 → Google Web Search (Serper API)
  Step 2 → LLM Trust Analysis (Groq / Llama 3.3)
  Step 3 → MCA Database Cross-Check (fuzzy + exact match)
  Step 4 → Final Verdict with confidence score

Output: ✅ GENUINE — Matched in MCA: Sanatan Communications Pvt Ltd (97.4%)
```

---

## Features

| Feature               | Description                                                     |
| --------------------- | --------------------------------------------------------------- |
| 🌐 Web Intelligence   | Searches Google and extracts trust signals from top results     |
| 🤖 LLM Scoring        | Groq-powered analysis returns a 0–100 trust score + red flags   |
| 🏢 MCA Verification   | Cross-checks against Ministry of Corporate Affairs company data |
| 🔎 Smart Matching     | Exact, strong, and average match tiers using RapidFuzz          |
| 📊 Risk Dashboard     | Visual confidence breakdown with signal indicators              |
| 🚩 Red Flag Detection | Surfaces scam signals, inconsistencies, and missing footprints  |
| 📁 JSON Reports       | Download full evaluation report for any company                 |

---

## Verdict Logic

```
Trust Score 70–100  →  ✅ GENUINE
Trust Score 40–69   →  ⚠️  SUSPICIOUS
Trust Score  0–39   →  ❌ NOT GENUINE

MCA Match adds weight but never overrides the score range.
```

---

## Tech Stack

```
Language     Python 3.10+
UI           Streamlit
LLM          Groq API  (Llama 3.3 70B)
Web Search   Serper API  (Google Search)
MCA Matching RapidFuzz
Data         Pandas
Config       python-dotenv
```

---

## Project Structure

```
company-evaluator/
│
├── app.py                  # Streamlit UI
├── evaluator.py            # Main pipeline orchestrator
├── requirements.txt
├── .env                    # API keys (never commit this)
│
├── data/
│   └── mca_companies.csv   # Downloaded from mca.gov.in
│
└── utils/
    ├── web_search.py       # Serper API integration
    ├── ai_scoring.py       # Groq LLM trust scoring
    ├── mca_checker.py      # Fuzzy MCA matching engine
    └── verdict.py          # Final verdict logic
```

---

## Setup

### 1. Clone and enter the project

```bash
git clone <your_repo_url>
cd company-evaluator
```

### 2. Create and activate virtual environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API keys

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_key_here
SERPER_API_KEY=your_serper_key_here
```

Get your keys here:

- Groq → https://console.groq.com
- Serper → https://serper.dev (2,500 free searches/month)

### 5. Add MCA data

Download the Company Master Data CSV from the MCA portal:

```
mca.gov.in → Master Data → Company Master Data → Download
```

Place it at:

```bash
data/mca_companies.csv
```

### 6. Run

```bash
streamlit run app.py
```

---

## MCA Match Tiers

| Score  | Label         | Meaning                               |
| ------ | ------------- | ------------------------------------- |
| 100%   | Exact Match   | Name matches perfectly after cleaning |
| 85–99% | Strong Match  | Minor suffix/spelling difference      |
| 70–84% | Average Match | Similar — verify manually             |
| < 70%  | No Match      | Not found in MCA database             |

---

## Example Results

| Company                        | Trust Score | MCA Match    | Verdict        |
| ------------------------------ | ----------- | ------------ | -------------- |
| Infosys Limited                | 91/100      | Exact        | ✅ Genuine     |
| Sanatan Communications Pvt Ltd | 60/100      | Strong (97%) | ⚠️ Suspicious  |
| XYZ Fake Ventures              | 22/100      | None         | ❌ Not Genuine |

---

## Roadmap

- [ ] PDF report export
- [ ] Domain age and WHOIS analysis
- [ ] LinkedIn credibility scoring
- [ ] Real-time news sentiment analysis
- [ ] Multi-agent verification pipeline
- [ ] CIN-based direct MCA lookup

---

## Author

**Raj Narayan Singh**  
AI Engineer  
[GitHub](#) · [LinkedIn](#)

---

> ⚠️ This tool is for informational purposes only. Always verify critical business decisions through official government channels.
