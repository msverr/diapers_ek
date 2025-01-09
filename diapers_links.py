import requests
from bs4 import BeautifulSoup
import json

def collect_diapers_data(output_file="diapers_links.json"):
    """
    Function collecting links to products from the ek.ua website and writing them to a JSON file.
    
    Arguments:
    - output_file (str): The name of the file where the links are saved.
    """
    ek = "https://ek.ua/ua/list/659/&page={}"
    diapers_pages = [ek.format(page) for page in range(1, 295)]
    
    diapers = []

    for url in diapers_pages:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            product_containers = soup.find_all("td", class_="model-short-info")
            for product in product_containers:
                link = product.find("a")
                if link:
                    full_link = f"https://ek.ua{link.get('data-url')}"
                    diapers.append(full_link)
        else:
            print(f"Unable to retrieve data from {url}, error code: {response.status_code}")


    with open(output_file, "w") as f:
        json.dump(diapers, f, indent=4, ensure_ascii=False)
    print(f"Collected {len(diapers)} links and saved to file {output_file}")
    
if __name__ == "__main__":
    collect_diapers_data()