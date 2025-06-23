import csv
import requests
from bs4 import BeautifulSoup

def extract_youtube_links(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        youtube_links = []
        for link in links:
            href = link['href']
            if "youtube.com" in href or "youtu.be" in href:
                youtube_links.append(href)

        return list(set(youtube_links))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    input_file = "brands.csv"
    output_file = "youtube_links.csv"
    
    results = []

    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['URL'].strip()
            brand = row['BRAND'].strip()
            print(f"Scraping {brand}...")
            yt_links = extract_youtube_links(url)
            for link in yt_links:
                results.append({
                    'Brand': brand,
                    'YouTube Link': link
                })

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Brand', 'YouTube Link']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Done! Saved to {output_file}")

if __name__ == "__main__":
    main()
