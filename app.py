from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

# Define colors and corresponding symbols
colors = [
    [92, 69, 53], [192, 194, 189], [64, 53, 45],
    [123, 123, 118], [187, 144, 101], [55, 44, 41], [123, 90, 101]
]
symbols = ['#', 'O', 'X', '\\', 'S', '*', '%']  # Corresponding symbols

def closest_color(pixel, color_list):
    """Find the closest color to the given pixel."""
    pixel = np.array(pixel)  # Convert pixel to NumPy array
    color_list = np.array(color_list)  # Convert list to NumPy array
    distances = np.linalg.norm(color_list - pixel, axis=1)  # Compute Euclidean distance
    closest_index = np.argmin(distances)  # Get index of closest color
    return closest_index  # Return index of closest color

def convert_image_to_ascii_image(image_path, colors, symbols, out_width, out_height):
    """Convert an image to ASCII and save it as an image with optional gridlines."""
    if os.path.exists(image_path) and image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        try:
            img = Image.open(image_path).convert('RGB')  # Convert image to RGB
            img = img.resize((out_width, out_height))  # Resize for better ASCII output
            pixels = img.load()
            font_size = 12  # Font size of ASCII symbols

            ascii_art = []

            count = 0
            for y in range(img.height):
                row = []
                for x in range(img.width):
                    original_pixel = pixels[x, y]  # Get RGB pixel
                    closest_index = closest_color(original_pixel, colors)  # Find closest color index
                    row.append(symbols[closest_index])  # Map to symbol
                    count += 1
                ascii_art.append(row)

            # Create an image from ASCII art
            output_width = img.width * font_size
            output_height = img.height * font_size
            ascii_image = Image.new("RGB", (output_width, output_height), "white")
            draw = ImageDraw.Draw(ascii_image)
            print(count)

            # Load a monospaced font (use a built-in or custom font)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)  # Windows
            except IOError:
                font = ImageFont.load_default()  # Use default font if arial.ttf is not found

           # Calculate text centering offsets
            char_width, char_height = font.getbbox("X")[2:]   # Get size of a single character
            x_offset = (font_size - char_width) // 2  # Center X
            y_offset = (font_size - char_height) // 2  # Center Y

            # Draw ASCII symbols centered in grid cells
            for y, row in enumerate(ascii_art):
                for x, char in enumerate(row):
                    draw.text((x * font_size + x_offset, y * font_size + y_offset), char, fill="black", font=font)

            # Draw gridlines
            for x in range(0, output_width, font_size):
                draw.line([(x, 0), (x, output_height)], fill="gray", width=1)  # Vertical lines
            for y in range(0, output_height, font_size):
                draw.line([(0, y), (output_width, y)], fill="gray", width=1)  # Horizontal lines

            # Save the ASCII image
            ascii_image.save("ascii_image_with_grid.png")
            ascii_image.show()
            print("ASCII image with grid saved as ascii_image_with_grid.png!")

        except Exception as e:
            print(f"Error processing image: {e}")
    else:
        print("Invalid file path or unsupported file format.")

# Example usage
image_path = "test_img_2.jpg"  # Replace with actual image path
out_width = 70
out_height = 93
convert_image_to_ascii_image(image_path, colors, symbols, out_width, out_height)
