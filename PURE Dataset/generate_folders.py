from pathlib import Path

# Folder where this Python script is located
main_folder = Path(__file__).parent

# Find all PDF files in the folder
for pdf_file in main_folder.glob("*.pdf"):
    # Get filename without .pdf extension
    folder_name = pdf_file.stem

    # Create folder with the same name
    new_folder = main_folder / folder_name
    new_folder.mkdir(exist_ok=True)

    print(f"Created: {new_folder.name}")

print("\nDone!")
