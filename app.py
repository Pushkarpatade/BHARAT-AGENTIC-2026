import streamlit as st
import PyPDF2
from agent import BharatAgent
import json

st.set_page_config(page_title="Bharat Agentic MSME Navigator", page_icon="🇮🇳", layout="wide")

@st.cache_resource
def get_agent():
    return BharatAgent()

agent = get_agent()

st.title("🌾 Bharat Agentic: MSME Compliance & Subsidy Navigator")
st.markdown("Unlike generic AI, this agent **runs multi-dimensional compliance checks (Aadhaar, Udyam, GST)**, checks **hard eligibility rules**, and **auto-drafts government forms** to save you CA fees!")

with st.sidebar:
    st.header("📂 1. Profile Extraction Engine")
    st.write("Upload a PDF. We use Groq Vision/Text to parse it safely.")
    
    with open("msme_demo_profile.pdf", "rb") as pdf_file:
        st.download_button(label="📥 Download Demo PDF to Test", data=pdf_file, file_name="msme_demo_profile.pdf", mime="application/pdf")
        
    uploaded_file = st.file_uploader("Upload Profile PDF", type=["pdf"])
    
    if st.button("Analyze Profile"):
        if uploaded_file is not None:
            with st.spinner("Extracting via Groq Engine..."):
                reader = PyPDF2.PdfReader(uploaded_file)
                text = "".join([page.extract_text() for page in reader.pages])
                
                extracted_info = agent.extract_document_info(text)
                try:
                    info_dict = json.loads(extracted_info)
                    st.session_state['business_context'] = info_dict
                    
                    # RUN COMPLIANCE CHECK AUTOMATICALLY
                    verification = agent.verify_government_documents(info_dict)
                    st.session_state['verification_report'] = verification
                    
                    st.success("✅ Profile Processed & Context Locked!")
                    st.json(info_dict)
                except Exception as e:
                    st.session_state['business_context'] = extracted_info
                    st.warning("Processed Text:")
                    st.write(extracted_info)
        else:
            st.warning("Please upload a PDF.")
            
    st.divider()
    
    st.header("📝 2. Agentic Form Drafter")
    scheme_to_draft = st.selectbox("Select Scheme to Auto-Fill", ["MUDRA Loan (Shishu)", "Udyam Registration", "PMEGP Subsidy"])
    
    if st.button("Generate Application Draft"):
        if 'business_context' in st.session_state:
            with st.spinner(f"Agent is drafting {scheme_to_draft} form..."):
                draft = agent.generate_form_draft(scheme_to_draft, st.session_state['business_context'])
                st.session_state['generated_draft'] = draft
                st.success("Draft Generated!")
        else:
            st.error("Please Analyze a Profile first!")

# Main UI - Tabs for Chat vs Action
tab1, tab2, tab3 = st.tabs(["💬 Advisor Chat", "🛡️ Central Verification Dashboard", "📄 Generated Documents"])

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Namaste! I am your Action-Oriented MSME Agent. Upload your profile and I will automatically cross-check your Aadhaar, GST, and Udyam status!"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("E.g., tell under 5 lkh, or compare schemes...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            with st.spinner("Agent computing eligibility across Gov APIs..."):
                context = {
                    "Profile": st.session_state.get('business_context', 'No profile'),
                    "Verification_Status": st.session_state.get('verification_report', 'Not verified yet')
                }
                
                # RESTORED FEATURE: Proactively show Vector search for Live Gov Data Comparison!
                trigger_words = ["lkh", "lakh", "loan", "scheme", "subsidy", "compare"]
                if any(word in user_input.lower() for word in trigger_words):
                    st.info("🔍 Searching Live Gov Schemes Database (Qdrant)...")
                    schemes = agent.search_schemes(user_input)
                    st.success(schemes)
                
                response = agent.process_chat(user_input, str(context))
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.header("🛡️ Multi-Dimensional Gov API Verification")
    st.markdown("Real-world problem solved: Rural users spend weeks visiting different portals for Aadhaar linking, GST checks, and Udyam checks. This agent connects to simulated APIs to consolidate your entire compliance health in 5 seconds.")
    
    if 'verification_report' in st.session_state:
        st.write("### Live API Cross-Check Results")
        for key, val in st.session_state['verification_report'].items():
            if "✅" in val:
                st.success(f"**{key.replace('_', ' ')}**: {val}")
            elif "❌" in val:
                st.error(f"**{key.replace('_', ' ')}**: {val}")
            else:
                st.warning(f"**{key.replace('_', ' ')}**: {val}")
    else:
        st.info("Upload and Analyze a PDF profile first to run the Verification Engine.")

with tab3:
    st.header("Your Auto-Filled Documents")
    if 'generated_draft' in st.session_state:
        st.markdown(st.session_state['generated_draft'])
        st.download_button("Download Draft (TXT)", st.session_state['generated_draft'], file_name="application_draft.txt")
    else:
        st.info("No documents generated yet. Use the sidebar to Auto-Fill a form!")
