from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from diapers_links import collect_diapers_data
import json

links_file = "diapers_links.json"

# Load diaper links data with error handling
def load_diaper_links(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"The file {file_path} was not found. Collecting data...")
        collect_diapers_data(file_path)
        with open(file_path, "r") as f:
            return json.load(f)

diapers = load_diaper_links(links_file)

# Extract product features from the webpage
def extract_product_features(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    features_key = soup.find_all("span", class_="nobr")
    features_value = soup.find_all("td", class_="val")
    features = {key.text.strip(): value.text.strip() for key, value in zip(features_key, features_value)}
    brand_name_tag = soup.find("div", class_="op1-tt")
    brand_name = brand_name_tag.text.strip() if brand_name_tag else "Unknown"
    product = {"URL": url, "Brand": brand_name}
    product.update({f"Feature {i+1}": list(features.items())[i] if i < len(features) else "" for i in range(10)})
    return product

# Collect data for all diapers
product_data = [extract_product_features(diaper) for diaper in diapers]

df = pd.DataFrame(product_data)
df_sorted = df.sort_values(by="Brand", ascending=True)
brand_counts = df_sorted.groupby("Brand").size().reset_index(name="Count")

with pd.ExcelWriter("diapers_data_from_ek.xlsx") as writer:
    df_sorted.to_excel(writer, sheet_name="Products", index=False)
    brand_counts.to_excel(writer, sheet_name="Brand Analysis", index=False)

# Brand analysis: Top 5 by number of products
top_brands = brand_counts.sort_values(by="Count", ascending=False).head(5)

# Feature frequency analysis
all_features = [features[0] for features in df_sorted.iloc[:, 2:12].values.flatten() if isinstance(features, tuple) and features[0]]
features_analysis = pd.Series(all_features).value_counts().reset_index()
features_analysis.columns = ["Feature", "Count"]

# Extract weight range from feature text
def extract_weight_range(feature_text):
    if isinstance(feature_text, tuple) and "kg" in feature_text[1]:
        match = re.search(r"(\d+)\s*–\s*(\d+)\s*\u043aг", feature_text[1])
        if match:
            return f"{match.group(1)}-{match.group(2)} kg"
    return "Other"

df_sorted["Weight Range"] = df_sorted["Feature 4"].apply(extract_weight_range)
weight_distribution = df_sorted["Weight Range"].value_counts().reset_index(name="Count")
weight_distribution.columns = ["Weight Range", "Count"]

with pd.ExcelWriter("diapers_data_from_ek.xlsx", mode="a", engine="openpyxl") as writer:
    top_brands.to_excel(writer, sheet_name="Top Brands", index=False)
    features_analysis.to_excel(writer, sheet_name="Feature Analysis", index=False)
    weight_distribution.to_excel(writer, sheet_name="Weight Distribution", index=False)

print("Additional analytics saved to a file!")
