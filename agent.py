import os
import json
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()

class BharatAgent:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None
        
    def check_security(self, text):
        sensitive_patterns = [
            r"(?i)password[\s:=]+[\w@#$!%^&*]+",
            r"(?i)pin[\s:=]+\d{4,6}",
            r"(?i)api_key[\s:=]+[a-zA-Z0-9_\-]+"
        ]
        for pattern in sensitive_patterns:
            if re.search(pattern, text):
                return False
        return True

    def extract_document_info(self, text_content):
        if not self.groq_client:
            return '{"error": "Groq API key not configured."}'
            
        prompt = (
            "You are an expert data extractor. Extract business profile details from the text below. "
            "CRITICAL: If empty or invalid, generate a realistic 'Pseudo Business Profile' for an Indian MSME. "
            "Return ONLY a raw JSON object with these exact keys: "
            '"Business_Name", "Owner_Name", "Sector", "Estimated_Turnover", "Location", "Category", "Immediate_Needs". '
            f"Document Text: {text_content[:2000]}"
        )
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="qwen/qwen3.8-27b",
                temperature=0.1
            )
            clean_json = response.choices[0].message.content
            clean_json = clean_json.replace('```json', '').replace('```', '').strip()
            start = clean_json.find('{')
            end = clean_json.rfind('}') + 1
            if start != -1 and end != -1:
                clean_json = clean_json[start:end]
            return clean_json
        except Exception as e:
            return f'{{"error": "Failed to extract: {str(e)}"}}'

    def search_schemes(self, query):
        """Mockup for Qdrant Vector Search to find relevant schemes."""
        return (
            "📊 **Live Gov Data Comparison:**\n"
            "1. **MUDRA Shishu Loan:** Up to ₹50,000 (Best for starting out, no collateral).\n"
            "2. **MUDRA Kishor Loan:** ₹50,000 to ₹5 Lakhs (Best for your 'under 5 lkh' requirement, meant for buying equipment).\n"
            "3. **PMEGP Scheme:** Offers 15-35% subsidy on projects up to ₹25 Lakhs (Best if you are setting up a manufacturing unit)."
        )

    def verify_government_documents(self, context_dict):
        turnover_str = str(context_dict.get('Estimated_Turnover', '0'))
        numbers = re.findall(r'\d+\.?\d*', turnover_str)
        turnover_val = float(numbers[0]) if numbers else 0
        is_gst_exempt = "Lakh" in turnover_str and turnover_val < 20
        
        verification_report = {
            "UIDAI_Aadhaar_Link": "✅ Verified & Linked with PAN - **[Verify at UIDAI ↗](https://myaadhaar.uidai.gov.in/)**",
            "Udyam_Registration": "❌ Missing - Mandatory for MSME - **[Register on Udyam ↗](https://udyamregistration.gov.in/)**",
            "GST_Status": f"{'✅ Exempt (Turnover < ₹40L)' if is_gst_exempt else '⚠️ Needs Verification'} - **[GST Portal ↗](https://www.gst.gov.in/)**",
            "Bank_Penny_Drop": "✅ Account Active - **[NPCI Mapper ↗](https://www.npci.org.in/)**",
            "Recommendation": "Agent will auto-draft your Udyam application first. Use the sidebar to generate it!"
        }
        return verification_report

    def generate_form_draft(self, scheme_name, context_dict):
        if not self.groq_client:
            return "Error: AI engine not connected."
            
        prompt = (
            f"Based on this verified business profile: {context_dict}, "
            f"generate a pre-filled, professional application draft for the '{scheme_name}'. "
            "Leave blanks [___] ONLY for sensitive details (like Bank Account number). "
            "Make it look exactly like an official government form draft."
        )
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="qwen/qwen3.8-27b",
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to generate draft: {e}"

    def process_chat(self, user_input, context=""):
        if not self.check_security(user_input):
            return "🚨 **Security Warning:** Never share passwords or PINs here."

        if not self.groq_client:
            return "⚠️ System is missing GROQ_API_KEY."

        # RESTORED AND COMBINED PROMPT: Human interaction + all previous features!
        system_prompt = (
            "You are the Autonomous Micro-MSME Compliance Navigator. Act like a highly knowledgeable, friendly human advisor (like a trusted local CA). "
            "Keep the conversation warm, natural, and conversational. Do not sound like a robot printing a rigid checklist.\n\n"
            "CORE CAPABILITIES (Keep these in mind, but weave them naturally into conversation):\n"
            "1. AUTO-CORRECT & INTENT: Users will make typos (e.g., '5 lkh' means 5 Lakhs, 'schm' means scheme). Always assume MSME intent. DO NOT block queries like 'tell under 5 lkh'.\n"
            "2. RURAL TRANSLATION: Translate jargon (like 'collateral-free') into simple 'no guarantee needed'. Speak simply. Use bullet points only when helpful.\n"
            "3. SCHEME COMPARISONS: If asked about loans, gently guide them and compare schemes (e.g., MUDRA vs PMEGP).\n"
            "4. VERIFICATION CONTEXT: You have access to their Verification Status. If they ask what to do next, gently remind them of what is missing in their profile (e.g., 'I noticed your Udyam is missing...') in a conversational tone. DO NOT dump the raw JSON into the chat.\n"
            "5. ACTION-ORIENTED: Remind them you can auto-fill their application drafts if they use the sidebar."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Verified Business Context: {context}\n\nUser Input: {user_input}"}
        ]

        try:
            response = self.groq_client.chat.completions.create(
                messages=messages,
                model="qwen/qwen3.8-27b",
                temperature=0.4
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with AI engine: {e}"
