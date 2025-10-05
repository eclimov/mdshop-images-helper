import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling

'''
Each image in 'input' folder should have the following name pattern:
<product_id_integer>#<product_name_ru>#<product_name_ro>
'''
def process_images(
        input_dir="../assets/products-icons-large",
        output_dir="../assets/screensaver",
        background_size=(1600, 900),
        font_path="../assets/_font/Onest/Onest-Bold.ttf"  # path to .ttf font
):
    # Cleanup and create output directory (ensure that exists)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Background color items
    green_items = [1, 29, 30, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
                   73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 86, 87, 88, 89, 91, 92, 93, 95, 98, 99, 100, 101,
                   102, 103, 104, 105, 106, 107, 110, 111, 112, 114, 115, 116, 143]
    blue_items = [2, 3, 10, 12, 13, 14, 15, 16, 17, 37, 38, 42, 47, 48, 49, 50, 117, 119, 130, 131, 133, 134, 135, 136,
                  137, 138, 139]
    purple_items = [4, 5, 6, 8, 9, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 35, 40, 43, 44, 45, 46, 108, 109, 113, 123,
                    124, 125, 127, 141, 142]
    orange_items = [7, 27, 28, 33, 34, 36, 41, 85, 90, 96, 97, 118, 120, 121, 128, 129, 132, 140]
    red_items = [31, 32, 33, 132, 144, 145, 146, 126]

    # Process all PNG files in this folder
    for file_name in os.listdir(input_dir):
        if not file_name.lower().endswith(".png"):
            continue

        file_name_without_extension = os.path.splitext(file_name)[0]

        input_path = os.path.join(input_dir, file_name)
        output_name = file_name_without_extension.lower() + ".jpg"
        output_path = os.path.join(output_dir, output_name)

        product_id, product_name_ru, product_name_ro = file_name_without_extension.split("#")

        # Set background color
        if int(product_id) in green_items:
            background_color = (140, 184, 142)  # Green
        elif int(product_id) in blue_items:
            background_color = (70, 130, 180)  # Blue
        elif int(product_id) in purple_items:
            background_color = (106, 90, 205)  # Purple
        elif int(product_id) in orange_items:
            background_color = (255, 192, 103)  # Orange
        elif int(product_id) in red_items:
            background_color = (255, 100, 92)  # Red
        else:
            background_color = (0, 0, 0)  # Black by default


        # Create background
        background = Image.new("RGBA", background_size, background_color + (255,))
        draw = ImageDraw.Draw(background)

        # Load and scale overlay (50%)
        overlay = Image.open(input_path).convert("RGBA")
        new_width = overlay.width // 2
        new_height = overlay.height // 2
        overlay_resized = overlay.resize((new_width, new_height), Resampling.LANCZOS)

        # Center position
        bg_width, bg_height = background.size
        position = (
            (bg_width - new_width) // 2,
            (bg_height - new_height) // 2
        )

        # Paste overlay with transparency
        background.paste(overlay_resized, position, overlay_resized)

        ###############################################################################
        # Draw text
        text_layer = Image.new("RGBA", background.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        try:
            font_top = ImageFont.truetype(font_path, 128)
            font_middle = ImageFont.truetype(font_path, 86)
            font_bottom = ImageFont.truetype(font_path, 70)
        except IOError:
            print(f"⚠️ Font not found: {font_path}. Using default font.")
            font_top = font_middle = font_bottom = ImageFont.load_default()

        # Initialize text
        top_text = product_id.upper()
        middle_text = product_name_ru.upper()
        bottom_text = product_name_ro.upper()

        # Helper to center text
        def draw_centered_text(text, y, font, alpha):
            text_width = draw.textlength(text, font=font)
            x = (bg_width - text_width) / 2
            draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))

        # Opaque top text
        draw_centered_text(top_text, 64, font_top, 255)

        # Semi-transparent middle & bottom text (opacity 70%)
        draw_centered_text(middle_text, 680, font_middle, int(255 * 0.7))  # 70% transparency
        draw_centered_text(bottom_text, 800, font_bottom, int(255 * 0.7))  # 70% transparency
        ###############################################################################

        # Merge text layer with background ---
        combined = Image.alpha_composite(background, text_layer)

        # Convert to RGB and save as JPG
        final_image = combined.convert("RGB")
        final_image.save(output_path, "JPEG", quality=95)
        print(f"✅ Saved: {output_path}")

if __name__ == "__main__":
    process_images()
