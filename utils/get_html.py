import os
import requests
import undetected_chromedriver as uc

from bs4 import BeautifulSoup

def fetch_html(url):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--allow-running-insecure-content")

    chrome_bin = os.environ.get('chrome_bin')
    chrome_options.binary_location = chrome_bin

    driver = uc.Chrome(options=chrome_options)

    try:
        driver.get(url)
        return driver.page_source
    finally:
        driver.quit()
    

def extract_pdf_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'pdf' in href.lower():
            pdf_links.append(href)
    return pdf_links

def extract_title_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_tags = soup.find_all('p', class_='title is-5 mathjax')
    titles = [tag.get_text(strip=True) for tag in title_tags]
    return titles

def download_pdfs(pdf_links, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    saved_paths = []
    
    for link in pdf_links:
        try:
            response = requests.get(link, stream=True)
            if response.status_code == 200:
                file_name = link.split('/')[-1]
                file_path = os.path.join(save_dir, file_name + '.pdf')
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"Downloaded: {file_path}")
                saved_paths.append(os.path.abspath(file_path))
            else:
                print(f"Failed to download: {link} (Status Code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {link}: {e}")
    
    return saved_paths