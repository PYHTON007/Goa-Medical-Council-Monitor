from pathlib import Path

from openai import OpenAI
from pypdf import PdfReader

from config import OPENAI_API_KEY


# GPT-5.6 Luna pricing
INPUT_COST_PER_MILLION = 1.00
OUTPUT_COST_PER_MILLION = 6.00


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract readable text from a PDF."""

    reader = PdfReader(str(pdf_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages).strip()


def summarize_pdf(pdf_path: Path):
    """
    Generate an AI summary of the PDF and return
    both the summary and API usage information.
    """

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    text = extract_pdf_text(pdf_path)

    if not text:
        return {
            "summary": (
                "⚠️ The PDF was updated, but I could not "
                "extract readable text from it."
            ),
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "cost": 0.0,
        }

    # Keep API usage under control while retaining
    # enough of the document for an accurate summary.
    max_characters = 20000

    if len(text) > max_characters:
        text = text[:max_characters]

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=(
            "You monitor official Goa Medical Council announcements "
            "for Foreign Medical Graduates and CRMI internship applicants. "
            "Summarize the document accurately and concisely. "
            "Use ONLY information explicitly stated in the document. "
            "Never invent dates, eligibility criteria, requirements, "
            "fees, hospitals, seats, deadlines, or procedures. "
            "Focus on information that materially affects FMGs."
        ),
        input=(
            "Analyze this Goa Medical Council FMG/CRMI document.\n\n"
            "Return a concise but complete Telegram-ready summary using "
            "only information contained in the document. "
            "Keep the summary ideally under 300 words. "
            "Do not repeat information. "
            "Complete every section before ending the response. "
            "If a date, year, number, or other detail is unclear in the "
            "source, reproduce it exactly as written and do not guess "
            "or correct it.\n\n"
            "Use these sections when relevant:\n\n"
            "🚨 WHAT CHANGED\n"
            "- Describe the important changes.\n\n"
            "📅 IMPORTANT DATES\n"
            "- List relevant dates and deadlines.\n\n"
            "📋 KEY REQUIREMENTS\n"
            "- List important eligibility/document requirements.\n\n"
            "🏥 INTERNSHIP / SELECTION DETAILS\n"
            "- Summarize hospitals, seats, selection process, or other "
            "relevant details if present.\n\n"
            "⚠️ IMPORTANT\n"
            "- Mention anything an FMG should be particularly careful "
            "about.\n\n"
            "Omit sections that are not relevant. "
            "Do not speculate.\n\n"
            "DOCUMENT:\n"
            f"{text}"
        ),
        max_output_tokens=500,
    )

    usage = response.usage

    input_tokens = usage.input_tokens or 0
    output_tokens = usage.output_tokens or 0
    total_tokens = usage.total_tokens or 0

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_COST_PER_MILLION

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_COST_PER_MILLION

    total_cost = input_cost + output_cost

    return {
        "summary": response.output_text.strip(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost": total_cost,
    }