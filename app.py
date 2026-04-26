import gradio as gr
import json
import pandas as pd
import google.generativeai as genai
import re
import os

# ====================== API KEY ======================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

with open("candidates.json", "r", encoding="utf-8") as f:
    CANDIDATES = json.load(f)[:12]

def clean_json(text):
    text = text.strip()
    text = re.sub(r'```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```\s*', '', text, flags=re.IGNORECASE)
    text = text.strip()
    start = text.find('[')
    end = text.rfind(']') + 1
    if start != -1 and end > start:
        text = text[start:end]
    return text

model = genai.GenerativeModel('gemini-2.5-flash')

def llm_call(prompt):
    return model.generate_content(prompt).text.strip()

# ====================== SIMULATED CONVERSATION (Only Top 5) ======================
def simulate_conversation(jd_text, candidate):
    prompt = f"""Short natural conversation for job: {jd_text[:120]}

Candidate: {candidate['name']}, {candidate['title']}, {candidate['location']}.

Return ONLY this JSON:
{{
  "conversation": [
    {{"role": "Recruiter", "message": "..."}},
    {{"role": "Candidate", "message": "..."}},
    {{"role": "Recruiter", "message": "..."}},
    {{"role": "Candidate", "message": "..."}}
  ],
  "interest_score": number (0-100)
}}
"""
    raw = llm_call(prompt)
    cleaned = clean_json(raw)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except:
        pass
    return {"conversation": [], "interest_score": 65}

# ====================== DYNAMIC SCORING (Fast + Location Aware) ======================
def score_candidates(jd_text):
    prompt = f"""You are an EXTREMELY STRICT recruiter.

Job Description:
{jd_text}

Candidates:
{json.dumps(CANDIDATES, indent=2)}

STRICT RULES:
- Detect the exact location mentioned in the JD
- Only candidates from that exact location can get high scores (70+)
- If location does not match → overall_match ≤ 25
- Consider experience and skills mentioned in JD

Return ONLY valid JSON array:
[
  {{"name": "Candidate Name", "overall_match": number, "explanation": "short reason"}}
]
"""
    raw = llm_call(prompt)
    cleaned = clean_json(raw)
    try:
        return json.loads(cleaned)
    except:
        return [{"name": c["name"], "overall_match": 40, "explanation": "Default match"} for c in CANDIDATES]

# ====================== MAIN FUNCTION ======================
def talent_scout(jd_text):
    if not jd_text.strip():
        return pd.DataFrame(), None

    scored_candidates = score_candidates(jd_text)

    results = []
    for i, score_data in enumerate(scored_candidates):
        cand = CANDIDATES[i]
        raw_match = score_data.get("overall_match", 60)
        match_score = int(raw_match) if str(raw_match).isdigit() else 60

        results.append({
            "Name": cand["name"],
            "Title": cand["title"],
            "Location": cand["location"],
            "Match Score": match_score,
            "Interest Score": 65,
            "Final Score": round(0.65 * match_score + 0.35 * 65),
            "Explanation": score_data.get("explanation", ""),
            "Conversation": []
        })

    results.sort(key=lambda x: x["Final Score"], reverse=True)
    df = pd.DataFrame(results[:10])

    # Generate conversations ONLY for top 5 (fast)
    for i in range(min(5, len(results))):
        conv_data = simulate_conversation(jd_text, CANDIDATES[i])
        results[i]["Interest Score"] = conv_data.get("interest_score", 65)
        results[i]["Conversation"] = conv_data.get("conversation", [])
        results[i]["Final Score"] = round(0.65 * results[i]["Match Score"] + 0.35 * results[i]["Interest Score"])

    results.sort(key=lambda x: x["Final Score"], reverse=True)
    df = pd.DataFrame(results[:10])

    csv_path = "shortlist.csv"
    df.to_csv(csv_path, index=False)

    return df, csv_path

# ====================== GRADIO INTERFACE ======================
with gr.Blocks(title="Talent Scout AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔍 Talent Scout AI")
    gr.Markdown("**AI-Powered Talent Scouting & Engagement Agent**")
    gr.Markdown("Deccan AI Catalyst Hackathon • Shalem Raju Pobbathi")

    jd_input = gr.Textbox(
        label="Paste Job Description",
        lines=12,
        placeholder="Python Developer needed in Hyderabad..."
    )

    btn = gr.Button("🚀 Start Talent Scouting", variant="primary", size="large")

    output_table = gr.DataFrame(label="Ranked Shortlist")
    csv_download = gr.File(label="📥 Download Shortlist as CSV")

    btn.click(
        fn=talent_scout,
        inputs=jd_input,
        outputs=[output_table, csv_download]
    )

if __name__ == "__main__":
    demo.launch()