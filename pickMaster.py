import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import os
# Function to scrape data under the specified headers and text surrounded by <strong> tags
def scrape_data_under_over_under(url, header_texts):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}  # Store the scraped data as a dictionary

        for header_text in header_texts:
            header_tags = soup.find_all('a', text=header_text)

            for header_tag in header_tags:
                # Find the next <strong> element within the same <h2> section
                strong_element = header_tag.find_next('strong')

                if strong_element:
                    # Extract the text within <strong> tags
                    strong_text = strong_element.text.strip()
                else:
                    strong_text = ""

                # Find the text under the <h2> section until the next similar link
                text_under_header = []
                next_element = header_tag.find_next_sibling()

                while next_element and next_element.name != 'a':
                    text_under_header.append(next_element.get_text().strip())
                    next_element = next_element.find_next_sibling()

                # Store the data in the dictionary with a unique key for each section
                data[f'{header_text}_{strong_text}'] = "\n".join(text_under_header) + " (Sports Book Wire)"

        return data
    else:
        print("Failed to retrieve data from {}".format(url))
        return {}

def scrape_data_azcentral(url, class_name3):
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        elements_with_class = soup.find_all('p', class_=class_name3)

        for i, element in enumerate(elements_with_class, 1):

            data[element.text.strip()] = element.text.strip() + "AZ Central Prediction"
        return data
    else:
        print("Failed to retrieve data from {}".format(url))
        return {}


# Function to scrape data from elements with a specific class
def scrape_data_with_class(url, class_name1):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}  # Store the scraped data as a dictionary

        # Find all elements with the specified class
        elements_with_class = soup.find_all('span', class_=class_name1)

        for i, element in enumerate(elements_with_class, 1):
            # Use the text as the header and the element text as the value
            data[element.text.strip()] = element.text.strip() + " (Covers Free Picks)"

        return data
    else:
        print("Failed to retrieve data from {}".format(url))
        return {}

def picks_type_scrape(url, pick_type):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pickType = {}

        elements_with_class = soup.find_all('span', class_=pick_type)

        for i, element in enumerate(elements_with_class, 1):
            pickType[element.text.strip()] = element.text.strip()
        
        return pickType
    else:
        print("Failed to retrieve pick type from {}".format(url))
        return {}

def picks_wise_scrape(url, class_name2, pickType):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        elements_with_class = soup.find_all(class_=class_name2)

        
        for i, element in enumerate(elements_with_class, 1):
                data[element.text.strip()] = element.text.strip() + "{}".format(pickType)
    
        return data
        
    else:
        print("Failed to retrieve data from {}".format(url))
        return{}

# Function to create an Excel file
def create_excel_file(data, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Scraped Data"

    # Write headers to the Excel file
    headers = ["Header", "Value"]
    ws.append(headers)

    # Write scraped data to the Excel file
    for header, value in data.items():
        ws.append([header, value])
        

    wb.save(output_file)

if __name__ == "__main__":
    # List of URLs to scrape (replace with actual URLs)
    urls = [
        "https://sportsbookwire.usatoday.com/2023/09/18/cleveland-browns-at-pittsburgh-steelers-odds-picks-and-predictions-2/",
        "https://www.covers.com/picks/nfl",
        "https://www.pickswise.com/nfl/picks/",
        # Add more URLs as needed
    ]

    # Specify the output Excel file name
    output_file = "scraped_data.xlsx"

    all_data = {}  # Initialize the dictionary inside the loop
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for url in urls:
        # Scrape data under specified headers
        header_texts_to_search = ["Over/Under", "Against the spread", "Moneyline"]
        header_data = scrape_data_under_over_under(url, header_texts_to_search)
        all_data.update(header_data)  # Store header-based data for each URL separately

        # Scrape data from elements with the specified class
        class_name1 = "cover-CoversPicks-PickString"
        class_name2 = "SelectionInfo_outcome__1i6jL"
        class_name3 = "gnt_ar_b_p"
        pick_type = "Pill_small__EfxDi Pill_pill__Hx16I Pill_light__m1ZLF Pill_secondary__iZOdZ"
        

        '''
        SelectionInfo_event__petE6 (span)
        '''


        class_data = scrape_data_with_class(url, class_name1)
        pick_data = picks_type_scrape(url, pick_type)
        class_data2 = picks_wise_scrape(url, class_name2, pick_data)
        class_data3 = scrape_data_azcentral(url, class_name3)
        all_data.update(class_data)  # Store class-based data for each URL separately
        all_data.update(class_data2)
        all_data.update(class_data3)

        file_size = os.stat(output_file)

    # Create the Excel file
    create_excel_file(all_data, output_file)

    print("Data has been scraped and saved to {}".format(output_file))
    print(file_size)
