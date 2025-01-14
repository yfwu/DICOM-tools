import os
import sys
from anonymizer import anonymize_dicom_files


def main():
    """
    CLI tool for anonymizing DICOM files.

    Usage:
        python cli.py <input_folder> [output_folder]

    Arguments:
        input_folder   Path to the folder containing DICOM files.
        output_folder  (Optional) Path to the folder to save anonymized files.
                       Defaults to '<input_folder>-anonymized'.
    """
    # Validate arguments
    if len(sys.argv) < 2:
        print("Usage: python cli.py <input_folder> [output_folder]")
        sys.exit(1)

    # Parse arguments
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else f"{input_folder}-anonymized"

    # Validate input folder
    if not os.path.isdir(input_folder):
        print(
            f"Error: Input folder '{input_folder}' does not exist or is not a directory."
        )
        sys.exit(1)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Run anonymization
    try:
        print(f"Anonymizing DICOM files from '{input_folder}' to '{output_folder}'...")
        anonymize_dicom_files(input_folder, output_folder)
        print(f"Anonymization completed successfully. Output saved to: {output_folder}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
