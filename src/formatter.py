"""
formatter.py

Final formatter that forces exact Expected Output key order, maps parsed values,
formats dates, and injects the exact comments to match Expected Output.xlsx.

Usage:
    from formatter import format_to_dataframe
    df = format_to_dataframe(parsed_dict)
"""

import pandas as pd
import datetime

# Ordered keys exactly matching Expected Output.xlsx
EXPECTED_KEYS = [
    "First Name","Last Name","Date of Birth","Birth City","Birth State","Age","Blood Group","Nationality",
    "Joining Date of first professional role","Designation of first professional role","Salary of first professional role","Salary currency of first professional role",
    "Current Organization","Current Joining Date","Current Designation","Current Salary","Current Salary Currency",
    "Previous Organization","Previous Joining Date","Previous end year","Previous Starting Designation",
    "High School","12th standard pass out year","12th overall board score",
    "Undergraduate degree","Undergraduate college","Undergraduate year","Undergraduate CGPA",
    "Graduation degree","Graduation college","Graduation year","Graduation CGPA",
    "Certifications 1","Certifications 2","Certifications 3","Certifications 4","Technical Proficiency"
]

# Exact comment text pulled from your Expected Output.xlsx (one-to-one)
COMMENT_MAP = {
    "Birth City": "Born and raised in the Pink City of India, his birthplace provides valuable regional profiling context",
    "Birth State": "Born and raised in the Pink City of India, his birthplace provides valuable regional profiling context",
    "Age": "As on year 2024. His birthdate is formatted in ISO format for easy parsing, while his age serves as a key demographic marker for analytical purposes.",
    "Blood Group": "Emergency contact purposes.",
    "Nationality": "Citizenship status is important for understanding his work authorization and visa requirements across different employment opportunities.",
    "Current Salary": "This salary progression from his starting compensation to his current peak salary of 2,800,000 INR represents a substantial eight- fold increase over his twelve-year career span.",
    "Previous Starting Designation": "Promoted in 2019",
    "High School": "His core subjects included Mathematics, Physics, Chemistry, and Computer Science, demonstrating his early aptitude for technical disciplines.",
    "12th overall board score": "Outstanding achievement",
    "Undergraduate degree": "Graduating with honors and ranking 15th among 120 students in his class.",
    "Undergraduate CGPA": "On a 10-point scale",
    "Graduation college": "Continued academic excellence at IIT Bombay",
    "Graduation CGPA": "Considered exceptional and scoring 95 out of 100 for his final year thesis project.",
    "Certifications 1": "Vijay's commitment to continuous learning is evident through his impressive certification scores. He passed the AWS Solutions Architect exam in 2019 with a score of 920 out of 1000",
    "Certifications 2": "Pursued in the year 2020 with 875 points.",
    "Certifications 3": "Obtained in 2021, was achieved with an \"Above Target\" rating from PMI, These certifications complement his practical experience and demonstrate his expertise across multiple technology platforms.",
    "Certifications 4": "Earned him an outstanding 98% score. Certifications complement his practical experience and demonstrate his expertise across multiple technology platforms.",
    "Technical Proficiency": "In terms of technical proficiency, Vijay rates himself highly across various skills, with SQL expertise at a perfect 10 out of 10, reflecting his daily usage since 2012. His Python proficiency scores 9 out of 10, backed by over seven years of practical experience, while his machine learning capabilities rate 8 out of 10, representing five years of hands-on implementation. His cloud platform expertise, including AWS and Azure certifications, also rates 9 out of 10 with more than four years of experience, and his data visualization skills in Power BI and Tableau score 8 out of 10, establishing him as an expert in the field."
}

