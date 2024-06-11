import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import pandas as pd
import time

entry = None

def scrape_data(cdcr_number):
    try:
        # Setup Edge options
        edge_options = Options()
        # Commenting out the headless option to see the browser actions
        # edge_options.add_argument("--headless")  # Runs Edge in headless mode.

        # Setup the Edge driver, specify the correct path to your edgedriver
        service = EdgeService(executable_path='C:/edgedriver_win64/msedgedriver.exe')
        driver = webdriver.Edge(service=service, options=edge_options)

        # Navigate to the search page
        driver.get("https://apps.cdcr.ca.gov/ciris/search")

        # Wait for the CLOSE button to become clickable
        close_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[5]/div/button"))
        )
        close_button.click()

        # Wait for the Agree button to become clickable
        agree_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/div/main/div/div/div/div[3]/button"))
        )
        # Add a short delay before clicking the Agree button
        time.sleep(2)
        
        agree_button.click()

        # Wait for the CDCR Number button to become clickable
        cdcr_number_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div[2]/form/div/div[1]/div/div/div/div[2]"))
        )
        cdcr_number_button.click()

        # Enter the CDCR Number
        cdcr_input = driver.find_element(By.ID, "input-23")
        cdcr_input.send_keys(cdcr_number)

        # Click the Search button
        search_button = driver.find_element(By.XPATH, "//span[text()='search']")
        search_button.click()

        # Wait for results to load
        time.sleep(5)  # Adjust the sleep time if necessary for your internet speed

        # Check if "No Results" text appears
        no_results_text = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div[2]/div/div/div[1]/p[1]")
        if no_results_text and no_results_text[0].text == "No Results":
            # If "No Results" text is found, create a DataFrame with all entries marked as 'NAN' and exit
            df = pd.DataFrame({"First Name": ["NAN"],
                               "Middle Name": ["NAN"],
                               "Last Name": ["NAN"],
                               "CDCR Number": ["NAN"],
                               "Age": ["NAN"],
                               "Admission Date": ["NAN"],
                               "Current Location": ["NAN"],
                               "Commitment County": ["NAN"]})
            
            # Save the DataFrame to an Excel file
            df.to_excel("cdcr_data.xlsx", index=False)

            messagebox.showinfo("Info", "No results found. Excel sheet created with 'NAN' values.")
        else:

            # Extracting the data
            name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[1]").text
            cdcr_number = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]").text
            age = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[3]").text
            admission_date = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[4]").text
            current_location = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[5]").text
            commitment_county = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[6]").text

            # Split the name into parts
            name_parts = name.split(",")
            if len(name_parts) == 2:
                # Split the second part further to separate first name and middle name
                name_parts_second_part = name_parts[1].strip().split()
                if len(name_parts_second_part) == 1:
                    first_name = name_parts_second_part[0]
                    middle_name = ""
                else:
                    first_name = name_parts_second_part[0]
                    middle_name = " ".join(name_parts_second_part[1:])
                last_name = name_parts[0].strip()
            elif len(name_parts) == 3:
                # If there are three parts, assume first part is last name, second part is first name, and third part is middle name
                last_name = name_parts[0].strip()
                first_name = name_parts[1].strip()
                middle_name = name_parts[2].strip()
            else:
                # Handle cases where the name format is unexpected
                first_name = ""
                middle_name = ""
                last_name = ""

            # Create a dictionary with the data
            data = { 
                "First Name": first_name,
                "Middle Name": middle_name,
                "Last Name": last_name,
                "CDCR Number": cdcr_number,
                "Age": age,
                "Admission Date": admission_date,
                "Current Location": current_location,
                "Commitment County": commitment_county
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame([data])

        # Save the DataFrame to an Excel file
        df.to_excel("cdcr_data.xlsx", index=False)

        messagebox.showinfo("Success", "Data has been saved to cdcr_data.xlsx")
        pass
        # Display the scraped data in a pop-up
        message = f"First Name: {first_name}\n" \
                  f"Middle Name: {middle_name}\n" \
                  f"Last Name: {last_name}\n" \
                  f"CDCR Number: {cdcr_number}\n" \
                  f"Age: {age}\n" \
                  f"CDCR Admission Date: {admission_date}\n" \
                  f"Current Location: {current_location}\n" \
                  f"Commitment County: {commitment_county}"

        messagebox.showinfo("Scraped Data", message)    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        driver.quit()

def start_scraping():
    cdcr_number = entry.get()
    if not cdcr_number or not (any(char.isdigit() for char in cdcr_number) and any(char.isalpha() for char in cdcr_number)) or len(cdcr_number) != 6:
        # If CDCR Number is not provided, doesn't contain both a digit and an alphabet character, or not of length 6,
        # create a DataFrame with all entries marked as 'NAN' and exit
        df = pd.DataFrame({"First Name": ["NAN"],
                           "Middle Name": ["NAN"],
                           "Last Name": ["NAN"],
                           "CDCR Number": ["NAN"],
                           "Age": ["NAN"],
                           "Admission Date": ["NAN"],
                           "Current Location": ["NAN"],
                           "Commitment County": ["NAN"]})

        # Save the DataFrame to an Excel file
        df.to_excel("cdcr_data.xlsx", index=False)

        messagebox.showinfo("Info", "Invalid or missing CDCR Number. Excel sheet created with 'NAN' values.")
    else:
        scrape_data(cdcr_number)


def scrape_with_gui():
    root = tk.Tk()
    root.title("CDCR Data Scraper")
    root.geometry("300x200")

    label = tk.Label(root, text="Enter CDCR Number:", font=("Arial", 12))
    label.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 12), width=20)
    entry.pack()

    def start_scraping():
        cdcr_number = entry.get()
        if not cdcr_number or not (any(char.isdigit() for char in cdcr_number) and any(char.isalpha() for char in cdcr_number)) or len(cdcr_number) != 6:
            # If CDCR Number is not provided, doesn't contain both a digit and an alphabet character, or not of length 6,
            # create a DataFrame with all entries marked as 'NAN' and exit
            df = pd.DataFrame({"First Name": ["NAN"],
                               "Middle Name": ["NAN"],
                               "Last Name": ["NAN"],
                               "CDCR Number": ["NAN"],
                               "Age": ["NAN"],
                               "Admission Date": ["NAN"],
                               "Current Location": ["NAN"],
                               "Commitment County": ["NAN"]})

            # Save the DataFrame to an Excel file
            df.to_excel("cdcr_data.xlsx", index=False)

            messagebox.showinfo("Info", "Invalid or missing CDCR Number. Excel sheet created with 'NAN' values.")
        else:
            scrape_data(cdcr_number)

    button = tk.Button(root, text="Start Scraping", font=("Arial", 12), command=start_scraping)
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    scrape_with_gui()

