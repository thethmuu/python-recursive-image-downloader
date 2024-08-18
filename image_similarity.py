import os
from PIL import Image
import imagehash
from collections import defaultdict


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


def print_similar_images(similar_images):
    if similar_images:
        print("\nSimilar images found:")
        for base_image, similar_list in similar_images.items():
            print(f"Group:")
            print(f"  - {os.path.basename(base_image)}")
            for similar in similar_list:
                print(f"  - {os.path.basename(similar)}")
    else:
        print("\nNo similar images found.")
