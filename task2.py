pip install pillow
from PIL import Image
import numpy as np

def encrypt_image(image_path, key, method):
    # Load the image
    img = Image.open(image_path)
    img_array = np.array(img)

    # Encrypt the image based on the selected method
    if method == 'xor':
        encrypted_array = img_array ^ key
    elif method == 'swap':
        encrypted_array = img_array.copy()
        encrypted_array[..., 0], encrypted_array[..., 2] = img_array[..., 2], img_array[..., 0]  # Swap R and B channels
    elif method == 'reverse':
        encrypted_array = np.bitwise_not(img_array)  # Bitwise NOT operation
    elif method == 'shift':
        encrypted_array = np.roll(img_array, shift=1, axis=2)  # Circular shift of pixel values
    else:
        raise ValueError("Invalid encryption method")

    # Convert back to image
    encrypted_image = Image.fromarray(encrypted_array)
    return encrypted_image

def decrypt_image(encrypted_image, key, method):
    # Convert back to array
    encrypted_array = np.array(encrypted_image)

    # Decrypt the image based on the selected method
    if method == 'xor':
        decrypted_array = encrypted_array ^ key
    elif method == 'swap':
        decrypted_array = encrypted_array.copy()
        decrypted_array[..., 0], decrypted_array[..., 2] = encrypted_array[..., 2], encrypted_array[..., 0]  # Swap back R and B channels
    elif method == 'reverse':
        decrypted_array = np.bitwise_not(encrypted_array)  # Bitwise NOT operation
    elif method == 'shift':
        decrypted_array = np.roll(encrypted_array, shift=-1, axis=2)  # Reverse circular shift
    else:
        raise ValueError("Invalid decryption method")

    # Convert back to image
    decrypted_image = Image.fromarray(decrypted_array)
    return decrypted_image

def main():
    print("Image Encryption Tool")
    print("----------------------")
    
    while True:
        action = input("Do you want to (e)ncrypt or (d)ecrypt an image? (q to quit): ").lower()
        if action == 'q':
            break
        
        image_path = input("Enter the path to the image: ")
        key = int(input("Enter a key (1-255): "))
        method = input("Choose a method (xor, swap, reverse, shift): ").lower()

        if action == 'e':
            encrypted_image = encrypt_image(image_path, key, method)
            encrypted_image.save("encrypted_image.png")
            print("Image encrypted and saved as 'encrypted_image.png'")
        
        elif action == 'd':
            encrypted_image = Image.open("encrypted_image.png")
            decrypted_image = decrypt_image(encrypted_image, key, method)
            decrypted_image.save("decrypted_image.png")
            print("Image decrypted and saved as 'decrypted_image.png'")
        
        else:
            print("Invalid action. Please choose 'e' or 'd'.")

if __name__ == "__main__":
    main()
