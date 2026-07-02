#this code is only for orchestration

from urllib.parse import urlparse
import pandas as pd

from unimatch_scraper.crawler import crawl, close_driver
from unimatch_scraper.extractor import extract_with_gpt


universities = {
    "Stanford University": "https://www.stanford.edu/"
    
}


def flatten(data):

    return {
        "university": data.get("university"),

        # Admissions
        "early_action": data["admissions"]["early_action_deadline"],
        "early_decision": data["admissions"]["early_decision_deadline"],
        "regular_decision": data["admissions"]["regular_decision_deadline"],
        "rolling_admissions": data["admissions"]["rolling_admissions"],
        "sat_act": data["admissions"]["sat_act_policy"],
        "toefl": data["admissions"]["toefl_min"],
        "ielts": data["admissions"]["ielts_min"],
        "duolingo": data["admissions"]["duolingo_min"],
        "required_documents": ", ".join(data["admissions"]["required_documents"] or []),

        # Tuition
        "in_state": data["tuition"]["in_state"],
        "out_of_state": data["tuition"]["out_of_state"],
        "international_tuition": data["tuition"]["international"],
        "fees": data["tuition"]["mandatory_fees"],
        "financial_aid": data["tuition"]["financial_aid"],
        "scholarships": data["tuition"]["scholarships"],
        "merit_awards": data["tuition"]["merit_awards"],

        # Academics
        "program_catalog": data["academics"]["program_catalog_available"],
        "degree_summary": data["academics"]["degree_requirements_summary"],
        "majors": ", ".join(data["academics"]["majors"] or []),
        "minors": ", ".join(data["academics"]["minors"] or []),
        "languages": ", ".join(data["academics"]["languages_of_instruction"] or [])
    }


results = []

for name, url in universities.items():

    print(f"\n===== {name} =====")

    domain = urlparse(url).netloc

    pages = crawl(url, domain)

    result = extract_with_gpt(name, pages)

    if result:
        result["university"] = name
        results.append(result)


close_driver()

df = pd.DataFrame([flatten(r) for r in results])
df.to_csv("universities_1.csv", index=False)

print("\nSaved to universities_1.csv")