import os
import requests
from urllib.parse import urlparse
import uuid

def fetch_image():
    # Prompt the user for a URL
    url = input("Enter the image URL: ").strip()
    
    # Create directory if it doesn't exist
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Fetch the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename:  # If no filename in URL, generate one
            filename = f"image_{uuid.uuid4().hex}.jpg"
        
        save_path = os.path.join(save_dir, filename)

        # Save the image in binary mode
        with open(save_path, "wb") as file:
            file.write(response.content)

        print(f"✅ Image successfully saved at: {save_path}")

    except requests.exceptions.MissingSchema:
        print("❌ Invalid URL format. Please include http:// or https://")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Please check your internet.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error occurred: {e}")
    except requests.exceptions.Timeout:
        print("❌ The request timed out. Try again later.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_image()
