import urllib.request
import os
from bs4 import BeautifulSoup
import requests
import sys


def download_image(url, folder):
    try:
        filename = os.path.join(folder, url.split("/")[-1])
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def get_image_page_links(url, selector):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return [a["href"] for a in soup.select(selector)]
    except Exception as e:
        print(f"Error getting image page links: {e}")
        return []


def get_image_src(url, selector):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        img = soup.select_one(selector)
        return img["src"] if img else None
    except Exception as e:
        print(f"Error getting image source: {e}")
        return None


def download_images(download_folder):
    # Prompt the user for the gallery URL and selectors
    gallery_url = input("Please enter the gallery URL: ").strip()
    if not gallery_url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    gallery_selector = input(
        "Enter the CSS selector for image page links (e.g., '.photo-album-wrapper .photo-item a'): "
    ).strip()
    image_selector = input(
        "Enter the CSS selector for the image on the image page (e.g., '.features-video img'): "
    ).strip()

    base_url = "/".join(gallery_url.split("/")[:3])  # Extract base URL

    # Create download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Get image page links from the gallery page
    image_page_links = get_image_page_links(gallery_url, gallery_selector)
    downloaded_count = 0
    for link in image_page_links:
        # Handle relative URLs
        full_link = link if link.startswith("http") else f"{base_url}{link}"
        img_src = get_image_src(full_link, image_selector)
        print(img_src)
        if img_src:
            # Handle relative URLs for image sources
            full_img_src = (
                img_src if img_src.startswith("http") else f"{base_url}{img_src}"
            )
            download_image(full_img_src, download_folder)
            downloaded_count += 1

    print(f"Total images downloaded: {downloaded_count}")
