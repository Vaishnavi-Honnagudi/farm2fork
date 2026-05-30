import os
import urllib.request
import json

def generate_narrative(farm_data: dict, compliance: dict) -> str:
    crop = farm_data.get("crop", "produce").title()
    farmer = farm_data.get("farmer_name", "the farmer")
    location = farm_data.get("location", "India")
    harvest = farm_data.get("harvest_date", "recent")
    water = farm_data.get("water_source", "unspecified")
    overall = "COMPLIANT" if compliance.get("overall_compliant") else "NON-COMPLIANT"

    results = compliance.get("results", [])
    pesticide_summary = ""
    for r in results:
        pesticide_summary += f"- {r['pesticide']}: applied {r['dose_applied']} mg/kg, MRL limit {r['mrl_limit']} mg/kg, status {r['status']}\n"

    prompt = f"""You are an FSSAI-certified food safety analyst writing an official produce traceability report.

Farm: {farmer}, {location}
Crop: {crop}
Harvest Date: {harvest}
Water Source: {water}
Overall FSSAI Status: {overall}

Pesticide Compliance Results:
{pesticide_summary}

Write a professional traceability report with exactly these 4 sections:
1. Cultivation Summary
2. Input Safety Analysis
3. FSSAI Compliance Assessment
4. Recommendations

Tone: formal, third-person, factual. Total length: 300-400 words."""

    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        return data["candidates"][0]["content"]["parts"][0]["text"]


def generate_summary_badge(farm_data: dict, compliance: dict) -> dict:
    results = compliance.get("results", [])
    fails = [r for r in results if r.get("status") == "FAIL"]
    warns = [r for r in results if r.get("status") == "WARN"]

    if fails:
        risk = "HIGH"
        headline = f"{len(fails)} pesticide(s) exceed FSSAI MRL limits"
    elif warns:
        risk = "MEDIUM"
        headline = f"{len(warns)} pesticide(s) flagged for pre-harvest interval"
    else:
        risk = "LOW"
        headline = "All inputs within FSSAI safety limits"

    return {"risk_level": risk, "headline": headline}