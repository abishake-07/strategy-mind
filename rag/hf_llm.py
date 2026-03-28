"""Answer generation via Hugging Face Inference API (OpenAI-compatible).

Sends the assembled context prompt to a hosted HF model and returns the generated answer.
"""
import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

_DEFAULT_MODEL = os.getenv("HUGGINGFACE_MODEL", "Qwen/Qwen2.5-7B-Instruct:together").strip()
_HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()


def generate(prompt: str, model: str = None, max_tokens: int = 1024) -> str:
    """Call the HF Inference API (OpenAI-compatible) with the assembled prompt and return the generated answer."""
    model = (model or _DEFAULT_MODEL).strip()
    print(f"[DEBUG] Using model: {model}", file=sys.stderr)
    print(f"[DEBUG] Token set: {'Yes' if _HF_API_KEY else 'No'}", file=sys.stderr)

    system_prompt = """You are a strategic consulting assistant specialized in business intelligence and competitive analysis.

Your role:
- Synthesize complex business strategy data into actionable insights
- Combine knowledge graph intelligence with research document evidence
- Provide consulting-style recommendations with specific, measurable outcomes
- Highlight strategic gaps, opportunities, and risks
- Reference specific KPIs and playbooks when relevant

Output format:
- Start with Executive Summary
- Provide Key Impacts/Findings with supporting evidence
- Include Recommended Actions with implementation priorities
- End with Metrics to Track

Tone: Professional, data-driven, consulting-style (not academic)
"""

    try:
        client = InferenceClient(api_key=_HF_API_KEY)
        print(f"[DEBUG] InferenceClient created", file=sys.stderr)

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )

        text = completion.choices[0].message.content
        print(f"[DEBUG] Generated {len(text)} chars", file=sys.stderr)
        return text.strip()
    except Exception as e:
        print(f"[ERROR] HF API failed: {type(e).__name__}: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise
