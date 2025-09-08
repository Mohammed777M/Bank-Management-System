import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

def fetch_interest_rates():
    try:
        url = 'https://www.bankbazaar.com/personal-loan-interest-rates.html'  # Example URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {"error": "Failed to fetch data from the site"}

        soup = BeautifulSoup(response.content, 'html.parser')

        interest_data = {}

        # Example scraping logic: Select table rows that might contain interest rates
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    bank_name = cols[0].text.strip()
                    interest_rate = cols[1].text.strip()
                    interest_data[bank_name] = interest_rate
        else:
            return {"error": "Table not found on the page"}

        return interest_data

    except Exception as e:
        return {"error": f"Unable to fetch interest rates: {str(e)}"}
