import os
import shutil
from PIL import Image
from PIL.Image import Resampling


def resize_pngs_in_folder(
        input_dir="../assets/products-icons-large",
        output_dir="../assets/products-icons-small",
        size=(64, 64)  # target resolution (width, height)
):
    """
    Resize all PNG images in the input directory and save to output directory.
    Transparency is preserved.
    """
    # Cleanup and create output directory (ensure that exists)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all PNG files
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".png"):
            continue  # skip non-PNG files

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        try:
            # Open and convert to RGBA to preserve transparency
            img = Image.open(input_path).convert("RGBA")

            # Resize using high-quality filter
            resized = img.resize(size, Resampling.LANCZOS)

            # Save result
            resized.save(output_path, "PNG")
            print(f"✅ Resized: {filename} → {size[0]}x{size[1]}")
        except Exception as e:
            print(f"⚠️ Failed to process {filename}: {e}")

    print("\n🎯 Done. All resized images saved in:", output_dir)


if __name__ == "__main__":
    resize_pngs_in_folder()
