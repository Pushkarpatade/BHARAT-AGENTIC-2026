from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="MSME Business Profile: Shanti Handlooms", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", size=12)
details = [
    "Owner Name: Shanti Devi",
    "Aadhaar Number: 1234-XXXX-5678",
    "PAN Card: ABCDE1234F",
    "Category: Women Entrepreneur (SC Category)",
    "Location: Varanasi, Uttar Pradesh, 221001",
    "Sector: Manufacturing (Textile & Handlooms)",
    "Estimated Annual Turnover: 4.5 Lakhs",
    "Current Udyam Registration: Not Registered",
    "Immediate Need: Seeking a loan of Rs. 3 Lakhs to buy 2 new weaving machines."
]

for detail in details:
    pdf.cell(200, 10, txt=detail, ln=True)

pdf.output("msme_demo_profile.pdf")
print("Demo PDF created successfully!")
