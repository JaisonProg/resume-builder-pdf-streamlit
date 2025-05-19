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
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, full_name, ln=True, align="C")

    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 12)
        if isinstance(content, list):
            for item in content:
                self.multi_cell(0, 8, f"- {item}")
        else:
            self.multi_cell(0, 8, content)
        self.ln(5)

if st.button("Generate PDF Resume"):
    pdf = PDF()
    pdf.add_page()
    pdf.add_section("Contact Information", f"{phone}\n{email}\n{linkedin}")
    pdf.add_section("Professional Summary", summary)
    pdf.add_section("Education", education.splitlines())
    pdf.add_section("Work Experience", experience.splitlines())
    pdf.add_section("Skills", [s.strip() for s in skills.split(",")])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        with open(tmp_file.name, "rb") as f:
            st.download_button("Download Resume PDF", f, file_name="resume.pdf", mime="application/pdf")

