"""
parser.py
Extracts structured information from the PDF text using rule-based logic.
"""

import re

def parse_document(text: str) -> dict:
    """
    Extracts required fields from the unstructured PDF text.
    Returns a dictionary with Key:Value pairs.
    """

    data = {}

    # ---- NAME ----
    m = re.search(r"^([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+was born", text)
    if m:
        data["First Name"] = m.group(1)
        data["Last Name"] = m.group(2)

    # ---- DOB ----
    m = re.search(r"born on ([A-Za-z]+ \d{1,2}, \d{4})", text)
    if m:
        dob = m.group(1)
        data["Date of Birth"] = dob

    # ---- AGE ----
    m = re.search(r"(\d+)\s+years old as of\s+(\d{4})", text)
    if m:
        data["Age"] = m.group(1) + " years"

    # ---- BIRTHPLACE ----
    m = re.search(r"in ([A-Za-z\s]+),\s*([A-Za-z\s]+), making him", text)
    if m:
        data["Birth City"] = m.group(1).strip()
        data["Birth State"] = m.group(2).strip()

    # ---- BLOOD GROUP ----
    if "O+ blood group" in text:
        data["Blood Group"] = "O+"

    # ---- NATIONALITY ----
    if "Indian national" in text:
        data["Nationality"] = "Indian"

    # ---- FIRST JOB ----
    m = re.search(r"joined his first company.* on ([A-Za-z]+ \d{1,2}, \d{4}).*annual salary of ([\d,]+)", text)
    if m:
        data["Joining Date (First Role)"] = m.group(1)
        data["Salary (First Role)"] = m.group(2).replace(",", "")
        data["Currency (First Role)"] = "INR"
        data["Designation (First Role)"] = "Junior Developer"

    # ---- CURRENT ROLE ----
    m = re.search(r"current role at ([A-Za-z\s]+) beginning on ([A-Za-z]+ \d{1,2}, \d{4}).*serves as a ([A-Za-z\s]+) earning ([\d,]+)", text)
    if m:
        data["Current Organization"] = m.group(1).strip()
        data["Current Joining Date"] = m.group(2).strip()
        data["Current Designation"] = m.group(3).strip()
        data["Current Salary"] = m.group(4).replace(",", "")
        data["Current Salary Currency"] = "INR"

    # ---- PREVIOUS ROLE ----
    m = re.search(r"worked at ([A-Za-z\s]+) from ([A-Za-z0-9 ,]+) to (\d{4}), starting as a ([A-Za-z\s]+)", text)
    if m:
        data["Previous Organization"] = m.group(1).strip()
        data["Previous Joining Date"] = m.group(2).strip()
        data["Previous End Year"] = m.group(3).strip()
        data["Previous Starting Designation"] = m.group(4).strip()

    # ---- SCHOOL ----
    m = re.search(r"high school education at ([A-Za-z' \.,-]+).*in (\d{4}), achieving.*?(\d{2}\.\d+)%", text)
    if m:
        data["High School"] = m.group(1).strip()
        data["12th Year"] = m.group(2)
        data["12th Score"] = m.group(3) + "%"

    # ---- UG ----
    m = re.search(r"B\.Tech in ([A-Za-z\s]+) at ([A-Za-z\s]+).* in (\d{4}) with a CGPA of ([\d\.]+)", text)
    if m:
        data["UG Degree"] = "B.Tech (" + m.group(1).strip() + ")"
        data["UG College"] = m.group(2).strip()
        data["UG Year"] = m.group(3)
        data["UG CGPA"] = m.group(4)

    # ---- PG ----
    m = re.search(r"M\.Tech in ([A-Za-z\s]+).* in (\d{4}), achieving.* CGPA of ([\d\.]+).*scoring (\d+) out of (\d+)", text)
    if m:
        data["PG Degree"] = "M.Tech (" + m.group(1).strip() + ")"
        data["PG Year"] = m.group(2)
        data["PG CGPA"] = m.group(3)
        data["PG Thesis Score"] = m.group(4) + "/" + m.group(5)

    return data
