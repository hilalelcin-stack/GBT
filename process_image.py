from rembg import remove
from PIL import Image

input_path = "WhatsApp Image 2026-04-01 at 13.22.21.jpeg"
output_path = "profile_cleaned.jpg"

try:
    print("Loading image...")
    input_image = Image.open(input_path)
    print("Removing background...")
    output_image = remove(input_image)
    
    print("Applying white background...")
    white_bg = Image.new("RGBA", output_image.size, "WHITE")
    white_bg.paste(output_image, (0, 0), output_image)
    
    white_bg = white_bg.convert("RGB")
    white_bg.save(output_path, "JPEG", quality=92)
    print(f"Successfully saved to {output_path}")
except Exception as e:
    print(f"Error processing image: {e}")
