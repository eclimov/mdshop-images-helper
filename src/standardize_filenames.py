import os

def rename_files_in_directory(directory):
    # Loop through all files in the given directory
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)

        # Skip if it's not a file
        if not os.path.isfile(old_path):
            continue

        # Replace ' - ' with ',' in the filename
        new_filename = filename.replace(' - ', ',')

        # Only rename if there's an actual change
        if new_filename != filename:
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_filename}")

if __name__ == "__main__":
    # Example: specify your directory path here
    target_directory = r"..\assets\_products-icons-source"
    rename_files_in_directory(target_directory)