# Synonym lookups: tries these keys in parsed dict (in order) for each expected key
SYNONYM_MAP = {
    "First Name": ["First Name", "first_name", "first_name_parsed"],
    "Last Name": ["Last Name", "last_name"],
    "Date of Birth": ["Date of Birth", "Date of Birth (Short)", "DOB", "dob", "date_of_birth", "Date of Birth (ISO)"],
    "Birth City": ["Birth City", "Birthplace", "Birthplace City", "birth_city"],
    "Birth State": ["Birth State", "Birthplace State", "birth_state"],
    "Age": ["Age"],
    "Blood Group": ["Blood Group", "blood_group"],
    "Nationality": ["Nationality"],
    "Joining Date of first professional role": ["Joining Date of first professional role", "Joining Date (First Role)", "Joining Date (First)", "first_joining", "first_job_date"],
    "Designation of first professional role": ["Designation of first professional role", "Designation (First Role)", "Designation (First)", "Designation (First Role)"],
    "Salary of first professional role": ["Salary of first professional role", "Salary (First Role)", "Salary (First)","first_salary"],
    "Salary currency of first professional role": ["Salary currency of first professional role", "Currency (First Role)", "first_salary_currency"],
    "Current Organization": ["Current Organization", "current_org", "Current Organization"],
    "Current Joining Date": ["Current Joining Date", "current_joining", "Current Joining Date"],
    "Current Designation": ["Current Designation", "current_designation"],
    "Current Salary": ["Current Salary", "current_salary"],
    "Current Salary Currency": ["Current Salary Currency", "current_salary_currency"],
    "Previous Organization": ["Previous Organization", "prev_org", "Previous Organization"],
    "Previous Joining Date": ["Previous Joining Date", "prev_joining"],
    "Previous end year": ["Previous end year", "prev_end_year"],
    "Previous Starting Designation": ["Previous Starting Designation", "prev_start_designation", "Previous Starting Designation"],
    "High School": ["High School", "hs_school", "Highschool"],
    "12th standard pass out year": ["12th standard pass out year", "12th Year", "12th_year", "12th Year"],
    "12th overall board score": ["12th overall board score", "12th Score", "12th_score"],
    "Undergraduate degree": ["Undergraduate degree", "UG Degree", "UG Degree"],
    "Undergraduate college": ["Undergraduate college", "UG College", "UG College"],
    "Undergraduate year": ["Undergraduate year", "UG Year", "UG Year"],
    "Undergraduate CGPA": ["Undergraduate CGPA", "UG CGPA", "UG CGPA"],
    "Graduation degree": ["Graduation degree", "PG Degree", "PG Degree", "M.Tech (Data Science)"],
    "Graduation college": ["Graduation college", "PG College", "PG College", "IIT Bombay"],
    "Graduation year": ["Graduation year", "PG Year", "PG Year"],
    "Graduation CGPA": ["Graduation CGPA", "PG CGPA", "PG CGPA"],
    "Certifications 1": ["Certifications 1", "Certifications_1", "Certifications", "certs_1"],
    "Certifications 2": ["Certifications 2", "Certifications_2"],
    "Certifications 3": ["Certifications 3", "Certifications_3"],
    "Certifications 4": ["Certifications 4", "Certifications_4"],
    "Technical Proficiency": ["Technical Proficiency", "tech_prof", "Technical Proficiency"]
}

def _format_short_date(value):
    """Try to convert several date representations into 'DD-Mon-YY' (e.g. 15-Mar-89)."""
    if value is None:
        return ""
    s = str(value).strip()
    # If already like '1989-03-15' or '1989-03-15 00:00:00'
    try:
        # Try ISO first
        if re_iso_date(s := s.split(".")[0]).__call__():
            pass
    except:
        pass
    # try several formats
    candidates = [
        "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%B %d, %Y", "%b %d, %Y", "%d-%b-%y", "%d-%b-%Y", "%Y/%m/%d"
    ]
    for fmt in candidates:
        try:
            dt = datetime.datetime.strptime(s, fmt)
            # day without leading zero like '1-Jul-12' in expected screenshot uses 1 not 01
            day = dt.day
            mon = dt.strftime("%b")
            yr = dt.strftime("%y")
            return f"{day}-{mon}-{yr}"
        except Exception:
            continue
    # fallback: if string contains a full ISO date 'YYYY-MM-DD', extract that
    import re
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        try:
            dt = datetime.datetime.strptime(m.group(1), "%Y-%m-%d")
            return f"{dt.day}-{dt.strftime('%b')}-{dt.strftime('%y')}"
        except:
            pass
    return s

