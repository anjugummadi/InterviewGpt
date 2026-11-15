import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()


def get_groq_client():
    """
    Initializes and returns the Groq client securely from environment variables.
    Checks system environment variables first, then Streamlit secrets if running inside Streamlit.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            pass

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Please set your GROQ_API_KEY in a .env file "
            "or as an environment variable before running evaluation."
        )

    return Groq(api_key=api_key)


def evaluate_answer(question, answer):
    """
    Evaluates candidate's answer using Groq LLM API.
    """
    try:
        client = get_groq_client()
    except Exception as err:
        return f"⚠️ **Configuration Error:** {str(err)}"

    prompt = f"""
You are a Senior Technical Interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer and provide:

1. Technical Score (out of 10)
2. Communication Score (out of 10)
3. Strengths
4. Weaknesses
5. Missing Concepts
6. Improved Answer
7. Final Recommendation

Provide detailed feedback.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an expert interviewer specializing in:

- Python
- SQL
- Machine Learning
- Deep Learning
- NLP
- Generative AI
- RAG
- LangChain

Provide professional interview feedback.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as err:
        return f"⚠️ **Groq API Error:** {str(err)}"


if __name__ == "__main__":

    print("=" * 70)
    print("INTERVIEW ANSWER EVALUATOR")
    print("=" * 70)

    question = input(
        "\nEnter Interview Question:\n\n"
    )

    answer = input(
        "\nEnter Candidate Answer:\n\n"
    )

    result = evaluate_answer(
        question,
        answer
    )

    print("\n")
    print("=" * 70)
    print("INTERVIEW EVALUATION REPORT")
    print("=" * 70)
    print(result)
