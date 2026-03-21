
from openai import AsyncOpenAI
from ..config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_with_llm(log_summary: str):
    prompt = f"""
Return ONLY valid JSON (no markdown).

Schema:
{{
  "primary_issue": string,
  "severity": string,
  "probable_root_cause": string,
  "recommended_actions": string[],
  "confidence_score": float
}}

Log summary:
{log_summary}
"""

    response = await client.chat.completions.create(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are a senior site reliability engineer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content
