# **Diapers Parser with Analytics**

## **Project Description**
This project scrapes data about diapers from the price aggregator website ([ek.ua](https://ek.ua)), extracts product characteristics, and performs data analysis. The collected data is saved in structured formats for further use.

## **Features**
- **Product Links Collection**:
  - Automatically scrapes all product links in the "diapers" category.
  - Saves the links to a `diapers_links.json` file in the following format:
    ```json
    [
        "https://ek.ua/ua/SENI-SUPER-TRIO-L---10-PCS.htm",
        "https://ek.ua/ua/HUGGIES-PANTS-GIRL-4---104-PCS.htm",
        "https://ek.ua/ua/PAMPERS-ACTIVE-BABY-6---128-PCS.htm",
        ...
    ]
    ```

- **Product Characteristics Extraction**:
  - Parses each product page to collect details like:
    - Size
    - Quantity per pack
    - Price
    - Type (e.g., diapers, pants)
    - Manufacturer
  - Saves the parsed data in an Excel file: `diapers_data_from_ek.xlsx`.

- **Data Analysis**:
  - Performs analytics on the scraped data directly in Excel, including:
    - Price comparison by brand and product type.
    - Distribution of products by size.
    - Summary statistics (average price, median, etc.).

## **Project Files**

├── diapers_data_from_ek.xlsx  # Excel file with parsed data and analysis
├── diapers_links.json         # JSON file with product links
├── diapers_links.py           # Script to scrape product links
├── diapersEK.py               # Script to scrape product details and generate analytics
├── README.md                  # Project documentation


