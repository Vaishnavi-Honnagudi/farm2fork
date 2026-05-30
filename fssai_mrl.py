"""
FSSAI Maximum Residue Limits (MRL) Database
Based on FSSAI Food Safety and Standards (Contaminants, Toxins and Residues) Regulations
Values in mg/kg (ppm)
"""

FSSAI_MRL_DB = {
    "tomato": {
        "chlorpyrifos":    {"mrl": 0.5,  "unit": "mg/kg", "hazard": "medium"},
        "cypermethrin":    {"mrl": 0.5,  "unit": "mg/kg", "hazard": "medium"},
        "lambda-cyhalothrin": {"mrl": 0.2, "unit": "mg/kg", "hazard": "medium"},
        "imidacloprid":    {"mrl": 1.0,  "unit": "mg/kg", "hazard": "low"},
        "mancozeb":        {"mrl": 3.0,  "unit": "mg/kg", "hazard": "low"},
        "metalaxyl":       {"mrl": 0.5,  "unit": "mg/kg", "hazard": "low"},
        "profenofos":      {"mrl": 0.5,  "unit": "mg/kg", "hazard": "medium"},
        "spinosad":        {"mrl": 0.5,  "unit": "mg/kg", "hazard": "low"},
        "azoxystrobin":    {"mrl": 3.0,  "unit": "mg/kg", "hazard": "low"},
        "deltamethrin":    {"mrl": 0.2,  "unit": "mg/kg", "hazard": "medium"},
        "abamectin":       {"mrl": 0.02, "unit": "mg/kg", "hazard": "high"},
        "dimethoate":      {"mrl": 1.0,  "unit": "mg/kg", "hazard": "medium"},
    },
    "leafy greens": {
        "chlorpyrifos":    {"mrl": 0.05, "unit": "mg/kg", "hazard": "high"},
        "cypermethrin":    {"mrl": 1.0,  "unit": "mg/kg", "hazard": "medium"},
        "lambda-cyhalothrin": {"mrl": 1.0, "unit": "mg/kg", "hazard": "medium"},
        "imidacloprid":    {"mrl": 0.5,  "unit": "mg/kg", "hazard": "low"},
        "mancozeb":        {"mrl": 5.0,  "unit": "mg/kg", "hazard": "low"},
        "spinosad":        {"mrl": 2.0,  "unit": "mg/kg", "hazard": "low"},
        "abamectin":       {"mrl": 0.05, "unit": "mg/kg", "hazard": "high"},
        "dimethoate":      {"mrl": 0.5,  "unit": "mg/kg", "hazard": "medium"},
        "profenofos":      {"mrl": 0.1,  "unit": "mg/kg", "hazard": "high"},
        "deltamethrin":    {"mrl": 0.5,  "unit": "mg/kg", "hazard": "medium"},
        "azoxystrobin":    {"mrl": 10.0, "unit": "mg/kg", "hazard": "low"},
        "metalaxyl":       {"mrl": 2.0,  "unit": "mg/kg", "hazard": "low"},
    },
    "rice": {
        "chlorpyrifos":    {"mrl": 0.1,  "unit": "mg/kg", "hazard": "high"},
        "cypermethrin":    {"mrl": 0.05, "unit": "mg/kg", "hazard": "high"},
        "lambda-cyhalothrin": {"mrl": 0.05, "unit": "mg/kg", "hazard": "high"},
        "imidacloprid":    {"mrl": 0.05, "unit": "mg/kg", "hazard": "high"},
        "carbofuran":      {"mrl": 0.1,  "unit": "mg/kg", "hazard": "high"},
        "monocrotophos":   {"mrl": 0.05, "unit": "mg/kg", "hazard": "high"},
        "trifloxystrobin": {"mrl": 0.05, "unit": "mg/kg", "hazard": "medium"},
        "azoxystrobin":    {"mrl": 0.05, "unit": "mg/kg", "hazard": "medium"},
        "propiconazole":   {"mrl": 0.1,  "unit": "mg/kg", "hazard": "medium"},
        "deltamethrin":    {"mrl": 0.01, "unit": "mg/kg", "hazard": "high"},
        "abamectin":       {"mrl": 0.01, "unit": "mg/kg", "hazard": "high"},
        "mancozeb":        {"mrl": 0.1,  "unit": "mg/kg", "hazard": "medium"},
    }
}

PESTICIDE_CATEGORIES = {
    "chlorpyrifos": "Organophosphate",
    "cypermethrin": "Pyrethroid",
    "lambda-cyhalothrin": "Pyrethroid",
    "imidacloprid": "Neonicotinoid",
    "mancozeb": "Dithiocarbamate Fungicide",
    "metalaxyl": "Systemic Fungicide",
    "profenofos": "Organophosphate",
    "spinosad": "Spinosyn Insecticide",
    "azoxystrobin": "Strobilurin Fungicide",
    "deltamethrin": "Pyrethroid",
    "abamectin": "Avermectin",
    "dimethoate": "Organophosphate",
    "carbofuran": "Carbamate",
    "monocrotophos": "Organophosphate",
    "trifloxystrobin": "Strobilurin Fungicide",
    "propiconazole": "Triazole Fungicide",
}

def check_compliance(crop: str, pesticides: list[dict]) -> dict:
    """
    Check pesticide inputs against FSSAI MRL limits.
    pesticides: list of {"name": str, "dose": float, "unit": "mg/kg"}
    Returns compliance report dict.
    """
    crop_lower = crop.lower()
    db = FSSAI_MRL_DB.get(crop_lower, {})
    results = []
    overall_pass = True

    for p in pesticides:
        name = p.get("name", "").lower().strip()
        dose = float(p.get("dose", 0))

        if name not in db:
            results.append({
                "pesticide": p.get("name"),
                "category": PESTICIDE_CATEGORIES.get(name, "Unknown"),
                "dose_applied": dose,
                "mrl_limit": "N/A",
                "status": "NOT_IN_DB",
                "hazard": "unknown",
                "remark": "Not found in FSSAI MRL database for this crop. Use with caution."
            })
            continue

        mrl = db[name]["mrl"]
        hazard = db[name]["hazard"]
        compliant = dose <= mrl

        if not compliant:
            overall_pass = False

        results.append({
            "pesticide": p.get("name"),
            "category": PESTICIDE_CATEGORIES.get(name, "Unknown"),
            "dose_applied": dose,
            "mrl_limit": mrl,
            "status": "PASS" if compliant else "FAIL",
            "hazard": hazard,
            "remark": _get_remark(compliant, hazard, dose, mrl)
        })

    return {
        "overall_compliant": overall_pass,
        "crop": crop,
        "results": results,
        "fssai_ref": "Food Safety and Standards (Contaminants, Toxins and Residues) Regulations, 2011"
    }

def _get_remark(compliant, hazard, dose, mrl):
    if not compliant:
        excess = ((dose - mrl) / mrl) * 100
        return f"EXCEEDS MRL by {excess:.1f}%. Unsafe for sale. Pre-harvest interval must be observed."
    if hazard == "high":
        return "Within limit but high-hazard pesticide. Observe strict PHI."
    if hazard == "medium":
        return "Compliant. Monitor application frequency."
    return "Compliant. Low concern."
