import urllib.request
import os
from bs4 import BeautifulSoup
import requests
import sys
import time

# Create a session object
session = requests.Session()

# Set up headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def download_image(url, folder):
    try:
        filename = os.path.join(folder, url.split("/")[-1])

        # Use session to download image
        response = session.get(url, headers=headers)
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def get_image_page_links(url, selector):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return [a["href"] for a in soup.select(selector)]
    except Exception as e:
        print(f"Error getting image page links: {e}")
        return []


def get_image_src(url, selector):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
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

    def get_input_with_default(prompt, default):
        user_input = input(
            f"{prompt} (Press Enter to use default '{default}'): "
        ).strip()
        return user_input if user_input else default

    gallery_selector = get_input_with_default(
        "Enter the CSS selector for image page links",
        ".photo-album-wrapper .photo-item a",
    )

    image_selector = get_input_with_default(
        "Enter the CSS selector for the image on the image page", ".features-video img"
    )

    base_url = "/".join(gallery_url.split("/")[:3])  # Extract base URL

    # Create download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Get image page links from the gallery page
    image_page_links = get_image_page_links(gallery_url, gallery_selector)
    print("image_page_links", image_page_links)
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


# Run the function
if __name__ == "__main__":
    download_folder = "downloaded_images"
    download_images(download_folder)
