AI-Powered Document Structuring & Data Extraction

This project is an AI-assisted system that converts unstructured PDF documents into clean, structured Excel outputs. It automatically extracts key:value information, detects contextual notes, and formats everything according to the expected output format.
Deployed live using Streamlit Cloud.

🚀 Live Demo

👉 Streamlit App:
https://ai-document-structuring-ddykmgwntnu5q2rxkg5gpp.streamlit.app/

Upload any PDF and generate structured Excel output instantly.

📄 Project Overview

This tool reads unorganized or semi-structured document data and transforms it into a structured spreadsheet. It ensures:

Accurate extraction of all PDF content

Key:value relationship detection

Context-based comment generation

Clean Excel output identical to the expected format

100% retention of original wording (no paraphrasing)

🧠 Features

📤 Upload unstructured PDF

🧩 Extract key:value pairs

📝 Auto-generate contextual "Comments"

📊 Export to Excel in required format

🔍 Preserve all wording from the PDF

🌐 Fully deployed on Streamlit Cloud

🧱 Modular architecture (extract, parse, format, export)

📂 Folder Structure
AI Document Structuring/
│
├── src/
│   ├── extractor.py        # Extracts text from PDF
│   ├── parser.py           # Identifies key:value pairs
│   ├── formatter.py        # Builds final structured rows
│   ├── export_excel.py     # Writes Excel files
│   └── app.py              # Streamlit UI
│
├── requirements.txt
├── Data Input.pdf          # Sample input
└── Expected Output.xlsx    # Sample output format

🛠️ Tech Stack

Python

pdfplumber

pandas

openpyxl

Streamlit

🧪 How to Run Locally
git clone https://github.com/<your-username>/AI-Document-Structuring.git
cd "AI Document Structuring"

pip install -r requirements.txt
streamlit run src/app.py

📌 Usage

Open the live Streamlit link

Upload your PDF file

View the extracted structured table

Download Output.xlsx

The system ensures no missing data, no summarization, and complete accuracy.

📝 About the Assignment

This project fulfills the requirement to:

Convert unstructured PDF → structured Excel

Capture 100% of content

Maintain original language

Include contextual comments

Host a live working demo

Provide a GitHub repository with source code

👤 Author

Om Ghope
AI Intern — Document Structuring Assignment
omgghope26@gmail.com
