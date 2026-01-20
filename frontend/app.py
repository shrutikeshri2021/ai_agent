import streamlit as st
import requests

st.set_page_config(page_title="AI Web Test Agent", layout="wide", page_icon="🤖")

st.markdown("""
<style>

/* ================= GLOBAL BACKGROUND ================= */
.stApp {
    background-color: #050510;
    background-image:
        radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.25), transparent 30%),
        radial-gradient(circle at 85% 30%, rgba(56, 189, 248, 0.25), transparent 30%);
    color: #e6f7ff;
}

/* ================= HEADINGS ================= */
h1, h2, h3, h4 {
    font-weight: 800 !important;
    color: #ffffff !important;
    text-shadow:
        0 0 6px rgba(0, 255, 255, 0.6),
        0 0 14px rgba(188, 19, 254, 0.4);
}

h1 {
    font-size: 2.6rem !important;
    background: linear-gradient(90deg, #00f2ff, #bc13fe, #00ff99);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ================= NORMAL TEXT ================= */
p, span, label, div {
    color: #d9faff !important;
}

/* ================= INPUTS & TEXT AREAS ================= */
textarea, input {
    background: rgba(10, 15, 35, 0.95) !important;
    color: #00f2ff !important;
    border: 1px solid rgba(0, 242, 255, 0.45) !important;
    border-radius: 12px !important;
    font-family: Consolas, monospace;
    box-shadow: 0 0 12px rgba(0, 242, 255, 0.25);
}

textarea::placeholder {
    color: #7dd3fc !important;
}

/* ================= BUTTONS ================= */
.stButton > button {
    background: linear-gradient(135deg, #00f2ff, #bc13fe) !important;
    color: #020617 !important;
    font-weight: 800 !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 0.6rem 1.3rem !important;
    box-shadow:
        0 0 18px rgba(0, 242, 255, 0.6),
        0 0 30px rgba(188, 19, 254, 0.4);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: scale(1.04);
    box-shadow:
        0 0 30px rgba(0, 242, 255, 0.9),
        0 0 50px rgba(188, 19, 254, 0.7);
}

/* ================= METRICS ================= */
[data-testid="stMetric"] {
    background: rgba(10, 15, 35, 0.9);
    border: 1px solid rgba(0, 242, 255, 0.4);
    border-radius: 16px;
    padding: 14px;
    box-shadow: 0 0 18px rgba(0, 242, 255, 0.25);
}

[data-testid="stMetricLabel"] {
    color: #7dd3fc !important;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #ef4444 !important;
    font-size: 1.6rem !important;
    font-weight: 900;
}

/* ================= PROGRESS BAR ================= */
.stProgress > div > div {
    background: linear-gradient(90deg, #00ffcc, #00f2ff, #bc13fe) !important;
}

/* ================= BADGES ================= */
.badge {
    display: inline-block;
    padding: 0.4em 0.9em;
    font-size: 0.75em;
    font-weight: 800;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.badge-pass {
    background: rgba(0, 255, 128, 0.12);
    color: #00ff80;
    border: 1px solid #00ff80;
    box-shadow: 0 0 14px rgba(0, 255, 128, 0.5);
}

.badge-fail {
    background: rgba(255, 0, 76, 0.12);
    color: #ff004c;
    border: 1px solid #ff004c;
    box-shadow: 0 0 14px rgba(255, 0, 76, 0.5);
}

/* ================= STEP CARDS ================= */
.step-card {
    background: rgba(10, 15, 35, 0.85);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(0, 242, 255, 0.45);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow:
        0 0 18px rgba(0, 242, 255, 0.3),
        inset 0 0 10px rgba(188, 19, 254, 0.15);
}

.step-title {
    color: #ffffff !important;
    font-size: 1.1rem;
    font-weight: 700;
}

.step-target {
    color: #00ffcc !important;
    background: rgba(0, 255, 204, 0.15);
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid rgba(0, 255, 204, 0.5);
    font-family: Consolas, monospace;
}

/* ================= ERROR ================= */
.error-text {
    color: #ff4d6d !important;
    background: rgba(255, 50, 100, 0.15);
    border: 1px solid #ff4d6d;
    padding: 10px;
    border-radius: 8px;
    box-shadow: inset 0 0 12px rgba(255, 50, 100, 0.25);
    font-weight: 600;
}

/* ================= LOGS ================= */
textarea[aria-label="Logs"] {
    background: rgba(5, 10, 30, 0.95) !important;
    color: #00f2ff !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0, 242, 255, 0.4);
    box-shadow: inset 0 0 12px rgba(0, 242, 255, 0.2);
    font-family: Consolas, monospace;
}

/* ================= JSON REPORT ================= */
[data-testid="stJson"] {
    background-color: #FFB6C1 !important; /* Light Pink Background */
    border: 2px solid #000080 !important;
    border-radius: 14px !important;
}

[data-testid="stJson"] * {
    color: #000080 !important; /* Dark Navy Blue Text */
    text-shadow: none !important; /* Remove neon glow for readability */
    font-weight: bold;
}

/* Attempt to target numbers (Best effort for Streamlit internal) */
[data-testid="stJson"] span[style*="rgb"] {
    color: #8B0000 !important; /* Deep Red for highlighted numbers/values */
}

[data-testid="stJson"] pre {
    background: transparent !important;
    color: #1e3a8a !important;   /* navy blue */
    font-family: Consolas, monospace !important;
    font-size: 0.95rem !important;
}
            /* JSON test case numbers (0,1,step_no) */
[data-testid="stJson"] span[class*="number"] {
    color: #ff0000 !important;
    font-weight: 700 !important;
}



    

</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Agent Web Tester")
st.markdown("Automate your web testing with natural language instructions.")

# Tabs for Run and History
tab1, tab2 = st.tabs(["▶️ Run Test", "📜 History"])

with tab1:
    col1, col2 = st.columns([2, 1])

    if "report" not in st.session_state:
        st.session_state.report = None
    
    with col1:
        instruction = st.text_area(
            "📝 Test Scenario",
            placeholder="1. Open youtube.com\n2. Search for Python Tutorials\n3. Verify the results page loads",
            height=150,
            help="Enter each step on a new line."
        )

    with col2:
        st.write("### ⚙️ Controls")
        if st.button("▶️ Run Test", type="primary", use_container_width=True):
            if not instruction:
                st.warning("Please enter test steps.")
            else:
                st.session_state.pdf_file = None
                st.session_state.json_file = None

                with st.spinner("🤖 Agent is executing test..."):
                    try:
                        res = requests.post(
                            "http://127.0.0.1:5000/run",
                            json={"instruction": instruction},
                            timeout=120
                        )

                        if res.status_code == 200:
                            st.session_state.report = res.json()
                            st.balloons()
                        else:
                            st.error("Backend error")
                            st.text(res.text)

                    except requests.exceptions.ConnectionError:
                        st.error("Backend crashed or browser blocked the test")

        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.report = None
            st.rerun()

    # ================= RESULTS =================
    if st.session_state.report:
        st.divider()
        summary = st.session_state.report["summary"]

        st.subheader("📊 Execution Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Steps", summary["total_steps"])
        m2.metric("Passed", summary["passed"])
        m3.metric("Failed", summary["failed"])
        m4.metric("Success Rate", f"{summary['pass_percentage']}%")

        st.progress(summary['pass_percentage'] / 100)

        st.subheader("🧪 Step Execution")
        for step in st.session_state.report["steps"]:
            status = step["status"]
            badge_class = "badge-pass" if status == "PASS" else "badge-fail"

            error_html = ""
            if "error" in step and step["error"]:
                error_html = f'<div class="error-text">⚠️ {step["error"]}</div>'

            st.markdown(f"""
            <div class="step-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="step-title">Step {step['step_no']}: {step['action']}</span>
                    <span class="badge {badge_class}">{status}</span>
                </div>
                <div style="margin-top:8px;"> 
                    Target: <span class="step-target">{step['target']}</span>
                </div>
                {error_html}
            </div>
            """, unsafe_allow_html=True)
            
            if step.get("screenshot"):
                # Fetch image server-side to ensure it loads even if client can't hit backend port directly
                try:
                    img_url = f"http://127.0.0.1:5000/screenshots/{step['screenshot']}"
                    img_resp = requests.get(img_url, timeout=5)
                    if img_resp.status_code == 200:
                        st.image(img_resp.content, caption=f"Step {step['step_no']} Screenshot", width=600)
                    else:
                        st.warning(f"Screenshot found but failed to load. (Status: {img_resp.status_code})")
                except Exception as e:
                    st.warning(f"Could not retrieve screenshot: {e}")

        st.subheader("📜 Playwright Logs")
        st.text_area("Logs", "\n".join(st.session_state.report.get("logs", [])), height=200)

        st.subheader("📄 JSON Report")
        st.json(st.session_state.report)

    st.subheader("📥 Download Report")
    d1, d2 = st.columns(2)

    if "json_file" not in st.session_state:
        st.session_state.json_file = None

    with d2:
        if st.button("🧾 Generate JSON", use_container_width=True):
            response = requests.get("http://127.0.0.1:5000/download/json")
            if response.status_code == 200:
                st.session_state.json_file = response.content
            else:
                st.error("Failed to fetch JSON report")

        if st.session_state.json_file:
            st.download_button(
                label="⬇️ Download JSON",
                data=st.session_state.json_file,
                file_name="test_report.json",
                mime="application/json",
                use_container_width=True
            )

    if "pdf_file" not in st.session_state:
        st.session_state.pdf_file = None

    with d1:
        if st.button("📄 Generate PDF", use_container_width=True):
            response = requests.get("http://127.0.0.1:5000/download/pdf")
            if response.status_code == 200:
                st.session_state.pdf_file = response.content
            else:
                st.error("Failed to fetch PDF report")

        if st.session_state.pdf_file:
            st.download_button(
                label="⬇️ Download PDF",
                data=st.session_state.pdf_file,
                file_name="test_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

with tab2:
    st.subheader("📜 Test Run History")
    
    col_h1, col_h2 = st.columns([1, 4])
    with col_h1:
        if st.button("🔄 Refresh History"):
            st.rerun()
    with col_h2:
        if st.button("🗑️ Delete All History", type="primary"):
            try:
                requests.delete("http://127.0.0.1:5000/history")
                st.success("History deleted!")
                st.rerun()
            except:
                st.error("Failed to delete history")
        
    try:
        res = requests.get("http://127.0.0.1:5000/history")
        if res.status_code == 200:
            history = res.json()
            if not history:
                st.info("No test runs found yet.")
            else:
                # Calculate Pass Percentage
                for run in history:
                    total = run.get("total_steps", 0)
                    passed = run.get("passed", 0)
                    if total > 0:
                        run["pass_percent"] = f"{round((passed / total) * 100, 1)}%"
                    else:
                        run["pass_percent"] = "0%"

                st.dataframe(
                    history, 
                    column_config={
                        "timestamp": "Date & Time",
                        "instruction": "Test Instruction",
                        "total_steps": "Total Steps",
                        "passed": "Passed ✅",
                        "failed": "Failed ❌",
                        "pass_percent": "Pass % 📈",
                        "status": st.column_config.TextColumn("Status"),
                    },
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.error("Failed to fetch history")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

