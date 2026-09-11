from pathlib import Path
import pandas as pd

# ============================================================
# Configuration
# ============================================================

# Main folder = folder where this Python script is located
main_folder = Path(__file__).parent

# Excel file
excel_file = main_folder / "requirement.xlsx"


# ============================================================
# Read Excel file
# ============================================================

try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    print(f"ERROR: Could not find {excel_file.name}")
    input("Press Enter to exit...")
    exit()

# Check required columns
required_columns = [
    "RequirementID",
    "FunctionalRequirements",
    "UseCaseScenarios"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("ERROR: The following columns are missing from requirement.xlsx:")
    for column in missing_columns:
        print(f"  - {column}")
    input("Press Enter to exit...")
    exit()


# ============================================================
# Create a dictionary using RequirementID as the key
# ============================================================

requirements = {}

for _, row in df.iterrows():

    requirement_id = str(row["RequirementID"]).strip()

    # Skip empty RequirementID cells
    if not requirement_id or requirement_id.lower() == "nan":
        continue

    functional_requirement = row["FunctionalRequirements"]
    use_case_scenario = row["UseCaseScenarios"]

    # Convert empty/NaN cells to empty strings
    if pd.isna(functional_requirement):
        functional_requirement = ""
    else:
        functional_requirement = str(functional_requirement)

    if pd.isna(use_case_scenario):
        use_case_scenario = ""
    else:
        use_case_scenario = str(use_case_scenario)

    requirements[requirement_id] = {
        "FR": functional_requirement,
        "UseCase": use_case_scenario
    }


# ============================================================
# Match folders with RequirementID
# ============================================================

processed = 0
skipped = 0

for folder in main_folder.iterdir():

    # Only process directories
    if not folder.is_dir():
        continue

    folder_name = folder.name

    # Check whether folder name exists in RequirementID
    if folder_name not in requirements:
        print(f"Skipped (no matching RequirementID): {folder_name}")
        skipped += 1
        continue

    data = requirements[folder_name]

    # --------------------------------------------------------
    # Create FR.txt
    # --------------------------------------------------------

    fr_file = folder / "FR.txt"

    with open(fr_file, "w", encoding="utf-8") as f:
        f.write(data["FR"])


    # --------------------------------------------------------
    # Create usecase.txt
    # --------------------------------------------------------

    usecase_file = folder / "usecase.txt"

    with open(usecase_file, "w", encoding="utf-8") as f:
        f.write(data["UseCase"])


    print(f"Processed: {folder_name}")

    processed += 1


# ============================================================
# Summary
# ============================================================

print("\n========================================")
print("Processing completed!")
print("========================================")
print(f"Folders processed : {processed}")
print(f"Folders skipped   : {skipped}")
print("========================================")

input("\nPress Enter to exit...")
