import os


def get_dicom_files(input_dir):
    """
    Recursively retrieves all DICOM file paths from the input directory.

    Parameters:
        input_dir (str): Directory to search for DICOM files.

    Returns:
        list: List of file paths to DICOM files.
    """
    dicom_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".dcm") or file.endswith("DCM"):
                # Check for DICOM file extension
                dicom_files.append(os.path.join(root, file))
    return dicom_files
