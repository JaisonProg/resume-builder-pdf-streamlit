import streamlit as st
from fpdf import FPDF
import tempfile

st.title("Resume Builder (PDF Version)")

# --- Input Fields ---
full_name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email")
linkedin = st.text_input("LinkedIn URL")

summary = st.text_area("Professional Summary")
education = st.text_area("Education (one per line)")
experience = st.text_area("Work Experience (one per line)")
skills = st.text_input("Skills (comma-separated)")

# --- PDF Resume Generator ---
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 10, full_name, ln=True, align="C")
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, f"{phone} | {email} | {linkedin}", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, lines):
        self.set_font("Helvetica", "", 12)
        for line in lines:
            self.multi_cell(0, 10, f"• {line.strip()}")

if st.button("Generate PDF Resume"):
    pdf = PDF()
    pdf.add_page()

    # Summary
    if summary.strip():
        pdf.section_title("Professional Summary")
        pdf.section_body([summary])

    # Education
    if education.strip():
        pdf.section_title("Education")
        pdf.section_body(education.strip().split("\n"))

    # Experience
    if experience.strip():
        pdf.section_title("Work Experience")
        pdf.section_body(experience.strip().split("\n"))

    # Skills
    if skills.strip():
        pdf.section_title("Skills")
        skill_list = [s.strip() for s in skills.split(",") if s.strip()]
        pdf.section_body(skill_list)

    # Save PDF to bytes
   #  pdf_output = pdf.output(dest="S").encode("latin-1", errors="ignore")
import tempfile

with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
    pdf.output(tmpfile.name)
    st.success("PDF generated successfully!")
    with open(tmpfile.name, "rb") as file:
        st.download_button(label="Download Resume as PDF", data=file, file_name="resume.pdf", mime="application/pdf")

