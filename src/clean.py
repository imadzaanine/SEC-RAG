from bs4 import BeautifulSoup

def clean_html_to_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove script/style tags
    for tag in soup(["script", "style"]):
        tag.decompose()
    
    # Remove the Inline XBRL header block (contains all the tag metadata, no narrative text)
    for tag in soup.find_all("ix:header"):
        tag.decompose()
    
    # Remove any element explicitly hidden via inline style (common for XBRL tagging)
    for tag in soup.find_all(style=lambda value: value and "display:none" in value.replace(" ", "")):
        tag.decompose()
    
    text = soup.get_text(separator=" ")
    text = " ".join(text.split())
    
    return text

if __name__ == "__main__":
    cleaned_text = clean_html_to_text("data/aapl_10k.htm")
    print("Total characters:", len(cleaned_text))
    print("First 500 characters:")
    print(cleaned_text[:500])