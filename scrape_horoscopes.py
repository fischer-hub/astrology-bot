import requests
from bs4 import BeautifulSoup

# Specify the URL of the webpage you want to scrape
url = 'https://www.astrology.com/horoscope/daily/yesterday/aries.html#Thursday'


# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text from the webpage (you may need to inspect the HTML structure)
    extracted_text = soup.get_text(separator='\n', strip=True)
    
    # Print or use the extracted text as needed
    print(soup)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
