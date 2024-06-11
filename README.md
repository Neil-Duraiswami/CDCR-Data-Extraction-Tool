# CDCR-Data-Extraction-Tool

The CDCR Data Extraction Tool is a Python application designed to automate the extraction of inmate data from the [California Department of Corrections and Rehabilitation (CDCR) website](https://apps.cdcr.ca.gov/ciris). It provides a user-friendly interface for inputting CDCR numbers and generates Excel reports containing the extracted inmate information.

## Purpose

The purpose of this tool is to streamline the process of gathering inmate information from the CDCR website. It eliminates the need for manual data entry and allows users to quickly retrieve essential information about inmates using their CDCR numbers.

## Methodology

The tool utilizes web scraping technique known as "browser automation" or "headless browsing" with the Selenium framework to extract inmate data from the CDCR website. Upon entering a CDCR number, the application navigates to the inmate search page, enters the provided CDCR number, and retrieves relevant information such as the inmate's name, CDCR number, age, admission date, current location, and commitment county. This information is then formatted into a DataFrame and saved into an Excel file for further analysis or record-keeping.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Edge WebDriver (Download and specify the correct path in the code or set it as a system variable)
- Internet connection

## Installation

1. Clone the repository: `https://github.com/Neil-Duraiswami/CDCR-Data-Extraction-Tool.git`
2. Navigate to the project directory: `cd CDCR-Data-Extraction-Tool`


## Usage

1. **Configure WebDriver:**
    - Download the Edge WebDriver suitable for your system from the official website.
    - **Option 1:** Specify the path in the code:
        ```python
        service = EdgeService(executable_path='C:/path/to/your/msedgedriver.exe')
        ```
    - **Option 2:** Add WebDriver directory to the system PATH:
        - Extract the WebDriver executable to a directory.
        - Add this directory to your system's PATH environment variable.

2. Run the application: `python cdcr_scraper.py`
3. Enter the CDCR Number of the inmate you wish to retrieve data for.
4. Click the "Start Scraping" button to initiate the data extraction process.
5. The application will extract the inmate data and save it to an Excel file named `cdcr_data.xlsx`.

## Requirements

The following Python libraries are required to run the application:

- tkinter
- selenium
- pandas


## Disclaimer

This tool is intended for educational and research purposes only. Use it responsibly and in compliance with all applicable laws and regulations.

