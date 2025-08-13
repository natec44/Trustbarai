import streamlit as st
import os
# Note: This prototype uses OpenAI. Set OPENAI_API_KEY as an environment variable before running.
# pip install openai streamlit python-dotenv

try:
    import openai
except Exception:
    openai = None

st.set_page_config(page_title="TrustBar AI Dashboard", layout="wide")

# Header
st.image("TrustBarAI.png", width=220)  # Replace with your logo file in the same directory
st.title("TrustBar AI — Law Firm Assistant")
st.write("Prototype dashboard: Case intake, document drafting, communication summarizers, legal research helper, and analytics.")


def call_openai(prompt, model="gpt-4o-mini", max_tokens=800, temperature=0.2):
    if openai is None:
        return "OpenAI SDK not installed in this environment."
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Please set OPENAI_API_KEY environment variable in your hosting environment."
    openai.api_key = api_key
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"OpenAI call failed: {e}"


# Sidebar navigation
st.sidebar.title("Tools")
tool = st.sidebar.radio("", ["Case Intake Assistant", "Document Drafting", "Client Communication Summarizer", "Legal Research Helper", "Analytics Dashboard"])

if tool == "Case Intake Assistant":
    st.header("Case Intake Assistant")
    st.write("Collect standardized client intake information and generate a summary for quick review.")
    with st.form("intake_form"):
        client_name = st.text_input("Client Name")
        client_contact = st.text_input("Contact (email or phone)")
        case_type = st.selectbox("Case Type", ["Divorce", "Child Custody", "Support", "Domestic Violence", "Other"])
        short_history = st.text_area("Brief Case History / Details", height=150)
        submit = st.form_submit_button("Generate Intake Summary")
    if submit:
        prompt = f"Create a concise professional intake summary for a family law case.\n\nClient: {client_name}\nContact: {client_contact}\nCase Type: {case_type}\nDetails: {short_history}\n\nProvide: 1) 3-sentence case summary, 2) Suggested next steps (up to 5), 3) Potential documents needed."
        result = call_openai(prompt)
        st.subheader("Intake Summary")
        st.success(result)

elif tool == "Document Drafting":
    st.header("Document Drafting")
    st.write("Draft demand letters, engagement letters, or simple pleadings from prompts. Always have a licensed attorney review before sending.")
    with st.form("doc_form"):
        doc_type = st.selectbox("Document Type", ["Demand Letter", "Engagement Letter", "Pleading (basic)", "Custom"])
        recipient = st.text_input("Recipient (Name / Opposing Party)")
        key_points = st.text_area("Key Points / Facts to Include", height=200)
        tone = st.selectbox("Tone", ["Professional", "Firm", "Conciliatory", "Neutral"])
        submit_doc = st.form_submit_button("Generate Draft")
    if submit_doc:
        prompt = f"Draft a {doc_type} to {recipient}. Include these points: {key_points}. Tone: {tone}. Keep legal disclaimers and recommend attorney review."
        result = call_openai(prompt)
        st.subheader("Draft Output")
        st.info("**DISCLAIMER:** This draft is AI-generated. Have a licensed attorney review and edit before sending to clients or courts.") 
        st.text_area("Generated Document", value=result, height=400)

elif tool == "Client Communication Summarizer":
    st.header("Client Communication Summarizer")
    st.write("Upload an email thread, transcript, or paste communication and get a concise summary and recommended action items.")
    uploaded = st.file_uploader("Upload .txt, .docx or paste text below", type=['txt','docx','pdf'])
    raw_text = st.text_area("Or paste client communication here:", height=250)
    if uploaded is not None:
        try:
            import textract
            raw_text = textract.process(uploaded).decode('utf-8')
        except Exception as e:
            st.warning("Document parsing not available in this environment. Consider pasting text instead.")
    if st.button("Summarize Communication"):
        if not raw_text.strip():
            st.error("Please paste or upload communication content to summarize.")
        else:
            prompt = f"Summarize the following client communication into a short brief (3-6 bullets) and list 3 recommended action items for the attorney.\n\nCommunication:\n{raw_text}"
            result = call_openai(prompt)
            st.subheader("Summary & Actions")
            st.write(result)

elif tool == "Legal Research Helper":
    st.header("Legal Research Helper")
    st.write("Ask a question and get a summarized explanation, potential next steps, and suggested search terms. Not a substitute for legal research.")
    question = st.text_input("Enter legal question or issue:")
    if st.button("Search"):
        if not question.strip():
            st.error("Please enter your legal question or issue.")
        else:
            prompt = f"Provide a concise summary for a family law question. Include: 1) Short answer, 2) Key statutes or code sections to check, 3) Suggested search keywords and 4) Recommended next steps for an attorney. Question: {question}"
            result = call_openai(prompt)
            st.subheader("Research Summary")
            st.write(result)

elif tool == "Analytics Dashboard":
    st.header("Analytics Dashboard")
    st.write("Basic usage metrics for prototype (sample data).")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Queries (30d)", "125")
    col2.metric("Unique Firms", "6")
    col3.metric("Avg. Response Time", "2.4s")
    st.write("Recent queries:") 
    st.table([{"tool":"Document Drafting","user":"firm_a","time":"2025-07-01"},
              {"tool":"Intake Summary","user":"firm_b","time":"2025-07-02"},
              {"tool":"Communication Summarizer","user":"firm_c","time":"2025-07-03"}])
    st.info("This is prototype analytics data. In production, we will connect to a database and track real usage.")