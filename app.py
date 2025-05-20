import streamlit as st
from fpdf import FPDF
import tempfile

# === PDF CLASS ===
class ResumePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 10, full_name, ln=True, align="C")
        self.set_font("Helvetica", "", 11)
        contact_line = f"{email} | {phone} | {linkedin}"
        self.cell(0, 8, contact_line, ln=True, align="C")
        self.ln(4)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 10, title.upper(), ln=True)
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def section_body(self, text):
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def add_edu(self, degree, school, location, grad_date):
        self.set_font("Helvetica", "B", 12)
        self.cell(140, 7, f"{degree}, {school}", ln=0)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 7, grad_date, ln=1, align="R")
        self.set_font("Helvetica", "I", 11)
        self.cell(0, 6, location, ln=True)
        self.ln(2)

    def add_exp(self, title, company, location, date, bullets):
        self.set_font("Helvetica", "B", 12)
        self.cell(140, 7, title, ln=0)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 7, date, ln=1, align="R")
        self.set_font("Helvetica", "I", 11)
        self.cell(0, 6, f"{company}, {location}", ln=True)
        self.set_font("Helvetica", "", 11)
        for b in bullets:
            if b.strip():
                self.cell(5)
                self.cell(0, 6, f"- {b.strip()}", ln=True)
        self.ln(2)

    def add_skills(self, skills_list):
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, ", ".join(skills_list))
        self.ln(1)

# === STREAMLIT INTERFACE ===
st.title("Resume Builder (PDF Format)")

# Personal Info
full_name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")
linkedin = st.text_input("LinkedIn URL")

# Summary
summary = st.text_area("Professional Summary (2–4 lines)")

# Education
degree = st.text_input("Degree (e.g. B.S. in CS)")
school = st.text_input("School Name")
school_location = st.text_input("Education Location")
grad_date = st.text_input("Graduation Date")

# Experience
exp_title = st.text_input("Job Title")
exp_company = st.text_input("Company Name")
exp_location = st.text_input("Job Location")
exp_date = st.text_input("Job Date (e.g. Summer 2024)")
exp_bullets_input = st.text_area("Job Responsibilities (one per line)")
exp_bullets = exp_bullets_input.strip().split("\n")

# Skills
skills_input = st.text_input("Skills (comma-separated)")

# === PDF GENERATION ===
if st.button("Generate Resume PDF"):
    pdf = ResumePDF()
    pdf.add_page()

    pdf.section_title("Professional Summary")
    pdf.section_body(summary)

    pdf.section_title("Education")
    pdf.add_edu(degree, school, school_location, grad_date)

    pdf.section_title("Work Experience")
    pdf.add_exp(exp_title, exp_company, exp_location, exp_date, exp_bullets)

    pdf.section_title("Skills")
    pdf.add_skills(skills_list)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            st.download_button("📄 Download Resume PDF", f, file_name="resume.pdf", mime="application/pdf")

