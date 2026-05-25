from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_email(subject, sender):
    prompt = f"""
You are a job application tracker.

Extract structured info from this email.

Rules:
 - Infer company from sender email domain or body or subject
 - Infer role from subject or body
 - Confidence is between 0.0 and 1.0
 - Valid status: applied, rejected, interview, assessment, offer, other
 - Default to "unknown" if role or company cannot be inferred

Return ONLY valid JSON.

Schema:
{{
  "company": "...",
  "role": "...",
  "status": "applied | rejected | interview | assessment | offer | other",
  "confidence": 0.0
}}

Email:
Subject: {subject}
From: {sender}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured job application data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
