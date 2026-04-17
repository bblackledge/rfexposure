from xhtml2pdf import pisa
from icecream import ic


def convert_html_to_pdf(source_html, output_filename):
    # Open output file for writing (truncated binary)
    with open(output_filename, "wb") as output_file:
        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(source_html, dest=output_file)

    # Return True on success and False on errors
    return pisa_status.err


def append_documents(html_content):
    # Ensure the HTML content is properly structured

    # Output PDF file name
    output_pdf = "output.pdf"

    # Convert the combined HTML content to a single PDF
    # combined_html_content = html_content + '<pdf:nextpage />' + html_content
    result = convert_html_to_pdf(html_content, output_pdf)

    if result == 0:
        return "PDF created successfully"
    else:
        return f"Error occurred while creating PDF. Error code: {result}"
