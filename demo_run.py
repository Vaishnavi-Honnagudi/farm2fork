"""
demo_run.py — Standalone demo: generates DOCX reports + QR codes for all 3 crops.
Run: python demo_run.py
Requires ANTHROPIC_API_KEY in environment.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fssai_mrl        import check_compliance
from report_generator import generate_report
from qr_generator     import generate_qr
from llm_narrative    import generate_narrative, generate_summary_badge
from demo_data        import DEMO_PRODUCE
import json

def run_demo(crop_key: str):
    print(f"\n{'='*60}")
    print(f"  Processing: {crop_key.upper()}")
    print(f"{'='*60}")

    farm_data = DEMO_PRODUCE[crop_key]

    # 1. FSSAI Compliance
    print("  [1/4] Running FSSAI MRL compliance check...")
    compliance = check_compliance(crop_key, farm_data.get("pesticides", []))
    status = "✅ COMPLIANT" if compliance["overall_compliant"] else "❌ NON-COMPLIANT"
    print(f"        Overall Status: {status}")
    for r in compliance["results"]:
        icon = "✅" if r["status"] == "PASS" else ("⚠️" if r["status"] == "NOT_IN_DB" else "❌")
        print(f"        {icon} {r['pesticide']}: {r['dose_applied']} mg/kg "
              f"(MRL: {r['mrl_limit']}) — {r['status']}")

    # 2. Summary badge
    print("  [2/4] Generating risk summary...")
    badge = generate_summary_badge(farm_data, compliance)
    print(f"        Risk Level: {badge['risk_level']} | {badge['headline']}")

    # 3. AI Narrative
    print("  [3/4] Generating AI narrative (calling Anthropic API)...")
    try:
        narrative = generate_narrative(farm_data, compliance)
        print(f"        Narrative: {narrative[:120].strip()}...")
    except Exception as e:
        narrative = f"[Demo mode - narrative skipped: {e}]"
        print(f"        ⚠️  Narrative skipped: {e}")

    # 4. DOCX + QR
    print("  [4/4] Creating DOCX report and QR code...")
    report_path = generate_report(farm_data, compliance, narrative, output_dir="reports")
    qr_path     = generate_qr(farm_data, report_path, output_dir="qrcodes")
    print(f"        📄 Report: {report_path}")
    print(f"        📱 QR:     {qr_path}")

    return {"report": report_path, "qr": qr_path, "compliance": compliance, "badge": badge}


if __name__ == "__main__":
    print("\n🌾  Farm-to-Fork Traceability Demo")
    print("    Running for: Tomato | Leafy Greens | Rice\n")

    results = {}
    for crop in ["tomato", "leafy greens", "rice"]:
        try:
            results[crop] = run_demo(crop)
        except Exception as e:
            print(f"  ❌ Error for {crop}: {e}")

    print(f"\n{'='*60}")
    print("  DEMO COMPLETE — Summary")
    print(f"{'='*60}")
    for crop, res in results.items():
        badge = res["badge"]
        icon  = "✅" if res["compliance"]["overall_compliant"] else "❌"
        print(f"  {icon} {crop.title():15s} | Risk: {badge['risk_level']:6s} | {badge['headline']}")

    print("\n  Files generated:")
    for crop, res in results.items():
        print(f"    {crop.title()}: {os.path.basename(res['report'])}")
    print()