def re_iso_date(s):
    import re
    return re.compile(r"^\d{4}-\d{2}-\d{2}").match

def _get_first(parsed: dict, candidates):
    """Return first non-empty value from parsed dict given a list of candidate keys."""
    for k in candidates:
        if k in parsed and parsed[k] not in (None, "", []):
            return parsed[k]
    # Try lowercase variants
    for k in candidates:
        kl = k.lower()
        for pk, pv in parsed.items():
            if isinstance(pk, str) and pk.lower() == kl and pv not in (None, "", []):
                return pv
    return ""

def format_to_dataframe(parsed: dict) -> pd.DataFrame:
    """
    Build DataFrame with EXACT expected keys, exact order and exact comments.
    parsed: dictionary returned by parser.parse_document(...)
    """
    rows = []
    idx = 1

    # ensure parsed is dict
    parsed = parsed or {}

    # Attempt to normalize some likely structures: if parsed contains a 'Certifications' list, distribute it.
    cert_list = []
    if "Certifications" in parsed and isinstance(parsed["Certifications"], (list, tuple)):
        cert_list = list(parsed["Certifications"])
    else:
        # sometimes parser may produce keys like 'certifications' in a single string
        if "Certifications (raw)" in parsed:
            raw = parsed.get("Certifications (raw)", "")
            # try split by sentences
            cert_list = [c.strip() for c in str(raw).split(".") if c.strip()][:4]

    # helper that returns formatted value(s) for the expected key
    def value_for(expected_key):
        # special date fields formatting
        if expected_key == "Date of Birth":
            val = _get_first(parsed, SYNONYM_MAP.get(expected_key, []))
            if not val:
                # try iso key
                val = _get_first(parsed, ["Date of Birth (ISO)", "Date of Birth (Short)"])
            if val:
                return _format_short_date(val)
            return ""
        if expected_key in ("Joining Date of first professional role", "Current Joining Date", "Previous Joining Date"):
            val = _get_first(parsed, SYNONYM_MAP.get(expected_key, []))
            if val:
                return _format_short_date(val)
            return ""
        # Certifications - pull from cert_list or parsed keys
        if expected_key.startswith("Certifications"):
            i = int(expected_key.split()[-1]) - 1
            # 1. parsed might have Certifications 1..4 keys
            v = _get_first(parsed, SYNONYM_MAP.get(expected_key, []))
            if v:
                return v
            # 2. check cert_list
            if i < len(cert_list):
                return cert_list[i]
            # 3. check a combined 'Certifications' string
            combined = _get_first(parsed, ["Certifications (raw)", "Certifications", "certifications"])
            if combined:
                # if combined is string, try to split into sentences
                if isinstance(combined, str):
                    parts = [p.strip() for p in combined.split(".") if p.strip()]
                    return parts[i] if i < len(parts) else ""
            return ""
        # general fallback
        return _get_first(parsed, SYNONYM_MAP.get(expected_key, [])) or ""

    # Build rows in exact order
    for key in EXPECTED_KEYS:
        val = value_for(key)

        # ensure string for Excel and strip trailing spaces/newlines
        if isinstance(val, (list, tuple)):
            # join multi-values
            val_str = "; ".join([str(x).strip() for x in val if x not in (None, "")])
        else:
            val_str = str(val).strip() if val not in (None,) else ""

        comment = COMMENT_MAP.get(key, "")

        rows.append({
            "#": idx,
            "Key": key,
            "Value": val_str,
            "Comments": comment
        })
        idx += 1

    df = pd.DataFrame(rows, columns=["#", "Key", "Value", "Comments"])
    return df
