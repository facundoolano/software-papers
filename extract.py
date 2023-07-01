import os
import requests
from bs4 import BeautifulSoup


def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ']).rstrip()


def download_article(url, title, save_folder):
    # Create save_folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)
    try:
        response = requests.get(url, timeout=5)  # specify a timeout
    except requests.exceptions.Timeout:
        print(f'Timeout error for URL: {url}')
        return
    except requests.exceptions.TooManyRedirects:
        print(f'TooManyRedirects error occurred with {url}')
        return
    except requests.exceptions.RequestException as e:
        print(f'RequestException error occurred with {url}. Exception: {e}')
        return

    if response.status_code == 200:
        # Sanitize title before using it as filename
        title = sanitize_filename(title)
        with open(os.path.join(save_folder, f'{title}.pdf'), 'wb') as f:
            f.write(response.content)


def extract_urls_from_webpage(webpage_url):
    response = requests.get(webpage_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li')

    articles = []
    for item in items:
        a_tag = item.find('a')
        if a_tag:
            url = a_tag.get('href')
            # If URL starts with '/', append the domain name
            if url and url.startswith('/'):
                url = 'https://github.com' + url
            # Check if URL is valid and is a pdf
            if url and url.endswith('.pdf'):
                title = item.text.split(a_tag.text)[0].strip()
                articles.append((url, title))

    return articles


if __name__ == '__main__':
    webpage_url = input("Please enter the URL of the webpage: ")
    save_folder = '/folder you need to save'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    articles = extract_urls_from_webpage(webpage_url)
    for url, title in articles:
        download_article(url, title, save_folder)
