"""
Farm-to-Fork Supply Chain Traceability Report Generator
Streamlit App — PS-A9
"""
import streamlit as st
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fssai_mrl        import check_compliance, FSSAI_MRL_DB
from report_generator import generate_report
from qr_generator     import generate_qr
from llm_narrative    import generate_narrative, generate_summary_badge
from demo_data        import DEMO_PRODUCE
from PIL import Image
import pandas as pd
# Auto-load report from QR code scan
query_params = st.query_params
if "batch_id" in query_params:
    batch_id = query_params["batch_id"]
    # Map batch_id to demo produce
    batch_map = {
        "TOM-KA-2024-001": "tomato",
        "SPG-MH-2024-007": "leafy greens",
        "RIC-AP-2024-012": "rice"
    }
    if batch_id in batch_map:
        crop = batch_map[batch_id]
        st.set_page_config(
            page_title="Farm2Fork Traceability",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.markdown("## 📱 QR Scan — Auto Loading Report")
        run_pipeline(DEMO_PRODUCE[crop])
        st.stop()
st.set_page_config(
    page_title="Farm2Fork Traceability",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title   { font-size:2.2rem; font-weight:700; color:#1A5C2E; margin-bottom:0; }
    .sub-title    { font-size:1rem; color:#666; margin-top:0; margin-bottom:2rem; }
    .section-head { font-size:1.1rem; font-weight:600; color:#1A5C2E;
                    border-bottom:2px solid #D5E8D4; padding-bottom:4px; margin-top:1rem; }
    .stButton>button { background-color:#1A5C2E; color:white; border:none;
                       border-radius:6px; font-weight:600; }
    .stButton>button:hover { background-color:#145023; }
</style>
""", unsafe_allow_html=True)


# ── PIPELINE ─────────────────────────────────────────────────────
def run_pipeline(farm_data: dict):
    crop = farm_data.get("crop", "produce")
    st.markdown("---")
    st.markdown(f"## 📊 Traceability Report — {crop.title()}")

    prog = st.progress(0, text="Starting analysis…")

    prog.progress(20, text="🔬 Checking FSSAI MRL compliance…")
    compliance = check_compliance(crop, farm_data.get("pesticides", []))

    prog.progress(40, text="📝 Calculating risk profile…")
    badge = generate_summary_badge(farm_data, compliance)

    prog.progress(55, text="🤖 Generating AI traceability narrative…")
    try:
        narrative = generate_narrative(farm_data, compliance)
    except Exception as e:
        narrative = f"[Narrative unavailable — check ANTHROPIC_API_KEY: {e}]"

    prog.progress(75, text="📄 Building DOCX report…")
    report_path = generate_report(
        farm_data, compliance, narrative,
        output_dir="/home/claude/farm2fork/reports"
    )

    prog.progress(90, text="📱 Generating QR code…")
    qr_path = generate_qr(
        farm_data, report_path,
        output_dir="/home/claude/farm2fork/qrcodes"
    )

    prog.progress(100, text="✅ Done!")

    # ── Summary metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Crop",       crop.title())
    c2.metric("Batch ID",   farm_data.get("batch_id", "—"))
    c3.metric("Pesticides", len(compliance.get("results", [])))
    fails = sum(1 for r in compliance.get("results", []) if r.get("status") == "FAIL")
    c4.metric("Violations", fails)

    if compliance["overall_compliant"]:
        st.success(f"✅ **FSSAI STATUS: COMPLIANT** — {badge['headline']}")
    else:
        st.error(f"❌ **FSSAI STATUS: NON-COMPLIANT** — {badge['headline']}")

    risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(badge["risk_level"], "⚪")
    st.markdown(f"**Risk Level:** {risk_emoji} {badge['risk_level']}")

    # ── MRL Table
    with st.expander("🔬 FSSAI MRL Compliance Details", expanded=True):
        results = compliance.get("results", [])
        if results:
            df = pd.DataFrame(results)
            df.columns = [c.replace("_", " ").title() for c in df.columns]

            def color_status(val):
                m = {"PASS": "background-color:#D5F5E3;color:#1A7A40;font-weight:bold",
                     "FAIL": "background-color:#FADBD8;color:#A93226;font-weight:bold",
                     "NOT_IN_DB": "background-color:#FEF9E7;color:#B7950B;font-weight:bold"}
                return m.get(val, "")

            def color_hazard(val):
                m = {"high": "color:#A93226;font-weight:bold",
                     "medium": "color:#B7950B;font-weight:bold",
                     "low": "color:#1A7A40;font-weight:bold"}
                return m.get(val, "")

            styled = df.style.map(color_status, subset=["Status"]) \
                             .map(color_hazard,  subset=["Hazard"])
            st.dataframe(styled, use_container_width=True, hide_index=True)
        else:
            st.info("No pesticides to evaluate.")

    # ── Narrative
    with st.expander("📖 AI-Generated Traceability Narrative", expanded=True):
        st.markdown(narrative)

    # ── Downloads
    st.markdown("---")
    d1, d2, d3 = st.columns([2, 2, 1])
    with d1:
        st.markdown("#### 📄 DOCX Report")
        with open(report_path, "rb") as f:
            st.download_button("⬇️ Download Report (.docx)", f.read(),
                               file_name=os.path.basename(report_path),
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               use_container_width=True)
    with d2:
        st.markdown("#### 📱 QR Code")
        with open(qr_path, "rb") as f:
            st.download_button("⬇️ Download QR (.png)", f.read(),
                               file_name=os.path.basename(qr_path),
                               mime="image/png", use_container_width=True)
    with d3:
        st.markdown("#### Preview")
        st.image(Image.open(qr_path), width=120)

    st.balloons()


# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    try:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/FSSAI_logo.png/240px-FSSAI_logo.png",
                 width=120)
    except Exception:
        pass
    st.markdown("### 🌾 Farm2Fork")
    st.markdown("**Standard:** FSSAI MRL 2011  \n**Version:** 1.0")
    st.markdown("---")
    mode = st.radio("Mode", ["📋 Enter Farm Data", "🎯 Demo (3 Crops)"])
    st.markdown("---")
    st.markdown("**Supported Crops**")
    st.markdown("- 🍅 Tomato\n- 🥬 Leafy Greens\n- 🌾 Rice")

# ── HEADER
st.markdown('<p class="main-title">🌾 Farm-to-Fork Traceability System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">FSSAI MRL Compliance · AI Narrative Reports · QR-Linked Digital Certificates</p>',
            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  MODE 1 — MANUAL FORM
# ══════════════════════════════════════════════════════════════════
if mode == "📋 Enter Farm Data":
    st.markdown("---")

    st.markdown('<p class="section-head">🏡 Farm & Batch Details</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        farmer_name = st.text_input("Farmer Name", placeholder="e.g. Ramaiah B. Patil")
        crop        = st.selectbox("Crop", ["Tomato", "Leafy Greens", "Rice"])
        variety     = st.text_input("Variety", placeholder="e.g. Arka Rakshak F1")
    with c2:
        location    = st.text_input("Location", placeholder="e.g. Kolar, Karnataka")
        state       = st.text_input("State",    placeholder="e.g. Karnataka")
        area        = st.text_input("Area Cultivated", placeholder="e.g. 2.5 acres")
    with c3:
        batch_id    = st.text_input("Batch ID", value=f"BATCH-{datetime.date.today().strftime('%Y%m%d')}")
        quantity    = st.text_input("Quantity", placeholder="e.g. 4000 kg")
        water_src   = st.selectbox("Water Source", ["Borewell", "Canal", "River", "Rainwater", "Drip"])
        irr_type    = st.selectbox("Irrigation", ["Drip", "Sprinkler", "Flood", "Furrow"])

    dc1, dc2 = st.columns(2)
    sow_date  = dc1.date_input("Sowing Date",  datetime.date.today() - datetime.timedelta(days=90))
    harv_date = dc2.date_input("Harvest Date", datetime.date.today())

    # Fertilisers
    st.markdown('<p class="section-head">🧪 Fertilisers Applied</p>', unsafe_allow_html=True)
    num_fert = st.number_input("Number of fertilisers", 0, 8, 2, key="nf")
    fertilisers = []
    if num_fert:
        hh = st.columns(4)
        for h, t in zip(hh, ["Name", "Quantity", "Date", "Method"]):
            h.markdown(f"**{t}**")
    for i in range(int(num_fert)):
        fc = st.columns(4)
        fn = fc[0].text_input(f"fn{i}", key=f"fn{i}", label_visibility="collapsed", placeholder="Fertiliser")
        fq = fc[1].text_input(f"fq{i}", key=f"fq{i}", label_visibility="collapsed", placeholder="50 kg/acre")
        fd = fc[2].date_input(f"fd{i}", key=f"fd{i}", label_visibility="collapsed")
        fm = fc[3].selectbox(f"fm{i}",  key=f"fm{i}", label_visibility="collapsed",
                              options=["Basal", "Top dressing", "Fertigation", "Foliar spray"])
        if fn:
            fertilisers.append({"name": fn, "quantity": fq, "date": str(fd), "method": fm})

    # Pesticides
    st.markdown('<p class="section-head">☠️ Pesticides / Agrochemicals</p>', unsafe_allow_html=True)
    crop_key = crop.lower()
    avail    = list(FSSAI_MRL_DB.get(crop_key, {}).keys())
    st.info(f"💡 FSSAI DB pesticides for {crop}: {', '.join(avail)}")

    num_pest = st.number_input("Number of pesticides", 0, 8, 2, key="np")
    pesticides = []
    if num_pest:
        hp = st.columns(5)
        for h, t in zip(hp, ["Name", "Dose (mg/kg)", "Date", "PHI Days", "Target"]):
            h.markdown(f"**{t}**")
    for i in range(int(num_pest)):
        pc = st.columns(5)
        pn = pc[0].selectbox(f"pn{i}", key=f"pn{i}", label_visibility="collapsed", options=[""] + avail)
        pd_ = pc[1].number_input(f"pd{i}", key=f"pd{i}", label_visibility="collapsed",
                                  min_value=0.0, max_value=50.0, step=0.01)
        pdt = pc[2].date_input(f"pdt{i}", key=f"pdt{i}", label_visibility="collapsed")
        pp  = pc[3].number_input(f"pp{i}", key=f"pp{i}", label_visibility="collapsed",
                                  min_value=0, max_value=60, value=7)
        pt  = pc[4].text_input(f"pt{i}",  key=f"pt{i}", label_visibility="collapsed", placeholder="Target pest")
        if pn:
            pesticides.append({"name": pn, "dose": pd_, "date": str(pdt), "phi_days": pp, "target": pt})

    st.markdown("---")
    if st.button("🚀 Generate Traceability Report", use_container_width=True):
        if not farmer_name or not location:
            st.error("Please enter Farmer Name and Location.")
        else:
            run_pipeline({
                "batch_id": batch_id, "crop": crop_key, "variety": variety,
                "farmer_name": farmer_name, "location": location, "state": state,
                "area": area, "sowing_date": str(sow_date), "harvest_date": str(harv_date),
                "quantity": quantity, "water_source": water_src, "irrigation_type": irr_type,
                "fertilisers": fertilisers, "pesticides": pesticides,
            })


# ══════════════════════════════════════════════════════════════════
#  MODE 2 — DEMO
# ══════════════════════════════════════════════════════════════════
else:
    st.markdown("---")
    st.markdown("### 🎯 Demo: 3 Produce Types")
    d1, d2, d3 = st.columns(3)
    demo_choice = None
    with d1:
        st.markdown("#### 🍅 Tomato\nKolar, Karnataka  \nBatch: TOM-KA-2024-001")
        if st.button("Generate Tomato Report", use_container_width=True, key="demo_tom"):
            demo_choice = "tomato"
    with d2:
        st.markdown("#### 🥬 Leafy Greens\nNashik, Maharashtra  \nBatch: SPG-MH-2024-007")
        if st.button("Generate Greens Report", use_container_width=True, key="demo_grn"):
            demo_choice = "leafy greens"
    with d3:
        st.markdown("#### 🌾 Rice\nKrishna Dist., AP  \nBatch: RIC-AP-2024-012")
        if st.button("Generate Rice Report", use_container_width=True, key="demo_ric"):
            demo_choice = "rice"

    if demo_choice:
        run_pipeline(DEMO_PRODUCE[demo_choice])
