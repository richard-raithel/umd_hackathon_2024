# Synthetic File Generator and Data Analysis Tools

## Overview

This repository provides tools for generating synthetic test reports in Word, Excel, and PDF formats, along with scripts for analyzing and visualizing machine and product data. It includes an API example, data extraction utilities, and integration with OpenAI for text generation and text-to-speech capabilities.

---

## Features

### Synthetic File Generation
- **File Formats**:
  - Generate synthetic reports in Word (`.docx`), Excel (`.xlsx`), and PDF (`.pdf`) formats.
  - Reports include realistic content such as tables, paragraphs, and lists.

- **Randomized Test Data**:
  - Use randomized machine names, product names, and test results.
  - Ensure unique content across documents.

- **Master CSV File**:
  - Consolidates all test results into a single `master_test_results.csv` file for data analysis.

### Data Analysis and Visualization
- **Plotting Scripts**:
  - `plot_machine_frequency.py`: Visualize machine usage frequency.
  - `plot_viscometer_data.py`: Analyze and plot viscometer data.

### OpenAI Integration
- **API Usage**:
  - `api_example.py`: Demonstrates using the OpenAI API for text generation tasks.
  - `openai_tts_test.py`: Leverages OpenAI for text-to-speech functionality.

### Data Extraction
- **Extract Data**:
  - `extract_data.py`: Extracts and preprocesses data from various sources for use in analysis or report generation.

### Main Applications
- **Main Scripts**:
  - `main.py`: Entry point for generating synthetic reports.
  - `main_gpt.py`: Integrates GPT-based enhancements for synthetic data generation or analysis.

---

## Requirements

### Prerequisites
- Python 3.8 or higher
- OpenAI API key for GPT integration
- Required Python libraries (install via `requirements.txt`):
  - `fpdf`
  - `docx`
  - `xlsxwriter`
  - `pandas`
  - `matplotlib`
  - `Faker`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/synthetic-file-generator.git
   cd synthetic-file-generator
