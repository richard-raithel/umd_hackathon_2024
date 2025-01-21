import os
import csv
import pandas as pd
from openai import AzureOpenAI
from docx import Document
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI model and client configuration
model_name = "gpt-4o-2024-08-06"
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

# Load machine names and products from files
def load_data(filename):
    with open(filename, 'r') as file:
        return [line.strip().split(',')[0] for line in file.readlines()]

machines = load_data('data/extract_machines')
products = load_data('data/extract_products')

def extract_answer_key_from_document(document_content, report_name):
    """
    Extracts test data from the document content and formats it as an answer key using the Azure OpenAI API.

    Parameters:
    - document_content (str): The content of the document.
    - report_name (str): The name of the report.

    Returns:
    - answer_key (str): The formatted answer key as a CSV string.
    """
    prompt = (
        "Extract data from the report into CSV format. Each row should have up to 3 ingredients assigned to ing_1, ing_2, and ing_3. "
        "Each row must include: report name, machine, ing_1, ing_2, ing_3, result, and unit. "
        "Strictly follow the format: report name, machine, ing_1, ing_2, ing_3, result, unit. "
        "Exclude double quotes unless part of the data. No headers. Do not modify machine names or units. "
        f"Use only these machines: {', '.join(machines)} and these ingredient combinations: {', '.join(products)}. "
        f"Output data as CSV without extra text or formatting.\n"
        f"Report name: {report_name}\n"
        f"Document content: {document_content}"
    )

    # Call the Azure OpenAI API for chat completions
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the generated text
    response_text = response.choices[0].message.content
    return response_text

def save_answer_key_to_csv(answer_key, output_file_path):
    """
    Saves the generated answer key to a CSV file.

    Parameters:
    - answer_key (str): The answer key in CSV format as a string.
    - output_file_path (str): The path to save the CSV file.
    """
    # Split the answer key into rows
    rows = [row.split(',') for row in answer_key.strip().split('\n')]

    # Save to CSV
    with open(output_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header if the file is empty
        if file.tell() == 0:
            writer.writerow(['report name', 'machine', 'ing_1', 'ing_2', 'ing_3', 'result', 'unit'])
        # Write each row to the CSV
        for row in rows:
            writer.writerow(row)

    print(f"Answer key saved to {output_file_path}")

def process_excel_file(file_path, output_file_path):
    """
    Processes each sheet in an Excel file and extracts the answer key.

    Parameters:
    - file_path (str): The path to the Excel file.
    - output_file_path (str): The path to save the combined answer key CSV.
    """
    xls = pd.ExcelFile(file_path)
    report_name = os.path.splitext(os.path.basename(file_path))[0]

    for sheet_name in xls.sheet_names:
        sheet_data = pd.read_excel(xls, sheet_name=sheet_name).to_string(index=False)
        print(f"Processing sheet: {sheet_name} from {file_path}...")

        # Extract answer key from sheet data
        answer_key = extract_answer_key_from_document(sheet_data, f"{report_name}")

        # Save the answer key to the CSV file
        save_answer_key_to_csv(answer_key, output_file_path)

def process_word_file(file_path, output_file_path):
    """
    Processes a Word document (.docx) and extracts the answer key.

    Parameters:
    - file_path (str): The path to the Word file.
    - output_file_path (str): The path to save the combined answer key CSV.
    """
    document = Document(file_path)
    report_name = os.path.splitext(os.path.basename(file_path))[0]

    # Extract text from the Word document
    document_content = "\n".join([para.text for para in document.paragraphs])
    print(f"Processing {file_path}...")

    # Extract answer key from document content
    answer_key = extract_answer_key_from_document(document_content, report_name)

    # Save the answer key to the CSV file
    save_answer_key_to_csv(answer_key, output_file_path)

def process_pdf_file(file_path, output_file_path):
    """
    Processes a PDF file and extracts the answer key.

    Parameters:
    - file_path (str): The path to the PDF file.
    - output_file_path (str): The path to save the combined answer key CSV.
    """
    reader = PdfReader(file_path)
    report_name = os.path.splitext(os.path.basename(file_path))[0]

    # Extract text from each page in the PDF
    document_content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    print(f"Processing {file_path}...")

    # Extract answer key from document content
    answer_key = extract_answer_key_from_document(document_content, report_name)

    # Save the answer key to the CSV file
    save_answer_key_to_csv(answer_key, output_file_path)

def process_folder_of_documents(folder_path, output_file_path):
    """
    Processes all documents in a folder, extracts the answer key data, and saves it to a CSV file.

    Parameters:
    - folder_path (str): Path to the folder containing the documents.
    - output_file_path (str): Path to save the combined answer key CSV.
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            if file_name.endswith(('.xlsx', '.xls')):
                # Handle Excel files
                process_excel_file(file_path, output_file_path)
            elif file_name.endswith('.docx'):
                # Handle Word files
                process_word_file(file_path, output_file_path)
            elif file_name.endswith('.pdf'):
                # Handle PDF files
                process_pdf_file(file_path, output_file_path)
            else:
                # Handle text files
                with open(file_path, 'r', encoding='utf-8') as file:
                    document_content = file.read()
                    report_name = os.path.splitext(file_name)[0]
                    print(f"Processing {file_name}...")

                    # Extract answer key from document content
                    answer_key = extract_answer_key_from_document(document_content, report_name)

                    # Save the answer key to the CSV file
                    save_answer_key_to_csv(answer_key, output_file_path)

# Example usage
folder_path = 'synthetic_files/reports_2024-09-26_00-06-13'  # Replace with the path to your folder of documents
output_file_path = 'combined_answer_key.csv'  # Define the path to save the combined answer key CSV

import time

# Start timing
start_time = time.time()

# Process all documents in the folder
process_folder_of_documents(folder_path, output_file_path)

# Calculate the total runtime
total_runtime = time.time() - start_time
num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

# Print total and average time per document
print(f"Total time to process all documents: {total_runtime:.2f} seconds.")
if num_files > 0:
    print(f"Average time per document: {total_runtime / num_files:.2f} seconds.")
else:
    print("No files were processed.")
