import requests
from bs4 import BeautifulSoup

def scrape_barcode_details(barcode):
    url = f"https://www.barcodelookup.com/{barcode}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract product name
        product_name = soup.find("h4", {"class": "product-name"}).text.strip() if soup.find("h4", {"class": "product-name"}) else "Unknown Product"
        
        # Extract product details
        product_details = {}
        details_table = soup.find("table", {"class": "product-details"})
        if details_table:
            for row in details_table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    product_details[key] = value
        
        return {"name": product_name, "details": product_details}
    else:
        return {"error": f"Failed to retrieve data. HTTP Status Code: {response.status_code}"}

# Example usage
barcode = "4808680230979"  # Replace with a valid barcode
result = scrape_barcode_details(barcode)
if "error" in result:
    print(result["error"])
else:
    print("Product Name:", result["name"])
    print("Product Details:", result["details"])

