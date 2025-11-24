"""
export_excel.py
Exports the structured DataFrame and raw text into an Excel file.
"""

import pandas as pd
from pathlib import Path

def export_to_excel(df, raw_text, output_path):
    """
    Writes 2 sheets:
    1. Output (structured)
    2. RawText (full PDF text)
    """

    p = Path(output_path)

    with pd.ExcelWriter(p, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Output", index=False)
        pd.DataFrame({"RawText": [raw_text]}).to_excel(writer, sheet_name="RawText", index=False)

    return str(p.resolve())
