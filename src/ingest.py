import os 
import requests

# SEC requires a descptive User-Agent header to be set to identify who is making the request.

HEADER = {
    "User-Agent": "Imad Zaanine imadzaanine@gmail.com"
}

# SEC EDGAR identifies every company by a CIK number (Central Index Key)

APPLE_CIK = "0000320193"

def get_filing_list(cik):
    # Get the list of filings for a given CIK number from the SEC EDGAR database.
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=HEADER)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def find_latest_10k_filing(data):
    # Find the latest 10-K filling from the list of filings.
    recent = data["filings"]["recent"]
    forms = recent["form"]

    for i,form_type in enumerate(forms):
        if form_type == "10-K":
            accession_number = recent["accessionNumber"][i]
            primary_document = recent["primaryDocument"][i]
            filing_date = recent["filingDate"][i]
            return {
                "accession_number": accession_number,
                "primary_document": primary_document,
                "filing_date": filing_date
            }
    return None  # Return None if no 10-K filing is found


def build_filing_url(cik, accession_number, primary_document):
    cik_stripped = str(int(cik))  # removes leading zeros
    accession_no_dashes = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{cik_stripped}/{accession_no_dashes}/{primary_document}"
    return url


def download_filing(url, save_path):
    response = requests.get(url, headers=HEADER)
    response.raise_for_status()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"Saved filing to {save_path}")

    

if __name__ == "__main__":
    data = get_filing_list(APPLE_CIK)
    print(data["name"])
    
    latest_10k = find_latest_10k_filing(data)
    print("Latest 10-K Filing:")
    print("Accession Number:", latest_10k["accession_number"])
    print("Primary Document:", latest_10k["primary_document"])
    print("Filing Date:", latest_10k["filing_date"])
    
    url = build_filing_url(APPLE_CIK, latest_10k["accession_number"], latest_10k["primary_document"])
    print("Filing URL:", url)
    
    download_filing(url, "data/aapl_10k.htm")