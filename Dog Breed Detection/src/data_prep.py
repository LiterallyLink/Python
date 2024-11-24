import os
import tensorflow as tf
from pathlib import Path

def get_breed_names(data_dir):
    """
    Get a list of dog breeds from the directory names, all in lowercase
    """
    breed_names = []
    for breed_dir in os.listdir(data_dir):
        # Remove the numerical prefix and convert dashes to spaces
        # Example: 'n02085620-Chihuahua' -> 'chihuahua'
        breed_name = breed_dir.split('-', 1)[1] if '-' in breed_dir else breed_dir
        # Convert to lowercase
        breed_name = breed_name.lower()
        breed_names.append(breed_name)
    
    # Sort alphabetically for consistency
    breed_names.sort()
    return breed_names

def load_image_and_label(image_path, image_size=(224, 224)):
    """
    Load and preprocess a single image, and return its breed label
    """
    img = tf.io.read_file(image_path)
    # Decode the JPEG image to a tensor
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, image_size)
    # Normalize pixel values
    img = img / 255.0

    # Format breed name from the path
    parts = tf.strings.split(image_path, os.path.sep)
    breed_folder = parts[-2]
    breed_name =  tf.strings.split(breed_folder, '-')[-1]
    breed_name = tf.strings.lower(breed_name)

    return img, breed_name

# TESTS
if __name__ == "__main__":
    data_dir = "data/stanford_dogs/images"
    
    # Test breed names function
    breeds = get_breed_names(data_dir)
    print("First 5 breed names:", breeds[:5])
    
    # Test image loading function
    # Find first image for testing
    for breed_dir in os.listdir(data_dir):
        breed_path = os.path.join(data_dir, breed_dir)
        if os.path.isdir(breed_path):
            for image_file in os.listdir(breed_path):
                if image_file.endswith('.jpg'):
                    test_image_path = os.path.join(breed_path, image_file)
                    img, breed = load_image_and_label(test_image_path)
                    print(f"\nTest image loaded:")
                    print(f"Image shape: {img.shape}")
                    print(f"Breed: {breed.numpy().decode('utf-8')}")
                    break
            break