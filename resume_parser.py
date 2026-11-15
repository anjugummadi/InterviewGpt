import pdfplumber


def extract_resume_text(pdf_path):
    """
    Extract text from uploaded resume PDF
    """

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    except Exception as e:
        return f"Error reading PDF: {str(e)}"


if __name__ == "__main__":

    import os
    sample_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_resume.pdf")
    if os.path.exists(sample_pdf):
        text = extract_resume_text(sample_pdf)
        print(text[:1000])
    else:
        print("Resume parser module ready. Place a sample PDF to test standalone.")