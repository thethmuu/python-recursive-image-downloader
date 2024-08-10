import urllib.request
import os
from bs4 import BeautifulSoup
import requests
import sys

download_folder = os.path.join(os.path.expanduser(
    '~'), 'Pictures', 'web_scraped_images')


def download_image(url, folder):
    # Extract the filename from the URL
    filename = os.path.join(folder, os.path.basename(url))

    # Check if the file already exists
    if os.path.exists(filename):
        print(f"File '{os.path.basename(filename)}' already exists in the download folder.")
        print("Stopping the program to avoid overwriting existing files.")
        sys.exit(1)

    # Create a custom request with a user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)

    # Download the file using the custom request
    with open(filename, 'wb') as f:
        f.write(urllib.request.urlopen(req).read())
    print(f"File '{os.path.basename(filename)}' downloaded successfully.")


def get_image_page_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    gallery_div = soup.find('div', id='gallery')
    if gallery_div:
        masonry_items = gallery_div.find_all('div', class_='masonry-item')
        return [item.find('a')['href'] for item in masonry_items if item.find('a') and item.find('a')['href'] != '#']
    return []


def get_image_src(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    gallery_container = soup.find('div', class_='gallery-container')
    if gallery_container:
        img_tag = gallery_container.find('img')
        return img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
    return None


def main():
    # Prompt the user for the gallery URL
    gallery_url = input("Please enter the gallery URL: ").strip()

    if not gallery_url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    base_url = '/'.join(gallery_url.split('/')[:3])  # Extract base URL

    # Create download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Get image page links from the gallery page
    image_page_links = get_image_page_links(gallery_url)
    downloaded_count = 0
    for link in image_page_links:
        # Handle relative URLs
        full_link = link if link.startswith('http') else f"{base_url}{link}"
        img_src = get_image_src(full_link)
        print(img_src)
        if img_src:
            # Handle relative URLs for image sources
            full_img_src = img_src if img_src.startswith('http') else f"{base_url}{img_src}"
            download_image(full_img_src, download_folder)
            downloaded_count += 1

    print(f"Total images downloaded: {downloaded_count}")


if __name__ == "__main__":
    main()