
import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key="YOUR_API_KEY")

st.title("AI Resume & Job Matcher")

resume = st.text_area("Paste Resume")
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze"):
    prompt = f"""
You are an advanced Applicant Tracking System (ATS) and senior hiring manager.

RESUME:
{resume}

JOB DESCRIPTION:
{job_desc}

Return output in STRICT JSON:

{{
  "match_score": number,
  "matched_skills": [],
  "missing_skills": [],
  "resume_improvements": [],
  "keyword_gaps": [],
  "summary": ""
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    output = response.choices[0].message.content

    try:
        result = json.loads(output)
        st.success(f"Match Score: {result['match_score']}%")
        st.write("Matched Skills:", result["matched_skills"])
        st.write("Missing Skills:", result["missing_skills"])
        st.write("Improvements:", result["resume_improvements"])
        st.write("Keyword Gaps:", result["keyword_gaps"])
        st.write("Summary:", result["summary"])
    except:
        st.error("Invalid JSON output. Try again.")
        st.text(output)
