import os
import sys
from file_downloader import download_images
from similar_finder import find_and_group_similar_images

download_folder = os.path.join(
    os.path.expanduser("~"), "Pictures", "web_scraped_images"
)


def main():
    print("Welcome to the Image Tool!")
    print("1. Download images from a website")
    print("2. Find similar images in a folder")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        download_images(download_folder)
    elif choice == "2":
        folder_path = input(
            f"Enter the folder path to search for similar images (press Enter for default: {download_folder}): "
        ).strip()
        if not folder_path:
            folder_path = download_folder
        find_and_group_similar_images(folder_path)
    else:
        print("Invalid choice. Please run the program again and select 1 or 2.")
        sys.exit(1)


if __name__ == "__main__":
    main()
