#this code is only for Open AI
import json
from openai import OpenAI

client = OpenAI()

SCHEMA_PROMPT = """
You are an expert university data extraction system.

Your task is to read university website text and extract ONLY factual information that is explicitly stated or clearly implied.

IMPORTANT RULES:
- Do NOT guess or hallucinate values.
- If information is not found, return null (or empty list).
- Normalize values when possible (e.g., "Fall 2025" → "Fall 2025").
- Extract information ONLY from the provided text.

Return ONLY valid JSON in this exact format:

{
  "university": "",
  "admissions": {
    "early_action_deadline": null,
    "early_decision_deadline": null,
    "regular_decision_deadline": null,
    "rolling_admissions": null,
    "sat_act_policy": null,
    "toefl_min": null,
    "ielts_min": null,
    "duolingo_min": null,
    "required_documents": [],
    "other_requirements": {
      "domestic": [],
      "international": []
    }
  },
  "tuition": {
    "in_state": null,
    "out_of_state": null,
    "international": null,
    "mandatory_fees": null,
    "financial_aid": null,
    "scholarships": null,
    "merit_awards": null
  },
  "academics": {
    "program_catalog_available": null,
    "degree_requirements_summary": null,
    "majors": [],
    "minors": [],
    "languages_of_instruction": []
  }
}

EXTRACTION GUIDELINES:

ADMISSIONS:
- early_action_deadline: look for "Early Action" dates
- early_decision_deadline: look for "Early Decision" dates
- regular_decision_deadline: look for "Regular Decision"
- rolling_admissions: true/false or description if stated
- sat_act_policy: test optional / required / flexible / superscoring
- english tests:
  - TOEFL minimum score (e.g., "100 iBT")
  - IELTS minimum score (e.g., "7.0")
  - Duolingo minimum score if mentioned
- required_documents: transcripts, essays, recommendation letters, CV, etc.
- other_requirements:
  - domestic: special requirements for US students
  - international: visa, financial proof, etc.

TUITION:
- in_state: only for public US universities
- out_of_state: tuition for non-residents
- international: tuition for international students
- mandatory_fees: required fees (housing, admin, etc.)
- financial_aid: need-based aid info
- scholarships: scholarships mentioned
- merit_awards: merit-based funding

ACADEMICS:
- program_catalog_available: true/false if catalog exists
- degree_requirements_summary: short summary of degree structure
- majors: list ALL majors mentioned
- minors: list ALL minors mentioned
- languages_of_instruction: e.g., English, French, Spanish

Return ONLY JSON. No explanation. No extra text.
"""

def extract_with_gpt(university, pages):

    text = "\n\n".join([p["text"] for p in pages])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SCHEMA_PROMPT},
            {"role": "user", "content": f"University: {university}\n\n{text}"}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        print("JSON parse failed")
        return None

