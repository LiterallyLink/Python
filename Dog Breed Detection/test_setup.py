# test_setup.py
import os
import tensorflow as tf

def test_environment():
    # Test 1: Check TensorFlow installation
    print("TensorFlow version:", tf.__version__)
    print("GPU Available:", tf.test.is_built_with_cuda())
    
    # Test 2: Check project structure
    project_root = os.getcwd()
    required_dirs = ['data', 'src']
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print("❌ Missing directories:", missing_dirs)
    else:
        print("✓ Project structure looks good!")
    
    # Test 3: Try to load and preprocess a sample image
    data_dir = 'data/stanford_dogs'
    if os.path.exists(data_dir):
        # Find first image file in any subdirectory
        image_found = False
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    test_image_path = os.path.join(root, file)
                    image_found = True
                    try:
                        img = tf.io.read_file(test_image_path)
                        img = tf.image.decode_jpeg(img, channels=3)
                        img = tf.image.resize(img, [224, 224])
                        img = img / 255.0
                        print(f"✓ Successfully loaded and processed image: {test_image_path}")
                        print(f"✓ Image shape: {img.shape}")
                        break
                    except Exception as e:
                        print(f"❌ Error processing image: {str(e)}")
            if image_found:
                break
        if not image_found:
            print("❌ No image files found in data directory")
    else:
        print(f"❌ Data directory not found at {data_dir}")

if __name__ == "__main__":
    print("Running setup tests...")
    print("-" * 50)
    test_environment()