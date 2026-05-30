"""
Demo produce data for Tomato, Leafy Greens, and Rice.
Used for batch demo generation.
"""

DEMO_PRODUCE = {
    "tomato": {
        "batch_id": "TOM-KA-2024-001",
        "crop": "tomato",
        "variety": "Arka Rakshak (F1 Hybrid)",
        "farmer_name": "Ramaiah B. Patil",
        "location": "Kolar, Karnataka",
        "state": "Karnataka",
        "area": "2.5 acres",
        "sowing_date": "2024-08-15",
        "harvest_date": "2024-11-20",
        "quantity": "4,200 kg",
        "water_source": "Borewell + Drip Irrigation",
        "irrigation_type": "Drip Irrigation",
        "fertilisers": [
            {"name": "Urea",            "quantity": "50 kg/acre", "date": "2024-09-01", "method": "Basal"},
            {"name": "DAP",             "quantity": "30 kg/acre", "date": "2024-09-01", "method": "Basal"},
            {"name": "Potassium Nitrate","quantity": "5 kg/acre", "date": "2024-10-10", "method": "Fertigation"},
            {"name": "Calcium Nitrate", "quantity": "3 kg/acre", "date": "2024-10-25", "method": "Foliar spray"},
        ],
        "pesticides": [
            {"name": "Chlorpyrifos",      "dose": 0.3,  "date": "2024-09-15", "phi_days": 15, "target": "Fruit borer"},
            {"name": "Mancozeb",          "dose": 2.0,  "date": "2024-10-05", "phi_days": 7,  "target": "Early blight"},
            {"name": "Imidacloprid",      "dose": 0.8,  "date": "2024-10-15", "phi_days": 7,  "target": "Whitefly"},
            {"name": "Azoxystrobin",      "dose": 1.5,  "date": "2024-11-01", "phi_days": 3,  "target": "Late blight"},
        ],
    },

    "leafy greens": {
        "batch_id": "SPG-MH-2024-007",
        "crop": "leafy greens",
        "variety": "Palak / Spinach (Jyoti variety)",
        "farmer_name": "Sunita Deshmukh",
        "location": "Nashik, Maharashtra",
        "state": "Maharashtra",
        "area": "0.8 acres",
        "sowing_date": "2024-10-01",
        "harvest_date": "2024-11-25",
        "quantity": "1,200 kg",
        "water_source": "Canal Water (Godavari)",
        "irrigation_type": "Sprinkler",
        "fertilisers": [
            {"name": "Vermicompost",  "quantity": "1 ton/acre", "date": "2024-10-01", "method": "Basal"},
            {"name": "Urea",          "quantity": "20 kg/acre", "date": "2024-10-10", "method": "Top dressing"},
            {"name": "Micronutrient mix","quantity": "2 kg/acre","date": "2024-10-20", "method": "Foliar spray"},
        ],
        "pesticides": [
            {"name": "Spinosad",          "dose": 0.1,  "date": "2024-10-18", "phi_days": 3, "target": "Leaf miner"},
            {"name": "Chlorpyrifos",      "dose": 0.08, "date": "2024-11-01", "phi_days": 15,"target": "Aphids"},  # High hazard, very low dose
            {"name": "Azoxystrobin",      "dose": 4.0,  "date": "2024-11-10", "phi_days": 3, "target": "Downy mildew"},
        ],
    },

    "rice": {
        "batch_id": "RIC-AP-2024-012",
        "crop": "rice",
        "variety": "BPT 5204 (Samba Mahsuri)",
        "farmer_name": "Venkatesh Reddy",
        "location": "Krishna District, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "area": "5.0 acres",
        "sowing_date": "2024-07-10",
        "harvest_date": "2024-11-15",
        "quantity": "12,500 kg",
        "water_source": "Krishna River Canal",
        "irrigation_type": "Flood Irrigation",
        "fertilisers": [
            {"name": "Urea",                "quantity": "60 kg/acre",  "date": "2024-07-15", "method": "Basal"},
            {"name": "Super Phosphate",     "quantity": "40 kg/acre",  "date": "2024-07-15", "method": "Basal"},
            {"name": "Muriate of Potash",   "quantity": "20 kg/acre",  "date": "2024-08-01", "method": "Top dressing"},
            {"name": "Zinc Sulphate",       "quantity": "5 kg/acre",   "date": "2024-08-15", "method": "Soil application"},
            {"name": "Urea (top dress)",    "quantity": "25 kg/acre",  "date": "2024-09-01", "method": "Top dressing"},
        ],
        "pesticides": [
            {"name": "Chlorpyrifos",      "dose": 0.05, "date": "2024-08-20", "phi_days": 21, "target": "Stem borer"},
            {"name": "Trifloxystrobin",   "dose": 0.04, "date": "2024-09-15", "phi_days": 14, "target": "Blast fungus"},
            {"name": "Imidacloprid",      "dose": 0.04, "date": "2024-09-28", "phi_days": 21, "target": "Brown planthopper"},
        ],
    }
}
