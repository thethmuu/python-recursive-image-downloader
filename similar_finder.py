import os
from PIL import Image
import imagehash
from collections import defaultdict
import shutil


def find_similar_images(directory, hash_size=8, threshold=5):
    """
    Find similar images in the given directory.

    :param directory: Path to the directory containing images
    :param hash_size: Hash size for the perceptual hash (default: 8)
    :param threshold: Maximum hamming distance to consider images as similar (default: 5)
    :return: Dictionary of similar image groups
    """
    image_hashes = {}
    similar_images = defaultdict(list)

    for filename in os.listdir(directory):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            filepath = os.path.join(directory, filename)
            try:
                with Image.open(filepath) as img:
                    hash = imagehash.average_hash(img, hash_size)
                    image_hashes[filepath] = hash
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Compare hashes
    processed = set()
    for filepath, hash in image_hashes.items():
        if filepath in processed:
            continue

        for other_filepath, other_hash in image_hashes.items():
            if filepath != other_filepath and other_filepath not in processed:
                distance = hash - other_hash
                if distance <= threshold:
                    similar_images[filepath].append(other_filepath)
                    processed.add(other_filepath)

        processed.add(filepath)

    return similar_images


def move_similar_images(similar_images, base_directory):
    if similar_images:
        print("\nSimilar images found:")
        similar_items_dir = os.path.join(base_directory, "similar_items")
        os.makedirs(similar_items_dir, exist_ok=True)

        for base_image, similar_list in similar_images.items():
            group_dir = os.path.join(similar_items_dir, os.path.basename(base_image))
            os.makedirs(group_dir, exist_ok=True)

            print(f"Group:")
            print(f"  - {os.path.basename(base_image)}")
            shutil.move(base_image, group_dir)

            for similar in similar_list:
                print(f"  - {os.path.basename(similar)}")
                shutil.move(similar, group_dir)

        print(f"\nSimilar images have been moved to: {similar_items_dir}")
    else:
        print("\nNo similar images found.")


def find_and_group_similar_images(folder_path):
    similar_images = find_similar_images(folder_path)
    move_similar_images(similar_images, folder_path)
